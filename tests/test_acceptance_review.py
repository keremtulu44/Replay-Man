import pandas as pd
import pytest

from replayman.acceptance_review import down_acceptance_representatives, open_result
from replayman.dip_research import Period


def test_multiple_levels_at_same_bar_are_not_multiple_trades():
    events = pd.DataFrame([{'event': 'acceptance', 'direction': 'down', 'event_position': 20, 'source_pivot_position': 8},
                           {'event': 'acceptance', 'direction': 'down', 'event_position': 20, 'source_pivot_position': 3},
                           {'event': 'acceptance', 'direction': 'down', 'event_position': 21, 'source_pivot_position': 7},
                           {'event': 'acceptance', 'direction': 'up', 'event_position': 21, 'source_pivot_position': 1}])
    raw, unique = down_acceptance_representatives(events)
    assert len(raw) == 3 and len(unique) == 2
    assert unique.iloc[0].source_pivot_position == 3


def test_delayed_open_and_strict_split_end_are_respected():
    times = pd.date_range('2026-01-01', periods=10, freq='h', tz='UTC')
    close = [10. + i for i in range(10)]
    bars = pd.DataFrame({'ts_utc': times, 'open': close, 'high': [x+1 for x in close],
                         'low': [x-1 for x in close], 'close': close})
    period = Period('all', times[0], times[-1]+pd.Timedelta(hours=1))
    a = open_result(bars, 2, entry_lag=1, horizon=3, period=period, benchmark=None)
    b = open_result(bars, 2, entry_lag=2, horizon=3, period=period, benchmark=None)
    assert a['start_ts'] == times[3] and a['end_ts'] == times[5]
    assert b['start_ts'] == times[4] and b['end_ts'] == times[6]
    assert a['directional_return'] == pytest.approx(-(15/13 - 1))
    boundary = Period('short', times[0], times[6])
    assert open_result(bars, 2, entry_lag=2, horizon=3, period=boundary, benchmark=None)['status'] == 'censored'
