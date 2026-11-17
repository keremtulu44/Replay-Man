import numpy as np
import pandas as pd
import pytest
from replayman.tenbar_research import make_windows, asof_hour, source_features, nonoverlap, target_labels, metrics


def bars(n=40):
    t=pd.date_range('2026-01-01',periods=n,freq='4h',tz='UTC')
    return pd.DataFrame({'ts_utc':t,'open':100.,'high':110.,'low':90.,'close':100.})


def test_asof_never_uses_future_and_stale_fails():
    t=pd.date_range('2026-01-01',periods=12,freq='h',tz='UTC')
    b=pd.DataFrame({'ts_utc':t,'close':100.+np.arange(12)})
    target=pd.to_datetime(['2026-01-01T10:30Z','2026-01-05T10:30Z'])
    x=asof_hour(target,b);assert x.price.iloc[0]==109 and pd.isna(x.price.iloc[1])
    b.loc[10:,'close']=50000
    assert asof_hour(target,b).price.iloc[0]==109


def test_episodes_no_overlap_and_no_outcomes():
    w=pd.DataFrame({'start_pos':[0,1,9,10,19,20], 'end_pos':[9,10,18,19,28,29],
                    'time_split':['train']*5+['test']})
    assert nonoverlap(w,np.ones(len(w),dtype=bool)).tolist()==[True,False,False,True,False,True]
    assert nonoverlap(w,np.array([False,True,True,True,True,True])).tolist()==[False,True,False,False,True,True]


def test_target_same_after_and_prefix_and_missing_intermediate():
    b=bars();target=b.copy();target.loc[9,'close']=97.;target.loc[19,'close']=100.
    w=make_windows(b,'4h',train_end='2026-02-01T00:00Z',validation_end='2026-03-01T00:00Z')
    out=target_labels(w,b,target,'4h',train_end='2026-02-01T00:00Z',validation_end='2026-03-01T00:00Z')
    assert out.same_return.iloc[0]==pytest.approx(-.03)
    assert out.after_return.iloc[0]==pytest.approx(100/97-1)
    assert out.same_excess.iloc[0]==pytest.approx(-.03)
    changed=target.copy();changed.loc[10:,'close']=101.
    out2=target_labels(w,b,changed,'4h',train_end='2026-02-01T00:00Z',validation_end='2026-03-01T00:00Z')
    assert out2.same_return.iloc[0]==pytest.approx(out.same_return.iloc[0])
    missing=target.drop(index=4).reset_index(drop=True)
    assert pd.isna(target_labels(w,b,missing,'4h',train_end='2026-02-01T00:00Z',validation_end='2026-03-01T00:00Z').same_return.iloc[0])
    assert pd.isna(out.after_return.iloc[-1])


def test_split_purge_and_exact_threshold_counts():
    b=bars(30);w=make_windows(b,'4h',train_end='2026-01-04T00:00Z',validation_end='2026-02-01T00:00Z')
    out=target_labels(w,b,b,'4h',train_end='2026-01-04T00:00Z',validation_end='2026-02-01T00:00Z')
    assert pd.isna(out.after_return.iloc[0])
    m=metrics([True,True,False],[-.03,-.02,-.8],[.1,np.nan,.5])
    assert m['n']==2 and m['down3_count']==1 and m['down3_rate']==.5 and m['excess_n']==1


def test_fx_conversion_and_threshold_episodes_cannot_see_future():
    b=bars(32);w=make_windows(b,'4h',train_end='2026-02-01T00:00Z',validation_end='2026-03-01T00:00Z')
    t=pd.date_range('2025-12-31T20:00Z',periods=200,freq='h')
    src=pd.DataFrame({'ts_utc':t,'close':100+np.arange(len(t))*.1})
    fx=pd.DataFrame({'ts_utc':t,'close':np.full(len(t),2.)})
    full=source_features(w,src,fx)
    usd=full[full.unit=='USD'].reset_index(drop=True);tr=full[full.unit=='TRY_proxy'].reset_index(drop=True)
    np.testing.assert_allclose(usd.source_return,tr.source_return,equal_nan=True)
    cut=src[src.ts_utc+pd.Timedelta('1h') <= w.signal_close_proxy.iloc[5]].reset_index(drop=True)
    pref=source_features(w.iloc[:6].reset_index(drop=True),cut,fx)
    cols=['end_pos','unit','source_return','episode_up2','episode_up4']
    expected=full[full.end_pos.isin(w.end_pos.iloc[:6])][cols].reset_index(drop=True)
    pd.testing.assert_frame_equal(expected,pref[cols].reset_index(drop=True),check_dtype=False)


def test_pair_study_baseline_and_trigger_count_not_ex_post_selected():
    from tools.measure_tenbar_reactions import pair_study
    src=pd.DataFrame({'end_pos':[9,10,20],'time_split':['test']*3,'source_return':[.05,.05,-.05],
                      'source_max_hourly_jump':[.01,.01,.01],'fixed_nonoverlap':[True,False,True],'episode_up4':[True,False,False],
                      'episode_down4':[False,False,True],'episode_up2':[True,False,False],
                      'episode_down2':[False,False,True],
                      'episode_up4_no_jump10':[True,False,False], 'episode_down4_no_jump10':[False,False,True],
                      'episode_up2_no_jump10':[True,False,False], 'episode_down2_no_jump10':[False,False,True],
                      'episode_up0':[True,False,False], 'episode_down0':[False,False,True],
                      'episode_up0_no_jump10':[True,False,False], 'episode_down0_no_jump10':[False,False,True]})
    labels=pd.DataFrame({'end_pos':[9,10,20],'same_return':[-.04,.02,-.01],'same_excess':[-.03,.01,0.],
                         'after_return':[np.nan,.9,.2],'after_excess':[np.nan,.8,.1],
                         'post_open_return':[np.nan,.9,.2],'post_open_excess':[np.nan,.8,.1]})
    r=pd.DataFrame(pair_study(src,labels,{}))
    same=r[(r.jump_filter=='all')&(r.time_split=='test')&(r.response=='same')&(r.sampling=='all_bars')&(r.source_condition=='up4')].iloc[0]
    assert same.n==2 and same.down3_count==1 and same.down3_rate==.5
    baseline=r[(r.jump_filter=='all')&(r.time_split=='test')&(r.response=='same')&(r.sampling=='all_bars')&(r.source_condition=='all')].iloc[0]
    assert baseline.n==3 and baseline.down3_count==1
    # The first shock was selected before seeing that its after outcome is missing;
    # we do not replace it with the second event with a known outcome.
    after=r[(r.jump_filter=='all')&(r.time_split=='test')&(r.response=='after')&(r.sampling=='shock_episode')&(r.source_condition=='up4')].iloc[0]
    assert after.selected_source_signals==1 and after.n==0


def test_jump10_sensitivity_is_known_at_signal_and_not_a_future_filter():
    b=bars(30);w=make_windows(b,'4h',train_end='2026-02-01T00:00Z',validation_end='2026-03-01T00:00Z')
    t=pd.date_range('2025-12-31T20:00Z',periods=200,freq='h')
    src=pd.DataFrame({'ts_utc':t,'close':100.});fx=pd.DataFrame({'ts_utc':t,'close':2.})
    # This bar closes before the first signal and a large move is observable by then.
    src.loc[src.ts_utc==pd.Timestamp('2026-01-01T12:00Z'),'close']=120.
    result=source_features(w.iloc[:1].reset_index(drop=True),src,fx)
    assert (result.source_max_hourly_jump>.1).all()
    changed=src.copy();changed.loc[changed.ts_utc>w.signal_close_proxy.iloc[0],'close']=50000
    again=source_features(w.iloc[:1].reset_index(drop=True),changed,fx)
    pd.testing.assert_series_equal(result.source_max_hourly_jump,again.source_max_hourly_jump)


def test_strictly_delayed_entry_and_post_return_split():
    benchmark=bars(40); target=benchmark.copy()
    # Signal index 9 closes at index 10's start; index 10 must be skipped.
    target.loc[10,'open']=10.;target.loc[10,'low']=1.
    target.loc[11,'open']=120.;target.loc[11,'high']=130.
    target.loc[20,'close']=90.
    windows=make_windows(benchmark,'4h',train_end='2026-02-01T00:00Z',validation_end='2026-03-01T00:00Z')
    row=target_labels(windows,benchmark,target,'4h',train_end='2026-02-01T00:00Z',validation_end='2026-03-01T00:00Z').iloc[0]
    assert row.post_open_entry_ts==benchmark.ts_utc.iloc[11]
    assert row.post_open_close_proxy==benchmark.ts_utc.iloc[20]+pd.Timedelta(hours=4)
    assert row.post_open_return==pytest.approx(90/120-1)
    assert row.post_open_excess==pytest.approx(90/120-1)
    missing=target.drop(index=15).reset_index(drop=True)
    assert pd.isna(target_labels(windows,benchmark,missing,'4h',train_end='2026-02-01T00:00Z',validation_end='2026-03-01T00:00Z').post_open_return.iloc[0])
    crossed=target_labels(windows,benchmark,target,'4h',train_end='2026-01-04T12:00Z',validation_end='2026-03-01T00:00Z')
    assert pd.isna(crossed.post_open_return.iloc[0])


def test_direction_count_keeps_zero_and_missing_out_of_denominator():
    m=metrics([True,True,True,True],[-.01,0.,.05,np.nan],[0.,0.,0.,np.nan])
    assert (m['n'],m['negative_count'],m['flat_count'],m['positive_count'])==(3,1,1,1)
    assert m['negative_rate']==pytest.approx(1/3) and m['down3_count']==0
