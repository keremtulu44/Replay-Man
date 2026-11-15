import pandas as pd
from pathlib import Path
from replayman.replay import load_bars
P=Path('research/measurements/book-batch2');e=pd.read_csv(P/'events.csv');e.event_ts=pd.to_datetime(e.event_ts,utc=True)
def rate(x):x=x.dropna();return (x>0).mean() if len(x) else float('nan')
refs={'IDX_XU100','IDX_GSPC','FX_USDTRY','METAL_GOLD','OIL_BRENT'};deltas={'1h':'1h','2h':'2h','4h':'4h','1d':'1D'}
for aid in refs:
 col=f'{aid}_return5';e=e.drop(columns=[col],errors='ignore');pieces=[]
 for path in Path('data/ohlcv').glob(f'*/{aid}/*/bars/*.csv'):
  b=load_bars(path);pieces.append(pd.DataFrame({'interval':path.stem,'available_ts':b.ts_utc+pd.Timedelta(deltas[path.stem]),col:b.close.pct_change(5)}))
 if not pieces:continue
 right=pd.concat(pieces).sort_values('available_ts');out=[]
 for interval,left in e.groupby('interval',sort=False):
  r=right[right.interval==interval].drop(columns='interval');left=left.sort_values('event_ts');out.append(pd.merge_asof(left,r,left_on='event_ts',right_on='available_ts',direction='backward',tolerance=pd.Timedelta('3D')).drop(columns='available_ts'))
 e=pd.concat(out,ignore_index=True)
parts=[]
for col in [f'{a}_return5' for a in refs if f'{a}_return5' in e]:
 x=e.dropna(subset=[col]).copy();x['context']=pd.cut(x[col],[-float('inf'),0,float('inf')],labels=['negative','positive'])
 z=x.groupby(['group','interval','time_split','event','thesis_direction','context'],observed=True).agg(observations=('asset_id','size'),assets=('asset_id','nunique'),median_excess_20=('excess_20','median'),win_rate_20=('excess_20',rate),median_excess_60=('excess_60','median'),win_rate_60=('excess_60',rate)).reset_index();z.insert(5,'reference',col);parts.append(z)
pd.concat(parts,ignore_index=True).to_csv(P/'cross_market_study.csv',index=False)
