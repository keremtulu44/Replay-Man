"""On önceden tanımlanmış lifecycle filtresinin geçmiş veri üzerinde keşif testi.

Tüm filtreler ikinci ziyaret kapanışında bilinir. Gelecek OHLC yalnız önceden
ayrılmış çıktı alanlarından okunur; yatırım veya bağımsız test değildir.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from replayman.replay import load_bars
from tools.summarize_lifecycle import compare_groups

KINDS=['horizontal','dwell','impulse','sloped']
FILTERS={
 'F01':'previous_gap_11plus', 'F02':'touches_3plus', 'F03':'visit_duration_5plus',
 'F04':'approach_toward_1atr_5bar', 'F05':'approach_progress_rising',
 'F06':'approach_efficiency_atleast_060', 'F07':'band_width_le_1atr',
 'F08':'exit_progress_atleast_half_atr', 'F09':'visit_has_both_bounds_bar',
 'F10':'at_least_3_prior_visits',
}


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def indicator(mask, valid):
    return pd.Series(np.where(valid, np.where(mask,'yes','no'),'unknown'))


def extract_features(bars: pd.DataFrame, events: pd.DataFrame):
    """Yaklaşım yalnız start öncesi; ziyaret ölçüleri yalnız end'e kadar."""
    close=bars.close.to_numpy(dtype=float);high=bars.high.to_numpy(dtype=float);low=bars.low.to_numpy(dtype=float)
    prev=bars.close.shift(1)
    tr=pd.concat([bars.high-bars.low,(bars.high-prev).abs(),(bars.low-prev).abs()],axis=1).max(axis=1)
    atr=tr.rolling(14,min_periods=14).mean().to_numpy(dtype=float)
    s=events.start_position.to_numpy(dtype=int);e=events.end_position.to_numpy(dtype=int)
    if (s<1).any() or (e<s).any() or (e>=len(close)).any():raise ValueError('Geçersiz ziyaret konumu')
    stamps=pd.to_datetime(events.end_bar_ts,utc=True).reset_index(drop=True)
    if not stamps.equals(bars.ts_utc.iloc[e].reset_index(drop=True)):
        raise ValueError('Bitiş etiketi veya bar pozisyonu uyuşmuyor')
    # Valid indices guarded by masks, clamped only to avoid wraparound access.
    prev_atr=atr[s-1];valid_atr=np.isfinite(prev_atr)&(prev_atr>0)
    enough=s>=11
    prev5=np.maximum(s-6,0);prev10=np.maximum(s-11,0)
    direction_to_band=np.where(events.start_side.to_numpy()=='below',1.,-1.)
    valid_side=events.start_side.isin(['above','below']).to_numpy()
    recent=direction_to_band*(close[s-1]-close[prev5])
    prior=direction_to_band*(close[prev5]-close[prev10])
    path_cum=np.r_[0.,np.cumsum(np.abs(np.diff(close)))]
    path=path_cum[s-1]-path_cum[prev10]
    net=np.abs(close[s-1]-close[prev10]); eff=np.divide(net,path,out=np.full(len(s),np.nan),where=path>0)
    gap=s-pd.to_numeric(events.prior_end_position,errors='coerce').to_numpy(dtype=float)
    width=events.upper_at_start.to_numpy(dtype=float)-events.lower_at_start.to_numpy(dtype=float)
    exit_direction=np.where(events.end_side.to_numpy()=='above',1.,-1.)
    out=pd.DataFrame(index=range(len(events)))
    out['F01']=indicator(gap>=11,np.isfinite(gap)&(gap>=1))
    touch=pd.to_numeric(events.touch_bars,errors='coerce').to_numpy(dtype=float)
    out['F02']=indicator(touch>=3,np.isfinite(touch)&(touch>=1))
    out['F03']=indicator((e-s+1)>=5,np.ones(len(s),dtype=bool))
    out['F04']=indicator(recent>=prev_atr,(s>=6)&valid_atr&valid_side)
    out['F05']=indicator(recent>prior,enough&valid_atr&valid_side)
    out['F06']=indicator(eff>=.6,enough&np.isfinite(eff))
    out['F07']=indicator(width<=prev_atr,np.isfinite(width)&(width>=0)&valid_atr)
    out['F08']=indicator(exit_direction*(close[e]-close[np.maximum(e-2,0)])>=.5*prev_atr,(e>=2)&valid_atr)
    amb=pd.to_numeric(events.ambiguous_bars,errors='coerce').to_numpy(dtype=float)
    out['F09']=indicator(amb>=1,np.isfinite(amb)&(amb>=0))
    prior_count=pd.to_numeric(events.visit_number,errors='coerce').to_numpy(dtype=float)-1
    out['F10']=indicator(prior_count>=3,np.isfinite(prior_count)&(prior_count>=0))
    return out


def load_data(root: Path):
    inputs=[];parts=[]; manifests=[]
    for kind in KINDS:
        folder=root/f'lifecycle-{kind}'
        path=folder/'events.csv.xz';mf=folder/'input-manifest.csv'
        data=pd.read_csv(path)
        parts.append(data[data.pattern.isin(['cross_then_same','same_then_same'])].copy())
        manifests.append(pd.read_csv(mf)[['asset_id','interval','path','sha256']])
        inputs.append({'path':str(path),'sha256':sha(path), 'manifest_sha256':sha(mf)})
    manifest=pd.concat(manifests,ignore_index=True)
    if (manifest.groupby(['asset_id','interval']).sha256.nunique()>1).any():raise ValueError('Fiyat manifestleri farklı')
    manifest=manifest.drop_duplicates(['asset_id','interval']).set_index(['asset_id','interval'])
    data=pd.concat(parts,ignore_index=True)
    output=[]
    for (asset,interval),g in data.groupby(['asset_id','interval'],sort=True):
        info=manifest.loc[(asset,interval)];path=Path(info['path'])
        if sha(path)!=info['sha256']:raise ValueError(f'Fiyat hash farklı: {path}')
        bars=load_bars(path)
        features=extract_features(bars,g)
        output.append(pd.concat([g.reset_index(drop=True),features],axis=1))
    return pd.concat(output,ignore_index=True),inputs


def compare_all(data:pd.DataFrame, draws=500):
    summaries=[]; desc=[]
    usable=data[data.excess_5.notna()].copy()
    for fid in FILTERS:
        valid=usable[usable[fid].isin(['yes','no'])].copy()
        # Filtre evet/hayır, yalnız ikinci ziyaret senaryosunda.
        within=valid[valid.pattern.eq('cross_then_same')].copy()
        within['pattern']=np.where(within[fid].eq('yes'),'cross_then_same','same_then_same')
        c=compare_groups(within,draws=draws,seed=20261117)
        if len(c):c['comparison']='filter_yes_vs_no_in_retest';c['filter_id']=fid;summaries.append(c)
        # Aynı filtre kategorisinde retest ile iki aynı-taraf ziyaret kontrolü.
        same_filter=valid[valid[fid].eq('yes')].copy()
        c=compare_groups(same_filter,draws=draws,seed=20261117)
        if len(c):c['comparison']='retest_vs_control_filter_yes';c['filter_id']=fid;summaries.append(c)
        grouped=valid.groupby(['kind','interval','split','end_side','pattern',fid],sort=True)
        x=grouped.agg(n=('excess_5','size'),assets=('asset_id','nunique'),
                      excess_median=('excess_5','median'),raw_directional_median=('directional_5','median'),
                      raw_positive=('directional_5',lambda z:(z>0).mean())).reset_index().rename(columns={fid:'filter_value'})
        x['filter_id']=fid;desc.append(x)
    return pd.concat(desc,ignore_index=True),pd.concat(summaries,ignore_index=True)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path('research/measurements/zone-memory'))
    p.add_argument('--output',type=Path,required=True);p.add_argument('--draws',type=int,default=500);args=p.parse_args(argv)
    data,inputs=load_data(args.root);groups,comparisons=compare_all(data,args.draws)
    args.output.mkdir(parents=True,exist_ok=True)
    keys=['asset_id','interval','kind','zone_id','visit_number','start_position','end_position']
    data[keys+list(FILTERS)].to_csv(args.output/'features.csv.xz',index=False,compression={'method':'xz','preset':6})
    groups.to_csv(args.output/'groups.csv',index=False)
    comparisons.to_csv(args.output/'comparisons.csv',index=False)
    manifest={'status':'exploratory_post_hoc','intervals':['1d','4h'],'filters':FILTERS,'inputs':inputs,'records':len(data),
              'draws':args.draws,'seed':20261117,'source_sha256':sha(Path(__file__)),
              'bootstrap_sha256':sha('tools/summarize_lifecycle.py'),'bar_loader_sha256':sha('replayman/replay.py'),
              'warning':'Tarihsel veri önceden incelendi; alt gruplar bağımsız/eşleştirilmiş değil, çoklu deneme düzeltmesi yok.'}
    (args.output/'summary.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(data)} olay, {len(groups)} grup, {len(comparisons)} karşılaştırma')
    return 0


if __name__=='__main__':raise SystemExit(main())
