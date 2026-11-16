"""Cilt 2 P5: sıkışma, ilk taşma, geri alma ve karşı tarafa genişleme."""
from pathlib import Path
import json,pandas as pd,numpy as np
from replayman.replay import load_bars,causal_features
from replayman.book_features import attach_forward
ROOT=Path('data/ohlcv');OUT=Path('research/measurements/cilt2-compression');H=(5,20,40,60)
def rate(x):x=x.dropna();return float((x>0).mean()) if len(x) else float('nan')
def main():
 OUT.mkdir(parents=True,exist_ok=True);parts=[];inventory=[]
 for p in sorted(ROOT.glob('*/*/*/bars/*.csv')):
  b=load_bars(p);f=causal_features(b);events=[];counts={}
  for window in (6,10,15):
   upper=b.high.shift(1).rolling(window,min_periods=window).max();lower=b.low.shift(1).rolling(window,min_periods=window).min();width=(upper-lower)/f.atr.replace(0,np.nan);compressed=(width<=3)&(f.mean_overlap>=.35)
   duration=compressed.astype(int).groupby((~compressed).cumsum()).cumsum()
   for direction in ('up','down'):
    close_out=(b.close>upper) if direction=='up' else (b.close<lower);probe=((b.high>upper)&(b.close<=upper)) if direction=='up' else ((b.low<lower)&(b.close>=lower))
    for typ,mask,thesis in [('compression_break',compressed.shift(1).fillna(False)&close_out,direction),('compression_probe_reject',compressed.shift(1).fillna(False)&probe,'down' if direction=='up' else 'up')]:
     name=f'{typ}_{direction}_w{window}';ix=f.index[mask.fillna(False)];counts[name]=len(ix)
     if len(ix):events.append(pd.DataFrame({'event':name,'direction':direction,'thesis_direction':thesis,'known_at_position':ix,'event_ts':b.loc[ix].ts_utc,'compression_width_atr':width.loc[ix],'compression_duration':duration.shift(1).loc[ix],'break_range_atr':f.loc[ix].range_atr}))
   # Kapanış kırılımından sonraki 5 barda karşı sınırın kapanışla aşılması.
   for i in range(window+1,len(b)-5):
    if not bool(compressed.iloc[i-1]):continue
    direction='up' if b.close.iloc[i]>upper.iloc[i] else 'down' if b.close.iloc[i]<lower.iloc[i] else None
    if not direction:continue
    opposite=None
    for j in range(i+1,i+6):
     if direction=='up' and b.close.iloc[j]<lower.iloc[i]:opposite=j;break
     if direction=='down' and b.close.iloc[j]>upper.iloc[i]:opposite=j;break
    if opposite is not None:events.append(pd.DataFrame([{'event':f'opposite_expansion_after_{direction}_w{window}','direction':direction,'thesis_direction':'down' if direction=='up' else 'up','known_at_position':opposite,'event_ts':b.ts_utc.iloc[opposite],'compression_width_atr':width.iloc[i],'compression_duration':duration.shift(1).iloc[i],'break_range_atr':f.range_atr.iloc[i]}]));counts[f'opposite_expansion_after_{direction}_w{window}']=counts.get(f'opposite_expansion_after_{direction}_w{window}',0)+1
  inventory.append({'group':p.parts[-5],'asset_id':p.parts[-4],'interval':p.stem,'bars':len(b),**counts})
  if events:
   e=attach_forward(pd.concat(events,ignore_index=True),b,H);e.insert(0,'group',p.parts[-5]);e.insert(1,'asset_id',p.parts[-4]);e.insert(2,'interval',p.stem);parts.append(e)
 ev=pd.concat(parts,ignore_index=True);ev.event_ts=pd.to_datetime(ev.event_ts,utc=True)
 bench=[]
 for p in ROOT.glob('bist_indices/IDX_XU100/*/bars/*.csv'):
  b=load_bars(p);x=pd.DataFrame({'interval':p.stem,'event_ts':b.ts_utc})
  for q in H:x[f'bench_{q}']=b.close.shift(-q).div(b.close).sub(1)
  bench.append(x)
 ev=ev.merge(pd.concat(bench),on=['interval','event_ts'],how='left');sg=ev.thesis_direction.map({'up':1,'down':-1})
 for q in H:ev[f'excess_{q}']=ev[f'directional_return_{q}']-sg*ev[f'bench_{q}']
 rank=ev.groupby(['asset_id','interval']).event_ts.rank(method='first',pct=True);ev['time_split']=pd.cut(rank,[0,.6,.8,1],labels=['train','validation','test'],include_lowest=True);ev['break_size_band']=pd.cut(ev.break_range_atr,[-float('inf'),.8,1.5,float('inf')],labels=['contracted','normal','expanded'])
 pd.DataFrame(inventory).fillna(0).to_csv(OUT/'inventory.csv',index=False);keys=['group','interval','time_split','event','direction','thesis_direction','break_size_band'];spec={'observations':('asset_id','size'),'assets':('asset_id','nunique')}
 for q in H:spec.update({f'ready_{q}':(f'excess_{q}','count'),f'median_excess_{q}':(f'excess_{q}','median'),f'win_rate_{q}':(f'excess_{q}',rate)})
 ev.groupby(keys,observed=True).agg(**spec).reset_index().to_csv(OUT/'event_study.csv',index=False)
 summary={'events':len(ev),'assets':int(ev.asset_id.nunique()),'event_counts':ev.event.value_counts().to_dict()};(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
