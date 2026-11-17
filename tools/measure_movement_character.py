"""Daha önce kaydedilmiş ziyaretlerde, temastan önceki hareketi araştır."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

from replayman.movement_character import approach_character
from replayman.replay import load_bars


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pilot', type=Path, required=True, help='Girdi ziyaret dizini')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    if args.output.resolve() == args.pilot.resolve():
        raise ValueError('Çıktı pilot diziniyle aynı olamaz')
    manifest = pd.read_csv(args.pilot / 'input-manifest.csv')
    visits = pd.read_csv(args.pilot / 'visits.csv.gz')
    outcomes = pd.read_csv(args.pilot / 'outcomes.csv.gz')
    if visits.visit_id.duplicated().any():
        raise ValueError('Yinelenen ziyaret kimliği')
    parts = []
    for source in manifest.to_dict('records'):
        path = Path(source['path'])
        if sha(path) != source['sha256']:
            raise ValueError(f'Girdi değişmiş: {path}')
        bars = load_bars(path)
        selected = visits[(visits.asset_id == source['asset_id']) & (visits.series_id == source['series_id']) & (visits.interval == source['interval'])]
        for visit in selected.to_dict('records'):
            pos = int(visit['position'])
            if pos < 0 or pos >= len(bars) or abs(float(bars.iloc[pos].close) - float(visit['reference_close'])) > 1e-8:
                raise ValueError(f'Ziyaret/girdi uyuşmazlığı: {visit["visit_id"]}')
        features = approach_character(bars, selected)
        features.insert(0, 'interval', source['interval'])
        features.insert(0, 'asset_id', source['asset_id'])
        parts.append(features)
    features = pd.concat(parts, ignore_index=True)
    if set(features.visit_id) != set(visits.visit_id):
        raise ValueError('Manifest dışı ziyaret var')
    args.output.mkdir(parents=True, exist_ok=True)
    features.to_csv(args.output / 'movement-features.csv.gz', index=False, compression='gzip')
    # Yalnız örnekleme amaçlı betimleme: birleşim, aynı ziyaretin sonraki sonucu.
    paired = features.merge(outcomes.loc[outcomes.horizon == 5, ['visit_id', 'status', 'return']], on='visit_id', validate='one_to_one', suffixes=('_feature', '_outcome'))
    valid = paired[(paired.status_feature == 'observed') & (paired.status_outcome == 'observed')].copy()
    valid['progress_group'] = valid.progress_change_atr.map(lambda v: 'rising' if v > 0 else 'falling' if v < 0 else 'unchanged')
    summary = []
    for (interval, group), sample in valid.groupby(['interval', 'progress_group'], sort=True):
        directional = sample['return'] * sample.approach_direction
        summary.append({'interval': interval, 'progress_group': group, 'visits': len(sample),
                        'assets': int(sample.asset_id.nunique()), 'median_return_5bar': float(sample['return'].median()),
                        'positive_fraction_5bar': float((sample['return'] > 0).mean()),
                        'median_approach_direction_return_5bar': float(directional.median()),
                        'positive_approach_direction_fraction_5bar': float((directional > 0).mean())})
    pd.DataFrame(summary, columns=['interval', 'progress_group', 'visits', 'assets', 'median_return_5bar',
                                  'positive_fraction_5bar', 'median_approach_direction_return_5bar',
                                  'positive_approach_direction_fraction_5bar']).to_csv(args.output / 'descriptive-5bar.csv', index=False)
    config = {'pilot': args.pilot.as_posix(), 'pilot_visits_sha256': sha(args.pilot / 'visits.csv.gz'),
              'pilot_outcomes_sha256': sha(args.pilot / 'outcomes.csv.gz'),
              'pilot_manifest_sha256': sha(args.pilot / 'input-manifest.csv'),
              'features_sha256': sha(args.output / 'movement-features.csv.gz'),
              'movement_code_sha256': sha(Path(__file__).resolve().parents[1] / 'replayman/movement_character.py'),
              'tool_code_sha256': sha(__file__), 'visits': len(features),
              'feature_status': features.status.value_counts().to_dict(),
              'notice': 'Betimleyici pilot; nedensel etki veya indikatör başarısı göstermez.'}
    (args.output / 'summary.json').write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(config, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
