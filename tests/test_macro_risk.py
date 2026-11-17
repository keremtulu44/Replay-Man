import numpy as np
import pandas as pd
import pytest
from tools.measure_macro_risk import calculate_rows
from replayman.tenbar_research import make_windows, target_labels
from tests.test_tenbar_research import bars


def test_totals_are_weighted_and_missing_selected_is_not_replaced():
    src=pd.DataFrame({'end_pos':[9,19,29,39], 'time_split':['train','train','validation','test'],
                      'source_return':[-.03]*4,'source_max_hourly_jump':[.01]*4,
                      'fixed_nonoverlap':[True]*4})
    for cond in ('down0','up0','down2','up2','down4','up4'):
        src['episode_'+cond]=[True]*4
        src['episode_'+cond+'_no_jump10']=[True]*4
    labels=pd.DataFrame({'end_pos':src.end_pos,'same_return':[-.01,0.,-.04,np.nan],
                         'same_excess':[0.]*4,'post_open_return':[-.01,0.,-.04,np.nan], 'post_open_excess':[0.]*4})
    result=pd.DataFrame(calculate_rows(src,labels,{}))
    r=result[(result.response=='post_open')&(result.source_condition=='down2')&(result.jump_filter=='all')].set_index('time_split')
    assert r.loc['total','selected_source_signals']==4
    assert r.loc['total','n']==3 and r.loc['total','negative_count']==2 and r.loc['total','flat_count']==1
    assert r.loc['total','negative_rate']==pytest.approx(2/3)
    assert r.loc['total','n']==sum(r.loc[x,'n'] for x in ('train','validation','test'))
    assert r.loc['total','baseline_negative_count']==2 and r.loc['total','risk_flag']=='ornek_yetersiz'


def test_post_outcome_does_not_require_old_target_history():
    b=bars(40);target=b.drop(index=4).reset_index(drop=True)
    w=make_windows(b,'4h',train_end='2026-02-01T00:00Z',validation_end='2026-03-01T00:00Z')
    row=target_labels(w,b,target,'4h',train_end='2026-02-01T00:00Z',validation_end='2026-03-01T00:00Z').iloc[0]
    assert pd.isna(row.same_return) and row.post_open_return==0


def test_warning_at_seventy_percent_and_ten_observations():
    src=pd.DataFrame({'end_pos':list(range(10)), 'time_split':['train']*10,
                      'source_return':[-.03]*10,'source_max_hourly_jump':[.01]*10,
                      'fixed_nonoverlap':[True]*10})
    for c in ('down0','up0','down2','up2','down4','up4'):
        src['episode_'+c]=True;src['episode_'+c+'_no_jump10']=True
    ret=[-.01]*7+[.01]*3
    labels=pd.DataFrame({'end_pos':src.end_pos,'same_return':ret,'same_excess':ret,
                         'post_open_return':ret,'post_open_excess':ret})
    r=pd.DataFrame(calculate_rows(src,labels,{}))
    row=r[(r.response=='post_open')&(r.source_condition=='down2')&(r.jump_filter=='all')&(r.time_split=='total')].iloc[0]
    assert row.n==10 and row.negative_count==7 and row.risk_flag=='tarihsel_uyari'
