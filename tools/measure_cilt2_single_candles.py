"""Cilt 2 P2: tek mum geometrisini sürekli değer ve kayıtlı varyantlarla ölçer."""
from pathlib import Path
import json,pandas as pd
from replayman.replay import load_bars,causal_features
from replayman.book_features import attach_forward
ROOT=Path('data/ohlcv');OUT=Path('research/measurements/cilt2-single-candles');H=(5,20,40,60)
def rate(x):x=x.dropna();return float((x>0).mean()) if len(x) else float('nan')
def main():
 OUT.mkdir(parents=True,exist_ok=True);parts=[];inventory=[]
 for p in sorted(ROOT.glob('*/*/*/bars/*.csv')):
  b=load_bars(p);f=causal_features(b);span=f['range'].replace(0,float('nan'));upper=f.upper_wick/span;lower=f.lower_wick/span
  base=pd.DataFrame({'known_at_position':f.index,'event_ts':b.ts_utc,'body_ratio':f.body_ratio,'close_location':f.close_location,'upper_wick_ratio':upper,'lower_wick_ratio':lower,'range_atr':f.range_atr})
  specs=[]
  for wick in (.4,.5,.6):
   for body in (.2,.3):
    specs += [(f'bull_pin_w{wick}_b{body}',(lower>=wick)&(f.body_ratio<=body)&(f.close_location>=.6),'up'),(f'bear_pin_w{wick}_b{body}',(upper>=wick)&(f.body_ratio<=body)&(f.close_location<=.4),'down')]
  specs += [('bull_marubozu',(f.direction>0)&(f.body_ratio>=.8)&(upper<=.1)&(lower<=.1),'up'),('bear_marubozu',(f.direction<0)&(f.body_ratio>=.8)&(upper<=.1)&(lower<=.1),'down'),('long_bull_close',(f.direction>0)&(f.body_ratio>=.6)&(f.range_atr>=1),'up'),('long_bear_close',(f.direction<0)&(f.body_ratio>=.6)&(f.range_atr>=1),'down'),('lower_wick_rejection',(lower>=.5)&(f.close_location>=.6),'up'),('upper_wick_rejection',(upper>=.5)&(f.close_location<=.4),'down')]
  counts={};events=[]
  for name,mask,direction in specs:
   ix=f.index[mask.fillna(False)];counts[name]=len(ix)
   if len(ix):
    x=base.loc[ix].copy();x['event']=name;x['direction']=direction;x['thesis_direction']=direction;events.append(x)
  inventory.append({'group':p.parts[-5],'asset_id':p.parts[-4],'interval':p.stem,'bars':len(b),'doji_like':int((f.body_ratio<=.1).sum()),**counts})
  if events:
   e=attach_forward(pd.concat(events,ignore_index=True),b,H);e.insert(0,'group',p.parts[-5]);e.insert(1,'asset_id',p.parts[-4]);e.insert(2,'interval',p.stem);parts.append(e)
 ev=pd.concat(parts,ignore_index=True);ev.event_ts=pd.to_datetime(ev.event_ts,utc=True)
 bench=[]
 for p in ROOT.glob('bist_indices/IDX_XU100/*/bars/*.csv'):
  b=load_bars(p);x=pd.DataFrame({'interval':p.stem,'event_ts':b.ts_utc})
  for h in H:x[f'bench_{h}']=b.close.shift(-h).div(b.close).sub(1)
  bench.append(x)
 ev=ev.merge(pd.concat(bench),on=['interval','event_ts'],how='left');sign=ev.thesis_direction.map({'up':1,'down':-1})
 for h in H:ev[f'excess_{h}']=ev[f'directional_return_{h}']-sign*ev[f'bench_{h}']
 rank=ev.groupby(['asset_id','interval']).event_ts.rank(method='first',pct=True);ev['time_split']=pd.cut(rank,[0,.6,.8,1],labels=['train','validation','test'],include_lowest=True)
 ev['body_band']=pd.cut(ev.body_ratio,[-1,.1,.3,.6,2],labels=['doji','small','medium','large']);ev['range_band']=pd.cut(ev.range_atr,[-float('inf'),.8,1.5,float('inf')],labels=['contracted','normal','expanded'])
 ev.to_csv(OUT/'events.csv',index=False);pd.DataFrame(inventory).to_csv(OUT/'inventory.csv',index=False)
 keys=['group','interval','time_split','event','thesis_direction','body_band','range_band'];spec={'observations':('asset_id','size'),'assets':('asset_id','nunique')}
 for h in H:spec.update({f'ready_{h}':(f'excess_{h}','count'),f'median_excess_{h}':(f'excess_{h}','median'),f'win_rate_{h}':(f'excess_{h}',rate)})
 ev.groupby(keys,observed=True).agg(**spec).reset_index().to_csv(OUT/'event_study.csv',index=False)
 summary={'events':len(ev),'assets':int(ev.asset_id.nunique()),'event_counts':ev.event.value_counts().to_dict(),'note':'Olaylar geometrik varyantlar arasında bilerek örtüşebilir; bağımsız gözlem sayılmaz.'};(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
