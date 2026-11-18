import pandas as pd
from replayman.zone_lifecycle import track_zone
from tools.measure_zone_lifecycle import evaluate_bars


def bars(rows):
    return pd.DataFrame([{'ts_utc':pd.Timestamp('2026-01-01', tz='UTC') + pd.Timedelta(days=i),
                          'low':lo,'high':hi,'close':cl} for i,(lo,hi,cl) in enumerate(rows)])


def z(slope=0):
    return {'zone_id':'z','position':0,'lower':9.,'upper':11.,'slope_per_bar':slope}


def test_cross_then_retest_is_only_known_at_second_close():
    data=bars([(10,10,10), (12,13,12), (10,12,10), (8,9.5,8), (8,9.5,8),
               (8,10,8), (8,9.5,8)])
    result=track_zone(data,z())
    assert len(result)==2
    assert (result[0]['path'],result[0]['scenario'],result[0]['end_position'])==('cross','down_candidate',4)
    assert (result[1]['path'],result[1]['scenario'],result[1]['end_position'])==('same','down_retest',6)
    partial=track_zone(data.iloc[:6],z())
    assert partial[0]==result[0] and partial[1]['status']=='censored' and partial[1]['scenario']=='unknown'
    changed=data.copy()
    changed.loc[5:, ['low','high','close']] = [1, 2, 2]
    assert track_zone(changed,z())[0] == result[0]


def test_alternating_outside_closes_do_not_complete():
    data=bars([(10,10,10),(12,12,12),(8,12,8),(12,12,12),(12,12,12)])
    x=track_zone(data,z())
    assert len(x)==1 and x[0]['end_position']==4 and x[0]['path']=='same'
    assert x[0]['ambiguous_bars']==1


def test_mixed_when_cross_immediately_reversed():
    data=bars([(10,10,10),(12,12,12),(9,10,9),(8,9,8),(8,9,8),
               (8,10,9),(11,12,12),(11,12,12)])
    x=track_zone(data,z())
    assert [a['scenario'] for a in x]==['down_candidate','mixed']


def test_evolving_band_and_side_at_previous_bar():
    data=bars([(10,10,10),(12,12,12),(11,12,11),(10,10,10),(10,10,10)])
    x=track_zone(data,z(.5))
    assert x[0]['start_side']=='above' and x[0]['lower_at_start']==10
    assert x[0]['path']=='cross'


def test_forward_outcomes_no_split_leak_and_missing_benchmark():
    data=bars([(10,10,10)]*25)
    times=data.ts_utc
    rec=pd.DataFrame([{'zone_id':'z','visit_number':1,'status':'completed','end_position':10,
                       'end_bar_ts':str(times.iloc[10]),'start_side':'below','end_side':'above',
                       'path':'cross','scenario':'up_candidate','prior_path':None,'prior_end_side':None}])
    cut1=times.iloc[17];cut2=times.iloc[20];end=times.iloc[-1]+pd.Timedelta(days=1)
    benchmark={x:100 for x in times}
    out=evaluate_bars(rec,data,benchmark,cut1,cut2,end)
    assert out.iloc[0].split=='train' and out.iloc[0].excess_5==0
    assert pd.isna(out.iloc[0].excess_10)
    del benchmark[times.iloc[15]]
    out=evaluate_bars(rec,data,benchmark,cut1,cut2,end)
    assert pd.isna(out.iloc[0].excess_5) and out.iloc[0].directional_5==0
