"""Bölge araştırması: yön, hafıza, hareket ve aynı-bar örtüşmesi taraması.

Geçmiş veriden üretilen betimleyici analizdir, işlem sinyali veya nedensel
etki testi değildir. Girdi olayları yalnız bilinen kapanış-barı vekilleridir.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd


FILES = {
    'yatay': ['universe-horizontal'],
    'oyalanma': ['universe-dwell'],
    'hizli_cikis': ['universe-impulse'],
    'egimli': ['universe-sloped', 'universe-sloped-hourly'],
}
KEYS = ['asset_id', 'interval', 'position']
COLS = ['asset_id', 'interval', 'position', 'bar_ts', 'memory_group', 'progress_group',
        'approach_direction', 'return_5bar', 'directional_excess', 'split', 'eligible', 'one_per_bar']


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_representatives(root: Path):
    parts, inputs = [], []
    for kind, folders in FILES.items():
        for folder in folders:
            path = root / folder / 'events.csv.gz'
            frame = pd.read_csv(path, usecols=COLS, dtype={'memory_group': str})
            frame = frame[frame.one_per_bar & frame.eligible & frame.directional_excess.notna() &
                          frame.approach_direction.isin([-1, 1])].copy()
            frame['kind'] = kind
            frame['bar_ts'] = pd.to_datetime(frame.bar_ts, utc=True)
            parts.append(frame)
            inputs.append({'kind': kind, 'path': path.as_posix(), 'sha256': sha(path), 'eligible_representatives': len(frame)})
    data = pd.concat(parts, ignore_index=True)
    if data.duplicated(['kind'] + KEYS).any():
        raise ValueError('Aynı tür/hisse/periyot/mum için birden fazla temsilci var')
    return data, inputs


def surface(data: pd.DataFrame) -> pd.DataFrame:
    keys = ['kind', 'interval', 'split', 'memory_group', 'progress_group', 'approach_direction']
    groups = data.groupby(keys, dropna=False, sort=True)
    result = groups.agg(n=('directional_excess', 'size'), assets=('asset_id', 'nunique'),
                        bar_dates=('bar_ts', 'nunique'), median_excess=('directional_excess', 'median'),
                        positive_fraction=('directional_excess', lambda x: (x > 0).mean())).reset_index()
    # Yönlü ham getiri ayrıca, benchmark farkıyla karıştırılmadan hesaplanır.
    oriented = data.assign(_directional_return=data.return_5bar * data.approach_direction)
    oriented = oriented.groupby(keys, dropna=False, sort=True)._directional_return.median().reset_index()
    result = result.merge(oriented, on=keys, validate='one_to_one')
    result = result.rename(columns={'_directional_return': 'median_directional_return'})
    per_stock = data.groupby(keys + ['asset_id'], dropna=False).directional_excess.agg(['size', 'median']).reset_index()
    per_stock = per_stock[per_stock['size'] >= 3].copy()
    per_stock['_negative'] = per_stock['median'] < 0
    per_stock['_positive'] = per_stock['median'] > 0
    counts = per_stock.groupby(keys, dropna=False).agg(assets_3plus=('asset_id', 'size'),
                                                      asset_negative=('_negative', 'sum'),
                                                      asset_positive=('_positive', 'sum')).reset_index()
    return result.merge(counts, on=keys, how='left', validate='one_to_one').fillna({'assets_3plus': 0, 'asset_negative': 0, 'asset_positive': 0})


def overlaps(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (interval, split), group in data.groupby(['interval', 'split'], sort=True):
        for a, b in itertools.combinations(FILES, 2):
            left = group[group.kind == a]
            right = group[group.kind == b]
            if left.empty or right.empty:
                continue
            both = left.merge(right, on=KEYS, suffixes=('_a', '_b'), validate='one_to_one')
            if len(both):
                if not (both.bar_ts_a == both.bar_ts_b).all():
                    raise ValueError(f'{a}/{b}: bar pozisyonu farklı tarihe denk geliyor')
                diff_return = (both.return_5bar_a - both.return_5bar_b).abs()
                if (diff_return > 1e-10).any():
                    raise ValueError(f'{a}/{b}: aynı barda ileri hisse sonucu farklı')
                same_side = both.approach_direction_a == both.approach_direction_b
                same_group = same_side & (both.progress_group_a == both.progress_group_b)
                direction_diff = (both.loc[same_side, 'directional_excess_a'] - both.loc[same_side, 'directional_excess_b']).abs()
                if (direction_diff > 1e-10).any():
                    raise ValueError(f'{a}/{b}: aynı barda ve yönde benchmark farkı farklı')
                same_memory = same_side & (both.memory_group_a == both.memory_group_b)
                both_memory = same_side & (both.memory_group_a == '1+') & (both.memory_group_b == '1+')
            else:
                same_side = same_group = same_memory = both_memory = pd.Series(dtype=bool)
            rows.append({'interval': interval, 'split': split, 'type_a': a, 'type_b': b,
                         'eligible_a': len(left), 'eligible_b': len(right), 'same_bar': len(both),
                         'same_side': int(same_side.sum()), 'same_side_and_progress': int(same_group.sum()),
                         'same_side_and_memory': int(same_memory.sum()), 'same_side_both_memory_1plus': int(both_memory.sum()),
                         'same_side_fraction_of_a': float(same_side.sum()/len(left)),
                         'same_side_fraction_of_b': float(same_side.sum()/len(right))})
    return pd.DataFrame(rows)


def weekly_bootstrap(data: pd.DataFrame, *, draws: int = 500, seed: int = 20261117) -> pd.DataFrame:
    """Günlük oyalanmada haftalık zaman bloklarıyla keşif belirsizliği.

    Aynı hafta içindeki hisseler birlikte yeniden örneklenir. Örtüşen beş-bar
    sonuçları haftalar arasında bağımlı kalabilir; tam güvence sağlamaz.
    """
    sample = data[(data.kind == 'oyalanma') & (data.interval == '1d') &
                  data.memory_group.isin(['0', '1+']) & data.progress_group.isin(['rising', 'falling'])].copy()
    sample['week'] = sample.bar_ts.dt.tz_localize(None).dt.to_period('W-SUN').dt.start_time
    rng = np.random.default_rng(seed)
    rows = []
    for (split, direction), group in sample.groupby(['split', 'approach_direction'], sort=True):
        for compare, left_q, right_q in [
            ('rising_minus_falling_memory_1plus', ('1+', 'rising'), ('1+', 'falling')),
            ('memory_1plus_minus_zero_rising', ('1+', 'rising'), ('0', 'rising')),
        ]:
            relevant = group[((group.memory_group == left_q[0]) & (group.progress_group == left_q[1])) |
                             ((group.memory_group == right_q[0]) & (group.progress_group == right_q[1]))].copy()
            left = (relevant.memory_group == left_q[0]) & (relevant.progress_group == left_q[1])
            right = ~left
            weeks = sorted(relevant.week.unique())
            observed = (float(relevant.loc[left, 'directional_excess'].median() - relevant.loc[right, 'directional_excess'].median())
                        if left.any() and right.any() else None)
            blocks = [relevant[relevant.week == w] for w in weeks]
            results = []
            if len(weeks) >= 5:
                for _ in range(draws):
                    picked = rng.integers(0, len(weeks), size=len(weeks))
                    resampled = pd.concat([blocks[i] for i in picked], ignore_index=True)
                    l = (resampled.memory_group == left_q[0]) & (resampled.progress_group == left_q[1])
                    if l.any() and (~l).any():
                        results.append(float(resampled.loc[l, 'directional_excess'].median() - resampled.loc[~l, 'directional_excess'].median()))
            lo, hi = (np.quantile(results, [.025, .975]) if results else (None, None))
            rows.append({'split': split, 'approach_direction': direction, 'comparison': compare,
                         'n_left': int(left.sum()), 'n_right': int(right.sum()), 'weeks': len(weeks),
                         'median_difference': observed, 'week_bootstrap_2_5pct': lo,
                         'week_bootstrap_97_5pct': hi, 'successful_draws': len(results)})
    return pd.DataFrame(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('research/measurements/zone-memory'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--draws', type=int, default=500)
    args = parser.parse_args(argv)
    if args.draws < 1:
        raise ValueError('draws pozitif olmalı')
    data, inputs = load_representatives(args.root)
    args.output.mkdir(parents=True, exist_ok=True)
    surface(data).to_csv(args.output / 'condition-surface.csv', index=False)
    overlaps(data).to_csv(args.output / 'same-bar-overlap.csv', index=False)
    weekly_bootstrap(data, draws=args.draws).to_csv(args.output / 'weekly-bootstrap.csv', index=False)
    summary = {'status': 'exploratory_post_hoc', 'input_events': len(data),
               'kind_counts': data.kind.value_counts().to_dict(), 'inputs': inputs,
               'bootstrap_draws': args.draws, 'bootstrap_seed': 20261117,
               'method_sha256': sha(Path(__file__)),
               'notice': 'Aynı mum/hisse ve aynı yön eşleşmelerinde ileri getiri aynıdır; bağımsız kanıt sayılmaz. Haftalık bootstrap tüm bağımlılığı çözmez.'}
    (args.output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
