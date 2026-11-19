import numpy as np
import pandas as pd
from tools.summarize_lifecycle import compare_groups, weighted_median_sorted


def test_weighted_median_matches_repeated_values():
    values=np.array([.1,.2,.3,.4]);week=np.array([0,1,0,1]);weights=np.array([2,1])
    assert weighted_median_sorted(values,week,weights)==np.median(np.repeat(values,weights[week]))
    assert np.isnan(weighted_median_sorted(values,week,np.array([0,0])))


def test_deterministic_bootstrap_and_different_group_assets():
    data=[]
    for w in range(6):
        for pattern,value in [('cross_then_same',.01),('same_then_same',-.01)]:
            data.append({'kind':'dwell','interval':'1d','split':'test','end_side':'above','pattern':pattern,
                         'excess_5':value,'asset_id':'A', 'end_bar_ts':pd.Timestamp('2026-01-01',tz='UTC')+pd.Timedelta(weeks=w)})
    a=compare_groups(pd.DataFrame(data),draws=20,seed=42)
    pd.testing.assert_frame_equal(a,compare_groups(pd.DataFrame(data),draws=20,seed=42))
    assert a.iloc[0].median_difference == .02 and a.iloc[0].bootstrap_low == .02
    assert a.iloc[0].asset_both_3plus==1 and a.iloc[0].asset_cross_higher==1
