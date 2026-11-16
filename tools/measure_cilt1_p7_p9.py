"""Cilt 1 P7-P9: trend sistemleri, seviye araçları ve nedensel çizim geometrisi."""
from pathlib import Path
import json,numpy as np,pandas as pd
from replayman.replay import load_bars,causal_features
from replayman.swings import confirmed_swings,SwingConfig
DATA=Path('data/ohlcv');ROOT=Path('research/measurements');H=(5,20,40,60)
PACKS={'cilt1-trend-systems':['adx_trend_up','adx_trend_down','supertrend_flip_up','supertrend_flip_down','ichimoku_bull','ichimoku_bear','tenkan_kijun_up','tenkan_kijun_down'],'cilt1-level-tools':['daily_pivot_break_up','daily_pivot_break_down','confirmed_resistance_break','confirmed_support_break','fib_382_hold','fib_618_hold'],'cilt1-drawing-tools':['regression_upper_break','regression_lower_break','pitchfork_median_cross_up','pitchfork_median_cross_down','gann_normalized_up','gann_normalized_down']}
def paths():return sorted(DATA.glob('*/*/*/bars/*.csv'))
def cross_up(a,b):return (a>b)&(a.shift(1)<=b.shift(1))
def cross_down(a,b):return (a<b)&(a.shift(1)>=b.shift(1))
def rate(x):x=x.dropna();return float((x>0).mean()) if len(x) else np.nan
def features(b,f):
 c,h,l=b.close.astype(float),b.high.astype(float),b.low.astype(float);x=pd.DataFrame(index=b.index);up=h.diff();dn=-l.diff();pdm=up.where((up>dn)&(up>0),0);mdm=dn.where((dn>up)&(dn>0),0);atr=f.atr;plus=100*pdm.rolling(14).mean()/atr;minus=100*mdm.rolling(14).mean()/atr;dx=100*(plus-minus).abs()/(plus+minus).replace(0,np.nan);adx=dx.rolling(14).mean();x['adx_trend_up']=(adx>25)&(plus>minus)&(adx>adx.shift(1));x['adx_trend_down']=(adx>25)&(minus>plus)&(adx>adx.shift(1))
 mid=(h+l)/2;basic_u=mid+3*atr;basic_l=mid-3*atr;fu=basic_u.copy();fl=basic_l.copy();trend=np.ones(len(b),dtype=int)
 for i in range(1,len(b)):
  if pd.isna(basic_u.iloc[i]):continue
  if pd.isna(fu.iloc[i-1]):
   fu.iloc[i]=basic_u.iloc[i];fl.iloc[i]=basic_l.iloc[i];trend[i]=trend[i-1];continue
  fu.iloc[i]=basic_u.iloc[i] if basic_u.iloc[i]<fu.iloc[i-1] or c.iloc[i-1]>fu.iloc[i-1] else fu.iloc[i-1];fl.iloc[i]=basic_l.iloc[i] if basic_l.iloc[i]>fl.iloc[i-1] or c.iloc[i-1]<fl.iloc[i-1] else fl.iloc[i-1];trend[i]=(-1 if c.iloc[i]<fl.iloc[i-1] else 1) if trend[i-1]==1 else (1 if c.iloc[i]>fu.iloc[i-1] else -1)
 t=pd.Series(trend,index=b.index);x['supertrend_flip_up']=(t==1)&(t.shift(1)==-1);x['supertrend_flip_down']=(t==-1)&(t.shift(1)==1)
 ten=(h.rolling(9).max()+l.rolling(9).min())/2;kij=(h.rolling(26).max()+l.rolling(26).min())/2;sa=(ten+kij)/2;sb=(h.rolling(52).max()+l.rolling(52).min())/2;x['ichimoku_bull']=(c>sa)&(c>sb)&(ten>kij);x['ichimoku_bear']=(c<sa)&(c<sb)&(ten<kij);x['tenkan_kijun_up']=cross_up(ten,kij);x['tenkan_kijun_down']=cross_down(ten,kij)
 # Önceki tamamlanmış UTC gününden klasik pivot; intraday aynı gün verisi kullanılmaz.
 day=b.ts_utc.dt.floor('D');daily=pd.DataFrame({'day':day,'h':h,'l':l,'c':c}).groupby('day').agg(h=('h','max'),l=('l','min'),c=('c','last')).shift(1);pivot=day.map(((daily.h+daily.l+daily.c)/3).to_dict());x['daily_pivot_break_up']=cross_up(c,pivot);x['daily_pivot_break_down']=cross_down(c,pivot)
 sw=confirmed_swings(b,f,config=SwingConfig(2,2));res=np.full(len(b),np.nan);sup=np.full(len(b),np.nan);last_h=last_l=np.nan;known={}
 for r in sw.itertuples():known.setdefault(int(r.confirmed_position),[]).append(r)
 triples=[]
 for i in range(len(b)):
  for r in known.get(i,[]):
   if r.kind=='high':last_h=r.price
   else:last_l=r.price
   triples.append((r.kind,r.price,r.pivot_position))
  res[i]=last_h;sup[i]=last_l
 res=pd.Series(res);sup=pd.Series(sup);x['confirmed_resistance_break']=cross_up(c,res);x['confirmed_support_break']=cross_down(c,sup)
 rng=(res-sup).abs();fib382=np.minimum(res,sup)+.382*rng;fib618=np.minimum(res,sup)+.618*rng;x['fib_382_hold']=(l<=fib382)&(c>fib382);x['fib_618_hold']=(l<=fib618)&(c>fib618)
 # Geçmiş 50 bar OLS kanalı; t anındaki kanal t dahil geçmişten hesaplanır.
 n=50;reg=np.full(len(b),np.nan);sd=np.full(len(b),np.nan);tt=np.arange(n)
 for i in range(n-1,len(b)):
  y=c.iloc[i-n+1:i+1].to_numpy();coef=np.polyfit(tt,y,1);fit=coef[0]*tt+coef[1];reg[i]=fit[-1];sd[i]=np.std(y-fit)
 reg=pd.Series(reg);sd=pd.Series(sd);x['regression_upper_break']=cross_up(c,reg+2*sd);x['regression_lower_break']=cross_down(c,reg-2*sd)
 # Son üç teyitli alternating pivotun A-C orta çizgisi, yalnız C teyidinden sonra ileri uzatılır.
 med=np.full(len(b),np.nan);last3=[]
 for i in range(len(b)):
  for r in known.get(i,[]):
   if not last3 or last3[-1][0]!=r.kind:last3.append((r.kind,float(r.price),int(r.pivot_position)))
   else:last3[-1]=(r.kind,float(r.price),int(r.pivot_position))
   last3=last3[-3:]
  if len(last3)==3:
   _,pa,ia=last3[0];_,pc,ic=last3[2];med[i]=pa+(pc-pa)*(i-ia)/max(ic-ia,1)
 med=pd.Series(med);x['pitchfork_median_cross_up']=cross_up(c,med);x['pitchfork_median_cross_down']=cross_down(c,med)
 norm_slope=(c-c.shift(20))/(20*atr);x['gann_normalized_up']=norm_slope>=1;x['gann_normalized_down']=norm_slope<=-1
 return x

def main():
 bench={}
 for p in DATA.glob('bist_indices/IDX_XU100/*/bars/*.csv'):
  b=load_bars(p);bench[p.stem]=b.set_index('ts_utc').close
 parts={k:[] for k in PACKS};counts={k:0 for k in PACKS};bear={e for e in sum(PACKS.values(),[]) if any(z in e for z in ['down','bear','support_break','lower_break'])}
 for p in paths():
  b=load_bars(p);f=causal_features(b);x=features(b,f);split=np.where(np.arange(len(b))/max(len(b),1)<.6,'train',np.where(np.arange(len(b))/max(len(b),1)<.8,'validation','test'))
  for pack,events in PACKS.items():
   for event in events:
    pos=np.flatnonzero(x[event].fillna(False));counts[pack]+=len(pos)
    if not len(pos):continue
    sg=-1 if event in bear else 1;d=pd.DataFrame({'group':p.parts[-5],'asset_id':p.parts[-4],'interval':p.stem,'event':event,'event_ts':b.ts_utc.iloc[pos].to_numpy(),'time_split':split[pos],'direction':sg})
    for hzn in H:
     raw=b.close.shift(-hzn).div(b.close).sub(1).iloc[pos].to_numpy()*sg;d[f'return_{hzn}']=raw
     if p.parts[-5]=='bist_equities' and p.stem in bench:q=bench[p.stem];br=(q.shift(-hzn)/q-1).reindex(pd.DatetimeIndex(b.ts_utc.iloc[pos])).to_numpy();d[f'excess_{hzn}']=raw-sg*br
     else:d[f'excess_{hzn}']=np.nan
    parts[pack].append(d)
 for pack,pp in parts.items():
  d=pd.concat(pp,ignore_index=True);out=ROOT/pack;out.mkdir(parents=True,exist_ok=True);spec={'observations':('asset_id','size'),'assets':('asset_id','nunique')}
  for h in H:spec.update({f'ready_{h}':(f'return_{h}','count'),f'median_return_{h}':(f'return_{h}','median'),f'positive_{h}':(f'return_{h}',rate),f'median_excess_{h}':(f'excess_{h}','median')})
  d.groupby(['group','interval','time_split','event','direction'],dropna=False).agg(**spec).reset_index().to_csv(out/'event_study.csv',index=False);d.groupby(['interval','event','asset_id']).agg(observations=('asset_id','size'),median_return_60=('return_60','median'),median_excess_60=('excess_60','median')).reset_index().to_csv(out/'symbol_results.csv',index=False);(out/'summary.json').write_text(json.dumps({'events':counts[pack],'assets':int(d.asset_id.nunique()),'events_by_type':PACKS[pack]},indent=2)+'\n')
 print(json.dumps(counts,indent=2))
if __name__=='__main__':main()
