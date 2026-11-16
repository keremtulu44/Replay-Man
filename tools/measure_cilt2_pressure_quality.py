"""Cilt 2 P4: baskı kaybı ve hareket kalitesi bileşenlerini tekil/birleşik ölçer."""
from pathlib import Path
import json,pandas as pd,numpy as np
from replayman.replay import load_bars,causal_features
from replayman.book_features import attach_forward
ROOT=Path('data/ohlcv');OUT=Path('research/measurements/cilt2-pressure-quality');H=(5,20,40,60)
def rate(x):x=x.dropna();return float((x>0).mean()) if len(x) else float('nan')
def main():
 OUT.mkdir(parents=True,exist_ok=True);parts=[];inventory=[]
 for p in sorted(ROOT.glob('*/*/*/bars/*.csv')):
  b=load_bars(p);f=causal_features(b);direction=np.sign(b.close-b.close.shift(5));overlap_recent=f.overlap_ratio.rolling(3,min_periods=3).mean();overlap_prior=f.overlap_ratio.shift(3).rolling(3,min_periods=3).mean();overlap_rise=overlap_recent-overlap_prior
  signed=np.sign(b.close-b.open);counter=(signed==-direction)&(f.body_ratio>=.5);base=pd.DataFrame({'known_at_position':f.index,'event_ts':b.ts_utc,'prior_direction':direction,'body_decay_ratio':f.body_decay_ratio,'progress_decay_ratio':f.progress_decay_ratio,'overlap_change':overlap_rise,'path_efficiency':f.path_efficiency})
  specs=[]
  for threshold in (.6,.8):
   body=f.body_decay_ratio<=threshold;progress=f.progress_decay_ratio<=threshold;ov=overlap_rise>=.10
   specs += [(f'body_decay_{threshold}',body),(f'progress_decay_{threshold}',progress),(f'body_progress_decay_{threshold}',body&progress),(f'triple_decay_{threshold}',body&progress&ov),(f'confirmed_counter_{threshold}',body&progress&ov&counter)]
  specs.append(('overlap_rise_0.10',overlap_rise>=.10));events=[];counts={}
  for name,mask in specs:
   mask=mask&(direction!=0);ix=f.index[mask.fillna(False)];counts[name]=len(ix)
   if len(ix):
    x=base.loc[ix].copy();x['event']=name;x['direction']=np.where(direction.loc[ix]>0,'up','down');x['thesis_direction']=np.where(direction.loc[ix]>0,'down','up');events.append(x)
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
 rank=ev.groupby(['asset_id','interval']).event_ts.rank(method='first',pct=True);ev['time_split']=pd.cut(rank,[0,.6,.8,1],labels=['train','validation','test'],include_lowest=True);ev['quality_band']=pd.cut(ev.path_efficiency,[-float('inf'),.3,.6,float('inf')],labels=['low','medium','high'])
 pd.DataFrame(inventory).to_csv(OUT/'inventory.csv',index=False);keys=['group','interval','time_split','event','direction','thesis_direction','quality_band'];spec={'observations':('asset_id','size'),'assets':('asset_id','nunique')}
 for q in H:spec.update({f'ready_{q}':(f'excess_{q}','count'),f'median_excess_{q}':(f'excess_{q}','median'),f'win_rate_{q}':(f'excess_{q}',rate)})
 ev.groupby(keys,observed=True).agg(**spec).reset_index().to_csv(OUT/'event_study.csv',index=False)
 ev.groupby(['group','interval','time_split','event','direction','thesis_direction'],observed=True).agg(**spec).reset_index().to_csv(OUT/'event_overall_study.csv',index=False)
 summary={'events':len(ev),'assets':int(ev.asset_id.nunique()),'event_counts':ev.event.value_counts().to_dict()};(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
