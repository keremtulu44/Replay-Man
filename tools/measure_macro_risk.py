"""Tüm emtia/BIST çiftlerinde geçmiş yön riskini hesaplar."""
from __future__ import annotations
import argparse
import csv
import gzip
import json
from pathlib import Path
import numpy as np
import pandas as pd
from replayman.replay import load_bars
from replayman.tenbar_research import make_windows, source_features, target_labels, metrics, condition_mask
from tools.measure_tenbar_reactions import get_paths, one_path, digest

CONDITIONS=('down0','up0','down2','up2','down4','up4')
PERIODS=('train','validation','test','total')
KEYS=('n','negative_count','negative_rate','positive_count','positive_rate','flat_count','flat_rate','down3_count','down3_rate')
COLUMNS=('source_id','source_symbol','unit','interval','target_id','target_symbol','target_group',
         'source_condition','response','jump_filter','time_split','selected_source_signals',*KEYS,
         'baseline_selected','baseline_n','baseline_negative_count','baseline_negative_rate',
         'baseline_down3_count','baseline_down3_rate','negative_rate_difference','sample_status','risk_flag')


def calculate_rows(src, labels, meta):
    """Olaylar hedeften bağımsız seçilir; toplam bölümler arası tasfiye edilen sonuçları içermez."""
    if not np.array_equal(src.end_pos.to_numpy(),labels.end_pos.to_numpy()):raise ValueError('Pencereler farklı')
    split=src.time_split.to_numpy();changed=src.source_return.to_numpy(float)
    jump=src.source_max_hourly_jump.to_numpy(float);fixed=src.fixed_nonoverlap.to_numpy(bool)
    for response in ('same','post_open'):
        r=labels[f'{response}_return'].to_numpy(float);ex=labels[f'{response}_excess'].to_numpy(float)
        for jf in ('all','no_jump10'):
            jump_ok=np.ones(len(src),dtype=bool) if jf=='all' else np.isfinite(jump)&(jump<=.10)
            for period in PERIODS:
                pm=np.ones(len(src),dtype=bool) if period=='total' else split==period
                base_mask=pm&fixed&jump_ok&condition_mask(changed,'all')
                base=metrics(base_mask,r,ex)
                for condition in CONDITIONS:
                    suffix='' if jf=='all' else '_no_jump10'
                    selected=pm&jump_ok&condition_mask(changed,condition)&src[f'episode_{condition}{suffix}'].to_numpy(bool)
                    m=metrics(selected,r,ex);n=m['n'];rate=m['negative_rate']
                    flag='ornek_yetersiz' if n<10 else ('tarihsel_uyari' if rate>=.7 else 'esik_altinda')
                    yield {**meta,'source_condition':condition,'response':response,'jump_filter':jf,'time_split':period,
                           'selected_source_signals':int(selected.sum()),**{k:m[k] for k in KEYS},
                           'baseline_selected':int(base_mask.sum()),'baseline_n':base['n'],
                           'baseline_negative_count':base['negative_count'],'baseline_negative_rate':base['negative_rate'],
                           'baseline_down3_count':base['down3_count'],'baseline_down3_rate':base['down3_rate'],
                           'negative_rate_difference':rate-base['negative_rate'],
                           'sample_status':m['sample_status'],'risk_flag':flag}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path('data/ohlcv'));p.add_argument('--output',type=Path,default=Path('research/measurements/macro-risk-screen'));args=p.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=True);manifest={};availability=[];source_files=[];stats={}
    def load(path,role):
        manifest[str(path)]={'role':role,'path':str(path),'sha256':digest(path)}
        return load_bars(path)
    fx=load(one_path(args.root,'fx','FX_USDTRY','1h'),'usdtry_1h')
    sources={}
    for path in get_paths(args.root,['energy','metals'],'1h'):
        b=load(path,'commodity_1h');sources[path.parts[-4]]=(b,str(b.symbol.iloc[0]))
    if not sources:raise ValueError('Emtia verisi yok')
    with gzip.open(out/'risk-table.csv.gz','wt',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=COLUMNS);writer.writeheader()
        for interval in ('1h','4h'):
            bench=load(one_path(args.root,'bist_indices','IDX_XU100',interval),'benchmark_'+interval)
            windows=make_windows(bench,interval);targets=get_paths(args.root,['bist_equities','bist_indices'],interval)
            if not targets:raise ValueError('BIST hedefi yok')
            stats[interval]={'benchmark_bars':len(bench),'eligible_windows':len(windows),'targets':len(targets)}
            by_source={}
            for asset,(b,symbol) in sources.items():
                src=source_features(windows,b,fx);src['source_id']=asset;src['source_symbol']=symbol;src['interval']=interval
                source_files.append(src);by_source[asset]={u:g.reset_index(drop=True) for u,g in src.groupby('unit',sort=False)}
            for i,path in enumerate(targets,1):
                b=load(path,'target_'+interval);asset=path.parts[-4];symbol=str(b.symbol.iloc[0]);group=path.parts[-5]
                labels=target_labels(windows,bench,b,interval)
                availability.append({'interval':interval,'target_id':asset,'target_symbol':symbol,'same_ready':int(labels.same_return.count()),'post_open_ready':int(labels.post_open_return.count())})
                for source,units in by_source.items():
                    for unit,src in units.items():
                        meta={'source_id':source,'source_symbol':src.source_symbol.iloc[0],'unit':unit,'interval':interval,'target_id':asset,'target_symbol':symbol,'target_group':group}
                        writer.writerows(calculate_rows(src,labels,meta))
                if i%25==0:print(f'{interval}: {i}/{len(targets)}',flush=True)
    # Excel/LibreOffice ile doğrudan açılabilen ana görünüm; tam tablo tüm split ve duyarlılıkları taşır.
    table=pd.read_csv(out/'risk-table.csv.gz')
    overview=table[(table.time_split=='total') & (table.jump_filter=='all') & (table.target_group=='bist_equities')]
    overview.to_csv(out/'risk-ozet-hisseler.csv',index=False)
    pd.concat(source_files,ignore_index=True).to_csv(out/'source-windows.csv.gz',index=False,compression='gzip')
    pd.DataFrame(manifest.values()).to_csv(out/'input-manifest.csv',index=False)
    pd.DataFrame(availability).to_csv(out/'target-availability.csv',index=False)
    summary={'frames':stats,'sources':len(sources),'input_files':len(manifest),'conditions':list(CONDITIONS),'bar_count':10,'train_end':'2026-07-01T00:00:00Z','validation_end':'2026-09-01T00:00:00Z'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
    from tools.organize_macro_risk import export
    export(out)
    print(json.dumps(summary,indent=2,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
