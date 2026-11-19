"""Lifecycle senaryosu ve gözlemsel karşılaştırma grubunun betimleyici özeti."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

KINDS=['horizontal','dwell','impulse','sloped']


def weighted_median_sorted(values, week_codes, week_weights):
    weights = week_weights[week_codes]
    total = int(weights.sum())
    if not total:
        return np.nan
    cumulative = np.cumsum(weights)
    a = values[np.searchsorted(cumulative, (total-1)//2 + 1)]
    b = values[np.searchsorted(cumulative, total//2 + 1)]
    return (a+b)/2


def compare_groups(events, draws=500, seed=20261117):
    if draws < 1: raise ValueError('draws pozitif olmalı')
    rng=np.random.default_rng(seed)
    f=events[(events.pattern.isin(['cross_then_same','same_then_same'])) & events.excess_5.notna()].copy()
    f['week']=pd.to_datetime(f.end_bar_ts,utc=True).dt.tz_localize(None).dt.to_period('W-SUN').dt.start_time
    rows=[]
    for key,g in f.groupby(['kind','interval','split','end_side'],sort=True):
        left=g[g.pattern=='cross_then_same'];right=g[g.pattern=='same_then_same']
        if left.empty or right.empty:continue
        weeks=sorted(g.week.unique());week_map={w:i for i,w in enumerate(weeks)}
        windex=np.array([week_map[w] for w in g.week],dtype=int)
        ordered=[]
        for pattern in ['cross_then_same','same_then_same']:
            mask=g.pattern.eq(pattern).to_numpy(); vals=g.excess_5.to_numpy()[mask]; wc=windex[mask]
            indices=np.argsort(vals); ordered.append((vals[indices],wc[indices]))
        simulations=[]
        if len(weeks)>=5:
            for _ in range(draws):
                weights=np.bincount(rng.integers(0,len(weeks),size=len(weeks)),minlength=len(weeks))
                d=weighted_median_sorted(*ordered[0],weights)-weighted_median_sorted(*ordered[1],weights)
                if np.isfinite(d):simulations.append(d)
        per=g.groupby(['asset_id','pattern']).excess_5.agg(['size','median']).reset_index()
        pivot=per[per['size']>=3].pivot(index='asset_id',columns='pattern',values='median')
        if {'cross_then_same','same_then_same'}.issubset(pivot.columns):
            common=pivot.dropna(subset=['cross_then_same','same_then_same']);dif=common.cross_then_same-common.same_then_same
        else:
            dif=pd.Series(dtype=float)
        ci=np.quantile(simulations,[.025,.975]) if simulations else [np.nan,np.nan]
        rows.append({**dict(zip(['kind','interval','split','end_side'],key)),
                     'n_cross_then_same':len(left),'assets_cross_then_same':left.asset_id.nunique(),
                     'n_same_then_same':len(right),'assets_same_then_same':right.asset_id.nunique(),
                     'median_cross_then_same':left.excess_5.median(),'median_same_then_same':right.excess_5.median(),
                     'median_difference':left.excess_5.median()-right.excess_5.median(),
                     'weeks':len(weeks),'bootstrap_draws':len(simulations),'bootstrap_low':ci[0],'bootstrap_high':ci[1],
                     'asset_both_3plus':len(dif),'asset_cross_higher':int((dif>0).sum()),'asset_cross_lower':int((dif<0).sum())})
    return pd.DataFrame(rows)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path('research/measurements/zone-memory'))
    p.add_argument('--output',type=Path,required=True);p.add_argument('--draws',type=int,default=500)
    args=p.parse_args(argv);inputs=[];parts=[]
    for kind in KINDS:
        for suffix in ['', '-hourly']:
            path=args.root/f'lifecycle-{kind}{suffix}'/'events.csv.xz'
            if not path.exists():
                raise FileNotFoundError(path)
            f=pd.read_csv(path);parts.append(f)
            inputs.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'events':len(f)})
    events=pd.concat(parts,ignore_index=True)
    if events.duplicated(['asset_id','interval','kind','end_position']).any():
        raise ValueError('Tek tür/hisse/periyot/mum için birden fazla temsilci')
    args.output.mkdir(parents=True,exist_ok=True)
    compare_groups(events,draws=args.draws).to_csv(args.output/'comparisons.csv',index=False)
    totals=events.groupby(['kind','interval','split','end_side','scenario']).agg(events=('scenario','size'),assets=('asset_id','nunique')).reset_index()
    totals.to_csv(args.output/'scenario-counts.csv',index=False)
    meta={'inputs':inputs,'draws':args.draws,'seed':20261117,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'notice':'Karşılaştırmalar eşleştirilmiş/nedensel değildir; gruplar farklı olaylardır ve haftalık bootstrap bağımlılığın tamamını çözmez.'}
    (args.output/'summary.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('rows',len(events),'comparisons yazıldı')
    return 0


if __name__=='__main__': raise SystemExit(main())
