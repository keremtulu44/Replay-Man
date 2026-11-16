import pandas as pd
from replayman.book_features import candle_and_regime_features,pullback_events
from replayman.replay import causal_features

def bars(n=80):
 c=[100+i*.2+(i%4) for i in range(n)];return pd.DataFrame({'ts_utc':pd.date_range('2026-01-01',periods=n,freq='h',tz='UTC'),'open':[x-.3 for x in c],'high':[x+1 for x in c],'low':[x-1 for x in c],'close':c,'volume':100})
def leg(d,s,e,a,b,k):
 dist=abs(b-a);return {'direction':d,'start_position':s,'end_position':e,'known_at_position':k,'distance':dist,'duration_bars':e-s,'speed_per_bar':dist/(e-s),'path_efficiency':.8}
def test_pullback_uses_confirmation_time_and_ratios():
 b=bars();f=causal_features(b);legs=pd.DataFrame([leg('up',1,5,100,110,7),leg('down',5,8,110,106,10)])
 e=pullback_events(legs,b,f).iloc[0];assert e.known_at_position==10;assert e.depth_ratio==.4;assert e.thesis_direction=='up'
def test_candle_and_regime_are_causal():
 b=bars();changed=b.copy();changed.loc[60:,'close']*=3
 a=candle_and_regime_features(b,causal_features(b)).iloc[:60];z=candle_and_regime_features(changed,causal_features(changed)).iloc[:60]
 pd.testing.assert_frame_equal(a,z)
def test_engulfing_definition():
 b=bars();b.loc[10,['open','close','high','low']]=[105,100,106,99];b.loc[11,['open','close','high','low']]=[99,106,107,98]
 f=candle_and_regime_features(b,causal_features(b));assert f.loc[11,'bullish_engulfing']==1
