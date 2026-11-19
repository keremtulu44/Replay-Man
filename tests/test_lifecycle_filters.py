import pandas as pd
from tools.analyze_lifecycle_filters import label_filters, analyze


def test_filter_boundaries_and_unknown():
    f=pd.DataFrame({'start_position':[11,12,3,4], 'prior_end_position':[1,1,None,4], 'touch_bars':[2,3,1,0]})
    x=label_filters(f)
    assert x.gap_group.tolist()==['within_10','after_10','unknown','unknown']
    assert x.touch_group.tolist()==['1to2','3plus','1to2','unknown']


def test_filters_computed_only_on_visit_end_and_compared_with_same_filter():
    rows=[]
    for i in range(6):
        for pattern, y, touch in [('cross_then_same',.01,3),('same_then_same',-.01,3),('same_then_same',.5,1)]:
            rows.append({'kind':'dwell','interval':'1d','split':'test','end_side':'above','pattern':pattern,
                         'excess_5':y,'directional_5':y,'excess_10':y,'asset_id':'A',
                         'end_bar_ts':pd.Timestamp('2026-01-01',tz='UTC')+pd.Timedelta(weeks=i),
                         'start_position':10,'prior_end_position':8,'touch_bars':touch})
    groups, comp=analyze(pd.DataFrame(rows),draws=20)
    result=comp[(comp['filter']=='touch_group')&(comp.filter_value=='3plus')].iloc[0]
    assert result.median_difference==.02 and result.n_cross_then_same==6 and result.n_same_then_same==6
    counts=groups[(groups['filter']=='touch_group')&(groups.filter_value=='3plus')]
    assert counts.events.sum()==12
