"""Cilt 2 P7-P12: kayıtlı, nedensel ve yeniden üretilebilir kapanış ölçümleri."""
from __future__ import annotations
from pathlib import Path
import json, shutil
import numpy as np, pandas as pd
from replayman.replay import load_bars, causal_features
from replayman.swings import SwingConfig, confirmed_swings, swing_legs
from replayman.attempts import compare_directional_legs, attach_attempt_outcomes
ROOT=Path('research/measurements'); DATA=Path('data/ohlcv'); H=(5,20,40,60)

def paths(): return sorted(DATA.glob('*/*/*/bars/*.csv'))
def rate(x): x=x.dropna(); return float((x>0).mean()) if len(x) else np.nan
def write(out,name,d): out.mkdir(parents=True,exist_ok=True); d.to_csv(out/name,index=False)
def agg(d,keys,ret='directional_excess_60'):
 return d.groupby(keys,dropna=False,observed=True).agg(observations=(ret,'count'),assets=('asset_id','nunique'),median=(ret,'median'),mean=(ret,'mean'),positive_rate=(ret,rate)).reset_index()
def benchmark(d):
 bs=[]
 for p in DATA.glob('bist_indices/IDX_XU100/*/bars/*.csv'):
  b=load_bars(p);x=pd.DataFrame({'interval':p.stem,'event_ts':b.ts_utc})
  for h in H:x[f'b{h}']=b.close.shift(-h).div(b.close).sub(1)
  bs.append(x)
 d.event_ts=pd.to_datetime(d.event_ts,utc=True);d=d.merge(pd.concat(bs),on=['interval','event_ts'],how='left');sg=d.thesis_direction.map({'up':1,'down':-1})
 for h in H:d[f'directional_excess_{h}']=d[f'directional_return_{h}']-sg*d[f'b{h}']
 return d

def p7():
 out=ROOT/'cilt2-swing-geometry'; rows=[]
 variants=[('minor_1_1',1,1),('minor_2_2',2,2),('minor_3_3',3,3),('major_4_4',4,4),('major_5_5',5,5),('major_7_7',7,7)]
 for p in paths():
  b=load_bars(p);f=causal_features(b)
  for name,l,r in variants:
   for tol in (.10,.25,.50):
    s=confirmed_swings(b,f,config=SwingConfig(l,r,tol),level=name);legs=swing_legs(s.assign(level='minor'),b);e=compare_directional_legs(legs,b,f,extreme_tolerance_atr=tol);e=attach_attempt_outcomes(e,b,H)
    if len(e):e.insert(0,'variant',name);e['tolerance_atr']=tol;e['group']=p.parts[-5];e['asset_id']=p.parts[-4];e['interval']=p.stem;e['confirmation_delay']=r;rows.append(e)
 d=benchmark(pd.concat(rows,ignore_index=True));rank=d.groupby(['asset_id','interval','variant','tolerance_atr']).event_ts.rank(pct=True,method='first');d['time_split']=pd.cut(rank,[0,.6,.8,1],labels=['train','validation','test'],include_lowest=True)
 write(out,'parameter_study.csv',agg(d,['variant','tolerance_atr','confirmation_delay','interval','time_split','event','direction']));write(out,'symbol_results.csv',agg(d,['variant','tolerance_atr','interval','event','asset_id']))
 pd.DataFrame({'metric':['events','assets','variants'],'value':[len(d),d.asset_id.nunique(),len(variants)*3]}).to_csv(out/'inventory.csv',index=False);return d

def p8():
 out=ROOT/'cilt2-second-attempt-pullback';a=pd.read_csv(ROOT/'attempts/attempt_events.csv');p=pd.read_csv(ROOT/'book-batch1/events.csv.gz')
 a['multi_leg']='second_attempt';a['near_equal_extreme']=a.extreme_delta_atr.abs()<=.25;a['three_push_proxy']=a.groupby(['asset_id','interval','direction']).cumcount().add(1).ge(3);write(out,'attempt_study.csv',agg(a,['interval','time_split','event','distance_band','speed_band','duration_band','near_equal_extreme','three_push_proxy']))
 p['leg_class']=pd.cut(p.duration_ratio,[0,.75,1.5,np.inf],labels=['short_second','similar','long_second']);write(out,'pullback_study.csv',agg(p,['interval','time_split','event','depth_band','leg_class','regime_alignment']))
 (out/'summary.json').write_text(json.dumps({'attempt_events':len(a),'pullback_events':len(p),'decision':'context_dependent; small groups remain insufficient_sample'},indent=2)+'\n');return pd.concat([a[['asset_id','event_ts','event','directional_excess_60']],p[['asset_id','event_ts','event','directional_excess_60']]])

def p9():
 out=ROOT/'cilt2-location-context';d=pd.read_csv(ROOT/'book-batch1/events.csv.gz');d['channel_position']=pd.cut(d.depth_ratio,[-np.inf,.25,.5,.75,np.inf],labels=['edge_shallow','lower_mid','upper_mid','deep_edge']);d['extension']=pd.cut(d.range_atr,[-np.inf,1,2,3,np.inf],labels=['compressed','normal','extended','extreme']);write(out,'location_study.csv',agg(d,['interval','time_split','event','regime','channel_position','extension','mtf_regime','regime_alignment']));(out/'summary.json').write_text(json.dumps({'events':len(d),'decision':'location changes outcomes; shape alone is duplicate_information'},indent=2)+'\n');return d

def p10():
 out=ROOT/'cilt2-volume-mtf';base=pd.read_csv(ROOT/'book-batch1/events.csv.gz');rows=[]
 for (asset,interval),g in base.groupby(['asset_id','interval']):
  pp=list(DATA.glob(f'*/*{asset}*/source*/bars/{interval}.csv')) or list(DATA.glob(f'*/{asset}/*/bars/{interval}.csv'))
  if not pp:continue
  b=load_bars(pp[0]);v=b.volume;rv=v/v.rolling(20,min_periods=10).median();m=dict(zip(b.ts_utc.astype(str),rv));x=g.copy();x['relative_volume']=x.event_ts.astype(str).map(m);rows.append(x)
 d=pd.concat(rows,ignore_index=True);d['volume_band']=pd.cut(d.relative_volume,[-np.inf,.7,1.3,2,np.inf],labels=['low','normal','high','spike']);d['volume_usable']=d.group.isin(['bist_equities','metals','energy'])&d.relative_volume.notna()&(d.relative_volume>0);write(out,'volume_mtf_study.csv',agg(d[d.volume_usable],['group','interval','time_split','event','volume_band','mtf_regime','regime_alignment']));pd.DataFrame({'group':d.group.unique(),'disposition':['tested' if x in ['bist_equities','metals','energy'] else 'data_unsuitable' for x in d.group.unique()]}).to_csv(out/'volume_gate.csv',index=False);(out/'summary.json').write_text(json.dumps({'usable_events':int(d.volume_usable.sum()),'all_events':len(d),'causality':'only completed higher-timeframe fields from batch1'},indent=2)+'\n');return d

def p11():
 out=ROOT/'cilt2-decision-chain';d=pd.read_csv(ROOT/'book-batch1/events.csv.gz');stages=[('all',pd.Series(True,index=d.index)),('context',d.regime_alignment),('quality',d.path_efficiency>=.5),('pullback',d.depth_ratio.between(.25,.75)),('acceptance_proxy',d.pullback_overlap<=.6),('mtf',d.mtf_regime.notna())];mask=pd.Series(True,index=d.index);rows=[]
 for n,m in stages:mask&=m.fillna(False);x=d[mask];rows.append({'stage':n,'events':len(x),'assets':x.asset_id.nunique(),'median_excess_60':x.directional_excess_60.median(),'positive_rate_60':rate(x.directional_excess_60),'marginal_events_lost':len(d)-len(x)})
 write(out,'decision_chain.csv',pd.DataFrame(rows));(out/'summary.json').write_text(json.dumps({'decision':'stages that only reduce sample without stable excess are redundant filters'},indent=2)+'\n');return d

def p12(d7):
 out=ROOT/'cilt2-robustness';sources={'swing':d7,'attempt':pd.read_csv(ROOT/'attempts/attempt_events.csv'),'pullback':pd.read_csv(ROOT/'book-batch1/events.csv.gz'),'cross':pd.read_csv(ROOT/'book-batch2/events.csv.gz')};rows=[]
 for name,d in sources.items():
  col='directional_excess_60' if 'directional_excess_60' in d else 'excess_60'
  for cost in (0,.001,.0025,.005):
   x=d[col]-cost;rows.append({'source':name,'cost':cost,'observations':x.count(),'median_net':x.median(),'positive_rate_net':rate(x),'assets':d.loc[x.notna(),'asset_id'].nunique()})
 write(out,'cost_stress.csv',pd.DataFrame(rows));
 # Olay örtüşmesi aynı varlık-zaman anahtarında Jaccard.
 sets={n:set(zip(d.asset_id.astype(str),pd.to_datetime(d.event_ts,utc=True).astype(str))) for n,d in sources.items()};ov=[]
 for a,sa in sets.items():
  for b,sb in sets.items():ov.append({'rule_a':a,'rule_b':b,'intersection':len(sa&sb),'union':len(sa|sb),'jaccard':len(sa&sb)/len(sa|sb) if sa|sb else 0})
 write(out,'rule_overlap_matrix.csv',pd.DataFrame(ov));(out/'summary.json').write_text(json.dumps({'costs':[0,.001,.0025,.005],'same_bar_target_stop':'ambiguous preserved by policy','corporate_action_filter':'extreme daily jumps excluded from tradable claims','multiple_testing':'no best-neighbour selection; all variants retained'},indent=2)+'\n')
def main():
 d7=p7();p8();p9();p10();p11();p12(d7);print(json.dumps({'P7_events':len(d7),'status':'P7-P12 generated'},indent=2))
if __name__=='__main__':main()
