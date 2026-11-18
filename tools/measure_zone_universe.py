"""BIST evreninde bölge ve hareket adaylarının tekrarlanabilir keşif taraması.

Beş barlık sonuçlar karar özelliklerinden ayrıdır. Çıktılar yalnız betimleyici,
örtüşen olaylar bağımsız değil; bar etiketleri gerçek kapanış zamanı değildir.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd

from replayman.behavior_zones import BehaviorConfig, scan_behavior_zones
from replayman.movement_character import approach_character
from replayman.replay import load_bars
from replayman.sloped_zones import SlopedConfig, scan_sloped_zones
from replayman.zone_memory import ZoneConfig, scan_zones


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('data/ohlcv'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--kind', choices=['horizontal', 'sloped', 'dwell', 'impulse'], required=True)
    parser.add_argument('--intervals', default='1h,2h,4h,1d')
    parser.add_argument('--method', choices=['atr', 'percent'], default='atr')
    parser.add_argument('--tolerance', type=float, default=.25)
    parser.add_argument('--limit', type=int, default=None)
    parser.add_argument('--representative-only', action='store_true', help='Yalnız her hisse/periyot/mum için seçilen bir ziyareti sakla')
    args = parser.parse_args(argv)
    intervals = list(dict.fromkeys(x.strip() for x in args.intervals.split(',') if x.strip()))
    if not intervals or any(x not in {'1h', '2h', '4h', '1d'} for x in intervals):
        raise ValueError('Geçerli periyot gerekli')
    assets = sorted(p.name for p in (args.root / 'bist_equities').iterdir() if p.is_dir())
    if args.limit is not None:
        if args.limit < 1:
            raise ValueError('limit pozitif olmalı')
        assets = assets[:args.limit]
    if not assets:
        raise ValueError('Hisse verisi yok')
    paths, manifest = [], []
    for asset in assets:
        for interval in intervals:
            candidates = sorted((args.root / 'bist_equities' / asset).glob(f'*/bars/{interval}.csv'))
            if len(candidates) != 1:
                raise ValueError(f'{asset}/{interval}: tam bir seri gerekli, bulunan {len(candidates)}')
            path = candidates[0]
            raw = pd.read_csv(path, usecols=['ts_utc', 'complete'] if interval in ('2h', '4h') else ['ts_utc'])
            bars = load_bars(path)
            if bars.empty:
                raise ValueError(f'Boş veri: {path}')
            series = path.parts[-3]
            for key, value in [('asset_id', asset), ('series_id', series), ('interval', interval)]:
                if key not in bars or set(bars[key].astype(str)) != {value}:
                    raise ValueError(f'Seri kimliği uyuşmazlığı: {path}, {key}')
            paths.append((asset, interval, path))
            manifest.append({'asset_id': asset, 'interval': interval, 'series_id': series, 'path': path.as_posix(),
                             'sha256': digest(path), 'input_rows': len(raw), 'usable_rows': len(bars),
                             'excluded_rows': len(raw)-len(bars), 'first_bar_label': str(bars.ts_utc.iloc[0]),
                             'last_bar_label': str(bars.ts_utc.iloc[-1])})
    manifest = pd.DataFrame(manifest)
    start = pd.to_datetime(manifest.first_bar_label, utc=True).min()
    end = pd.to_datetime(manifest.last_bar_label, utc=True).max()
    if start >= end:
        raise ValueError('Ortak dönem oluşturulamadı')
    cut1, cut2 = start + (end-start)*.6, start + (end-start)*.8
    end = end + pd.Timedelta(nanoseconds=1)
    benchmarks = {}
    benchmark_manifest = []
    for interval in intervals:
        bpaths = sorted((args.root / 'bist_indices' / 'IDX_XU100').glob(f'*/bars/{interval}.csv'))
        if len(bpaths) > 1:
            raise ValueError(f'XU100/{interval}: birden fazla seri var')
        if bpaths:
            benchmark = load_bars(bpaths[0])
            benchmarks[interval] = dict(zip(benchmark.ts_utc, benchmark.close.astype(float)))
            benchmark_manifest.append({'interval': interval, 'path': bpaths[0].as_posix(), 'sha256': digest(bpaths[0])})
        else:
            benchmarks[interval] = {}
    config = ZoneConfig(method=args.method, tolerance=args.tolerance)
    args.output.mkdir(parents=True, exist_ok=True)
    parts = []
    inventory = []
    for number, (asset, interval, path) in enumerate(paths, 1):
        bars = load_bars(path)
        series = path.parts[-3]
        key = f'{asset}:{series}:{interval}'
        if args.kind in {'dwell', 'impulse'}:
            zones, visits, _ = scan_behavior_zones(bars, config=BehaviorConfig(kind=args.kind, zone=config), series_key=key)
        elif args.kind == 'sloped':
            zones, visits, _ = scan_sloped_zones(bars, config=SlopedConfig(zone=config), series_key=key)
        else:
            zones, visits, _ = scan_zones(bars, config=config, series_key=key)
        inventory.append({'asset_id': asset, 'interval': interval, 'bars': len(bars),
                          'zone_creations': int((zones.event == 'zone_created').sum()), 'visits': len(visits)})
        if not visits.empty:
            features = approach_character(bars, visits)
            visits = visits.merge(features, on='visit_id', validate='one_to_one')
            pos = visits.position.to_numpy(dtype=int)
            finish = pos + 5
            available = finish < len(bars)
            values = bars.close.to_numpy(dtype=float)
            labels = pd.DatetimeIndex(bars.ts_utc)
            visits['asset_id'], visits['interval'] = asset, interval
            visits['bar_ts'] = labels.take(pos)
            visits['end_bar_ts'] = pd.Series(pd.NaT, index=visits.index, dtype='datetime64[us, UTC]')
            visits.loc[available, 'end_bar_ts'] = labels.take(finish[available])
            visits['return_5bar'] = np.nan
            valid_entry = available & (values[pos] != 0)
            visits.loc[valid_entry, 'return_5bar'] = values[finish[valid_entry]] / values[pos[valid_entry]] - 1
            market = benchmarks[interval]
            m_start = visits.bar_ts.map(market)
            m_end = visits.end_bar_ts.map(market)
            visits['benchmark_return_5bar'] = (m_end / m_start.replace(0, np.nan)) - 1
            visits['directional_return'] = visits.return_5bar * visits.approach_direction
            visits['directional_excess'] = (visits.return_5bar - visits.benchmark_return_5bar) * visits.approach_direction
            if args.kind in {'dwell', 'impulse'}:
                visits['memory_group'] = np.where(visits.prior_completed_visits == 0, '0', '1+')
            else:
                base = 2 if args.kind == 'sloped' else 1
                visits['memory_group'] = np.where(visits.reaction_count <= base, '0', '1+')
            visits['progress_group'] = np.select([visits.progress_change_atr < 0, visits.progress_change_atr > 0,
                                                  visits.progress_change_atr == 0], ['falling', 'rising', 'unchanged'], default='unknown')
            visits['split'] = np.select([visits.bar_ts < cut1, visits.bar_ts < cut2], ['train', 'validation'], default='test')
            boundary = visits.split.map({'train': cut1, 'validation': cut2, 'test': end})
            visits['eligible'] = (visits.status == 'observed') & visits.end_bar_ts.notna() & (visits.end_bar_ts < boundary) & visits.directional_return.notna()
            visits['one_per_bar'] = ~visits.sort_values(['position', 'zone_id', 'visit_id']).duplicated('position', keep='first')
            cols = ['asset_id', 'interval', 'zone_id', 'visit_id', 'position', 'bar_ts', 'end_bar_ts',
                    'memory_group', 'progress_group', 'approach_direction', 'return_5bar', 'benchmark_return_5bar',
                    'directional_return', 'directional_excess', 'split', 'eligible', 'one_per_bar']
            parts.append(visits.loc[visits.one_per_bar, cols] if args.representative_only else visits[cols])
        print(f'{number}/{len(paths)} {asset} {interval}: zones={inventory[-1]["zone_creations"]} visits={len(visits)}', flush=True)
    pd.DataFrame(inventory).to_csv(args.output / 'inventory.csv', index=False)
    manifest.to_csv(args.output / 'input-manifest.csv', index=False)
    pd.DataFrame(benchmark_manifest, columns=['interval', 'path', 'sha256']).to_csv(args.output / 'benchmark-manifest.csv', index=False)
    cols = ['asset_id', 'interval', 'zone_id', 'visit_id', 'position', 'bar_ts', 'end_bar_ts', 'memory_group', 'progress_group',
            'approach_direction', 'return_5bar', 'benchmark_return_5bar', 'directional_return', 'directional_excess', 'split', 'eligible', 'one_per_bar']
    events = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=cols)
    events.to_csv(args.output / 'events.csv.gz', index=False, compression='gzip')
    results, per_asset = [], []
    modes = [('one_visit_per_bar', events[events.one_per_bar.astype(bool)])]
    if not args.representative_only:
        modes.insert(0, ('all_visits', events))
    for mode, subset in modes:
        for keys, group in subset.groupby(['interval', 'split', 'memory_group', 'progress_group'], sort=True):
            good = group[group.eligible.astype(bool)]
            benchmark_good = good.directional_excess.dropna()
            results.append({'mode': mode, 'interval': keys[0], 'split': keys[1], 'memory_group': keys[2],
                            'progress_group': keys[3], 'visits': len(group), 'eligible': len(good),
                            'assets': int(good.asset_id.nunique()), 'benchmark_eligible': len(benchmark_good),
                            'median_directional_return': float(good.directional_return.median()) if len(good) else None,
                            'positive_fraction': float((good.directional_return > 0).mean()) if len(good) else None,
                            'median_directional_excess': float(benchmark_good.median()) if len(benchmark_good) else None})
            for asset, ag in good.groupby('asset_id', sort=True):
                per_asset.append({'mode': mode, 'interval': keys[0], 'split': keys[1], 'memory_group': keys[2],
                                  'progress_group': keys[3], 'asset_id': asset, 'eligible': len(ag),
                                  'median_directional_return': float(ag.directional_return.median()),
                                  'benchmark_eligible': int(ag.directional_excess.notna().sum()),
                                  'median_directional_excess': float(ag.directional_excess.median()) if ag.directional_excess.notna().any() else None})
    pd.DataFrame(results).to_csv(args.output / 'group-results.csv', index=False)
    pd.DataFrame(per_asset).to_csv(args.output / 'asset-results.csv', index=False)
    code = [Path(__file__), Path('replayman/zone_memory.py'), Path('replayman/behavior_zones.py'),
            Path('replayman/sloped_zones.py'), Path('replayman/movement_character.py'), Path('replayman/replay.py'), Path('replayman/swings.py')]
    metadata = {'status': 'exploratory', 'kind': args.kind, 'assets': len(assets), 'intervals': intervals,
                'series': len(paths), 'zones': int(sum(x['zone_creations'] for x in inventory)),
                'visits': int(sum(x['visits'] for x in inventory)), 'stored_visits': len(events),
                'representative_only': args.representative_only,
                'one_per_bar': int(events.one_per_bar.sum()) if len(events) else 0,
                'eligible': int(events.eligible.sum()) if len(events) else 0,
                'benchmark_eligible': int((events.eligible & events.directional_excess.notna()).sum()) if len(events) else 0,
                'boundary_first': str(start), 'boundary_train_end': str(cut1), 'boundary_validation_end': str(cut2), 'boundary_test_end': str(end),
                'zone_method': config.method, 'tolerance': config.tolerance, 'exit_closes': config.exit_closes, 'horizon': 5,
                'dwell_window': 10, 'dwell_width_atr': 2., 'impulse_bars': 5, 'impulse_distance_atr': 2.,
                'sloped_anchor_min': 8, 'sloped_anchor_max': 80, 'sloped_max_anchors_per_kind': 3,
                'python': platform.python_version(), 'pandas': pd.__version__, 'code_sha256': {p.name: digest(p) for p in code},
                'warning': 'Geçmişte incelenmiş tek yıllık veri; örtüşme, bağımlılık, üyelik yanlılığı ve kapanış zamanı kısıtlıdır.'}
    (args.output / 'summary.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(metadata, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
