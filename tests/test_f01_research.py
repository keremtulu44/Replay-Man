import numpy as np
import pandas as pd
from tools.evaluate_f01_matching import match_events, summarize_pairs
from tools.measure_f01_censoring import classify_window


def sample_event(kind,pos,z):
    t=pd.Timestamp('2026-01-01',tz='UTC')+pd.Timedelta(hours=pos*4)
    return {'asset_id':'A','interval':'4h','end_side':'below','pattern':kind,'split':'test',
            'zone_id':z,'visit_number':2,'start_position':pos-2,'prior_end_position':pos-13,'end_position':pos,
            'start_bar_ts':str(t-pd.Timedelta(hours=8)),'end_bar_ts':str(t),
            'volatility_pre':.02,'width_atr_pre':.7,'excess_5':.1,'directional_5':.2,
            'excess_10':.3,'directional_10':.4}


def test_matching_excludes_overlapping_outcomes_and_does_not_use_future():
    f=pd.DataFrame([sample_event('cross_then_same',50,'A'),sample_event('cross_then_same',75,'B'),
                    sample_event('cross_then_same',106,'C'),sample_event('same_then_same',55,'D'),
                    sample_event('same_then_same',57,'E'),sample_event('same_then_same',82,'F')])
    p,miss=match_events(f)
    assert len(p)==2 and len(miss)==1
    assert p.bar_distance.tolist()==[7,7] and p.control_id.nunique()==2
    altered=f.copy();altered[['excess_5','directional_5','excess_10','directional_10']]=np.nan
    q,miss2=match_events(altered)
    assert p[['case_id','control_id']].equals(q[['case_id','control_id']])
    assert miss.equals(miss2) and summarize_pairs(q).empty


def test_censoring_treats_open_visit_and_full_horizon_separately():
    c={'end_position':10,'end_side':'below'}
    v={'start_position':25,'end_position':28,'start_side':'below','path':'same'}
    assert classify_window(c,v,10,True)['status']=='no_return'
    z=classify_window(c,v,20,True)
    assert z['status']=='same_side_complete' and z['late_return']
    v['end_position']=40
    assert classify_window(c,v,20,True)['status']=='return_open_at_horizon'
    z=classify_window(c,v,20,False)
    assert z['status']=='censored' and z['return_observed'] and z['late_return']
