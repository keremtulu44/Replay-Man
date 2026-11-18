"""Yaşam döngüsü olaylarında iki küçük filtrenin keşif karşılaştırması.

Filtreler ikinci ziyaretin tamamlandığı anda bilinir. Aynı/tür/bar temsilcileri
ve önceden incelenmiş geçmiş kullanılır; sonuçlar doğrulanmış hipotez değildir.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

from tools.summarize_lifecycle import compare_groups

KINDS=['horizontal','dwell','impulse','sloped']


def label_filters(frame: pd.DataFrame):
    data=frame.copy()
    gap=data.start_position-data.prior_end_position
    valid_gap=(gap>=1)&gap.notna()
    data['gap_group']=np.where(~valid_gap,'unknown',np.where(gap<=10,'within_10','after_10'))
    touches=data.touch_bars
    data['touch_group']=np.where(touches.isna() | (touches<1),'unknown',np.where(touches>=3,'3plus','1to2'))
    return data


def descriptions(frame: pd.DataFrame):
    parts=[]
    for name in ['gap_group','touch_group']:
        g=frame.groupby(['kind','interval','split','end_side','pattern',name],dropna=False)
        z=g.agg(events=('pattern','size'), assets=('asset_id','nunique'),
                benchmark_n=('excess_5','count'), excess_median=('excess_5','median'),
                raw_n=('directional_5','count'), raw_median=('directional_5','median'),
                benchmark_n_10=('excess_10','count'),excess_median_10=('excess_10','median')).reset_index()
        z=z.rename(columns={name:'filter_value'});z['filter']=name;parts.append(z)
    return pd.concat(parts,ignore_index=True)


def analyze(frame: pd.DataFrame, draws=500):
    f=label_filters(frame)
    f=f[f.interval.isin(['1d','4h']) & f.pattern.isin(['cross_then_same','same_then_same'])].copy()
    comps=[]
    for feature in ['gap_group','touch_group']:
        for level,g in f.groupby(feature,sort=True):
            if level=='unknown':continue
            c=compare_groups(g,draws=draws,seed=20261117)
            if len(c):
                c['filter']=feature;c['filter_value']=level;comps.append(c)
    return descriptions(f),pd.concat(comps,ignore_index=True)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path('research/measurements/zone-memory'))
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--draws',type=int,default=500)
    args=p.parse_args(argv);parts=[];inputs=[]
    for k in KINDS:
        path=args.root/f'lifecycle-{k}'/'events.csv.xz'
        data=pd.read_csv(path);parts.append(data)
        inputs.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'records':len(data)})
    frame=pd.concat(parts,ignore_index=True)
    desc,comp=analyze(frame,draws=args.draws)
    args.output.mkdir(parents=True,exist_ok=True)
    desc.to_csv(args.output/'groups.csv',index=False)
    comp.to_csv(args.output/'comparisons.csv',index=False)
    meta={'status':'post_hoc_exploratory', 'intervals':['1d','4h'], 'inputs':inputs,'draws':args.draws,
          'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'comparison_code_sha256':hashlib.sha256(Path('tools/summarize_lifecycle.py').read_bytes()).hexdigest(),
          'caution':'Etiketler bilindiğinde olay sonu, gruplar eşleşmemiş, veriler daha önce incelenmiş, çoklu deneme var.'}
    (args.output/'summary.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(frame)} ziyaret, {len(desc)} alt grup ve {len(comp)} eşleşmemiş karşılaştırma')
    return 0


if __name__=='__main__':raise SystemExit(main())
