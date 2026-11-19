"""F01: aynı hisse ve benzer önceden bilinen özelliklerle eşleştirilmiş keşif.

Eşleştirmede ileri sonuç veya gerçekleşip gerçekleşmediği kullanılmaz; eksik
ufuk/benchmark, eşleştirmeden sonra ayrıca sansürlenir. Bağımsız test değildir.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from replayman.replay import load_bars

ROOT=Path('research/measurements/zone-memory')
MAX_BAR_DISTANCE=40
MIN_BAR_DISTANCE=6
VOL_RATIO=(.75,1/.75)
WIDTH_RATIO=(.5,2.)


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def add_covariates(events: pd.DataFrame, manifest: pd.DataFrame):
    if manifest.duplicated(['asset_id','interval']).any():raise ValueError('Yinelenen girdi manifesti')
    lookup=manifest.set_index(['asset_id','interval']);out=[]
    for (asset,interval),g in events.groupby(['asset_id','interval'],sort=True):
        info=lookup.loc[(asset,interval)];path=Path(info['path'])
        if sha(path)!=info.sha256:raise ValueError(f'Fiyat hash farklı: {path}')
        bars=load_bars(path); s=g.start_position.to_numpy(dtype=int);end=g.end_position.to_numpy(dtype=int)
        if (s<1).any() or (end>=len(bars)).any() or (end<s).any():raise ValueError('Pozisyon geçersiz')
        if not pd.to_datetime(g.end_bar_ts,utc=True).reset_index(drop=True).equals(bars.ts_utc.iloc[end].reset_index(drop=True)):
            raise ValueError('Bar etiketi uyuşmuyor')
        prev=bars.close.shift(1)
        tr=pd.concat([bars.high-bars.low,(bars.high-prev).abs(),(bars.low-prev).abs()],axis=1).max(axis=1)
        atr=tr.rolling(14,min_periods=14).mean().to_numpy(dtype=float)[s-1]
        reference=bars.close.to_numpy(dtype=float)[s-1]
        width=g.upper_at_start.to_numpy(dtype=float)-g.lower_at_start.to_numpy(dtype=float)
        valid=np.isfinite(atr)&(atr>0)&np.isfinite(reference)&(reference>0)&np.isfinite(width)&(width>0)
        vol=np.divide(atr,reference,out=np.full(len(g),np.nan),where=valid)
        scaled=np.divide(width,atr,out=np.full(len(g),np.nan),where=valid)
        z=g.reset_index(drop=True).copy();z['volatility_pre']=vol;z['width_atr_pre']=scaled
        out.append(z)
    return pd.concat(out,ignore_index=True) if out else pd.DataFrame()


def match_events(events: pd.DataFrame):
    """Vaka kronolojik; kontrol tekrar kullanılmaz, sonuç alanları incelenmez."""
    subset=events[(events.interval=='4h')&(events.end_side=='below')&events.pattern.isin(['cross_then_same','same_then_same'])].copy()
    subset=subset[(subset.start_position-subset.prior_end_position)>=11]
    subset=subset.sort_values(['asset_id','split','end_position','zone_id','visit_number']).reset_index(drop=True)
    pairs=[];unmatched=[];used=set()
    cases=subset[subset.pattern=='cross_then_same']
    controls=subset[subset.pattern=='same_then_same']
    for _,case in cases.iterrows():
        cid=f"{case.zone_id}:v{int(case.visit_number)}"
        if not np.isfinite(case.volatility_pre) or not np.isfinite(case.width_atr_pre) or case.volatility_pre<=0 or case.width_atr_pre<=0:
            unmatched.append({'asset_id':case.asset_id,'split':case['split'],'case_id':cid,'reason':'missing_covariates'});continue
        pool=controls[(controls.asset_id==case.asset_id)&(controls['split']==case['split'])&(~controls.index.isin(used))].copy()
        if not pool.empty:
            distance=(pool.end_position-case.end_position).abs()
            vr=pool.volatility_pre/case.volatility_pre
            wr=pool.width_atr_pre/case.width_atr_pre
            valid=(distance>=MIN_BAR_DISTANCE)&(distance<=MAX_BAR_DISTANCE)&vr.between(*VOL_RATIO)&wr.between(*WIDTH_RATIO)
            pool=pool[valid].copy()
            if not pool.empty:
                distance=(pool.end_position-case.end_position).abs()
                # Três explicitamente normalizados: tempo, volatilidade e largura.
                pool['_score']=distance/MAX_BAR_DISTANCE + np.abs(np.log(pool.volatility_pre/case.volatility_pre))/np.log(1/.75) + np.abs(np.log(pool.width_atr_pre/case.width_atr_pre))/np.log(2)
                pool=pool.sort_values(['_score','end_position','zone_id','visit_number'])
        if pool.empty:
            unmatched.append({'asset_id':case.asset_id,'split':case['split'],'case_id':cid,'reason':'no_eligible_unused_control'});continue
        control=pool.iloc[0];used.add(control.name)
        row={'asset_id':case.asset_id,'split':case['split'],'case_id':cid,
             'control_id':f"{control.zone_id}:v{int(control.visit_number)}",'bar_distance':abs(int(case.end_position-control.end_position)),
             'match_score':float(control['_score'])}
        for prefix,source in [('case',case),('control',control)]:
            for col in ['zone_id','visit_number','start_position','end_position','start_bar_ts','end_bar_ts',
                        'prior_end_position','volatility_pre','width_atr_pre','excess_5','directional_5','excess_10','directional_10']:
                row[f'{prefix}_{col}']=source[col]
        pairs.append(row)
    return pd.DataFrame(pairs),pd.DataFrame(unmatched,columns=['asset_id','split','case_id','reason'])


def bootstrap_cluster(values, labels, draws, rng):
    frame=pd.DataFrame({'value':values,'cluster':labels}).dropna()
    clusters=list(frame.groupby('cluster').value.apply(list))
    if len(clusters)<5:return np.nan,np.nan,len(clusters)
    simulated=[]
    for _ in range(draws):
        idx=rng.integers(0,len(clusters),size=len(clusters))
        simulated.append(float(np.median(np.concatenate([np.asarray(clusters[i]) for i in idx]))))
    lo,hi=np.quantile(simulated,[.025,.975]);return float(lo),float(hi),len(clusters)


def summarize_pairs(pairs, draws=1000, seed=20261117):
    if draws<1:raise ValueError('draws pozitif olmalı')
    rng=np.random.default_rng(seed);rows=[]
    if pairs.empty:return pd.DataFrame()
    for split,g in pairs.groupby('split',sort=True):
        for horizon in (5,10):
            for metric in ('excess','directional'):
                cols=[f'case_{metric}_{horizon}',f'control_{metric}_{horizon}']
                z=g.dropna(subset=cols).copy()
                if z.empty:continue
                delta=z[cols[0]]-z[cols[1]]
                weeks=pd.to_datetime(z.case_end_bar_ts,utc=True).dt.tz_localize(None).dt.to_period('W-SUN').dt.start_time
                wlo,whi,weeks_n=bootstrap_cluster(delta, weeks,draws,rng)
                alo,ahi,assets_n=bootstrap_cluster(delta, z.asset_id,draws,rng)
                rows.append({'split':split,'horizon':horizon,'metric':metric,'matched_pairs':len(g),
                             'eligible_pairs':len(z),'assets':z.asset_id.nunique(),
                             'case_median':z[cols[0]].median(),'control_median':z[cols[1]].median(),
                             'paired_median_difference':delta.median(),'paired_mean_difference':delta.mean(),
                             'case_higher':int((delta>0).sum()),'control_higher':int((delta<0).sum()),
                             'equal':int((delta==0).sum()),'week_clusters':weeks_n,'week_low':wlo,'week_high':whi,
                             'asset_clusters':assets_n,'asset_low':alo,'asset_high':ahi,'draws':draws})
    return pd.DataFrame(rows)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--draws',type=int,default=1000);args=p.parse_args(argv)
    source=args.root/'lifecycle-horizontal/events.csv.xz';manifest_path=args.root/'lifecycle-horizontal/input-manifest.csv'
    raw=pd.read_csv(source);m=pd.read_csv(manifest_path)
    candidates=raw[(raw.interval=='4h')&(raw.end_side=='below')&raw.pattern.isin(['cross_then_same','same_then_same'])].copy()
    candidates=candidates[(candidates.start_position-candidates.prior_end_position)>=11]
    data=add_covariates(candidates,m);pairs,unmatched=match_events(data)
    args.output.mkdir(parents=True,exist_ok=True)
    pairs.to_csv(args.output/'pairs.csv',index=False);unmatched.to_csv(args.output/'unmatched.csv',index=False)
    summarize_pairs(pairs,args.draws).to_csv(args.output/'results.csv',index=False)
    coverage=data.groupby(['split','pattern']).agg(events=('asset_id','size'),assets=('asset_id','nunique')).reset_index()
    coverage.to_csv(args.output/'eligible-inputs.csv',index=False)
    manifest={'status':'post_hoc_exploratory','input_path':str(source),'input_sha256':sha(source),
              'input_manifest_sha256':sha(manifest_path),'code_sha256':sha(Path(__file__)),'loader_sha256':sha('replayman/replay.py'),
              'bar_distance_min':MIN_BAR_DISTANCE,'bar_distance_max':MAX_BAR_DISTANCE,
              'vol_ratio_control_to_case':VOL_RATIO,'width_ratio_control_to_case':WIDTH_RATIO,'bootstrap_draws':args.draws,'seed':20261117,
              'note':'Aynı hisse, dönem ve yön; 11+ bar gecikme; greedy sonuç kullanmayan eşleştirme; kontrol gelecek veya geçmiş zamanda olabilir.'}
    (args.output/'summary.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('inputs',len(data),'pairs',len(pairs),'unmatched_cases',len(unmatched))
    return 0


if __name__=='__main__':raise SystemExit(main())
