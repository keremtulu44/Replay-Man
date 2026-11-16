"""ATK P2-P7 için yeni önceki-dönem bölge olayları ve çapraz-kitap sonuç envanteri."""
from pathlib import Path
import json,numpy as np,pandas as pd
from replayman.replay import load_bars,causal_features
DATA=Path('data/ohlcv');OUT=Path('research/measurements/atk-p2-p7');H=(5,20,40,60)
def rate(x):x=x.dropna();return float((x>0).mean()) if len(x) else np.nan
def main():
 OUT.mkdir(parents=True,exist_ok=True);bench={};parts=[]
 for p in DATA.glob('bist_indices/IDX_XU100/*/bars/*.csv'):
  b=load_bars(p);bench[p.stem]=b.set_index('ts_utc').close
 for p in sorted(DATA.glob('*/*/*/bars/*.csv')):
  b=load_bars(p);f=causal_features(b);day=b.ts_utc.dt.floor('D');week=b.ts_utc.dt.tz_localize(None).dt.to_period('W').dt.start_time.dt.tz_localize('UTC');levels={}
  for prefix,key in [('prev_day',day),('prev_week',week)]:
   z=pd.DataFrame({'key':key,'high':b.high,'low':b.low}).groupby('key').agg(high=('high','max'),low=('low','min')).shift(1);levels[prefix+'_high']=key.map(z.high);levels[prefix+'_low']=key.map(z.low)
  split=np.where(np.arange(len(b))/len(b)<.6,'train',np.where(np.arange(len(b))/len(b)<.8,'validation','test'))
  for name,level in levels.items():
   high_side=name.endswith('high');up=(b.close>level)&(b.close.shift(1)<=level.shift(1));down=(b.close<level)&(b.close.shift(1)>=level.shift(1));probe=((b.high>level)&(b.close<=level)) if high_side else ((b.low<level)&(b.close>=level));events=[(name+'_break',up if high_side else down,1 if high_side else -1),(name+'_probe_reject',probe,-1 if high_side else 1)]
   for event,mask,sg in events:
    pos=np.flatnonzero(mask.fillna(False));
    if not len(pos):continue
    d=pd.DataFrame({'group':p.parts[-5],'asset_id':p.parts[-4],'interval':p.stem,'event':event,'event_ts':b.ts_utc.iloc[pos].to_numpy(),'time_split':split[pos],'direction':sg,'distance_atr':((b.close-level).abs()/f.atr).iloc[pos].to_numpy()})
    for h in H:
     raw=b.close.shift(-h).div(b.close).sub(1).iloc[pos].to_numpy()*sg;d[f'return_{h}']=raw;d[f'excess_{h}']=np.nan
     if p.parts[-5]=='bist_equities' and p.stem in bench:
      q=bench[p.stem];br=(q.shift(-h)/q-1).reindex(pd.DatetimeIndex(b.ts_utc.iloc[pos])).to_numpy();d[f'excess_{h}']=raw-sg*br
    parts.append(d)
 d=pd.concat(parts,ignore_index=True);spec={'observations':('asset_id','size'),'assets':('asset_id','nunique'),'median_distance_atr':('distance_atr','median')}
 for h in H:spec.update({f'ready_{h}':(f'return_{h}','count'),f'median_return_{h}':(f'return_{h}','median'),f'positive_{h}':(f'return_{h}',rate),f'median_excess_{h}':(f'excess_{h}','median')})
 d.groupby(['group','interval','time_split','event','direction'],dropna=False).agg(**spec).reset_index().to_csv(OUT/'zone_event_study.csv',index=False);d.groupby(['interval','event','asset_id']).agg(observations=('asset_id','size'),median_return_60=('return_60','median'),median_excess_60=('excess_60','median')).reset_index().to_csv(OUT/'zone_symbol_results.csv',index=False)
 # Daha önce tamamlanan kitap ölçümlerini kayıp olmadan envantere bağla.
 refs=[]
 for path in sorted(Path('research/measurements').glob('*')):
  if path.name.startswith(('cilt1-','cilt2-','book-batch','attempts','ohlcv-baseline')):
   for f in path.glob('*.csv*'):refs.append({'measurement':path.name,'file':f.name,'bytes':f.stat().st_size})
 pd.DataFrame(refs).to_csv(OUT/'cross_book_measurement_inventory.csv',index=False);summary={'new_zone_events':len(d),'assets':int(d.asset_id.nunique()),'cross_book_files':len(refs),'mtf_source':'research/measurements/book-batch1/time_regime_mtf_study.csv'};(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
