"""Cilt 2 P3: iki, üç ve çok mumlu dizileri nedensel olarak ölçer."""
from pathlib import Path
import json,pandas as pd
from replayman.replay import load_bars,causal_features
from replayman.book_features import attach_forward
ROOT=Path('data/ohlcv');OUT=Path('research/measurements/cilt2-multi-candles');H=(5,20,40,60)
def rate(x):x=x.dropna();return float((x>0).mean()) if len(x) else float('nan')
def main():
 OUT.mkdir(parents=True,exist_ok=True);parts=[];inventory=[]
 for p in sorted(ROOT.glob('*/*/*/bars/*.csv')):
  b=load_bars(p);f=causal_features(b);o,h,l,c=(b[x].astype(float) for x in ('open','high','low','close'));body=(c-o).abs();bull=c>o;bear=c<o
  prev_hi=pd.concat([o.shift(1),c.shift(1)],axis=1).max(axis=1);prev_lo=pd.concat([o.shift(1),c.shift(1)],axis=1).min(axis=1);cur_hi=pd.concat([o,c],axis=1).max(axis=1);cur_lo=pd.concat([o,c],axis=1).min(axis=1)
  inside_body=(cur_hi<=prev_hi)&(cur_lo>=prev_lo)
  specs=[
   ('bull_engulf_strict',bull&bear.shift(1)&(cur_hi>=prev_hi)&(cur_lo<=prev_lo),'up'),('bear_engulf_strict',bear&bull.shift(1)&(cur_hi>=prev_hi)&(cur_lo<=prev_lo),'down'),
   ('bull_harami',bull&bear.shift(1)&inside_body,'up'),('bear_harami',bear&bull.shift(1)&inside_body,'down'),
   ('bull_two_bar_reclaim',bear.shift(1)&bull&(c>(o.shift(1)+c.shift(1))/2)&(f.body_ratio>=.5),'up'),('bear_two_bar_reclaim',bull.shift(1)&bear&(c<(o.shift(1)+c.shift(1))/2)&(f.body_ratio>=.5),'down'),
   ('morning_star',bear.shift(2)&(f.body_ratio.shift(2)>=.5)&(f.body_ratio.shift(1)<=.3)&bull&(c>(o.shift(2)+c.shift(2))/2),'up'),('evening_star',bull.shift(2)&(f.body_ratio.shift(2)>=.5)&(f.body_ratio.shift(1)<=.3)&bear&(c<(o.shift(2)+c.shift(2))/2),'down'),
   ('three_soldiers',bull&bull.shift(1)&bull.shift(2)&(c>c.shift(1))&(c.shift(1)>c.shift(2))&(f.body_ratio.rolling(3).min()>=.5),'up'),('three_crows',bear&bear.shift(1)&bear.shift(2)&(c<c.shift(1))&(c.shift(1)<c.shift(2))&(f.body_ratio.rolling(3).min()>=.5),'down'),
   ('bull_continuation_3',(f.body_ratio.shift(2)>=.6)&bull.shift(2)&bear.shift(1)&(body.shift(1)<body.shift(2))&bull&(c>h.shift(2)),'up'),('bear_continuation_3',(f.body_ratio.shift(2)>=.6)&bear.shift(2)&bull.shift(1)&(body.shift(1)<body.shift(2))&bear&(c<l.shift(2)),'down'),
   ('inside_break_up',(h.shift(1)<=h.shift(2))&(l.shift(1)>=l.shift(2))&(c>h.shift(2)),'up'),('inside_break_down',(h.shift(1)<=h.shift(2))&(l.shift(1)>=l.shift(2))&(c<l.shift(2)),'down')]
  events=[];counts={}
  for name,mask,d in specs:
   ix=f.index[mask.fillna(False)];counts[name]=len(ix)
   if len(ix):events.append(pd.DataFrame({'event':name,'direction':d,'thesis_direction':d,'known_at_position':ix,'event_ts':b.loc[ix].ts_utc,'body_ratio':f.loc[ix].body_ratio,'range_atr':f.loc[ix].range_atr,'path_efficiency':f.loc[ix].path_efficiency}))
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
 rank=ev.groupby(['asset_id','interval']).event_ts.rank(method='first',pct=True);ev['time_split']=pd.cut(rank,[0,.6,.8,1],labels=['train','validation','test'],include_lowest=True)
 pd.DataFrame(inventory).to_csv(OUT/'inventory.csv',index=False)
 keys=['group','interval','time_split','event','thesis_direction'];spec={'observations':('asset_id','size'),'assets':('asset_id','nunique')}
 for q in H:spec.update({f'ready_{q}':(f'excess_{q}','count'),f'median_excess_{q}':(f'excess_{q}','median'),f'win_rate_{q}':(f'excess_{q}',rate)})
 ev.groupby(keys,observed=True).agg(**spec).reset_index().to_csv(OUT/'event_study.csv',index=False)
 summary={'events':len(ev),'assets':int(ev.asset_id.nunique()),'event_counts':ev.event.value_counts().to_dict()};(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
