import numpy as np
import pandas as pd
from tools.investigate_f01_reasons import categorize, candidate_features, pair_decomposition, distance_bins, bin_contrast


def test_visit_time_categories_and_censoring():
    assert categorize(10,15,True)=='early_1_5'
    assert categorize(10,16,True)=='return_6_10'
    assert categorize(10,20,True)=='return_6_10'
    assert categorize(10,21,True)=='return_11_20'
    assert categorize(10,30,True)=='return_11_20'
    assert categorize(10,31,True)=='no_20'
    assert categorize(10,None,False)=='censored'


def test_landmark_uses_only_five_bars_and_excludes_early_and_censored():
    c=120.-np.arange(50)*.5
    bars=pd.DataFrame({'ts_utc':pd.date_range('2026-01-01',periods=50,freq='D',tz='UTC'),
                       'close':c,'high':c+1,'low':c-1})
    v={'end_position':20,'start_position':18,'end_bar_ts':str(bars.ts_utc.iloc[20]),
       'end_side':'below','upper_at_start':112.,'lower_at_start':111.,'touch_bars':2,
       'visit_number':3,'ambiguous_bars':0}
    cutoff=bars.ts_utc.iloc[-1]+pd.Timedelta(days=1)
    x=candidate_features(bars,v,27,True,cutoff)
    assert x['eligible_landmark'] and x['bucket']=='return_6_10'
    changed=bars.copy();changed.loc[26:,['high','low','close']]=[1000.,1.,500.]
    assert x==candidate_features(changed,v,27,True,cutoff)
    assert not candidate_features(bars,v,25,True,cutoff)['eligible_landmark']
    assert not candidate_features(bars,v,None,False,cutoff)['eligible_landmark']


def test_pair_mean_decomposition_is_additive():
    pairs=pd.DataFrame([{'split':'test','asset_id':'A','case_directional_5':.1,'control_directional_5':.02,
                        'case_excess_5':.05,'control_excess_5':.01,'case_end_position':20,'control_end_position':30}])
    x=pair_decomposition(pairs).iloc[0]
    assert np.isclose(x.mean_raw_delta-x.mean_market_delta,x.mean_excess_delta)
    assert np.isclose(x.mean_excess_delta,.04) and x.later_controls==1


def test_distance_bins_are_conditional_on_landmark():
    data=pd.DataFrame([{'eligible_landmark':True,'distance_after5_atr':.5,'bucket':'return_11_20','split':'test','scenario':'down_candidate','asset_id':'A'},
                       {'eligible_landmark':True,'distance_after5_atr':.8,'bucket':'no_20','split':'test','scenario':'down_candidate','asset_id':'B'},
                       {'eligible_landmark':False,'distance_after5_atr':None,'bucket':'early_1_5','split':'test','scenario':'down_candidate','asset_id':'C'}])
    x=distance_bins(data).iloc[0]
    assert x['n']==2 and x.returns_6_20==1 and x.fraction_return_6_20==.5


def test_week_and_asset_bin_contrast_are_deterministic():
    rows=[]
    for w in range(6):
        for dist,bucket in [(.5,'return_6_10'),(3.,'no_20')]:
            rows.append({'eligible_landmark':True,'distance_after5_atr':dist,'bucket':bucket,
                         'split':'test','scenario':'down_candidate','asset_id':f'A{w}',
                         'candidate_bar_ts':pd.Timestamp('2026-01-01',tz='UTC')+pd.Timedelta(weeks=w)})
    data=pd.DataFrame(rows);x=bin_contrast(data,draws=20,seed=3)
    pd.testing.assert_frame_equal(x,bin_contrast(data,draws=20,seed=3))
    assert x.iloc[0]['difference']==1 and x.iloc[0].week_low==1 and x.iloc[0].asset_low==1
