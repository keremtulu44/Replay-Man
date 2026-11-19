import numpy as np
import pandas as pd
from tools.analyze_lifecycle_ten_filters import extract_features, FILTERS


def make_bars():
    c=np.arange(30,dtype=float)+100
    return pd.DataFrame({'ts_utc':pd.date_range('2026-01-01',periods=30,freq='D',tz='UTC'),
                         'close':c,'high':c+1,'low':c-1})


def make_event(b):
    return pd.DataFrame([{'start_position':20,'end_position':24,'end_bar_ts':str(b.ts_utc.iloc[24]),
                          'start_side':'below','end_side':'below','prior_end_position':9,
                          'lower_at_start':115.,'upper_at_start':117.,'touch_bars':3,
                          'ambiguous_bars':1,'visit_number':4}])


def test_ten_filters_boundaries_and_causality():
    bars=make_bars();e=make_event(bars);f=extract_features(bars,e)
    assert list(f.columns)==list(FILTERS)
    assert f.loc[0,'F01']=='yes' and f.loc[0,'F02']=='yes' and f.loc[0,'F03']=='yes'
    assert f.loc[0,'F09']=='yes' and f.loc[0,'F10']=='yes'
    changed=bars.copy();changed.loc[25:,['low','high','close']]=[1.,2000.,1000.]
    pd.testing.assert_frame_equal(f,extract_features(changed,e))
    pd.testing.assert_frame_equal(f,extract_features(bars.iloc[:25],e))


def test_missing_gap_and_no_movement_are_unknown():
    bars=make_bars();bars['close']=100.;bars['high']=101.;bars['low']=99.
    e=make_event(bars);e.loc[0,'prior_end_position']=np.nan
    f=extract_features(bars,e)
    assert f.loc[0,'F01']=='unknown' and f.loc[0,'F06']=='unknown'
