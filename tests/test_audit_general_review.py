import pandas as pd
import pytest

from replayman.dip_research import Period
from tools.audit_general_review import independent_label, independent_trade_bounds


def test_audit_stop_target_bounds_gap_and_timeout():
    bars = pd.DataFrame({'open': [100., 97., 100.], 'high': [100.5, 98., 101.],
                         'low': [99.5, 96., 99.5], 'close': [100., 97., 100.5]})
    lower, upper = independent_trade_bounds(bars, 0, 1, 1.)
    assert lower == pytest.approx(-.03) and upper == pytest.approx(-.03)
    bars.loc[0, ['high', 'low']] = [103., 98.]
    lower, upper = independent_trade_bounds(bars, 0, 1, 1.)
    assert lower == pytest.approx(-.01) and upper == pytest.approx(.02)
    lower, upper = independent_trade_bounds(bars, 2, 2, 1.)
    assert lower == pytest.approx(.005) and upper == pytest.approx(.005)
    with pytest.raises(ValueError):
        independent_trade_bounds(bars, 0, 3, 1.)


def test_audit_dip_label_and_insufficient_followup():
    times = pd.date_range('2026-01-01', periods=12, freq='D', tz='UTC')
    bars = pd.DataFrame({'ts_utc': times, 'close': [10.] * 12})
    period = Period('test', times[0], times[-1] + pd.Timedelta(days=1))
    refs = pd.DataFrame([{'period': 'test', 'pivot_position': 3, 'pivot_low': 9.5}])
    assert independent_label(bars, 4, 1., refs, period) == 'matched'
    assert independent_label(bars, 4, .1, refs, period) == 'not_matched'
    assert independent_label(bars.iloc[:-1], 4, 1., refs, period) == 'censored'
