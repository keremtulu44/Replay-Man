"""Yatay 4s geçiş adaylarında geri geliş, tamamlanma ve sağ sansür incelemesi."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from replayman.replay import load_bars
from replayman.zone_memory import ZoneConfig, scan_zones
from replayman.zone_lifecycle import track_zone

ROOT=Path('research/measurements/zone-memory')
HORIZONS=(10,20,40)


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def classify_window(candidate, next_visit, horizon, full_window):
    """Yalnız aday sonrası sabit pencereye göre durum; eksik pencere sansürlü."""
    if horizon<1:raise ValueError('Ufuk pozitif olmalı')
    end=int(candidate['end_position']);limit=end+horizon
    start=None if next_visit is None else int(next_visit['start_position'])
    found=start is not None and start<=limit
    # Veri veya bölüm sonu öncesi gerçekleşmiş geri geliş varsa açıklama korunur;
    # tam-pencere oranları yalnız yeterli gözleme sahip adayları içerir.
    if not full_window:
        return {'status':'censored','return_observed':bool(found),'late_return':bool(found and start-end>=11)}
    if not found:return {'status':'no_return','return_observed':False,'late_return':False}
    late=start-end>=11
    pos=next_visit.get('end_position')
    if pos is None or pd.isna(pos) or int(pos)>limit:
        return {'status':'return_open_at_horizon','return_observed':True,'late_return':late}
    if next_visit.get('start_side')==candidate.get('end_side') and next_visit.get('path')=='same':
        return {'status':'same_side_complete','return_observed':True,'late_return':late}
    if next_visit.get('path')=='cross':
        return {'status':'opposite_side_complete','return_observed':True,'late_return':late}
    return {'status':'unknown_complete','return_observed':True,'late_return':late}


def summary(frame):
    rows=[]
    for (split,scenario,horizon),g in frame.groupby(['split','scenario','horizon']):
        observed=g[g.status!='censored']
        rows.append({'split':split,'scenario':scenario,'horizon':horizon,'candidates':len(g),
                     'assets':g.asset_id.nunique(),'full_windows':len(observed),
                     'censored':int(g.status.eq('censored').sum()),
                     'censored_return_observed':int((g.status.eq('censored')&g.return_observed).sum()),
                     'no_return':int(observed.status.eq('no_return').sum()),
                     'return_started':int(observed.return_observed.sum()),
                     'return_late_started':int(observed.late_return.sum()),
                     'same_side_complete':int(observed.status.eq('same_side_complete').sum()),
                     'same_side_complete_late':int((observed.status.eq('same_side_complete')&observed.late_return).sum()),
                     'opposite_side_complete':int(observed.status.eq('opposite_side_complete').sum()),
                     'return_open_at_horizon':int(observed.status.eq('return_open_at_horizon').sum()),
                     'unknown_complete':int(observed.status.eq('unknown_complete').sum()),
                     'fraction_return_started_full':observed.return_observed.mean() if len(observed) else None,
                     'fraction_same_side_complete_full':observed.status.eq('same_side_complete').mean() if len(observed) else None})
    return pd.DataFrame(rows)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--output',type=Path,required=True);args=p.parse_args(argv)
    lifecycle=args.root/'lifecycle-horizontal';manifest_path=lifecycle/'input-manifest.csv';manifest=pd.read_csv(manifest_path)
    manifest=manifest[manifest.interval=='4h'].sort_values('asset_id')
    if manifest.asset_id.duplicated().any():raise ValueError('Birden fazla seri')
    meta=json.loads((lifecycle/'summary.json').read_text());cut1=pd.Timestamp(meta['boundary_train_end']);cut2=pd.Timestamp(meta['boundary_validation_end']);last=pd.Timestamp(meta['boundary_test_end'])
    saved=pd.read_csv(lifecycle/'events.csv.xz');saved=saved[(saved.interval=='4h')&saved.scenario.isin(['up_candidate','down_candidate'])]
    saved_keys=set(zip(saved.asset_id,saved.zone_id,saved.end_position.astype(int),saved.scenario))
    generated_keys=set();out=[]
    for _,item in manifest.iterrows():
        path=Path(item.path)
        if sha(path)!=item.sha256:raise ValueError(f'Fiyat hash uyuşmuyor: {path}')
        bars=load_bars(path);series=path.parts[-3];key=f'{item.asset_id}:{series}:4h'
        zones,_,_=scan_zones(bars,config=ZoneConfig(),series_key=key)
        rows=[]
        for zone in zones[zones.event.eq('zone_created')].to_dict('records'):
            visits=track_zone(bars,zone)
            for i,visit in enumerate(visits):
                rows.append({**visit,'next_visit':visits[i+1] if i+1<len(visits) else None})
        done=[x for x in rows if x['status']=='completed']
        # Önce TÜM biten ziyaretlerde temsilci seçilir; yalnız sonra aday filtrelenir.
        done.sort(key=lambda x:(x['end_position'],x['zone_id'],x['visit_number']))
        seen=set()
        for v in done:
            pos=int(v['end_position'])
            if pos in seen:continue
            seen.add(pos)
            if v['scenario'] not in ('up_candidate','down_candidate'):continue
            generated_keys.add((item.asset_id,v['zone_id'],pos,v['scenario']))
            t=bars.ts_utc.iloc[pos];split='train' if t<cut1 else 'validation' if t<cut2 else 'test'
            boundary={'train':cut1,'validation':cut2,'test':last}[split]
            n=v['next_visit']
            for horizon in HORIZONS:
                endpoint=pos+horizon
                full=endpoint<len(bars) and bars.ts_utc.iloc[endpoint]<boundary
                # Bölüm sınırından sonra gerçekleşen ziyaret, o bölümde gözlenmemiştir.
                observed_next=n if n is not None and pd.Timestamp(n['start_bar_ts'])<boundary else None
                state=classify_window(v,observed_next,horizon,full)
                out.append({'asset_id':item.asset_id,'zone_id':v['zone_id'],'visit_number':v['visit_number'],
                            'candidate_position':pos,'candidate_bar_ts':str(t),'split':split,'scenario':v['scenario'],
                            'horizon':horizon,**state})
        print(item.asset_id,flush=True)
    if generated_keys!=saved_keys:
        raise ValueError(f'Önceki temsilcilerle uyuşmazlık: missing={len(saved_keys-generated_keys)} extra={len(generated_keys-saved_keys)}')
    frame=pd.DataFrame(out);args.output.mkdir(parents=True,exist_ok=True)
    frame.to_csv(args.output/'cohort.csv.xz',index=False,compression={'method':'xz','preset':6})
    summary(frame).to_csv(args.output/'summary.csv',index=False)
    info={'status':'exploratory','assets':len(manifest),'event_count':len(generated_keys),'horizons':HORIZONS,
          'input_manifest_sha256':sha(manifest_path),'reference_events_sha256':sha(lifecycle/'events.csv.xz'),
          'code_sha256':sha(Path(__file__)),'lifecycle_sha256':sha('replayman/zone_lifecycle.py'),
          'scanner_sha256':sha('replayman/zone_memory.py'),'loader_sha256':sha('replayman/replay.py'),
          'note':'Tam pencere ve bölüm sansürü; sayım aynı bölgenin ilk sonraki ziyaretini izler; temas sırası OHLC ile bilinmez.'}
    (args.output/'summary.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(info,ensure_ascii=False,indent=2))
    return 0


if __name__=='__main__':raise SystemExit(main())
