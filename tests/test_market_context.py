import numpy as np
import pandas as pd
from replayman.market_context import native_source_features
from replayman.tenbar_research import make_windows, source_features
from tools.measure_macro_risk import calculate_rows


def bars(n=80):
    return pd.DataFrame({'ts_utc':pd.date_range('2026-01-01',periods=n,freq='h',tz='UTC'),
                         'open':100.,'high':101.,'low':99.,'close':100.})


def test_native_features_match_existing_unconverted_and_are_past_only():
    b=bars();w=make_windows(b,'1h');src=bars();src['close']=100+np.arange(len(src))*.1
    fx=bars();fx['close']=2.
    native=native_source_features(w,src)
    old=source_features(w,src,fx);old=old[old.unit=='USD'].reset_index(drop=True)
    for col in ['source_return','source_max_hourly_jump','episode_up0','episode_up2','episode_down0']:
        np.testing.assert_allclose(native[col],old[col],equal_nan=True)
    cutoff=w.signal_close_proxy.iloc[12]
    changed=src.copy();changed.loc[changed.ts_utc+pd.Timedelta('1h')>cutoff,'close']=9999.
    again=native_source_features(w.iloc[:13].reset_index(drop=True),changed)
    for col in ['source_return','source_max_hourly_jump','episode_up0','episode_up2','episode_down0']:
        np.testing.assert_allclose(native[col].iloc[:13],again[col],equal_nan=True)


def test_native_past_only_expired_and_outcome_blind():
    b=bars();w=make_windows(b,'1h');source=bars(18);source.loc[10:,'close']=105.
    native=native_source_features(w,source)
    assert native.source_return.notna().any() and np.isnan(native.source_return.iloc[-1])
    labels=pd.DataFrame({'end_pos':w.end_pos,'same_return':np.nan,'same_excess':np.nan,
                         'post_open_return':np.nan,'post_open_excess':np.nan})
    rows=pd.DataFrame(calculate_rows(native,labels,{}))
    selected=rows[(rows.time_split=='train')&(rows.source_condition=='up2')&(rows.response=='post_open')&(rows.jump_filter=='all')].iloc[0]
    assert selected.selected_source_signals>0 and selected.n==0 and selected.risk_flag=='ornek_yetersiz'


def test_source_aware_baseline_is_selected_before_target_outcomes():
    from tools.measure_market_context import context_rows
    w=pd.DataFrame({'start_pos':[0,10,20,30], 'end_pos':[9,19,29,39], 'time_split':['train']*4,
                    'fixed_nonoverlap':[True]*4})
    src=w.copy();src['source_return']=[np.nan,.03,.03,.03];src['source_max_hourly_jump']=.01
    src['source_fixed']=[False,True,True,True];src['source_fixed_no_jump10']=src.source_fixed
    for cond in ('down0','up0','down2','up2','down4','up4'):
        src['episode_'+cond]=[False,True,True,True]
        src['episode_'+cond+'_no_jump10']=src['episode_'+cond]
    labels=pd.DataFrame({'end_pos':w.end_pos,'same_return':[.1,-.02,np.nan,.03], 'same_excess':0.,
                         'post_open_return':[.1,-.02,np.nan,.03],'post_open_excess':0.})
    row=pd.DataFrame(context_rows(src,labels,{})).query("response=='post_open' and jump_filter=='all' and source_condition=='up2' and time_split=='total'").iloc[0]
    assert row.available_baseline_selected==3 and row.available_baseline_n==2
    assert row.available_baseline_negative_count==1 and row.available_baseline_negative_rate==.5
