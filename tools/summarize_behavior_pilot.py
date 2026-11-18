"""Davranış pilotunu periyot, kronolojik bölüm ve hisse bazında özetle.

Bu betimleyici bir keşiftir. Tek ziyaret/bar görünümü tüm korelasyonu veya
örtüşen ufukları ortadan kaldırmaz, istatistiksel doğrulama değildir.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pilot', type=Path, required=True)
    parser.add_argument('--movement', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    if args.output.resolve() in {args.pilot.resolve(), args.movement.resolve()}:
        raise ValueError('Çıktı ayrı dizinde olmalı')
    cfg = json.loads((args.movement / 'summary.json').read_text(encoding='utf-8'))
    if (digest(args.pilot / 'visits.csv.gz') != cfg['pilot_visits_sha256'] or
            digest(args.pilot / 'outcomes.csv.gz') != cfg['pilot_outcomes_sha256'] or
            digest(args.pilot / 'input-manifest.csv') != cfg['pilot_manifest_sha256'] or
            digest(args.movement / 'movement-features.csv.gz') != cfg.get('features_sha256')):
        raise ValueError('Hareket çalışmasının girdisi veya özellik dosyası değişmiş')
    manifest = pd.read_csv(args.pilot / 'input-manifest.csv')
    visits = pd.read_csv(args.pilot / 'visits.csv.gz')
    features = pd.read_csv(args.movement / 'movement-features.csv.gz')
    outcomes = pd.read_csv(args.pilot / 'outcomes.csv.gz')
    if visits.visit_id.duplicated().any() or features.visit_id.duplicated().any():
        raise ValueError('Ziyaret veya özellik kimliği yineleniyor')
    if set(visits.visit_id) != set(features.visit_id):
        raise ValueError('Ziyaret ve özellik kimlikleri eşleşmiyor')
    features = features.drop(columns=['asset_id', 'interval'])
    data = visits.merge(features, on='visit_id', validate='one_to_one', suffixes=('', '_feature'))
    data = data.merge(outcomes.loc[outcomes.horizon == 5, ['visit_id', 'status', 'return', 'end_bar_ts']],
                      on='visit_id', validate='one_to_one', suffixes=('_feature', '_outcome'))
    data['bar_ts'] = pd.to_datetime(data.bar_ts, utc=True)
    data['end_bar_ts'] = pd.to_datetime(data.end_bar_ts, utc=True)
    first = pd.to_datetime(manifest.first_bar_label, utc=True).min()
    last = pd.to_datetime(manifest.last_bar_label, utc=True).max()
    if pd.isna(first) or pd.isna(last) or first >= last:
        raise ValueError('Ortak tarih sınırları oluşturulamadı')
    boundary1 = first + (last - first) * .6
    boundary2 = first + (last - first) * .8
    boundaries = [('train', first, boundary1), ('validation', boundary1, boundary2),
                  ('test', boundary2, last + pd.Timedelta(nanoseconds=1))]
    data['progress_group'] = data.progress_change_atr.map(lambda x: 'unknown' if pd.isna(x) else 'rising' if x > 0 else 'falling' if x < 0 else 'unchanged')
    data['directional_return'] = data['return'] * data.approach_direction
    # Bölgeyi sonuç ve grup bilgisine bakmadan deterministik seç.
    dedup = (data.sort_values(['asset_id', 'interval', 'position', 'zone_id', 'visit_id'])
             .drop_duplicates(['asset_id', 'interval', 'position'], keep='first'))
    results, per_asset = [], []
    for mode, subset in [('all_visits', data), ('one_visit_per_bar', dedup)]:
        for split, start, end in boundaries:
            current = subset[(subset.bar_ts >= start) & (subset.bar_ts < end)].copy()
            current['eligible'] = ((current.status_feature == 'observed') & (current.status_outcome == 'observed') &
                                   current.end_bar_ts.notna() & (current.end_bar_ts < end) & current.directional_return.notna())
            for keys, frame in current.groupby(['interval', 'progress_group'], sort=True):
                good = frame[frame.eligible]
                results.append({'mode': mode, 'split': split, 'interval': keys[0], 'progress_group': keys[1],
                                'visits': len(frame), 'eligible': len(good), 'assets': good.asset_id.nunique(),
                                'median_directional_return_5bar': float(good.directional_return.median()) if len(good) else None,
                                'positive_fraction': float((good.directional_return > 0).mean()) if len(good) else None})
                for asset, af in good.groupby('asset_id', sort=True):
                    per_asset.append({'mode': mode, 'split': split, 'interval': keys[0], 'progress_group': keys[1],
                                      'asset_id': asset, 'eligible': len(af),
                                      'median_directional_return_5bar': float(af.directional_return.median()),
                                      'positive_fraction': float((af.directional_return > 0).mean())})
    args.output.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(results, columns=['mode', 'split', 'interval', 'progress_group', 'visits', 'eligible', 'assets',
                                   'median_directional_return_5bar', 'positive_fraction']).to_csv(args.output / 'splits.csv', index=False)
    pd.DataFrame(per_asset, columns=['mode', 'split', 'interval', 'progress_group', 'asset_id', 'eligible',
                                     'median_directional_return_5bar', 'positive_fraction']).to_csv(args.output / 'per-asset.csv', index=False)
    metadata = {'pilot': str(args.pilot), 'movement': str(args.movement),
                'pilot_visits_sha256': digest(args.pilot / 'visits.csv.gz'),
                'pilot_outcomes_sha256': digest(args.pilot / 'outcomes.csv.gz'),
                'movement_features_sha256': digest(args.movement / 'movement-features.csv.gz'),
                'code_sha256': digest(Path(__file__)), 'input_visits': len(data), 'unique_asset_interval_positions': len(dedup),
                'bar_label_split_boundaries': [{'split': name, 'start_inclusive': str(start), 'end_exclusive': str(end)} for name, start, end in boundaries],
                'warning': 'Bar etiketlerine göre dönemleme; sonuç penceresi sınırı aşarsa dışlanır. Daha önce incelenmiş veri, bağımsız test değildir.'}
    (args.output / 'summary.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
