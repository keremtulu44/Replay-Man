"""F01: geri temas/gelmeme öncesi yol ve eşli sonuç bileşenleri.

Gözlemsel ilişki: gerçek alış/satış niyeti veya nedensel açıklama değildir.
Bitişten sonraki beş bar özelliği yalnız beşinci barda bilinir; önceki
ziyaretler/erken geri temaslar landmark karşılaştırmasına alınmaz.
"""
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
from tools.measure_f01_censoring import classify_window
from tools.summarize_lifecycle import compare_groups

ROOT=Path('research/measurements/zone-memory')


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def categorize(end, next_start, full_window):
    """İlk sonraki ziyaretin zamanı; eksik 20-bar penceresi ayrı."""
    if not full_window:return 'censored'
    if next_start is None or pd.isna(next_start) or int(next_start)>int(end)+20:return 'no_20'
    gap=int(next_start)-int(end)
    if gap < 1:raise ValueError('Sonraki ziyaret bitişten sonra başlamalı')
    if gap<=5:return 'early_1_5'
    if gap<=10:return 'return_6_10'
    return 'return_11_20'


def candidate_features(bars, visit, next_start, full_window, cutoff):
    """Aday kapanışı ve ilk beş barda bilinenler; daha sonraki mum kullanılmaz."""
    e=int(visit['end_position']);s=int(visit['start_position'])
    if e<s or e>=len(bars):raise ValueError('Pozisyon geçersiz')
    end_ts=bars.ts_utc.iloc[e]
    if end_ts!=pd.Timestamp(visit['end_bar_ts']):raise ValueError('Olay zaman etiketi uyuşmuyor')
    prev=bars.close.shift(1)
    tr=pd.concat([bars.high-bars.low,(bars.high-prev).abs(),(bars.low-prev).abs()],axis=1).max(axis=1)
    atr=tr.rolling(14,min_periods=14).mean().iloc[e]
    side=visit['end_side']; sign=1. if side=='above' else -1. if side=='below' else None
    if sign is None:raise ValueError('Giriş yönü yok')
    category=categorize(e,next_start,full_window)
    rec={'bucket':category,'candidate_duration':e-s+1,'touch_bars':int(visit['touch_bars']),
         'prior_completed_visits':int(visit['visit_number'])-1,'ambiguous_bars':int(visit['ambiguous_bars']),
         'atr_end':float(atr) if np.isfinite(atr) else None,
         'atr_over_close':None,'band_width_atr':None,'initial_distance_atr':None,
         'distance_after5_atr':None,'outward_progress5_atr':None,
         'away_wick5_atr':None,'toward_wick5_atr':None,'eligible_landmark':False}
    boundary=visit['upper_at_start'] if side=='above' else visit['lower_at_start']
    close0=float(bars.close.iloc[e])
    if not np.isfinite(atr) or atr<=0 or close0<=0:return rec
    rec['atr_over_close']=float(atr/close0)
    rec['band_width_atr']=float((visit['upper_at_start']-visit['lower_at_start'])/atr)
    rec['initial_distance_atr']=float(sign*(close0-boundary)/atr)
    end5=e+5
    if end5>=len(bars) or bars.ts_utc.iloc[end5]>=cutoff:return rec
    # İlk beş barda yeni ziyaret olursa onun gerçekleşmiş sonucu yaklaşım öncesi
    # bilgiymiş gibi kullanılamaz. Tam 20 pencere de gerekir.
    if category in ('censored','early_1_5'):return rec
    future=bars.iloc[e+1:end5+1];close5=float(bars.close.iloc[end5]);rec['eligible_landmark']=True
    rec['distance_after5_atr']=float(sign*(close5-boundary)/atr)
    rec['outward_progress5_atr']=float(sign*(close5-close0)/atr)
    if sign>0:
        away=max(0.,float(future.high.max())-close0);toward=max(0.,close0-float(future.low.min()))
    else:
        away=max(0.,close0-float(future.low.min()));toward=max(0.,float(future.high.max())-close0)
    rec['away_wick5_atr']=float(away/atr);rec['toward_wick5_atr']=float(toward/atr)
    return rec


def describe_landmark(data):
    x=data[data.eligible_landmark].copy()
    x['outcome']=np.where(x.bucket=='no_20','no_20','return_6_20')
    cols=['atr_over_close','band_width_atr','candidate_duration','touch_bars','prior_completed_visits',
          'initial_distance_atr','distance_after5_atr','outward_progress5_atr','away_wick5_atr','toward_wick5_atr']
    rows=[]
    for key,g in x.groupby(['split','scenario','outcome']):
        row=dict(zip(['split','scenario','outcome'],key));row.update(n=len(g),assets=g.asset_id.nunique())
        for col in cols:
            vals=g[col].dropna();row[col+'_median']=vals.median() if len(vals) else None
        rows.append(row)
    return pd.DataFrame(rows)


def distance_bins(data):
    x=data[data.eligible_landmark & data.distance_after5_atr.notna()].copy()
    x['distance_bin']=np.select([x.distance_after5_atr<0,x.distance_after5_atr<=1,x.distance_after5_atr<=2],['opposite_side','0_to_1','1_to_2'],default='>2')
    x['returned']=x.bucket.isin(['return_6_10','return_11_20'])
    return x.groupby(['split','scenario','distance_bin']).agg(n=('returned','size'),assets=('asset_id','nunique'),
              returns_6_20=('returned','sum'),fraction_return_6_20=('returned','mean')).reset_index()


def landmark_differences(data, draws=500):
    x=data[data.eligible_landmark].copy()
    x['pattern']=np.where(x.bucket=='no_20','cross_then_same','same_then_same')
    x['kind']='horizontal';x['interval']='4h';x['end_side']=x.scenario.map({'up_candidate':'above','down_candidate':'below'})
    x['end_bar_ts']=x.candidate_bar_ts
    rows=[]
    for col in ['initial_distance_atr','distance_after5_atr','outward_progress5_atr','band_width_atr']:
        sample=x.assign(excess_5=x[col])
        comp=compare_groups(sample,draws=draws,seed=20261117)
        if len(comp):comp['metric']=col;rows.append(comp)
    return pd.concat(rows,ignore_index=True) if rows else pd.DataFrame()


def bin_contrast(data, draws=500, seed=20261117):
    """Aynı tarafta yakın (0–1 ATR) eksi uzak (>2 ATR) geri geliş oranı."""
    rng=np.random.default_rng(seed);x=data[data.eligible_landmark & data.distance_after5_atr.notna()].copy()
    x=x[((x.distance_after5_atr>=0)&(x.distance_after5_atr<=1))|(x.distance_after5_atr>2)].copy()
    x['near']=x.distance_after5_atr<=1
    x['returned']=x.bucket.isin(['return_6_10','return_11_20'])
    x['week']=pd.to_datetime(x.candidate_bar_ts,utc=True).dt.tz_localize(None).dt.to_period('W-SUN').dt.start_time
    rows=[]
    for (split,scenario),g in x.groupby(['split','scenario']):
        near=g[g.near];far=g[~g.near]
        if near.empty or far.empty:continue
        def boot(cluster):
            table=g.groupby([cluster,'near']).returned.agg(['sum','size']).reset_index()
            labels=table[cluster].drop_duplicates().tolist()
            if len(labels)<5:return np.nan,np.nan,len(labels)
            mat=np.zeros((len(labels),4),dtype=float);idx={v:i for i,v in enumerate(labels)}
            for z in table.to_dict('records'):
                k=idx[z[cluster]];j=0 if z['near'] else 2;mat[k,j]=z['sum'];mat[k,j+1]=z['size']
            pick=rng.integers(0,len(labels),size=(draws,len(labels)))
            totals=mat[pick].sum(axis=1);valid=(totals[:,1]>0)&(totals[:,3]>0)
            differences=totals[valid,0]/totals[valid,1]-totals[valid,2]/totals[valid,3]
            if not len(differences):return np.nan,np.nan,len(labels)
            low,high=np.quantile(differences,[.025,.975]);return low,high,len(labels)
        wlo,whi,wn=boot('week');alo,ahi,an=boot('asset_id')
        rows.append({'split':split,'scenario':scenario,'near_n':len(near),'far_n':len(far),
                     'near_return_rate':near.returned.mean(),'far_return_rate':far.returned.mean(),
                     'difference':near.returned.mean()-far.returned.mean(),'week_clusters':wn,'week_low':wlo,'week_high':whi,
                     'asset_clusters':an,'asset_low':alo,'asset_high':ahi,'draws':draws})
    return pd.DataFrame(rows)


def pair_decomposition(pairs):
    rows=[]
    for split,g in pairs.groupby('split'):
        z=g.dropna(subset=['case_directional_5','control_directional_5','case_excess_5','control_excess_5']).copy()
        if z.empty:continue
        z['raw_delta']=z.case_directional_5-z.control_directional_5
        z['excess_delta']=z.case_excess_5-z.control_excess_5
        z['market_delta']=z.raw_delta-z.excess_delta
        rows.append({'split':split,'pairs':len(z),'assets':z.asset_id.nunique(),
                     'mean_raw_delta':z.raw_delta.mean(),'mean_market_delta':z.market_delta.mean(),
                     'mean_excess_delta':z.excess_delta.mean(),'median_raw_delta':z.raw_delta.median(),
                     'median_excess_delta':z.excess_delta.median(),
                     'later_controls':int((z.control_end_position>z.case_end_position).sum())})
    return pd.DataFrame(rows)


def pair_filter_breakdown(pairs,features):
    key=['asset_id','zone_id','visit_number']
    f=features[(features.interval=='4h')&(features.kind=='horizontal')][key+[f'F{i:02}' for i in range(2,11)]]
    if f.duplicated(key).any():raise ValueError('Olay filtre kimliği yinelendi')
    p=pairs.rename(columns={'case_zone_id':'zone_id','case_visit_number':'visit_number'}).merge(f,on=key,how='left',validate='many_to_one')
    if p.F02.isna().any():raise ValueError('Eşleşmiş vakaların filtre kaydı eksik')
    p=p.dropna(subset=['case_excess_5','control_excess_5','case_directional_5','control_directional_5']).copy()
    p['delta_excess']=p.case_excess_5-p.control_excess_5;p['delta_raw']=p.case_directional_5-p.control_directional_5
    rows=[]
    for fid in [f'F{i:02}' for i in range(2,11)]:
        for (split,level),g in p.groupby(['split',fid]):
            rows.append({'split':split,'filter':fid,'level':level,'pairs':len(g),'assets':g.asset_id.nunique(),
                         'median_excess_delta':g.delta_excess.median(),'median_raw_delta':g.delta_raw.median(),
                         'case_wins':int((g.delta_excess>0).sum()),'control_wins':int((g.delta_excess<0).sum())})
    return pd.DataFrame(rows)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--output',type=Path,required=True);args=p.parse_args(argv)
    root=args.root; source=root/'lifecycle-horizontal/events.csv.xz';cohort_path=root/'f01-censoring/cohort.csv.xz'
    prices_path=root/'lifecycle-horizontal/input-manifest.csv';pair_path=root/'f01-matched/pairs.csv';feature_path=root/'ten-filters/features.csv.xz'
    events=pd.read_csv(source);events=events[(events.interval=='4h')&events.scenario.isin(['up_candidate','down_candidate'])]
    c=pd.read_csv(cohort_path);c=c[c.horizon==20]
    keys=['asset_id','zone_id','visit_number','scenario']
    data=c.merge(events,on=keys,how='left',suffixes=('_cohort',''),validate='one_to_one')
    if data.end_position.isna().any() or not (data.candidate_position==data.end_position).all():raise ValueError('Aday kayıtları uyuşmuyor')
    if not (data.split_cohort==data['split']).all():raise ValueError('Dönemler uyuşmuyor')
    manifest=pd.read_csv(prices_path);manifest=manifest[manifest.interval=='4h'].set_index('asset_id')
    metadata=json.loads((root/'lifecycle-horizontal/summary.json').read_text())
    cut1=pd.Timestamp(metadata['boundary_train_end']);cut2=pd.Timestamp(metadata['boundary_validation_end']);last=pd.Timestamp(metadata['boundary_test_end'])
    parts=[]
    for asset,g in data.groupby('asset_id',sort=True):
        info=manifest.loc[asset];path=Path(info.path)
        if sha(path)!=info.sha256:raise ValueError(f'Girdi hash uyuşmuyor: {path}')
        bars=load_bars(path);series=path.parts[-3]
        zones,_,_=scan_zones(bars,config=ZoneConfig(),series_key=f'{asset}:{series}:4h')
        needed=set(g.zone_id);source_zones=zones[(zones.event=='zone_created')&zones.zone_id.isin(needed)]
        if set(source_zones.zone_id)!=needed:raise ValueError('Bölge kaynakları eksik')
        visits={}
        for zone in source_zones.to_dict('records'):
            full=track_zone(bars,zone)
            for i,v in enumerate(full):visits[(v['zone_id'],v['visit_number'])]=(v,full[i+1] if i+1<len(full) else None)
        for item in g.to_dict('records'):
            v,n=visits[(item['zone_id'],int(item['visit_number']))]
            boundary={'train':cut1,'validation':cut2,'test':last}[item['split']]
            next_visit=n if n is not None and pd.Timestamp(n['start_bar_ts'])<boundary else None
            full_window=item['status_cohort']!='censored'
            check=classify_window(v,next_visit,20,full_window)
            if check['status']!=item['status_cohort'] or check['return_observed']!=item['return_observed']:
                raise ValueError('Önceki sansür sonucu uyuşmuyor')
            pos=None if next_visit is None else next_visit['start_position']
            feat=candidate_features(bars,v,pos,full_window,boundary)
            parts.append({'asset_id':asset,'zone_id':v['zone_id'],'visit_number':v['visit_number'],
                          'candidate_position':v['end_position'],'candidate_bar_ts':v['end_bar_ts'],
                          'split':item['split'],'scenario':v['scenario'],'horizon20_status':item['status_cohort'],
                          'next_gap':None if pos is None or pos>v['end_position']+20 else pos-v['end_position'],**feat})
        print(asset,flush=True)
    out=pd.DataFrame(parts);pairs=pd.read_csv(pair_path);features=pd.read_csv(feature_path)
    args.output.mkdir(parents=True,exist_ok=True)
    out.to_csv(args.output/'candidates.csv.xz',index=False,compression={'method':'xz','preset':6})
    describe_landmark(out).to_csv(args.output/'landmark-groups.csv',index=False)
    distance_bins(out).to_csv(args.output/'landmark-distance.csv',index=False)
    landmark_differences(out).to_csv(args.output/'landmark-differences.csv',index=False)
    bin_contrast(out).to_csv(args.output/'landmark-bin-contrast.csv',index=False)
    out.groupby(['split','scenario','bucket']).agg(n=('bucket','size'),assets=('asset_id','nunique')).reset_index().to_csv(args.output/'candidate-outcomes.csv',index=False)
    pair_decomposition(pairs).to_csv(args.output/'pair-decomposition.csv',index=False)
    pair_filter_breakdown(pairs,features).to_csv(args.output/'pair-filters.csv',index=False)
    inputs=[source,cohort_path,prices_path,pair_path,feature_path]
    meta={'status':'exploratory_post_hoc','inputs':[{'path':str(x),'sha256':sha(x)} for x in inputs],
          'records':len(out),'code_sha256':sha(Path(__file__)),'lifecycle_sha256':sha('replayman/zone_lifecycle.py'),
          'scanner_sha256':sha('replayman/zone_memory.py'),'loader_sha256':sha('replayman/replay.py'),
          'comparison_sha256':sha('tools/summarize_lifecycle.py'),'censor_logic_sha256':sha('tools/measure_f01_censoring.py'),
          'warning':'İlk beş bar landmark; yalnız 20 bar tam pencere; hiçbir neden/işlem sinyali kanıtlanmaz.'}
    (args.output/'summary.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(meta,ensure_ascii=False,indent=2))
    return 0


if __name__=='__main__':raise SystemExit(main())
