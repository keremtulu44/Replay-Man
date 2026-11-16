"""Göreceli/çapraz piyasa, Cilt 1, formasyon, seans ve risk paketi."""
from pathlib import Path
import json,pandas as pd
from replayman.replay import load_bars,causal_features
from replayman.advanced_features import indicators,formation_events,risk_outcomes,session_features
from replayman.book_features import attach_forward
from replayman.swings import multi_level_swings
ROOT=Path('data/ohlcv');OUT=Path('research/measurements/book-batch2');H=(5,20,40,60)
def rate(x):x=x.dropna();return float((x>0).mean()) if len(x) else float('nan')
def main():
 paths=sorted(ROOT.glob('*/*/*/bars/*.csv'));OUT.mkdir(parents=True,exist_ok=True);parts=[];refs={}
 for p in paths:
  if p.parts[-4] in {'IDX_XU100','IDX_GSPC','FX_USDTRY','METAL_GOLD','OIL_BRENT'}:
   b=load_bars(p);refs[(p.parts[-4],p.stem)]=pd.DataFrame({'event_ts':b.ts_utc,'ref_return5':b.close.pct_change(5)})
 for p in paths:
  b=load_bars(p);f=indicators(b,causal_features(b));events=[]
  specs=[('rsi_oversold_exit',(f.rsi14.shift(1)<=30)&(f.rsi14>30),'up'),('rsi_overbought_exit',(f.rsi14.shift(1)>=70)&(f.rsi14<70),'down'),('macd_bull_cross',(f.macd_hist.shift(1)<=0)&(f.macd_hist>0),'up'),('macd_bear_cross',(f.macd_hist.shift(1)>=0)&(f.macd_hist<0),'down'),('bollinger_lower_reentry',(f.bollinger_position.shift(1)<-1)&(f.bollinger_position>=-1),'up'),('bollinger_upper_reentry',(f.bollinger_position.shift(1)>1)&(f.bollinger_position<=1),'down')]
  for name,mask,d in specs:
   ix=f.index[mask.fillna(False)];
   if len(ix):events.append(pd.DataFrame({'event':name,'direction':d,'thesis_direction':d,'known_at_position':ix,'event_ts':b.loc[ix].ts_utc}))
  form=formation_events(multi_level_swings(b,f),b,f)
  if len(form):events.append(form)
  if not events:continue
  e=pd.concat(events,ignore_index=True);pos=e.known_at_position.astype(int);e['adx_band']=['strong' if f.iloc[i].adx14>=25 else 'weak' for i in pos];e['bollinger_width']=[f.iloc[i].bollinger_width for i in pos]
  sf=session_features(e.event_ts);e=pd.concat([e.reset_index(drop=True),sf.reset_index(drop=True)],axis=1);e=attach_forward(e,b,H);e=risk_outcomes(e,b,f)
  e.insert(0,'group',p.parts[-5]);e.insert(1,'asset_id',p.parts[-4]);e.insert(2,'interval',p.stem);parts.append(e)
 ev=pd.concat(parts,ignore_index=True);ev.event_ts=pd.to_datetime(ev.event_ts,utc=True)
 # XU100 göreceli sonuç
 bench=[]
 for p in paths:
  if p.parts[-4]!='IDX_XU100':continue
  b=load_bars(p);x=pd.DataFrame({'interval':p.stem,'event_ts':b.ts_utc})
  for h in H:x[f'bench_{h}']=b.close.shift(-h).div(b.close).sub(1)
  bench.append(x)
 ev=ev.merge(pd.concat(bench),on=['interval','event_ts'],how='left');sg=ev.thesis_direction.map({'up':1,'down':-1})
 for h in H:ev[f'excess_{h}']=ev[f'directional_return_{h}']-sg*ev[f'bench_{h}']
 # çapraz piyasa geçmiş 5 bar bağlamları
 for aid in sorted({key[0] for key in refs}):
  pieces=[r.rename(columns={'ref_return5':f'{aid}_return5'}).assign(interval=interval) for (ref_id,interval),r in refs.items() if ref_id==aid]
  ev=ev.merge(pd.concat(pieces,ignore_index=True),on=['interval','event_ts'],how='left')
 rank=ev.groupby(['asset_id','interval']).event_ts.rank(method='first',pct=True);ev['time_split']=pd.cut(rank,[0,.6,.8,1],labels=['train','validation','test'],include_lowest=True)
 ev.to_csv(OUT/'events.csv',index=False)
 keys=['group','interval','time_split','event','thesis_direction','adx_band','session_bucket'];g=ev.groupby(keys,observed=True);spec={'observations':('asset_id','size'),'assets':('asset_id','nunique')}
 for h in H:spec.update({f'ready_{h}':(f'excess_{h}','count'),f'median_excess_{h}':(f'excess_{h}','median'),f'win_rate_{h}':(f'excess_{h}',rate)})
 g.agg(**spec).reset_index().to_csv(OUT/'event_study.csv',index=False)
 ev.groupby(['group','interval','event','risk_state_20'],observed=True).size().rename('observations').reset_index().to_csv(OUT/'risk_study.csv',index=False)
 summary={'events':len(ev),'assets':int(ev.asset_id.nunique()),'event_counts':ev.event.value_counts().to_dict(),'risk_counts':ev.risk_state_20.value_counts().to_dict()};(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
