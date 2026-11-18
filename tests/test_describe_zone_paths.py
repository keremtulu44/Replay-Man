import pandas as pd
from tools.describe_zone_paths import summarize_visit


def events(*items):
    return pd.DataFrame([{'position':p,'event':e,'bar_ts':str(p)} for p,e in items])


def test_same_side_inside_and_revisit():
    e = events((5,'visit_start'),(5,'touch_bar'),(5,'both_boundaries_ambiguous'),
               (5,'close_below'), (6,'touch_bar'), (7,'close_below'), (8,'close_below'),(8,'visit_end'))
    x = summarize_visit({'position':5,'approach_side':'below'}, e, 12, 30)
    assert x['exit_class']=='same_side' and x['touch_bars']==2 and x['duration_bars']==4
    assert x['both_boundaries_ambiguous'] and x['outside_then_inside_close'] and x['revisit_within_10']=='yes'


def test_opposite_side_and_alternating_are_distinct():
    e = events((5,'visit_start'),(5,'touch_bar'),(6,'close_above'),(7,'close_above'),(7,'visit_end'))
    assert summarize_visit({'position':5,'approach_side':'below'},e,None,30)['exit_class']=='opposite_side'
    altered=events((5,'touch_bar'),(6,'close_below'),(7,'close_above'),(7,'visit_end'))
    assert summarize_visit({'position':5,'approach_side':'below'},altered,None,30)['exit_class']=='unknown'
    assert summarize_visit({'position':5,'approach_side':'unknown'},e,None,30)['exit_class']=='unknown'


def test_open_and_future_horizon_censoring():
    ongoing=events((5,'visit_start'),(5,'touch_bar'))
    x = summarize_visit({'position':5,'approach_side':'below'},ongoing,None,6)
    assert x['exit_class']=='censored' and x['revisit_within_10']=='unknown'
    ended=events((5,'touch_bar'),(6,'close_below'),(7,'close_below'),(7,'visit_end'))
    assert summarize_visit({'position':5,'approach_side':'below'},ended,None,14)['revisit_within_10']=='censored'
    assert summarize_visit({'position':5,'approach_side':'below'},ended,None,17)['revisit_within_10']=='no'
