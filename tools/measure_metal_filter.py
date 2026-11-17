"""Sabitlenmiş metal risk uyarılarını sanal işlem adaylarında karşılaştırır."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from replayman.replay import load_bars
from replayman.tenbar_research import times, make_windows
from replayman.metal_backtest import signal_features, metal_windows, post_labels, expanding_history, simulate, period
from tools.measure_tenbar_reactions import one_path, get_paths


def group_stats(df,keys,mode,threshold,cost):
    """Aynı bilinen adaylara ait filtresiz, korunan ve elenen sonuçlar."""
    states=[]
    for metal in ('gold','silver'):
        ret=df[metal+'_return'].to_numpy(float);n=df[metal+'_n'].to_numpy(float);down=df[metal+'_down'].to_numpy(float)
        st=np.full(len(df),'unknown',dtype=object)
        finite=np.isfinite(ret);st[finite&(np.abs(ret)<=.02)]='no_signal'
        eligible=finite&(np.abs(ret)>.02)&(n>=10)
        st[eligible]='clear';st[eligible&(down/np.maximum(n,1)>=threshold)]='warning'
        states.append(st)
    a,b=states
    if mode=='gold':state=a
    elif mode=='silver':state=b
    elif mode=='either':state=np.where((a=='warning')|(b=='warning'),'warning',np.where((a=='unknown')|(b=='unknown'),'unknown','clear'))
    else:raise ValueError(mode)
    x=df[keys].copy();x['state']=state;x['available']=df.gross_lower.notna().to_numpy();x['ambiguous']=df.exit_reason.eq('ambiguous').to_numpy()
    x['lower']=df.gross_lower.to_numpy(float)-cost;x['upper']=df.gross_upper.to_numpy(float)-cost
    x['symbol']=df.target_symbol.to_numpy()
    for label,mask in [('all',np.ones(len(x),bool)),('paired',state!='unknown'),('kept',(state!='unknown')&(state!='warning')),('blocked',state=='warning'),('unknown',state=='unknown')]:
        valid=mask & x.available.to_numpy();x[label+'_candidates']=mask.astype(int);x[label+'_n']=valid.astype(int)
        for side in ('lower','upper'):
            v=x[side].to_numpy(float);x[label+'_'+side+'_sum']=np.where(valid,v,0.)
            x[label+'_'+side+'_wins']= (valid&(v>0)).astype(int)
            x[label+'_'+side+'_losses']=(valid&(v<0)).astype(int)
        x[label+'_ambiguous']=(valid&x.ambiguous.to_numpy()).astype(int)
    aggregations={c:'sum' for c in x.columns if any(c.startswith(label+'_') for label in ('all','paired','kept','blocked','unknown'))}
    result=x.groupby(keys,dropna=False,sort=False).agg(**{k:(k,'sum') for k in aggregations},symbols=('symbol','nunique')).reset_index()
    for label in ('all','paired','kept','blocked','unknown'):
        for side in ('lower','upper'):
            result[label+'_'+side+'_mean']=result[label+'_'+side+'_sum']/result[label+'_n'].replace(0,np.nan)
            result[label+'_'+side+'_win_rate']=result[label+'_'+side+'_wins']/result[label+'_n'].replace(0,np.nan)
    result['mode']=mode;result['threshold']=threshold;result['roundtrip_cost']=cost
    result['difference_lower']=result.kept_lower_mean-result.paired_lower_mean
    result['difference_upper']=result.kept_upper_mean-result.paired_upper_mean
    return result


def summarize(df,by_symbol=False):
    keys=['interval','strategy','horizon','atr_setting','time_split']
    if by_symbol:keys+=['target_id','target_symbol']
    # Total is pooled counts, not an unweighted average of split percentages.
    df=pd.concat([df,df.assign(time_split='total')],ignore_index=True)
    results=[]
    for mode in ('gold','silver','either'):
        for threshold in (.6,.7,.8):
            for cost in (0.,.001,.0025,.005):
                results.append(group_stats(df,keys,mode,threshold,cost))
    return pd.concat(results,ignore_index=True)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path('data/ohlcv'));p.add_argument('--output',type=Path,default=Path('research/measurements/metal-filter-backtest'));args=p.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=True);manifest={}
    def load(path,role):
        manifest[str(path)]={'role':role,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()};return load_bars(path)
    metals={name:load(one_path(args.root,'metals','METAL_'+name.upper(),'1h'),'source') for name in ('gold','silver')}
    records=[];availability=[]
    for interval in ('1h','4h'):
        bench=load(one_path(args.root,'bist_indices','IDX_XU100',interval),'benchmark_'+interval);bt=times(bench)
        windows=make_windows(bench,interval);source={k:metal_windows(windows,v) for k,v in metals.items()}
        endpos=windows.end_pos.to_numpy(int);lookup=np.full(len(bt),-1,dtype=int);lookup[endpos]=np.arange(len(windows))
        paths=get_paths(args.root,['bist_equities'],interval)
        if not paths:raise ValueError('Hisse verisi yok')
        for j,path in enumerate(paths,1):
            raw=load(path,'target_'+interval);asset=path.parts[-4];symbol=str(raw.symbol.iloc[0])
            aligned=raw.set_index('ts_utc').reindex(bt).reset_index().rename(columns={'index':'ts_utc'})
            feat=signal_features(aligned);post,post_end=post_labels(windows,bench,aligned,interval)
            histories={k:expanding_history(windows,v,post,post_end) for k,v in source.items()}
            counts=0
            for strategy in ('breakout20','failed_low5','trend_cross'):
                sig=np.flatnonzero(feat[strategy].to_numpy(bool)&(lookup>=0)&np.isfinite(feat.atr.to_numpy(float)))
                for pos in sig:
                    wi=lookup[pos];row={'interval':interval,'target_id':asset,'target_symbol':symbol,'strategy':strategy,
                                        'signal_ts':bt[pos]+pd.Timedelta(interval),'time_split':period(bt[pos]+pd.Timedelta(interval)),
                                        'atr':float(feat.atr.iloc[pos])}
                    for name in ('gold','silver'):
                        r=source[name].source_return.iloc[wi];row[name+'_return']=r
                        direction='up' if r>.02 else ('down' if r<-.02 else None)
                        row[name+'_condition']=(direction if direction else ('unknown' if not np.isfinite(r) else 'no_signal'))
                        row[name+'_n']=int(histories[name][direction+'_n'].iloc[wi]) if direction else 0
                        row[name+'_down']=int(histories[name][direction+'_down'].iloc[wi]) if direction else 0
                    for horizon in (10,20):
                        for setting,stop,target in [('atr1_2',1,2),('atr1.5_3',1.5,3)]:
                            outcome=simulate(aligned,bt,pos,row['atr'],interval,horizon,stop,target)
                            records.append({**row,'horizon':horizon,'atr_setting':setting,**(outcome or {'exit_reason':'missing','gross_lower':np.nan,'gross_upper':np.nan})})
                    counts+=1
            availability.append({'interval':interval,'target_id':asset,'target_symbol':symbol,'signals':counts,'post_label_n':int(np.isfinite(post).sum())})
            if j%20==0:print(f'{interval}: {j}/{len(paths)}, {len(records)} aday-varyant',flush=True)
    df=pd.DataFrame(records)
    if df.empty:raise ValueError('İşlem adayı oluşmadı')
    df.to_csv(out/'islem-adaylari.csv.gz',index=False,compression='gzip')
    comparison=summarize(df)
    comparison.to_csv(out/'karsilastirma.csv.gz',index=False,compression='gzip')
    # Küçük ve doğrudan açılabilir özet; bütün varyantlar üstteki tabloda kalır.
    view=comparison[(comparison.threshold==.7)&(comparison.roundtrip_cost==.001)]
    columns=['interval','strategy','horizon','atr_setting','time_split','mode','threshold','roundtrip_cost',
             'all_candidates','all_n','unknown_candidates','unknown_n','paired_n','blocked_n','kept_n',
             'paired_lower_mean','paired_upper_mean','kept_lower_mean','kept_upper_mean',
             'blocked_lower_mean','blocked_upper_mean','kept_ambiguous','difference_lower','difference_upper']
    view[columns].to_csv(out/'ornek-gorunum.csv',index=False)
    print('Hisse bazlı özetler hesaplanıyor',flush=True)
    summarize(df,True).to_csv(out/'hisse-karsilastirma.csv.gz',index=False,compression='gzip')
    pd.DataFrame(availability).to_csv(out/'kapsam.csv',index=False)
    pd.DataFrame(manifest.values()).to_csv(out/'girdi-manifest.csv',index=False)
    stats={'input_files':len(manifest),'candidate_variant_rows':len(df),'signals':len(df)//4,'targets':len({x['target_id'] for x in availability}),'ambiguities':int(df.exit_reason.eq('ambiguous').sum()),'missing_outcome':int(df.gross_lower.isna().sum()),'splits':['train','validation','test']}
    (out/'summary.json').write_text(json.dumps(stats,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(stats,indent=2,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
