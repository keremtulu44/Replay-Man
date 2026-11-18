"""Dört bölge türünde nedensel lifecycle senaryolarının keşif taraması."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

from replayman.behavior_zones import BehaviorConfig, scan_behavior_zones
from replayman.replay import load_bars
from replayman.sloped_zones import SlopedConfig, scan_sloped_zones
from replayman.zone_memory import ZoneConfig, scan_zones
from replayman.zone_lifecycle import track_zone


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def evaluate_bars(records, bars, benchmark, cut1, cut2, end):
    if records.empty:
        return records
    data = records.copy()
    data['end_position'] = pd.to_numeric(data.end_position)
    done = data.status.eq('completed')
    data['split'] = None
    labels = pd.DatetimeIndex(bars.ts_utc)
    times = pd.to_datetime(data.end_bar_ts, utc=True)
    data.loc[done, 'split'] = np.select([times[done] < cut1, times[done] < cut2], ['train', 'validation'], default='test')
    data['pattern'] = 'other'
    data.loc[data.scenario.isin(['up_retest','down_retest']), 'pattern'] = 'cross_then_same'
    control = (data.path.eq('same') & data.prior_path.eq('same') & data.start_side.eq(data.prior_end_side))
    data.loc[control, 'pattern'] = 'same_then_same'
    # Senaryo seçimi ve temsilci seçimi ileri sonuçtan bağımsızdır.
    data['representative'] = False
    chosen = data[done].sort_values(['end_position', 'zone_id', 'visit_number']).drop_duplicates(['end_position'])
    data.loc[chosen.index, 'representative'] = True
    for horizon in (5, 10):
        data[f'excess_{horizon}'] = np.nan
        data[f'directional_{horizon}'] = np.nan
        data[f'end_label_{horizon}'] = pd.Series(pd.NaT, index=data.index, dtype='datetime64[us, UTC]')
        q = data[done].copy()
        pos = q.end_position.to_numpy(dtype=int)
        future = pos + horizon
        valid = future < len(bars)
        q = q.loc[valid]
        pos, future = pos[valid], future[valid]
        if q.empty:
            continue
        end_labels = labels.take(future)
        boundary = pd.to_datetime(q.split.map({'train':cut1, 'validation':cut2, 'test':end}), utc=True)
        valid_boundary = end_labels < pd.DatetimeIndex(boundary)
        q = q.loc[valid_boundary]
        pos, future, end_labels = pos[valid_boundary], future[valid_boundary], end_labels[valid_boundary]
        if q.empty:
            continue
        prices = bars.close.to_numpy(dtype=float)
        stock_return = prices[future] / prices[pos] - 1
        start_bench = pd.Series(labels.take(pos)).map(benchmark).to_numpy(dtype=float)
        end_bench = pd.Series(end_labels).map(benchmark).to_numpy(dtype=float)
        market_return = end_bench / start_bench - 1
        direction = np.where(q.end_side.eq('above'), 1., -1.)
        data.loc[q.index, f'end_label_{horizon}'] = end_labels
        data.loc[q.index, f'directional_{horizon}'] = stock_return * direction
        data.loc[q.index, f'excess_{horizon}'] = (stock_return - market_return) * direction
    return data


def group_summary(frame):
    f = frame[(frame.status=='completed') & frame.representative].copy()
    output=[]
    for keys, g in f.groupby(['interval','split','end_side','pattern'], dropna=False):
        row = dict(zip(['interval','split','end_side','pattern'], keys))
        row.update(events=len(g), assets=g.asset_id.nunique(), dates=g.end_bar_ts.nunique(),
                   same=(g.path=='same').sum(), cross=(g.path=='cross').sum())
        for h in (5,10):
            x=g[f'excess_{h}'].dropna()
            row.update({f'n_{h}':len(x),f'median_excess_{h}':x.median() if len(x) else None,
                        f'positive_excess_{h}':(x>0).mean() if len(x) else None})
        output.append(row)
    return pd.DataFrame(output)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--kind', choices=['horizontal','dwell','impulse','sloped'], required=True)
    p.add_argument('--intervals', default='4h,1d')
    p.add_argument('--root', type=Path, default=Path('data/ohlcv'))
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--limit',type=int)
    args=p.parse_args(argv)
    intervals=list(dict.fromkeys(args.intervals.split(',')))
    if not intervals or any(x not in {'1h','2h','4h','1d'} for x in intervals):
        raise ValueError('Geçersiz periyot')
    assets=sorted(p.name for p in (args.root/'bist_equities').iterdir() if p.is_dir())
    if args.limit is not None:
        if args.limit < 1: raise ValueError('limit pozitif olmalı')
        assets=assets[:args.limit]
    meta_path=Path('research/measurements/zone-memory/universe-horizontal/summary.json')
    meta=json.loads(meta_path.read_text())
    cut1=pd.Timestamp(meta['boundary_train_end']);cut2=pd.Timestamp(meta['boundary_validation_end']);end=pd.Timestamp(meta['boundary_test_end'])
    benchmarks, benchmark_inputs = {}, []
    for interval in intervals:
        matches=list((args.root/'bist_indices'/'IDX_XU100').glob(f'*/bars/{interval}.csv'))
        if len(matches)!=1: raise ValueError(f'XU100 seri belirsiz: {interval}')
        b=load_bars(matches[0]);benchmarks[interval]=dict(zip(b.ts_utc,b.close.astype(float)))
        benchmark_inputs.append({'interval':interval,'path':str(matches[0]),'sha256':sha(matches[0])})
    config=ZoneConfig(method='atr',tolerance=.25)
    parts=[]; inventory=[]; manifest=[]
    for asset in assets:
        for interval in intervals:
            candidates=list((args.root/'bist_equities'/asset).glob(f'*/bars/{interval}.csv'))
            if len(candidates)!=1: raise ValueError(f'{asset}/{interval} seri belirsiz')
            path=candidates[0]; bars=load_bars(path); series=path.parts[-3]
            if bars.empty or any(set(bars[col].astype(str))!={val} for col,val in [('asset_id',asset),('series_id',series),('interval',interval)]):
                raise ValueError(f'Girdi seri uyuşmuyor: {path}')
            key=f'{asset}:{series}:{interval}'
            if args.kind=='horizontal': zones,_,_=scan_zones(bars, config=config, series_key=key)
            elif args.kind=='sloped': zones,_,_=scan_sloped_zones(bars, config=SlopedConfig(zone=config), series_key=key)
            else: zones,_,_=scan_behavior_zones(bars, config=BehaviorConfig(kind=args.kind, zone=config), series_key=key)
            created=zones[zones.event.eq('zone_created')]
            visits=[]
            for zone in created.to_dict('records'):
                visits.extend(track_zone(bars,zone))
            inventory.append({'asset_id':asset,'interval':interval,'zones':len(created),'visits':len(visits),
                              'completed':sum(x['status']=='completed' for x in visits),
                              'censored':sum(x['status']=='censored' for x in visits)})
            manifest.append({'asset_id':asset,'interval':interval,'path':str(path),'sha256':sha(path),'usable_bars':len(bars)})
            if visits:
                frame=pd.DataFrame(visits); frame['asset_id']=asset;frame['interval']=interval;frame['kind']=args.kind
                frame=evaluate_bars(frame,bars,benchmarks[interval],cut1,cut2,end)
                # Kaynakları koru; analizde olay anına göre her tür/bar için tek temsilci.
                parts.append(frame[frame.representative].copy())
            print(f'{args.kind} {asset} {interval}: {len(created)} bölge, {len(visits)} ziyaret',flush=True)
    args.output.mkdir(parents=True, exist_ok=True)
    f=pd.concat(parts,ignore_index=True) if parts else pd.DataFrame()
    if not f.empty:
        f.to_csv(args.output/'events.csv.gz',index=False,compression='gzip')
        group_summary(f).to_csv(args.output/'groups.csv',index=False)
    pd.DataFrame(inventory).to_csv(args.output/'inventory.csv',index=False)
    pd.DataFrame(manifest).to_csv(args.output/'input-manifest.csv',index=False)
    files=[Path(__file__),Path('replayman/zone_lifecycle.py'),Path('replayman/zone_memory.py'),
           Path('replayman/behavior_zones.py'),Path('replayman/sloped_zones.py'),Path('replayman/replay.py'),Path('replayman/swings.py')]
    summary={'kind':args.kind,'intervals':intervals,'assets':len(assets),'representative_events':len(f),
             'boundary_train_end':str(cut1),'boundary_validation_end':str(cut2),'boundary_test_end':str(end),
             'benchmark_inputs':benchmark_inputs,'code_sha256':{x.name:sha(x) for x in files},
             'warning':'Önceden incelenmiş geçmiş, olay/ufuk/hisse bağımlılığı; bar etiketleri kapanış zamanı değil.'}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
