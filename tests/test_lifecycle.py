import pandas as pd
from replayman.lifecycle import enrich_lifecycle

def test_lifecycle_counts_attempts_and_failure_details():
 b=pd.DataFrame({'open':[9]*8,'high':[9.5,10.5,9.5,11,12,10,8,7],'low':[8.5,8.8,8.5,9,10,8,7,6],'close':[9,9.5,9,10.8,11,8.8,7.5,7],'volume':100,'ts_utc':pd.date_range('2026-01-01',periods=8,freq='h',tz='UTC')})
 f=pd.DataFrame({'atr':[1.0]*8})
 common={'level':'minor','direction':'up','level_price':10.0,'source_pivot_position':0,'source_confirmed_position':0,'level_age_bars':1,'distance_close_atr':0}
 e=pd.DataFrame([{**common,'event':'probe_rejection','event_position':1,'event_ts':b.ts_utc.iloc[1],'bars_since_break':None},{**common,'event':'close_break','event_position':3,'event_ts':b.ts_utc.iloc[3],'bars_since_break':0},{**common,'event':'retest_hold','event_position':4,'event_ts':b.ts_utc.iloc[4],'bars_since_break':1},{**common,'event':'failure','event_position':5,'event_ts':b.ts_utc.iloc[5],'bars_since_break':2}])
 r=enrich_lifecycle(e,b,f);assert list(r.attempt_number)==[1,2,2,2]
 failure=r[r.event=='failure'].iloc[0];assert failure.old_area_depth_atr>1;assert failure.counter_expansion_position==6
 assert r[r.event=='retest_hold'].iloc[0].outside_duration==1
