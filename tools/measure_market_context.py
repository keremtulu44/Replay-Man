"""Endeks ve kurların BIST hisse bağlamını ölçer; işlem veya hacim kullanmaz."""
from __future__ import annotations
import argparse
import csv
import gzip
import json
from pathlib import Path
import numpy as np
import pandas as pd
from replayman.replay import load_bars
from replayman.tenbar_research import make_windows, target_labels, metrics
from replayman.market_context import native_source_features
from tools.measure_macro_risk import calculate_rows, COLUMNS
from tools.measure_tenbar_reactions import get_paths, one_path, digest


EXTRA_COLUMNS=('available_baseline_selected','available_baseline_n','available_baseline_negative_count',
               'available_baseline_negative_rate','available_baseline_down3_count','available_baseline_down3_rate',
               'available_negative_rate_difference')


def context_rows(src, labels, meta):
    """Eski sabit ızgaraya ek, kaynağı bilinen pencerelerden seçilen sabit baz."""
    split=src.time_split.to_numpy();baselines={}
    for response in ('same','post_open'):
        ret=labels[response+'_return'].to_numpy(float);ex=labels[response+'_excess'].to_numpy(float)
        for jf in ('all','no_jump10'):
            fixed=src['source_fixed' if jf=='all' else 'source_fixed_no_jump10'].to_numpy(bool)
            for period in ('train','validation','test','total'):
                mask=fixed & (np.ones(len(src),dtype=bool) if period=='total' else split==period)
                baselines[(response,jf,period)]=(int(mask.sum()),metrics(mask,ret,ex))
    for row in calculate_rows(src,labels,meta):
        selected,base=baselines[(row['response'],row['jump_filter'],row['time_split'])]
        yield {**row,'available_baseline_selected':selected,'available_baseline_n':base['n'],
               'available_baseline_negative_count':base['negative_count'],'available_baseline_negative_rate':base['negative_rate'],
               'available_baseline_down3_count':base['down3_count'],'available_baseline_down3_rate':base['down3_rate'],
               'available_negative_rate_difference':row['negative_rate']-base['negative_rate']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path('data/ohlcv'))
    p.add_argument('--output',type=Path,default=Path('research/measurements/market-context'))
    args=p.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
    manifest={};source_inventory=[];availability=[];frames=[];stats={}
    def load(path,role):
        manifest[str(path)]={'role':role,'path':str(path),'sha256':digest(path)}
        return load_bars(path)
    paths=get_paths(args.root,['bist_indices','global_indices','fx'],'1h')
    if not paths:raise ValueError('Kaynak serileri yok')
    sources={}
    for path in paths:
        b=load(path,'source_1h');asset=path.parts[-4];group=path.parts[-5]
        sources[asset]=(b,group,str(b.symbol.iloc[0]))
    with gzip.open(out/'risk-table.csv.gz','wt',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=('source_group',*COLUMNS,*EXTRA_COLUMNS));writer.writeheader()
        for interval in ('1h','4h'):
            bench=load(one_path(args.root,'bist_indices','IDX_XU100',interval),'benchmark_'+interval)
            windows=make_windows(bench,interval);paths=get_paths(args.root,['bist_equities'],interval)
            if not paths:raise ValueError('Hisse verileri bulunamadı')
            stats[interval]={'benchmark_bars':len(bench),'windows':len(windows),'targets':len(paths)}
            by_source={}
            for asset,(b,group,symbol) in sources.items():
                src=native_source_features(windows,b);src['source_id']=asset;src['source_group']=group;src['source_symbol']=symbol;src['interval']=interval
                by_source[asset]=src;frames.append(src)
                source_inventory.append({'interval':interval,'source_id':asset,'source_group':group,'source_symbol':symbol,
                                         'windows':len(src),'source_available':int(np.isfinite(src.source_return).sum()),
                                         'start_utc':str(b.ts_utc.min()),'end_utc':str(b.ts_utc.max())})
            for i,path in enumerate(paths,1):
                b=load(path,'target_'+interval);asset=path.parts[-4];symbol=str(b.symbol.iloc[0]);labels=target_labels(windows,bench,b,interval)
                availability.append({'interval':interval,'target_id':asset,'target_symbol':symbol,
                                     'same_ready':int(labels.same_return.count()),'post_open_ready':int(labels.post_open_return.count())})
                for source,src in by_source.items():
                    meta={'source_group':sources[source][1],'source_id':source,'source_symbol':sources[source][2],
                          'unit':'native','interval':interval,'target_id':asset,'target_symbol':symbol,'target_group':'bist_equities'}
                    writer.writerows(context_rows(src,labels,meta))
                if i%20==0:print(f'{interval}: {i}/{len(paths)} hisse',flush=True)
    table=pd.read_csv(out/'risk-table.csv.gz')
    overview=table[(table.time_split=='total')&(table.jump_filter=='all')]
    overview.to_csv(out/'hisse-ozet.csv',index=False)
    pd.concat(frames,ignore_index=True).to_csv(out/'source-windows.csv.gz',index=False,compression='gzip')
    pd.DataFrame(source_inventory).to_csv(out/'source-availability.csv',index=False)
    pd.DataFrame(availability).to_csv(out/'target-availability.csv',index=False)
    pd.DataFrame(manifest.values()).to_csv(out/'input-manifest.csv',index=False)
    summary={'sources':len(sources),'input_files':len(manifest),'frames':stats,'rows':len(table),'overview_rows':len(overview),
             'source_categories':['bist_indices','global_indices','fx'],'unit':'native','excluded':['volume']}
    (out/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
    from tools.organize_market_context import export
    export(out)
    print(json.dumps(summary,indent=2,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
