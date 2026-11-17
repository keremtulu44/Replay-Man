"""10 ortak BIST mumunda emtia değişimine hisse tepkilerini ölçer."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from replayman.replay import load_bars
from replayman.tenbar_research import CONDITIONS, make_windows, source_features, target_labels, condition_mask, metrics


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def get_paths(root,groups,interval):
    paths=[p for group in groups for p in sorted(root.glob(f'{group}/*/*/bars/{interval}.csv'))]
    ids=[p.parts[-4] for p in paths]
    if len(set(ids))!=len(ids):raise ValueError('Birden fazla seri var')
    return paths


def one_path(root,group,asset,interval):
    paths=list(root.glob(f'{group}/{asset}/*/bars/{interval}.csv'))
    if len(paths)!=1:raise ValueError(f'Tek seri gerekli: {group}/{asset}/{interval}')
    return paths[0]


def pair_study(src,labels,meta):
    if not np.array_equal(src.end_pos.to_numpy(),labels.end_pos.to_numpy()):raise ValueError('Pencere pozisyonları eşleşmiyor')
    rows=[];changed=src.source_return.to_numpy(float);split=src.time_split.to_numpy();fixed=src.fixed_nonoverlap.to_numpy(bool)
    for period in ('train','validation','test'):
        period_mask=split==period
        for response in ('same','after','post_open'):
            ret=labels[f'{response}_return'].to_numpy(float);excess=labels[f'{response}_excess'].to_numpy(float)
            for jump_filter in ('all','no_jump10'):
                jump=src.source_max_hourly_jump.to_numpy(float)
                jump_ok=np.ones(len(src),dtype=bool) if jump_filter=='all' else np.isfinite(jump) & (jump<=.10)
                for sampling in ('all_bars','fixed_nonoverlap','shock_episode'):
                    for condition in CONDITIONS:
                        if sampling=='shock_episode' and condition not in ('up4','down4','up2','down2','up0','down0'):continue
                        choice=condition_mask(changed,condition) & period_mask & jump_ok
                        if sampling=='fixed_nonoverlap':choice &= fixed
                        if sampling=='shock_episode':
                            suffix='' if jump_filter=='all' else '_no_jump10'
                            choice &= src[f'episode_{condition}{suffix}'].to_numpy(bool)
                        record={**meta,'time_split':period,'response':response,'sampling':sampling,'source_condition':condition,
                                'jump_filter':jump_filter,'selected_source_signals':int(choice.sum()),**metrics(choice,ret,excess)}
                        rows.append(record)
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path('data/ohlcv'))
    parser.add_argument('--output',type=Path,default=Path('research/measurements/10bar-commodity-reactions'))
    args=parser.parse_args();manifest=[];seen=set();study=[];source_files=[];focus=[];availability=[]
    fxpath=one_path(args.root,'fx','FX_USDTRY','1h');fx=load_bars(fxpath)
    def remember(path,role):
        if str(path) not in seen:
            seen.add(str(path));manifest.append({'role':role,'path':str(path),'sha256':digest(path)})
    remember(fxpath,'usdtry_1h')
    sources=get_paths(args.root,['energy','metals'],'1h')
    if not sources:raise ValueError('Emtia kaynakları yok')
    source_bars={}
    for path in sources:
        src=load_bars(path);asset=path.parts[-4]
        source_bars[asset]=(src,str(src.symbol.iloc[0]) if 'symbol' in src else asset)
        remember(path,'commodity_1h')
    stats={}
    for interval in ('1h','4h'):
        benchmark_path=one_path(args.root,'bist_indices','IDX_XU100',interval);bench=load_bars(benchmark_path);remember(benchmark_path,'benchmark_'+interval)
        windows=make_windows(bench,interval);stats[interval]={'benchmark_bars':len(bench),'eligible_windows':len(windows),'fixed_windows':int(windows.fixed_nonoverlap.sum())}
        by_source={}
        for asset,(bars,symbol) in source_bars.items():
            source=source_features(windows,bars,fx);source['source_id']=asset;source['source_symbol']=symbol;source['interval']=interval
            by_source[asset]={u:g.reset_index(drop=True) for u,g in source.groupby('unit',sort=False)}
            source_files.append(source)
        targets=get_paths(args.root,['bist_equities','bist_indices'],interval)
        if not targets:raise ValueError('BIST hedefleri yok')
        stats[interval]['targets']=len(targets)
        for num,path in enumerate(targets,1):
            group=path.parts[-5];asset=path.parts[-4];b=load_bars(path);remember(path,'target_'+interval)
            symbol=str(b.symbol.iloc[0]) if 'symbol' in b else asset
            labels=target_labels(windows,bench,b,interval)
            availability.append({'interval':interval,'target_id':asset,'target_symbol':symbol,'same_ready':int(labels.same_return.count()),'after_ready':int(labels.after_return.count())})
            for source,units in by_source.items():
                for unit,src in units.items():
                    meta={'source_id':source,'source_symbol':src.source_symbol.iloc[0],'unit':unit,'interval':interval,
                          'target_id':asset,'target_symbol':symbol,'target_group':group}
                    study.extend(pair_study(src,labels,meta))
                    if asset=='BIST_TUPRS' and source=='OIL_BRENT':
                        x=src.merge(labels,on='end_pos',validate='one_to_one');x['target_id']=asset;x['target_symbol']=symbol;focus.append(x)
            if num%25==0:print(f'{interval}: {num}/{len(targets)} hedef',flush=True)
    output=args.output;output.mkdir(parents=True,exist_ok=True)
    results=pd.DataFrame(study);features=pd.concat(source_files,ignore_index=True);events=pd.concat(focus,ignore_index=True)
    results.to_csv(output/'conditional-statistics.csv.gz',index=False,compression='gzip')
    focus_stats=results[(results.source_id=='OIL_BRENT') & (results.target_id=='BIST_TUPRS') &
                        (results.source_condition.isin(['all','up4','down4']))]
    focus_stats.to_csv(output/'brent-tuprs-ozet.csv',index=False)
    features.to_csv(output/'source-windows.csv.gz',index=False,compression='gzip')
    events.to_csv(output/'brent-tuprs-windows.csv.gz',index=False,compression='gzip')
    hits=events[(events.unit=='USD')&(events.source_return>=.04)&(events.same_return<=-.03)]
    hits.to_csv(output/'brent-tuprs-matches.csv',index=False)
    pd.DataFrame(manifest).to_csv(output/'input-manifest.csv',index=False)
    pd.DataFrame(availability).to_csv(output/'target-availability.csv',index=False)
    summary={'frames':stats,'sources':len(sources),'input_files':len(manifest),'bar_count':10,
             'conditions':list(CONDITIONS),'responses':['same','after','post_open'],
             'samples':['all_bars','fixed_nonoverlap','shock_episode'],'jump_filters':['all','no_jump10 (post hoc sensitivity)'],
             'train_end':'2026-07-01T00:00:00Z','validation_end':'2026-09-01T00:00:00Z',
             'example':'USD Brent >= 4% and TUPRS same 10 bars <= -3%',
             'example_matches_overlapping':len(hits),'limitations':'observational; observed splits; overlapping windows; nominal closes; no execution or causal claims'}
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
