"""Cilt 2 P6 kırılım yaşam döngüsü ayrıntıları ve tek-faktör parametre dayanıklılığı."""
from pathlib import Path
import json,pandas as pd
from replayman.replay import load_bars,causal_features
from replayman.swings import multi_level_swings
from replayman.structure import StructureConfig,structure_events,attach_event_outcomes
from replayman.lifecycle import enrich_lifecycle
ROOT=Path('data/ohlcv');OUT=Path('research/measurements/cilt2-lifecycle');H=(5,20,40,60)
def rate(x):x=x.dropna();return float((x>0).mean()) if len(x) else float('nan')
def paths():return sorted(ROOT.glob('*/*/*/bars/*.csv'))
def add_benchmark(ev):
 bench=[]
 for p in ROOT.glob('bist_indices/IDX_XU100/*/bars/*.csv'):
  b=load_bars(p);x=pd.DataFrame({'interval':p.stem,'event_ts':b.ts_utc})
  for h in H:x[f'bench_{h}']=b.close.shift(-h).div(b.close).sub(1)
  bench.append(x)
 ev=ev.merge(pd.concat(bench),on=['interval','event_ts'],how='left');sg=ev.thesis_direction.map({'up':1,'down':-1})
 for h in H:
  if f'directional_return_{h}' in ev:ev[f'excess_{h}']=ev[f'directional_return_{h}']-sg*ev[f'bench_{h}']
 return ev
def aggregate(ev,keys):
 spec={'observations':('asset_id','size'),'assets':('asset_id','nunique')}
 for h in H:spec.update({f'ready_{h}':(f'excess_{h}','count'),f'median_excess_{h}':(f'excess_{h}','median'),f'win_rate_{h}':(f'excess_{h}',rate)})
 return ev.groupby(keys,observed=True,dropna=False).agg(**spec).reset_index()
def main():
 OUT.mkdir(parents=True,exist_ok=True);parts=[]
 for p in paths():
  b=load_bars(p);f=causal_features(b);s=multi_level_swings(b,f);e=structure_events(b,f,s);e=enrich_lifecycle(e,b,f);e=attach_event_outcomes(e,b,H)
  if len(e):e.insert(0,'group',p.parts[-5]);e.insert(1,'asset_id',p.parts[-4]);e.insert(2,'interval',p.stem);parts.append(e)
 ev=add_benchmark(pd.concat(parts,ignore_index=True));ev.event_ts=pd.to_datetime(ev.event_ts,utc=True);rank=ev.groupby(['asset_id','interval']).event_ts.rank(method='first',pct=True);ev['time_split']=pd.cut(rank,[0,.6,.8,1],labels=['train','validation','test'],include_lowest=True)
 ev['distance_band']=pd.cut(ev.distance_close_atr.abs(),[-1,.1,.3,.6,float('inf')],labels=['near','small','medium','large']);ev['age_band']=pd.cut(ev.level_age_bars,[-1,10,30,60,1000],labels=['fresh','young','mature','old']);ev['attempt_band']=pd.cut(ev.attempt_number,[-1,1,2,3,1000],labels=['first','second','third','many']);ev['duration_band']=pd.cut(ev.outside_duration,[-1,1,3,5,1000],labels=['one','short','medium','long']);ev['failure_depth_band']=pd.cut(ev.old_area_depth_atr,[-float('inf'),.1,.3,.6,float('inf')],labels=['near','small','medium','deep']);ev['counter_expansion']=ev.counter_expansion_position.notna()
 keys=['group','interval','time_split','event','direction','thesis_direction','distance_band','age_band','attempt_band','duration_band','failure_depth_band','counter_expansion'];aggregate(ev,keys).to_csv(OUT/'detailed_event_study.csv',index=False)
 # Tek faktör parametre dayanıklılığı yalnız BIST hisseleri 4h: hesap yükünü kontrol altında tutar.
 variants=[('baseline',StructureConfig()),('tol005',StructureConfig(tolerance_atr=.05)),('tol020',StructureConfig(tolerance_atr=.20)),('accept1',StructureConfig(acceptance_closes=1)),('accept3',StructureConfig(acceptance_closes=3)),('follow1',StructureConfig(follow_through_bars=1)),('follow5',StructureConfig(follow_through_bars=5)),('failure5',StructureConfig(failure_bars=5)),('failure20',StructureConfig(failure_bars=20)),('age50',StructureConfig(max_level_age=50)),('age150',StructureConfig(max_level_age=150))]
 pp=[]
 for p in paths():
  if p.parts[-5]!='bist_equities' or p.stem!='4h':continue
  b=load_bars(p);f=causal_features(b);s=multi_level_swings(b,f)
  for name,cfg in variants:
   x=attach_event_outcomes(structure_events(b,f,s,config=cfg),b,(60,));x['variant']=name;x['asset_id']=p.parts[-4];x['interval']='4h';pp.append(x)
 pv=add_benchmark(pd.concat(pp,ignore_index=True));pv.groupby(['variant','event','direction','thesis_direction'],observed=True).agg(observations=('asset_id','size'),assets=('asset_id','nunique'),ready_60=('excess_60','count'),median_excess_60=('excess_60','median'),win_rate_60=('excess_60',rate)).reset_index().to_csv(OUT/'parameter_study.csv',index=False)
 summary={'events':len(ev),'assets':int(ev.asset_id.nunique()),'counter_expansions':int(ev.counter_expansion.sum()),'parameter_variants':[x[0] for x in variants]};(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
