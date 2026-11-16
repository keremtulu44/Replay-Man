"""Pullback, mum, rejim ve tamamlanmış üst-zaman bağlamını birlikte ölçer."""
from pathlib import Path
import json
import pandas as pd
from replayman.replay import load_bars,causal_features
from replayman.swings import multi_level_swings,swing_legs
from replayman.book_features import candle_and_regime_features,pullback_events,attach_forward
ROOT=Path('data/ohlcv');OUT=Path('research/measurements/book-batch1');H=(5,20,40,60)
def rate(x): x=x.dropna();return float((x>0).mean()) if len(x) else float('nan')
def paths():return sorted(ROOT.glob('*/*/*/bars/*.csv'))
def main():
 OUT.mkdir(parents=True,exist_ok=True); allparts=[]; inventory=[]
 byasset={}
 for p in paths():byasset.setdefault(p.parts[-4],{})[p.stem]=p
 for asset,series in byasset.items():
  loaded={};feat={}
  for interval,p in series.items():
   b=load_bars(p);f=candle_and_regime_features(b,causal_features(b));loaded[interval]=b;feat[interval]=f
  for interval,b in loaded.items():
   f=feat[interval]; group=series[interval].parts[-5]; parts=[]
   pb=pullback_events(swing_legs(multi_level_swings(b,f),b),b,f)
   if len(pb):parts.append(pb)
   specs=[('strong_bull_close','up'),('strong_bear_close','down'),('bullish_engulfing','up'),('bearish_engulfing','down')]
   for name,direction in specs:
    ix=f.index[f[name]==1]
    if len(ix):parts.append(pd.DataFrame({'event':name,'direction':direction,'thesis_direction':direction,'known_at_position':ix,'event_ts':b.loc[ix,'ts_utc']}))
   inventory.append({'group':group,'asset_id':asset,'interval':interval,'bars':len(b),'inside_bars':int(f.inside_bar.sum()),'outside_bars':int(f.outside_bar.sum()),'doji_like':int(f.doji_like.sum()),**{n:int(f[n].sum()) for n,_ in specs},**{f'regime_{r}':int((f.regime==r).sum()) for r in ['trend_up','trend_down','range','transition']}})
   if not parts:continue
   e=pd.concat(parts,ignore_index=True);pos=e.known_at_position.astype(int);e['regime']=[f.iloc[i].regime for i in pos];e['path_efficiency']=[f.iloc[i].path_efficiency for i in pos];e['range_atr']=[f.iloc[i].range_atr for i in pos]
   # Üst zaman yalnız bar süresi dolduktan sonra görünür.
   upper='4h' if interval in {'1h','2h'} and '4h' in loaded else None
   if upper:
    uf=feat[upper];ub=loaded[upper];u=pd.DataFrame({'available_ts':ub.ts_utc+pd.Timedelta(hours=4),'mtf_regime':uf.regime})
    e=pd.merge_asof(e.sort_values('event_ts'),u.sort_values('available_ts'),left_on='event_ts',right_on='available_ts',direction='backward').drop(columns='available_ts')
   else:e['mtf_regime']='not_measured'
   e['regime_alignment']=[('aligned' if (d=='up' and r=='trend_up') or (d=='down' and r=='trend_down') else 'opposed' if (d=='up' and r=='trend_down') or (d=='down' and r=='trend_up') else r) for d,r in zip(e.thesis_direction,e.mtf_regime)]
   e=attach_forward(e,b,H);e.insert(0,'group',group);e.insert(1,'asset_id',asset);e.insert(2,'interval',interval);allparts.append(e)
 events=pd.concat(allparts,ignore_index=True);events.event_ts=pd.to_datetime(events.event_ts,utc=True)
 # Benchmark
 bench=[]
 for p in paths():
  if p.parts[-4]!='IDX_XU100':continue
  b=load_bars(p);x=pd.DataFrame({'interval':p.stem,'event_ts':b.ts_utc})
  for h in H:x[f'benchmark_return_{h}']=b.close.shift(-h).div(b.close).sub(1)
  bench.append(x)
 events=events.merge(pd.concat(bench),on=['interval','event_ts'],how='left');sign=events.thesis_direction.map({'up':1,'down':-1})
 for h in H:events[f'directional_excess_{h}']=events[f'directional_return_{h}']-sign*events[f'benchmark_return_{h}']
 rank=events.groupby(['asset_id','interval']).event_ts.rank(method='first',pct=True);events['time_split']=pd.cut(rank,[0,.6,.8,1],labels=['train','validation','test'],include_lowest=True)
 events['depth_band']=pd.cut(events.get('depth_ratio'),[-float('inf'),.382,.618,1,float('inf')],labels=['shallow','medium','deep','over_100'])
 events.to_csv(OUT/'events.csv',index=False);pd.DataFrame(inventory).to_csv(OUT/'inventory.csv',index=False)
 keys=['group','interval','time_split','event','thesis_direction','regime','regime_alignment'];g=events.groupby(keys,observed=True)
 spec={'observations':('asset_id','size'),'assets':('asset_id','nunique')}
 for h in H:spec.update({f'ready_excess_{h}':(f'directional_excess_{h}','count'),f'median_excess_{h}':(f'directional_excess_{h}','median'),f'excess_win_rate_{h}':(f'directional_excess_{h}',rate)})
 g.agg(**spec).reset_index().to_csv(OUT/'time_regime_mtf_study.csv',index=False)
 pg=events[events.event=='pullback_confirmed'].groupby(keys+['depth_band'],observed=True).agg(**spec).reset_index();pg.to_csv(OUT/'pullback_depth_study.csv',index=False)
 summary={'events':len(events),'pullbacks':int((events.event=='pullback_confirmed').sum()),'candle_events':int((events.event!='pullback_confirmed').sum()),'assets':int(events.asset_id.nunique()),'series':int(events.groupby(['asset_id','interval']).ngroups)}
 (OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
