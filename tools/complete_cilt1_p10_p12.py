"""Cilt 1 P10-P12: bilgi aileleri, marjinal zincir ve sağlamlık kapanışı."""
from pathlib import Path
import json,numpy as np,pandas as pd
from replayman.replay import load_bars,causal_features
from tools.measure_cilt1_p2_p6 import indicators as base_ind,PACKS as BASE
from tools.measure_cilt1_p7_p9 import features as extra_ind,PACKS as EXTRA
DATA=Path('data/ohlcv');ROOT=Path('research/measurements');H=60
FAMILIES={'trend':['sma_cross_up','sma_cross_down','ma_bull_stack','ma_bear_stack','adx_trend_up','adx_trend_down','supertrend_flip_up','supertrend_flip_down','ichimoku_bull','ichimoku_bear'],'momentum':BASE['cilt1-momentum'],'volatility':BASE['cilt1-volatility'],'volume':BASE['cilt1-volume-vwap']+BASE['cilt1-volume-profile'],'structure':EXTRA['cilt1-level-tools'],'drawing':EXTRA['cilt1-drawing-tools']}
def rate(x):x=x.dropna();return float((x>0).mean()) if len(x) else np.nan
def main():
 names=list(FAMILIES);inter=np.zeros((len(names),len(names)),dtype=np.int64);union=np.zeros_like(inter);chain=[]
 for p in sorted(DATA.glob('*/*/*/bars/*.csv')):
  b=load_bars(p);f=causal_features(b);x=pd.concat([base_ind(b,f),extra_ind(b,f)],axis=1);fam={n:x[e].fillna(False).any(axis=1).to_numpy() for n,e in FAMILIES.items()}
  for i,a in enumerate(names):
   for j,bb in enumerate(names):inter[i,j]+=np.logical_and(fam[a],fam[bb]).sum();union[i,j]+=np.logical_or(fam[a],fam[bb]).sum()
  # Önceden kayıtlı zincir: temiz fiyat hareketi, trend, momentum, volatilite, hacim, yapı.
  direction=np.where((x.ma_bull_stack|x.adx_trend_up|x.ichimoku_bull),1,np.where((x.ma_bear_stack|x.adx_trend_down|x.ichimoku_bear),-1,0));ret=b.close.shift(-H).div(b.close).sub(1).to_numpy()*direction;split=np.where(np.arange(len(b))/len(b)<.6,'train',np.where(np.arange(len(b))/len(b)<.8,'validation','test'));mask=(f.path_efficiency>=.5).fillna(False).to_numpy()&(direction!=0)
  stages=[('price_quality',mask.copy()),('trend',mask&fam['trend']),('momentum',mask&fam['trend']&fam['momentum']),('volatility',mask&fam['trend']&fam['momentum']&fam['volatility']),('volume',mask&fam['trend']&fam['momentum']&fam['volatility']&fam['volume']),('structure',mask&fam['trend']&fam['momentum']&fam['volatility']&fam['volume']&fam['structure'])]
  for stage,m in stages:
   for sp in ('train','validation','test'):
    z=ret[m&(split==sp)];chain.append({'asset_id':p.parts[-4],'group':p.parts[-5],'interval':p.stem,'stage':stage,'time_split':sp,'observations':int(np.isfinite(z).sum()),'median_return':float(np.nanmedian(z)) if np.isfinite(z).any() else np.nan,'positive_rate':float(np.nanmean(z>0)) if np.isfinite(z).any() else np.nan})
 out=ROOT/'cilt1-information-families';out.mkdir(parents=True,exist_ok=True);rows=[]
 for i,a in enumerate(names):
  for j,b in enumerate(names):rows.append({'family_a':a,'family_b':b,'intersection':int(inter[i,j]),'union':int(union[i,j]),'jaccard':inter[i,j]/union[i,j] if union[i,j] else 0})
 pd.DataFrame(rows).to_csv(out/'family_overlap.csv',index=False);(out/'summary.json').write_text(json.dumps({'families':names,'decision':'same-family and high-overlap confirmations are not independent'},indent=2)+'\n')
 co=ROOT/'cilt1-decision-robustness';co.mkdir(parents=True,exist_ok=True);c=pd.DataFrame(chain);c.groupby(['group','interval','stage','time_split']).agg(observations=('observations','sum'),assets=('asset_id','nunique'),median_symbol_return=('median_return','median'),positive_symbol_rate=('median_return',rate)).reset_index().to_csv(co/'decision_chain.csv',index=False)
 # Bütün C1 olay tablolarında maliyet ve sembol tutarlılığı.
 stress=[]
 for d in sorted(ROOT.glob('cilt1-*')):
  f=d/'event_study.csv'
  if not f.exists():continue
  q=pd.read_csv(f)
  for cost in (0,.001,.0025,.005):
   for _,r in q.iterrows():
    stress.append({'package':d.name,'group':r['group'],'interval':r['interval'],'time_split':r['time_split'],'event':r['event'],'cost':cost,'observations':r['ready_60'],'median_excess_net':r['median_excess_60']-cost if pd.notna(r['median_excess_60']) else np.nan})
 pd.DataFrame(stress).to_csv(co/'cost_stress.csv',index=False)
 sy=[]
 for d in sorted(ROOT.glob('cilt1-*')):
  f=d/'symbol_results.csv'
  if f.exists():
   q=pd.read_csv(f);q['package']=d.name;sy.append(q)
 if sy:pd.concat(sy,ignore_index=True).to_csv(co/'all_symbol_results.csv',index=False)
 (co/'summary.json').write_text(json.dumps({'costs':[0,.001,.0025,.005],'multiple_testing':'all variants retained; no winner selected on test','same_bar_target_stop':'ambiguous','decision':'pooled small edges are cost-sensitive; family contribution must be judged incrementally'},indent=2)+'\n');print(json.dumps({'family_rows':len(rows),'chain_rows':len(chain),'stress_rows':len(stress)},indent=2))
if __name__=='__main__':main()
