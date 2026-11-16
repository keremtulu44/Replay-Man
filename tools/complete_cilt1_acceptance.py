"""Cilt 1 nihai kabul açıkları: komşuluk, MFE/MAE, ortak takvim, excess zinciri ve ablation."""
from pathlib import Path
import json,numpy as np,pandas as pd
from replayman.replay import load_bars,causal_features
from tools.measure_cilt1_p2_p6 import indicators as base_ind,profile,PACKS as BASE
from tools.measure_cilt1_p7_p9 import features as extra_ind,PACKS as EXTRA
DATA=Path('data/ohlcv');OUT=Path('research/measurements/cilt1-final-acceptance');H=(5,20,40,60)
FAM={'trend':['ma_bull_stack','ma_bear_stack','adx_trend_up','adx_trend_down','ichimoku_bull','ichimoku_bear'],'momentum':BASE['cilt1-momentum'],'volatility':BASE['cilt1-volatility'],'volume':BASE['cilt1-volume-vwap']+BASE['cilt1-volume-profile'],'structure':EXTRA['cilt1-level-tools'],'drawing':EXTRA['cilt1-drawing-tools']}
BEAR={e for e in sum([*BASE.values(),*EXTRA.values()],[]) if any(z in e for z in ['down','bear','below','lower_break'])}|{'rsi_above_70'}
def rate(x):x=x.dropna();return float((x>0).mean()) if len(x) else np.nan
def split(ts,lo,hi):return np.where(ts<lo,'train',np.where(ts<hi,'validation','test'))
def variants(b,f):
 c,h,l=b.close.astype(float),b.high.astype(float),b.low.astype(float);r={}
 for fast in (10,20,30):
  for slow in (40,50,60):
   a=c.ewm(span=fast,adjust=False,min_periods=fast).mean();z=c.ewm(span=slow,adjust=False,min_periods=slow).mean();r[f'ema_{fast}_{slow}_up']=(a>z)&(a.shift(1)<=z.shift(1));r[f'ema_{fast}_{slow}_down']=(a<z)&(a.shift(1)>=z.shift(1))
 for n in (7,14,21):
  d=c.diff();g=d.clip(lower=0).ewm(alpha=1/n,adjust=False,min_periods=n).mean();q=(-d.clip(upper=0)).ewm(alpha=1/n,adjust=False,min_periods=n).mean();v=100-100/(1+g/q.replace(0,np.nan))
  for low,high in ((25,75),(30,70),(35,65)):r[f'rsi_{n}_{low}_low']=v<low;r[f'rsi_{n}_{high}_high']=v>high
 for n in (15,20,30):
  m=c.rolling(n).mean();s=c.rolling(n).std()
  for k in (1.5,2,2.5):r[f'bb_{n}_{k}_up']=c>m+k*s;r[f'bb_{n}_{k}_down']=c<m-k*s
 up=h.diff();dn=-l.diff()
 for n in (10,14,20):
  pdm=up.where((up>dn)&(up>0),0);mdm=dn.where((dn>up)&(dn>0),0);atr=f.true_range.rolling(n).mean();plus=100*pdm.rolling(n).mean()/atr;minus=100*mdm.rolling(n).mean()/atr;adx=(100*(plus-minus).abs()/(plus+minus).replace(0,np.nan)).rolling(n).mean()
  for th in (20,25,30):r[f'adx_{n}_{th}_up']=(adx>th)&(plus>minus);r[f'adx_{n}_{th}_down']=(adx>th)&(minus>plus)
 for ten,kij,span in ((7,22,44),(9,26,52),(12,30,60)):
  t=(h.rolling(ten).max()+l.rolling(ten).min())/2;k=(h.rolling(kij).max()+l.rolling(kij).min())/2;sb=(h.rolling(span).max()+l.rolling(span).min())/2;r[f'ichi_{ten}_{kij}_{span}_up']=(c>(t+k)/2)&(c>sb)&(t>k);r[f'ichi_{ten}_{kij}_{span}_down']=(c<(t+k)/2)&(c<sb)&(t<k)
 for n in (30,50,80):
  slope=(c-c.shift(n))/(n*f.atr)
  for th in (.5,1,1.5):r[f'gann_{n}_{th}_up']=slope>=th;r[f'gann_{n}_{th}_down']=slope<=-th
 return pd.DataFrame(r)
def supertrend_variants(b,f):
 c=b.close.to_numpy(float);mid=((b.high+b.low)/2).to_numpy(float);atr=f.atr.to_numpy(float);out={}
 for mult in (2,3,4):
  bu=mid+mult*atr;bl=mid-mult*atr;fu=bu.copy();fl=bl.copy();tr=np.ones(len(b),int)
  for i in range(1,len(b)):
   if not np.isfinite(bu[i]):continue
   if not np.isfinite(fu[i-1]):fu[i]=bu[i];fl[i]=bl[i];continue
   fu[i]=bu[i] if bu[i]<fu[i-1] or c[i-1]>fu[i-1] else fu[i-1];fl[i]=bl[i] if bl[i]>fl[i-1] or c[i-1]<fl[i-1] else fl[i-1];tr[i]=(-1 if c[i]<fl[i-1] else 1) if tr[i-1]==1 else (1 if c[i]>fu[i-1] else -1)
  out[f'supertrend_{mult}_up']=(tr==1)&(np.roll(tr,1)==-1);out[f'supertrend_{mult}_down']=(tr==-1)&(np.roll(tr,1)==1);out[f'supertrend_{mult}_up'][0]=False;out[f'supertrend_{mult}_down'][0]=False
 return pd.DataFrame(out)
def profile_variants(b):
 tp=((b.high+b.low+b.close)/3).to_numpy();v=b.volume.to_numpy();out={}
 for w,bins,va in ((40,12,.68),(60,20,.70),(120,30,.75)):
  p=profile(tp,v,w,bins,va);out[f'profile_{w}_{bins}_{int(va*100)}_up']=(b.close>p.poc)&(b.close.shift(1)<=p.poc.shift(1));out[f'profile_{w}_{bins}_{int(va*100)}_down']=(b.close<p.poc)&(b.close.shift(1)>=p.poc.shift(1));out[f'profile_{w}_{bins}_{int(va*100)}_accept']=b.close.between(p.va_low,p.va_high)&b.close.shift(1).between(p.va_low.shift(1),p.va_high.shift(1))
 return pd.DataFrame(out)
def main():
 OUT.mkdir(parents=True,exist_ok=True);all_ts=[]
 for p in DATA.glob('*/*/*/bars/*.csv'):all_ts.extend(load_bars(p).ts_utc.tolist())
 lo,hi=pd.Series(all_ts).quantile([.6,.8]).tolist();bench={}
 for p in DATA.glob('bist_indices/IDX_XU100/*/bars/*.csv'):
  b=load_bars(p);bench[p.stem]=b.set_index('ts_utc').close
 par=[];evt=[];chain=[];abl=[];corr=[]
 for p in sorted(DATA.glob('*/*/*/bars/*.csv')):
  b=load_bars(p);f=causal_features(b);base=base_ind(b,f);extra=extra_ind(b,f);x=pd.concat([base,extra],axis=1);ts=b.ts_utc;sp=split(ts,lo,hi);group=p.parts[-5];asset=p.parts[-4];interval=p.stem
  q=pd.concat([variants(b,f),supertrend_variants(b,f)],axis=1)
  if group in {'bist_equities','metals','energy'}:q=pd.concat([q,profile_variants(b)],axis=1)
  for e in q:
   pos=np.flatnonzero(q[e].fillna(False));sg=-1 if ('down' in e or 'high' in e) else 1
   if len(pos):
    raw=b.close.shift(-60).div(b.close).sub(1).iloc[pos].to_numpy()*sg;ex=np.full(len(pos),np.nan)
    if group=='bist_equities' and interval in bench:
     z=bench[interval];br=(z.shift(-60)/z-1).reindex(pd.DatetimeIndex(ts.iloc[pos])).to_numpy();ex=raw-sg*br
    for ss in ('train','validation','test'):
     m=sp[pos]==ss;par.append({'variant':e,'family':e.split('_')[0],'group':group,'interval':interval,'time_split':ss,'observations':int(m.sum()),'ready':int(np.isfinite(raw[m]).sum()),'median_return':np.nanmedian(raw[m]) if np.isfinite(raw[m]).any() else np.nan,'median_excess':np.nanmedian(ex[m]) if np.isfinite(ex[m]).any() else np.nan})
  # Baseline tüm olaylarda MFE/MAE ve ortak takvim; ileri yollar horizon başına bir kez vektörize edilir.
  close=b.close.astype(float);future={}
  for hzn in H:
   fh=b.high.shift(-1)[::-1].rolling(hzn,min_periods=hzn).max()[::-1];fl=b.low.shift(-1)[::-1].rolling(hzn,min_periods=hzn).min()[::-1];future[hzn]=(close.shift(-hzn)/close-1,fh/close-1,fl/close-1)
  allowed=set(sum([*BASE.values(),*EXTRA.values()],[]))
  for e in x:
   if e not in allowed:continue
   pos=np.flatnonzero(x[e].fillna(False));sg=-1 if e in BEAR else 1
   for hzn in H:
    rr,mx,mn=future[hzn];z=pd.DataFrame({'i':pos,'ret':sg*rr.iloc[pos].to_numpy(),'mfe':(mx.iloc[pos] if sg==1 else -mn.iloc[pos]).to_numpy(),'mae':(mn.iloc[pos] if sg==1 else -mx.iloc[pos]).to_numpy()}).dropna();z['split']=sp[z.i.to_numpy(int)]
    for ss,g in z.groupby('split'):evt.append({'event':e,'group':group,'interval':interval,'time_split':ss,'horizon':hzn,'observations':len(g),'median_return':g.ret.median(),'median_mfe':g.mfe.median(),'median_mae':g.mae.median()})
  fam={n:x[e].fillna(False).any(axis=1).to_numpy() for n,e in FAM.items()}
  if group not in {'bist_equities','metals','energy'}:fam['volume']=np.zeros(len(b),dtype=bool)
  direction=np.where((x.ma_bull_stack|x.adx_trend_up|x.ichimoku_bull),1,np.where((x.ma_bear_stack|x.adx_trend_down|x.ichimoku_bear),-1,0));raw=b.close.shift(-60).div(b.close).sub(1).to_numpy()*direction;ex=np.full(len(b),np.nan)
  if group=='bist_equities' and interval in bench:
   z=bench[interval];br=(z.shift(-60)/z-1).reindex(pd.DatetimeIndex(ts)).to_numpy();ex=raw-direction*br
  stages=[];m=(f.path_efficiency>=.5).fillna(False).to_numpy()&(direction!=0);stages.append(('price_quality',m.copy()))
  for n in ('trend','momentum','volatility','volume','structure'):m=m&fam[n];stages.append((n,m.copy()))
  for n,m in stages:
   for ss in ('train','validation','test'):
    z=ex[m&(sp==ss)];chain.append({'asset_id':asset,'group':group,'interval':interval,'stage':n,'time_split':ss,'observations':int(np.isfinite(z).sum()),'median_excess':np.nanmedian(z) if np.isfinite(z).any() else np.nan})
  full=np.logical_and.reduce([fam[n] for n in FAM])&(direction!=0)
  for removed in ['none',*FAM]:
   m=full if removed=='none' else np.logical_and.reduce([fam[n] for n in FAM if n!=removed])&(direction!=0)
   z=ex[m];abl.append({'asset_id':asset,'group':group,'interval':interval,'removed_family':removed,'observations':int(np.isfinite(z).sum()),'median_excess':np.nanmedian(z) if np.isfinite(z).any() else np.nan})
  for a in FAM:
   for bb in FAM:corr.append({'group':group,'interval':interval,'family_a':a,'family_b':bb,'phi':np.corrcoef(fam[a].astype(float),fam[bb].astype(float))[0,1] if fam[a].std() and fam[bb].std() else np.nan})
 pd.DataFrame(par).to_csv(OUT/'parameter_study.csv',index=False);pd.DataFrame(evt).groupby(['event','group','interval','time_split','horizon']).agg(observations=('observations','sum'),median_return=('median_return','median'),median_mfe=('median_mfe','median'),median_mae=('median_mae','median')).reset_index().to_csv(OUT/'mfe_mae_common_calendar.csv',index=False)
 c=pd.DataFrame(chain).groupby(['group','interval','stage','time_split']).agg(observations=('observations','sum'),assets=('asset_id','nunique'),median_excess=('median_excess','median')).reset_index();order={'price_quality':0,'trend':1,'momentum':2,'volatility':3,'volume':4,'structure':5};c['_order']=c.stage.map(order);c=c.sort_values(['group','interval','time_split','_order']);c['marginal_excess']=c.groupby(['group','interval','time_split']).median_excess.diff();c.drop(columns='_order').to_csv(OUT/'decision_chain_excess.csv',index=False)
 pd.DataFrame(abl).groupby(['group','interval','removed_family']).agg(observations=('observations','sum'),assets=('asset_id','nunique'),median_excess=('median_excess','median')).reset_index().to_csv(OUT/'family_ablation.csv',index=False);pd.DataFrame(corr).groupby(['group','interval','family_a','family_b']).phi.median().reset_index().to_csv(OUT/'family_signal_correlation.csv',index=False)
 (OUT/'summary.json').write_text(json.dumps({'common_calendar_boundaries':[str(lo),str(hi)],'parameter_variants':len(pd.DataFrame(par).variant.unique()),'volume_gate_in_overlap':True,'status':'acceptance_supplement_generated'},indent=2)+'\n');print((OUT/'summary.json').read_text())
if __name__=='__main__':main()
