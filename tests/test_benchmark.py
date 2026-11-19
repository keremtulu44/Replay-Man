import numpy as np
import pandas as pd
import pytest

from replayman.benchmark import attach_exact_close_benchmark


def test_exact_end_time_not_independent_market_bar_count():
    dates = pd.date_range('2026-01-01', periods=6, freq='D', tz='UTC')
    market = pd.DataFrame({'interval': '1d', 'ts_utc': dates, 'close': [100, 110, 120, 130, 140, 150]})
    # Stock skips a market day. At stock +2 the end is day 3, not market +2.
    events = pd.DataFrame({'interval': ['1d', '1d'], 'event_ts': [dates[0], dates[0]],
                           'outcome_end_ts_2': [dates[3], dates[5]],
                           'directional_return_2': [.4, .4], 'thesis_direction': ['up', 'down']})
    out = attach_exact_close_benchmark(events, market, (2,))
    assert out.bench_2.iloc[0] == pytest.approx(.3)
    assert out.excess_2.iloc[0] == pytest.approx(.1)
    assert out.bench_2.iloc[1] == pytest.approx(.5)
    assert out.excess_2.iloc[1] == pytest.approx(.9)
    missing = attach_exact_close_benchmark(events, market.iloc[:-1], (2,))
    assert np.isnan(missing.bench_2.iloc[1]) and np.isnan(missing.excess_2.iloc[1])


def test_historical_p6_tool_uses_exact_end_and_new_output_dir(tmp_path, monkeypatch):
    import tools.measure_cilt2_lifecycle as tool
    from pathlib import Path
    root = tmp_path / 'data'
    bars = root / 'bist_indices' / 'IDX_XU100' / 'series' / 'bars'
    bars.mkdir(parents=True)
    dates = pd.date_range('2026-01-01', periods=4, freq='D', tz='UTC')
    pd.DataFrame({'ts_utc': dates, 'open': [100, 101, 102, 103], 'high': [101, 102, 103, 104],
                  'low': [99, 100, 101, 102], 'close': [100, 101, 102, 103], 'volume': 1}).to_csv(bars / '1d.csv', index=False)
    monkeypatch.setattr(tool, 'ROOT', root)
    events = pd.DataFrame({'interval': ['1d'], 'event_ts': [dates[0]], 'thesis_direction': ['up'],
                           'outcome_end_ts_60': [dates[3]], 'directional_return_60': [.05]})
    actual = tool.add_benchmark(events, (60,))
    assert actual.bench_60.iloc[0] == pytest.approx(.03)
    assert actual.excess_60.iloc[0] == pytest.approx(.02)
    assert tool.OUT != Path('research/measurements/cilt2-lifecycle')


def test_duplicate_benchmark_keys_are_rejected():
    date = pd.Timestamp('2026-01-01', tz='UTC')
    market = pd.DataFrame({'interval': ['1d', '1d'], 'ts_utc': [date, date], 'close': [1, 2]})
    ev = pd.DataFrame({'interval': ['1d'], 'event_ts': [date], 'outcome_end_ts_2': [date],
                       'directional_return_2': [0.], 'thesis_direction': ['up']})
    with pytest.raises(ValueError, match='tekil'):
        attach_exact_close_benchmark(ev, market, (2,))
