"""Cilt 1 indikatör, formasyon, seans ve risk ölçümleri."""
import numpy as np
import pandas as pd

def indicators(bars,base):
 o=base.copy();c=bars.close.astype(float);h=bars.high.astype(float);l=bars.low.astype(float)
 d=c.diff();up=d.clip(lower=0).rolling(14,min_periods=14).mean();dn=(-d.clip(upper=0)).rolling(14,min_periods=14).mean();o['rsi14']=100-100/(1+up/dn.replace(0,np.nan))
 e12=c.ewm(span=12,adjust=False).mean();e26=c.ewm(span=26,adjust=False).mean();o['macd']=e12-e26;o['macd_signal']=o.macd.ewm(span=9,adjust=False).mean();o['macd_hist']=o.macd-o.macd_signal
 mid=c.rolling(20,min_periods=20).mean();sd=c.rolling(20,min_periods=20).std();o['bollinger_position']=(c-mid)/(2*sd.replace(0,np.nan));o['bollinger_width']=4*sd/mid.replace(0,np.nan)
 lo=l.rolling(14,min_periods=14).min();hi=h.rolling(14,min_periods=14).max();o['stochastic_k']=100*(c-lo)/(hi-lo).replace(0,np.nan)
 tr=o.true_range;plus=h.diff();minus=-l.diff();pdm=plus.where((plus>minus)&(plus>0),0);mdm=minus.where((minus>plus)&(minus>0),0);atr=tr.rolling(14,min_periods=14).mean();pdi=100*pdm.rolling(14,min_periods=14).mean()/atr;mdi=100*mdm.rolling(14,min_periods=14).mean()/atr;o['adx14']=(100*(pdi-mdi).abs()/(pdi+mdi).replace(0,np.nan)).rolling(14,min_periods=14).mean()
 return o

def formation_events(swings,bars,features,tolerance_atr=.5):
 s=swings[swings.level=='minor'].sort_values('pivot_position');rows=[]
 for kind,name,thesis in [('high','double_top','down'),('low','double_bottom','up')]:
  q=s[s.kind==kind].to_dict('records')
  for a,b in zip(q,q[1:]):
   known=int(b['confirmed_position']);atr=features.iloc[known].get('atr',np.nan);tol=(atr*tolerance_atr if pd.notna(atr) else 0)
   if abs(b['price']-a['price'])<=tol and b['pivot_position']-a['pivot_position']>=3:
    rows.append({'event':name,'direction':kind,'thesis_direction':thesis,'known_at_position':known,'event_ts':bars.iloc[known].ts_utc,'separation_bars':b['pivot_position']-a['pivot_position'],'price_difference_atr':abs(b['price']-a['price'])/atr if atr else np.nan})
 return pd.DataFrame(rows)

def risk_outcomes(events,bars,features,horizon=20,target_atr=1.0,stop_atr=1.0):
 out=events.copy();states=[]
 for e in events.to_dict('records'):
  p=int(e['known_at_position']);sign=1 if e['thesis_direction']=='up' else -1;entry=float(bars.iloc[p].close);atr=float(features.iloc[p].atr) if pd.notna(features.iloc[p].atr) else np.nan
  state='insufficient'
  if atr and p+horizon<len(bars):
   target=entry+sign*target_atr*atr;stop=entry-sign*stop_atr*atr;state='timeout'
   for i in range(p+1,p+horizon+1):
    hit_t=bars.iloc[i].high>=target if sign==1 else bars.iloc[i].low<=target;hit_s=bars.iloc[i].low<=stop if sign==1 else bars.iloc[i].high>=stop
    if hit_t and hit_s:state='ambiguous';break
    if hit_t:state='target';break
    if hit_s:state='stop';break
  states.append(state)
 out['risk_state_20']=states;return out

def session_features(ts):
 t=pd.to_datetime(ts,utc=True);return pd.DataFrame({'utc_hour':t.dt.hour,'weekday':t.dt.weekday,'session_bucket':pd.cut(t.dt.hour,[-1,7,11,15,19,23],labels=['overnight','morning','midday','afternoon','evening'])})
