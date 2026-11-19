import pandas as pd
import pytest

from replayman.dip_research import Period
from replayman.p6_causal import classify_failure, event_result


def sample():
    ts = pd.date_range('2026-01-01', periods=8, freq='D', tz='UTC')
    data = pd.DataFrame({'ts_utc': ts, 'open': [10, 11, 12, 13, 14, 15, 16, 17],
                         'high': [12, 13, 14, 15, 16, 17, 18, 19],
                         'low': [9, 10, 11, 12, 13, 14, 15, 16],
                         'close': [11, 12, 13, 14, 15, 16, 17, 18]})
    period = Period('p', ts[0], ts[-1] + pd.Timedelta(days=1))
    return data, period


def test_censoring_distinguishes_unknown_and_unconfirmed():
    data, period = sample()
    assert classify_failure(data, 1, 3, period, window=4) == 'confirmed'
    assert classify_failure(data, 1, None, period, window=4) == 'not_confirmed'
    assert classify_failure(data.iloc[:5], 1, None, period, window=4) == 'censored'
    cut = Period('p', data.ts_utc.iloc[0], data.ts_utc.iloc[3])
    assert classify_failure(data, 1, 3, cut, window=4) == 'censored'
    with pytest.raises(ValueError):
        classify_failure(data, 1, 6, period, window=4)


def test_confirmation_open_and_exact_market_end():
    data, period = sample()
    market = data.drop(index=[3]).reset_index(drop=True)  # market omits stock's day 3
    result = event_result(data, 1, entry='next_open', sign=1, horizon=3, period=period, benchmark=market)
    assert result['start_ts'] == data.ts_utc.iloc[2]
    assert result['end_ts'] == data.ts_utc.iloc[4]
    assert result['start_price'] == 12
    assert result['directional_return'] == pytest.approx(15/12 - 1)
    assert result['benchmark_return'] == pytest.approx(15/12 - 1)
    assert result['old_end_mismatch'] is True
    down = event_result(data, 1, entry='close', sign=-1, horizon=3, period=period, benchmark=market)
    assert down['directional_return'] == pytest.approx(-(15/12 - 1))
    assert down['directional_excess'] == pytest.approx(0)
    missing = event_result(data, 1, entry='next_open', sign=1, horizon=2, period=period, benchmark=market)
    assert missing['status'] == 'observed' and missing['benchmark_return'] is None


def test_signal_at_confirmation_is_not_failure_trade():
    data, period = sample()
    failure = event_result(data, 1, entry='close', sign=1, horizon=2, period=period)
    confirmation = event_result(data, 3, entry='next_open', sign=1, horizon=2, period=period)
    assert failure['start_price'] == 12
    assert confirmation['start_price'] == 14
    assert confirmation['start_ts'] > failure['start_ts']
    assert event_result(data, 6, entry='next_open', sign=1, horizon=2, period=period)['status'] == 'censored'
