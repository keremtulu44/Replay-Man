"""Cilt 1 P2-P6: MA, momentum, volatilite, hacim/VWAP ve profil ölçümleri."""
from __future__ import annotations
from pathlib import Path
import json, numpy as np, pandas as pd
from replayman.replay import load_bars,causal_features
from replayman.swings import confirmed_swings,SwingConfig
DATA=Path('data/ohlcv');ROOT=Path('research/measurements');H=(5,20,40,60)
PACKS={
'cilt1-moving-averages':['sma_cross_up','sma_cross_down','ema_cross_up','ema_cross_down','price_above_sma200','price_below_sma200','ma_bull_stack','ma_bear_stack'],
'cilt1-momentum':['rsi_cross_30_up','rsi_cross_70_down','rsi_above_70','rsi_below_30','stoch_cross_up_20','stoch_cross_down_80','macd_signal_up','macd_signal_down','macd_zero_up','macd_zero_down'],
'cilt1-volatility':['bb_break_up','bb_break_down','bb_reentry_up','bb_reentry_down','bb_squeeze','bb_expansion','keltner_squeeze','atr_expansion','atr_contraction'],
'cilt1-volume-vwap':['rvol_high_up','rvol_high_down','vwap_cross_up','vwap_cross_down','avwap_cross_up','avwap_cross_down','low_volume_progress_loss'],
'cilt1-volume-profile':['poc_cross_up','poc_cross_down','value_area_accept','value_area_reject_up','value_area_reject_down'],}

def paths():return sorted(DATA.glob('*/*/*/bars/*.csv'))
def rate(x):x=x.dropna();return float((x>0).mean()) if len(x) else np.nan
def cross_up(a,b):return (a>b)&(a.shift(1)<=b.shift(1))
def cross_down(a,b):return (a<b)&(a.shift(1)>=b.shift(1))
def profile(tp,v,w=60,bins=20):
 n=len(tp);poc=np.full(n,np.nan);lo=np.full(n,np.nan);hi=np.full(n,np.nan)
 for i in range(w-1,n):
  x=tp[i-w+1:i+1];vv=v[i-w+1:i+1];mn=np.nanmin(x);mx=np.nanmax(x)
  if not np.isfinite(mn+mx) or mx<=mn or np.nansum(vv)<=0:continue
  edges=np.linspace(mn,mx,bins+1);idx=np.clip(np.searchsorted(edges,x,side='right')-1,0,bins-1);vol=np.bincount(idx,weights=np.nan_to_num(vv),minlength=bins);cent=(edges[:-1]+edges[1:])/2;j=int(vol.argmax());poc[i]=cent[j]
  order=np.argsort(np.abs(np.arange(bins)-j));cum=0;chosen=[];target=.7*vol.sum()
  for z in order:chosen.append(z);cum+=vol[z];
  # En yakın POC-merkezli binleri hedefe ulaşana dek seç.
  cum=0;chosen=[]
  for z in order:
   chosen.append(z);cum+=vol[z]
   if cum>=target:break
  lo[i]=edges[min(chosen)];hi[i]=edges[max(chosen)+1]
 return pd.DataFrame({'poc':poc,'va_low':lo,'va_high':hi})
def indicators(b,f):
 c=b.close.astype(float);h=b.high.astype(float);l=b.low.astype(float);v=b.volume.astype(float);tp=(h+l+c)/3
 x=pd.DataFrame(index=b.index);sma={n:c.rolling(n,min_periods=n).mean() for n in (20,50,100,200)};ema={n:c.ewm(span=n,adjust=False,min_periods=n).mean() for n in (12,20,26,50)}
 x['sma_cross_up']=cross_up(sma[20],sma[50]);x['sma_cross_down']=cross_down(sma[20],sma[50]);x['ema_cross_up']=cross_up(ema[20],ema[50]);x['ema_cross_down']=cross_down(ema[20],ema[50]);x['price_above_sma200']=c>sma[200];x['price_below_sma200']=c<sma[200];x['ma_bull_stack']=(sma[20]>sma[50])&(sma[50]>sma[100])&(sma[100]>sma[200]);x['ma_bear_stack']=(sma[20]<sma[50])&(sma[50]<sma[100])&(sma[100]<sma[200])
 d=c.diff();gain=d.clip(lower=0).ewm(alpha=1/14,adjust=False,min_periods=14).mean();loss=(-d.clip(upper=0)).ewm(alpha=1/14,adjust=False,min_periods=14).mean();rsi=100-100/(1+gain/loss.replace(0,np.nan));ll=l.rolling(14,min_periods=14).min();hh=h.rolling(14,min_periods=14).max();k=100*(c-ll)/(hh-ll).replace(0,np.nan);sd=k.rolling(3,min_periods=3).mean();macd=ema[12]-ema[26];sig=macd.ewm(span=9,adjust=False,min_periods=9).mean()
 x['rsi_cross_30_up']=cross_up(rsi,pd.Series(30,index=c.index));x['rsi_cross_70_down']=cross_down(rsi,pd.Series(70,index=c.index));x['rsi_above_70']=rsi>70;x['rsi_below_30']=rsi<30;x['stoch_cross_up_20']=cross_up(k,sd)&(k<30);x['stoch_cross_down_80']=cross_down(k,sd)&(k>70);x['macd_signal_up']=cross_up(macd,sig);x['macd_signal_down']=cross_down(macd,sig);x['macd_zero_up']=cross_up(macd,pd.Series(0,index=c.index));x['macd_zero_down']=cross_down(macd,pd.Series(0,index=c.index))
 mid=sma[20];std=c.rolling(20,min_periods=20).std();up=mid+2*std;dn=mid-2*std;width=(up-dn)/mid;ku=ema[20]+1.5*f.atr;kd=ema[20]-1.5*f.atr;atr_rel=f.atr/f.atr.rolling(50,min_periods=50).median()
 x['bb_break_up']=cross_up(c,up);x['bb_break_down']=cross_down(c,dn);x['bb_reentry_up']=cross_up(c,dn);x['bb_reentry_down']=cross_down(c,up);x['bb_squeeze']=width<width.rolling(100,min_periods=50).quantile(.2);x['bb_expansion']=width>width.rolling(100,min_periods=50).quantile(.8);x['keltner_squeeze']=(up-dn)<(ku-kd);x['atr_expansion']=atr_rel>1.5;x['atr_contraction']=atr_rel<.7
 rv=v/v.shift(1).rolling(20,min_periods=20).median();vw=(tp*v).rolling(20,min_periods=20).sum()/v.rolling(20,min_periods=20).sum().replace(0,np.nan);x['rvol_high_up']=(rv>=1.5)&(c>b.open);x['rvol_high_down']=(rv>=1.5)&(c<b.open);x['vwap_cross_up']=cross_up(c,vw);x['vwap_cross_down']=cross_down(c,vw);x['low_volume_progress_loss']=(rv<.7)&(f.progress_decay_ratio<.8)
 av=np.full(len(b),np.nan);sw=confirmed_swings(b,f,config=SwingConfig(2,2));anchors=dict(zip(sw.confirmed_position.astype(int),sw.pivot_position.astype(int)));anchor=None
 pv=(tp*v).to_numpy();vv=v.to_numpy()
 for i in range(len(b)):
  if i in anchors:anchor=anchors[i]
  if anchor is not None and np.nansum(vv[anchor:i+1])>0:av[i]=np.nansum(pv[anchor:i+1])/np.nansum(vv[anchor:i+1])
 av=pd.Series(av,index=c.index);x['avwap_cross_up']=cross_up(c,av);x['avwap_cross_down']=cross_down(c,av)
 pr=profile(tp.to_numpy(),v.to_numpy());poc=pr.poc;vl=pr.va_low;vh=pr.va_high;x['poc_cross_up']=cross_up(c,poc);x['poc_cross_down']=cross_down(c,poc);x['value_area_accept']=c.between(vl,vh)&c.shift(1).between(vl.shift(1),vh.shift(1));x['value_area_reject_up']=(l<vl)&(c>vl);x['value_area_reject_down']=(h>vh)&(c<vh)
 return x

def main():
 rows=[];inventory={k:0 for k in PACKS};bench={}
 for p in DATA.glob('bist_indices/IDX_XU100/*/bars/*.csv'):
  b=load_bars(p);bench[p.stem]=b.set_index('ts_utc').close
 for p in paths():
  b=load_bars(p);f=causal_features(b);x=indicators(b,f);pct=np.arange(len(b))/max(len(b),1);split=np.where(pct<.6,'train',np.where(pct<.8,'validation','test'))
  for pack,events in PACKS.items():
   out=[]
   if pack in {'cilt1-volume-vwap','cilt1-volume-profile'} and p.parts[-5] not in {'bist_equities','metals','energy'}:
    continue
   for event in events:
    pos=np.flatnonzero(x[event].fillna(False).to_numpy());inventory[pack]+=len(pos)
    if not len(pos):continue
    bearish={'sma_cross_down','ema_cross_down','price_below_sma200','ma_bear_stack','rsi_cross_70_down','rsi_above_70','stoch_cross_down_80','macd_signal_down','macd_zero_down','bb_break_down','bb_reentry_down','rvol_high_down','vwap_cross_down','avwap_cross_down','poc_cross_down','value_area_reject_down'}
    direction=np.full(len(pos),-1 if event in bearish else 1);d=pd.DataFrame({'group':p.parts[-5],'asset_id':p.parts[-4],'interval':p.stem,'event':event,'event_ts':b.ts_utc.iloc[pos].to_numpy(),'time_split':split[pos],'direction':direction})
    for hzn in H:
     raw=b.close.shift(-hzn).div(b.close).sub(1).iloc[pos].to_numpy()*direction;d[f'return_{hzn}']=raw
     if p.parts[-5]=='bist_equities' and p.stem in bench:
      q=bench[p.stem];br=(q.shift(-hzn)/q-1).reindex(pd.DatetimeIndex(b.ts_utc.iloc[pos])).to_numpy();d[f'excess_{hzn}']=raw-direction*br
     else:d[f'excess_{hzn}']=np.nan
    out.append(d)
   if out:rows.append((pack,pd.concat(out,ignore_index=True)))
 for pack in PACKS:
  d=pd.concat([z for k,z in rows if k==pack],ignore_index=True);out=ROOT/pack;out.mkdir(parents=True,exist_ok=True)
  keys=['group','interval','time_split','event','direction'];spec={'observations':('asset_id','size'),'assets':('asset_id','nunique')}
  for h in H:spec.update({f'ready_{h}':(f'return_{h}','count'),f'median_return_{h}':(f'return_{h}','median'),f'positive_{h}':(f'return_{h}',rate),f'median_excess_{h}':(f'excess_{h}','median')})
  d.groupby(keys,dropna=False).agg(**spec).reset_index().to_csv(out/'event_study.csv',index=False);d.groupby(['interval','event','asset_id']).agg(observations=('asset_id','size'),median_return_60=('return_60','median'),median_excess_60=('excess_60','median')).reset_index().to_csv(out/'symbol_results.csv',index=False);(out/'summary.json').write_text(json.dumps({'events':inventory[pack],'assets':int(d.asset_id.nunique()),'event_types':PACKS[pack],'raw_events_not_versioned':'Deterministic generator plus complete aggregates retained to avoid oversized Git artifacts.'},indent=2)+'\n')
 print(json.dumps(inventory,indent=2))
if __name__=='__main__':main()
