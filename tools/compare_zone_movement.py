"""Keşif: aynı hisse/bar olaylarında bölge türü, geliş ve birlikte basit karşılaştırma.

Fiyat barında ziyaret olunca başlangıç kapanışı kullanılır; gerçek emir veya
canlı tahmin testi değildir. Tekrarlanan ve seçilmiş olaylar bağımsız değildir.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from tools.analyze_zone_philosophy import load_representatives
from replayman.replay import load_bars

KINDS = ['yatay', 'oyalanma', 'hizli_cikis', 'egimli']
KEYS = ['asset_id', 'interval', 'position']
FLAGS = ['has_' + k for k in KINDS]
MODELS = {'side': ['approach_direction'],
          'movement': ['approach_direction', 'progress_group'],
          'zone': ['approach_direction'] + FLAGS,
          'combined': ['approach_direction', 'progress_group'] + FLAGS,
          'movement_path': ['approach_direction', 'progress_group', 'path_group'],
          'combined_path': ['approach_direction', 'progress_group', 'path_group'] + FLAGS}


def make_events(data: pd.DataFrame, anchor_order: list[str] | None = None):
    """Önceden belirlenen yatay > oyalanma > hızlı > eğimli sırasıyla tek bar.

    Tür bayrakları yalnız aynı mumda ve seçilmiş merkeze göre aynı tarafta
    temsilcisi olan türlerdir; geometrik kesişim veya tüm çizgiler değildir.
    """
    order = KINDS if anchor_order is None else anchor_order
    if len(order) != len(KINDS) or set(order) != set(KINDS):
        raise ValueError('Temsilci sırası dört türü birer kez içermeli')
    f = data.copy()
    if f.duplicated(KEYS + ['kind']).any():
        raise ValueError('Tür içinde yinelenen bar')
    if not set(f.kind).issubset(KINDS):
        raise ValueError('Bilinmeyen tür')
    if f[KEYS].isna().any().any():
        raise ValueError('Eksik olay anahtarı')
    # Farklı evren çalıştırmalarının dönem sınırı birkaç saat farklı olabiliyor.
    splits = f.groupby(KEYS, sort=False)['split'].nunique()
    conflict_keys = splits[splits > 1].reset_index()[KEYS]
    conflicted = len(conflict_keys)
    if conflicted:
        f = f.merge(conflict_keys.assign(_bad=True), on=KEYS, how='left')
        f = f[f._bad.isna()].drop(columns='_bad')
    f['_rank'] = f.kind.map({k: i for i, k in enumerate(order)})
    f = f.sort_values(KEYS + ['_rank'])
    anchors = f.drop_duplicates(KEYS).copy()
    anchors = anchors.rename(columns={'kind': 'anchor_kind', 'approach_direction': 'anchor_side',
                                      'progress_group': 'anchor_progress', 'directional_excess': 'anchor_y',
                                      'return_5bar': 'anchor_return', 'bar_ts': 'anchor_ts'})
    cols = KEYS + ['anchor_kind', 'anchor_side', 'anchor_progress', 'anchor_y', 'anchor_return', 'anchor_ts']
    m = f.merge(anchors[cols], on=KEYS, validate='many_to_one')
    if not (m.bar_ts == m.anchor_ts).all() or ((m.return_5bar - m.anchor_return).abs() > 1e-10).any():
        raise ValueError('Aynı anahtarda fiyat sonucu veya zaman farklı')
    same = m[m.approach_direction == m.anchor_side].copy()
    if ((same.directional_excess - same.anchor_y).abs() > 1e-10).any():
        raise ValueError('Aynı anahtar ve yön için sonuç farklı')
    # İlerleme aynı fiyat yoluyla hesaplansa da eğimli merkezin önceki konumu nedeniyle
    # farklı olması olasıdır: bayrakları koru, hareket yalnız temsilciye aittir.
    flag = same.pivot(index=KEYS, columns='kind', values='_rank').notna().reindex(columns=KINDS, fill_value=False)
    flag.columns = FLAGS
    out = anchors.merge(flag.reset_index(), on=KEYS, validate='one_to_one')
    out = out.rename(columns={'anchor_side':'approach_direction', 'anchor_progress':'progress_group',
                              'anchor_y':'directional_excess', 'anchor_return':'return_5bar', 'anchor_ts':'bar_ts'})
    out = out[out.progress_group.isin(['rising', 'falling'])].copy()
    out[FLAGS] = out[FLAGS].astype(int)
    cols = KEYS + ['bar_ts', 'split', 'anchor_kind', 'approach_direction', 'progress_group'] + FLAGS + ['return_5bar', 'directional_excess']
    return out[cols].sort_values(KEYS).reset_index(drop=True), conflicted


def path_labels(close: pd.Series, threshold: float = .6) -> pd.DataFrame:
    """Her bara kadar değil, yalnız önceki 11 kapanışla 10-adımlı yol verimi."""
    change = (close.shift(1) - close.shift(11)).abs()
    path = close.diff().abs().rolling(10, min_periods=10).sum().shift(1)
    efficiency = change / path.replace(0, np.nan)
    category = np.select([efficiency >= threshold, efficiency < threshold], ['direct', 'choppy'], default='unknown')
    return pd.DataFrame({'path_efficiency_10':efficiency, 'path_group':category})


def add_path_features(events: pd.DataFrame, manifest_path: Path):
    manifest = pd.read_csv(manifest_path)
    if manifest.duplicated(['asset_id', 'interval']).any():
        raise ValueError('Girdi manifestinde yinelenen hisse/periyot')
    lookup = manifest.set_index(['asset_id', 'interval'])
    pieces = []
    for (asset, interval), group in events.groupby(['asset_id', 'interval'], sort=True):
        info = lookup.loc[(asset, interval)]
        path = Path(info['path'])
        if hashlib.sha256(path.read_bytes()).hexdigest() != info['sha256']:
            raise ValueError(f'Girdi hash uyuşmuyor: {path}')
        bars = load_bars(path)
        positions = group.position.to_numpy(dtype=int)
        if (positions >= len(bars)).any() or (positions < 11).any():
            raise ValueError(f'Geçersiz bar konumu: {asset}/{interval}')
        stamps = pd.to_datetime(group.bar_ts, utc=True).reset_index(drop=True)
        expected = bars.ts_utc.iloc[positions].reset_index(drop=True)
        if not stamps.equals(expected):
            raise ValueError(f'Bar etiketi uyuşmuyor: {asset}/{interval}')
        labels = path_labels(bars.close.astype(float)).iloc[positions].reset_index(drop=True)
        pieces.append(pd.concat([group.reset_index(drop=True), labels], axis=1))
    return pd.concat(pieces, ignore_index=True)


def predictions(events: pd.DataFrame, min_train: int = 30):
    """Her periyotta train medyanları; az örnekli hücrede train taraf medyanı."""
    if min_train < 1:
        raise ValueError('min_train pozitif olmalı')
    pieces, score = [], []
    for interval, group in events.groupby('interval', sort=True):
        train = group[group.split == 'train']
        side_medians = train.groupby('approach_direction').directional_excess.median()
        if train.empty or len(side_medians) < 2:
            continue
        for split in ['validation', 'test']:
            check = group[group.split == split].copy()
            if check.empty:
                continue
            target = check.directional_excess.to_numpy()
            base = check.approach_direction.map(side_medians).to_numpy()
            predictions_for_split = {}
            for name, keys in MODELS.items():
                table = train.groupby(keys, dropna=False).directional_excess.agg(['median', 'size']).reset_index()
                check = check.merge(table.rename(columns={'median': '_median', 'size':'_size'}), on=keys, how='left', validate='many_to_one')
                fallback = check._size.fillna(0).to_numpy() < min_train
                values = check._median.to_numpy(copy=True)
                values[fallback] = base[fallback]
                predictions_for_split[name] = values
                score.append({'interval': interval, 'split': split, 'model': name, 'events': len(check),
                              'assets': check.asset_id.nunique(), 'dates': check.bar_ts.nunique(),
                              'mae': float(np.abs(target-values).mean()),
                              'bias': float((target-values).mean()), 'fallback_fraction': float(fallback.mean())})
                check = check.drop(columns=['_median','_size'])
            for name, values in predictions_for_split.items():
                check['prediction_' + name] = values
            pieces.append(check)
    return pd.concat(pieces, ignore_index=True) if pieces else pd.DataFrame(), pd.DataFrame(score)


def paired_scores(pred: pd.DataFrame):
    comparisons = [('movement', 'side'), ('zone', 'side'), ('combined', 'movement'),
                   ('combined', 'zone'), ('combined', 'side'), ('movement_path', 'movement'),
                   ('combined_path', 'movement_path'), ('combined_path', 'combined'), ('combined_path', 'side')]
    rows = []
    for (interval, split), g in pred.groupby(['interval', 'split']):
        for new, ref in comparisons:
            diff = (g.directional_excess - g['prediction_' + ref]).abs() - (g.directional_excess - g['prediction_' + new]).abs()
            per_asset = pd.DataFrame({'asset': g.asset_id, 'delta': diff}).groupby('asset').delta.mean()
            rows.append({'interval': interval, 'split': split, 'model': new, 'reference': ref, 'n':len(g),
                         'mae_improvement':float(diff.mean()), 'assets':len(per_asset),
                         'assets_improved':int((per_asset>0).sum()), 'assets_worse':int((per_asset<0).sum())})
    return pd.DataFrame(rows)


def weekly_intervals(pred: pd.DataFrame, draws: int = 500, seed: int = 20261117):
    """Tahminleri sabit tutup aynı haftanın olaylarını birlikte yeniden örnekle."""
    rng = np.random.default_rng(seed)
    rows = []
    pred = pred.copy()
    pred['week'] = pd.to_datetime(pred.bar_ts, utc=True).dt.tz_localize(None).dt.to_period('W-SUN').dt.start_time
    for (interval, split), g in pred.groupby(['interval', 'split']):
        for model, reference in [('movement','side'), ('zone','side'), ('combined','movement'),
                                 ('combined','zone'), ('combined','side'), ('movement_path','movement'),
                                 ('combined_path','movement_path'), ('combined_path','combined'), ('combined_path','side')]:
            delta = (g.directional_excess - g['prediction_'+reference]).abs() - (g.directional_excess - g['prediction_'+model]).abs()
            by_week = pd.DataFrame({'week':g.week, 'delta':delta}).groupby('week').delta.agg(['sum','size'])
            n = len(by_week)
            if n < 5:
                continue
            picks = rng.integers(0, n, size=(draws, n))
            values = by_week['sum'].to_numpy()[picks].sum(axis=1) / by_week['size'].to_numpy()[picks].sum(axis=1)
            low, high = np.quantile(values, [.025, .975])
            rows.append({'interval':interval, 'split':split, 'model':model, 'reference':reference,
                         'weeks':n, 'draws':draws, 'seed':seed, 'low':low, 'high':high})
    return pd.DataFrame(rows)


def groups(events: pd.DataFrame, include_path: bool = False):
    keys = ['interval', 'split', 'approach_direction'] + FLAGS + ['progress_group']
    if include_path:
        keys += ['path_group']
    return events.groupby(keys, sort=True).agg(n=('directional_excess', 'size'), assets=('asset_id', 'nunique'),
                                                median_excess=('directional_excess', 'median'),
                                                median_return=('return_5bar', 'median')).reset_index()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path('research/measurements/zone-memory'))
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--min-train', type=int, default=30)
    p.add_argument('--reverse-anchor', action='store_true', help='Temsilci önceliğini tersine çevir (duyarlılık)')
    p.add_argument('--summary-only', action='store_true', help='Büyük olay ve tahmin dosyalarını yazma')
    args = p.parse_args(argv)
    order = list(reversed(KINDS)) if args.reverse_anchor else KINDS
    raw, inputs = load_representatives(args.root)
    events, conflicts = make_events(raw, order)
    manifest_path = args.root / 'universe-horizontal' / 'input-manifest.csv'
    base_manifest = pd.read_csv(manifest_path)[['asset_id', 'interval', 'sha256']]
    for info in inputs:
        other_path = Path(info['path']).parent / 'input-manifest.csv'
        other = pd.read_csv(other_path)[['asset_id', 'interval', 'sha256']]
        matched = other.merge(base_manifest, on=['asset_id', 'interval'], how='left', suffixes=('_other', '_base'), validate='one_to_one')
        if matched.sha256_base.isna().any() or (matched.sha256_base != matched.sha256_other).any():
            raise ValueError(f'Fiyat manifestleri uyuşmuyor: {other_path}')
    events = add_path_features(events, manifest_path)
    pred, score = predictions(events, args.min_train)
    args.output.mkdir(parents=True, exist_ok=True)
    if not args.summary_only:
        events.to_csv(args.output/'events.csv.gz', index=False, compression='gzip')
        pred.to_csv(args.output/'predictions.csv.gz', index=False, compression='gzip')
    groups(events).to_csv(args.output/'groups.csv', index=False)
    groups(events, include_path=True).to_csv(args.output/'groups-path.csv', index=False)
    score.to_csv(args.output/'scores.csv', index=False)
    paired_scores(pred).to_csv(args.output/'paired-scores.csv', index=False)
    weekly_intervals(pred).to_csv(args.output/'weekly-intervals.csv', index=False)
    summary = {'status':'exploratory_post_hoc', 'input_representatives': len(raw), 'unique_events': len(events),
               'split_conflict_keys_removed': conflicts, 'anchor_order': order, 'minimum_train_cell': args.min_train,
               'events_by_interval_split': events.groupby(['interval','split']).size().reset_index(name='events').to_dict('records'),
               'inputs': inputs, 'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'loader_sha256': hashlib.sha256(Path('tools/analyze_zone_philosophy.py').read_bytes()).hexdigest(),
               'bar_loader_sha256': hashlib.sha256(Path('replayman/replay.py').read_bytes()).hexdigest(),
               'price_manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
               'path_threshold': 0.6, 'path_note': 'Son 10 kapanış değişimindeki net mutlak hareket / toplam mutlak yol; eşik sonradan keşif için seçildi.',
               'caution':'Bayraklar temsilî aynı-bar ve aynı-taraf olaylarıdır, geometrik alan kesişimi değildir; tüm veri keşif sonrası kullanılmıştır.'}
    (args.output/'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
