import pandas as pd
import pytest

from tools.audit_legacy_alignment import window_alignment


def test_independent_index_shift_can_end_on_the_wrong_date():
    ts = pd.date_range('2026-01-01', periods=6, freq='D', tz='UTC')
    market = pd.DataFrame({'close': range(6)}, index=pd.DatetimeIndex(ts, name='ts_utc'))
    stock = pd.DataFrame({'ts_utc': ts[[0, 2, 3, 5]]})
    result = window_alignment(stock, market, 2)
    assert result == {'stock_windows': 2, 'old_comparable': 2, 'old_end_mismatches': 2,
                      'start_missing': 0, 'old_end_unavailable': 0, 'exact_end_missing': 0}
    missing = window_alignment(stock, market.drop(ts[5]), 2)
    assert missing['exact_end_missing'] == 1
    with pytest.raises(ValueError):
        window_alignment(stock, market, 0)


def test_missing_start_market_end_and_index_validation():
    ts = pd.date_range('2026-01-01', periods=6, freq='D', tz='UTC')
    market = pd.DataFrame({'close': range(4)}, index=pd.DatetimeIndex(ts[1:5], name='ts_utc'))
    stock = pd.DataFrame({'ts_utc': ts[[0, 2, 4, 5]]})
    result = window_alignment(stock, market, 1)
    assert result == {'stock_windows': 3, 'old_comparable': 1, 'old_end_mismatches': 1,
                      'start_missing': 1, 'old_end_unavailable': 1, 'exact_end_missing': 1}
    empty = window_alignment(stock.iloc[:1], market, 2)
    assert all(value == 0 for value in empty.values())
    with pytest.raises(ValueError, match='tekil'):
        window_alignment(pd.concat([stock, stock.iloc[:1]]), market, 1)
    with pytest.raises(ValueError, match='tekil'):
        window_alignment(stock, market.iloc[::-1], 1)
