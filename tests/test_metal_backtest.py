import numpy as np
import pandas as pd
import pytest
from replayman.metal_backtest import signal_features, metal_windows, post_labels, expanding_history, simulate, classify, combine
from replayman.tenbar_research import make_windows
from tools.measure_metal_filter import group_stats


def bars(n=80):
    t=pd.date_range('2026-01-01',periods=n,freq='h',tz='UTC')
    return pd.DataFrame({'ts_utc':t,'open':100.,'high':101.,'low':99.,'close':100.})


def test_causal_signals_and_entry_strictly_after_known():
    b=bars();b.loc[29,'close']=103.;b.loc[29,'high']=104.
    full=signal_features(b);prefix=signal_features(b.iloc[:30])
    pd.testing.assert_frame_equal(full.iloc[:30],prefix)
    assert full.breakout20.iloc[29]
    result=simulate(b,pd.DatetimeIndex(b.ts_utc),29,1.,'1h',10,1,2)
    assert result['entry_ts']==b.ts_utc.iloc[31] # index 30 starts exactly at signal close


def test_both_touch_yields_two_prices_and_gap_uses_open():
    b=bars();bt=pd.DatetimeIndex(b.ts_utc)
    b.loc[12,['open','high','low','close']]=[100,103,98,100]
    x=simulate(b,bt,10,1,'1h',10,1,2)
    assert x['exit_reason']=='ambiguous' and x['gross_lower']==pytest.approx(-.01) and x['gross_upper']==pytest.approx(.02)
    b.loc[12,['open','high','low','close']]=[100,100.5,99.5,100]
    b.loc[13,['open','high','low','close']]=[97,98,96,97]
    x=simulate(b,bt,10,1,'1h',10,1,2)
    assert x['exit_reason']=='gap_stop' and x['gross_lower']==pytest.approx(-.03)


def test_missing_and_split_purge():
    b=bars();bt=pd.DatetimeIndex(b.ts_utc);b.loc[12,'close']=np.nan
    assert simulate(b,bt,10,1,'1h',10,1,2) is None
    b=bars();b.ts_utc=pd.date_range('2026-06-30T12:00Z',periods=80,freq='h');bt=pd.DatetimeIndex(b.ts_utc)
    assert simulate(b,bt,8,1,'1h',10,2,4) is None


def test_history_only_outcomes_closed_by_signal_and_selection_precedes_outcomes():
    w=pd.DataFrame({'signal_close_proxy':pd.date_range('2026-01-01',periods=4,freq='h',tz='UTC')})
    s=pd.DataFrame({'episode_up':[True,True,False,False],'episode_down':[False]*4})
    end=pd.Series(pd.to_datetime(['2026-01-01T02:00Z','2026-01-01T03:00Z',None,None],utc=True))
    # Input datetime units can differ between source CSV and generated outcome columns.
    w['signal_close_proxy']=w.signal_close_proxy.dt.as_unit('us')
    end=end.dt.as_unit('ns')
    h=expanding_history(w,s,np.array([-.1,.2,np.nan,np.nan]),end)
    assert h.up_n.tolist()==[0,0,1,2] and h.up_down.tolist()==[0,0,1,1]
    assert classify(.03,9,9,.7)=='unknown'
    assert classify(.02,0,0,.7)=='no_signal'
    assert classify(-.03,10,7,.7)=='warning'
    assert combine('warning','unknown')=='warning' and combine('clear','unknown')=='unknown'


def test_post_labels_excludes_split_and_missing():
    b=bars();w=make_windows(b,'1h');ret,end=post_labels(w,b,b,'1h')
    assert ret[0]==0 and end.iloc[0]==b.ts_utc.iloc[20]+pd.Timedelta('1h')
    broken=b.copy();broken.loc[15,'close']=np.nan
    r,_=post_labels(w,b,broken,'1h');assert np.isnan(r[0])


def test_paired_comparison_counts_unknown_and_cost():
    d=pd.DataFrame({'strategy':['x']*3,'gold_return':[-.03,-.03,np.nan], 'gold_n':[10,10,0],'gold_down':[8,2,0],
                    'silver_return':[0.]*3,'silver_n':[0]*3,'silver_down':[0]*3,
                    'gross_lower':[-.02,.03,.01],'gross_upper':[-.02,.04,.01],
                    'exit_reason':['stop','ambiguous','time'],'target_symbol':['A','B','C']})
    r=group_stats(d,['strategy'],'gold',.7,.001).iloc[0]
    assert (r.all_n,r.paired_n,r.kept_n,r.blocked_n,r.unknown_n)==(3,2,1,1,1)
    assert r.kept_lower_mean==pytest.approx(.029) and r.paired_lower_mean==pytest.approx(.004)
    assert r.kept_ambiguous==1 and r.kept_upper_mean==pytest.approx(.039)
