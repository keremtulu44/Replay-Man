from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from replayman.dip_research import Period, confirmation_events, scan_candidates
from tools.measure_dip_pilot import bootstrap_weekly_difference, load_external, summarize_outcomes


def test_external_precision_is_repaired_but_real_geometry_error_rejected(tmp_path: Path):
    path = tmp_path / 'ASELS.csv'
    path.write_text('Price,Close,High,Low,Open,Volume\n2024-01-01,10.0,9.999999999999998,9.0,9.5,100\n')
    data, meta = load_external(path)
    assert data.high.iloc[0] == 10.0 and meta['rounding_repairs'] == 1
    path.write_text('Price,Close,High,Low,Open,Volume\n2024-01-01,10.0,9.9,9.0,9.5,100\n')
    with pytest.raises(ValueError, match='ciddi OHLC'):
        load_external(path)


def test_cost_is_only_subtracted_from_the_observed_result():
    rows = pd.DataFrame([{'interval': '1d', 'period': 'test', 'variant': 'A_all', 'entry': 'next_open',
                          'horizon': 10, 'status': 'observed', 'asset_id': 'X',
                          'signal_ts': pd.Timestamp('2026-01-01', tz='UTC'), 'fixed_return': .01,
                          'excess_return': None, 'trade_lower': .01, 'trade_upper': .02,
                          'mfe': .03, 'mae': -.02, 'exit_reason': 'ambiguous', 'bars_held': 2},
                         {'interval': '1d', 'period': 'test', 'variant': 'A_all', 'entry': 'next_open',
                          'horizon': 10, 'status': 'censored', 'asset_id': 'X',
                          'signal_ts': pd.Timestamp('2026-01-02', tz='UTC'), 'fixed_return': None,
                          'excess_return': None, 'trade_lower': None, 'trade_upper': None,
                          'mfe': None, 'mae': None, 'exit_reason': None, 'bars_held': None}])
    result = summarize_outcomes(rows).iloc[0]
    assert result.observed == 1 and result.censored == 1 and result.benchmark_paired == 0
    assert result.net_median_010 == pytest.approx(.009)
    assert result.net_median_050 == pytest.approx(.005)
    assert result.ambiguous == 1 and result.trade_upper_median_gross == .02


def test_week_bootstrap_keeps_both_candidate_groups_and_is_reproducible():
    rows = []
    for i in range(8):
        for group, value in [('B_support', .02), ('A_no_support', .01)]:
            rows.append({'signal_ts': pd.Timestamp('2026-01-01', tz='UTC') + pd.Timedelta(days=7*i),
                         'variant': group, 'trade_lower': value})
    data = pd.DataFrame(rows)
    a = bootstrap_weekly_difference(data, 'trade_lower', draws=100)
    b = bootstrap_weekly_difference(data, 'trade_lower', draws=100)
    assert a == b and a['n_support'] == 8 and a['n_no_support'] == 8
    assert a['median_difference'] == pytest.approx(.01)
    assert a['ci_low'] == pytest.approx(.01) and a['ci_high'] == pytest.approx(.01)


def test_real_zone_and_candidate_prefix_is_not_changed_by_future_bars():
    rng = np.random.default_rng(41)
    center = 100 + np.cumsum(rng.normal(0, 1, 120))
    data = pd.DataFrame({'ts_utc': pd.date_range('2026-01-01', periods=120, freq='h', tz='UTC'),
                         'open': center, 'high': center + 1.5, 'low': center - 1.5,
                         'close': center + rng.uniform(-.8, .8, 120)})
    # Include deliberate candidates that exercise the zone scanner.
    data.loc[60, ['open', 'high', 'low', 'close']] = [center[60]-.4, center[60]+2, center[55:60].min()-3, center[60]+1]
    prefix = scan_candidates(data.iloc[:85], series_key='x')
    full = scan_candidates(data, series_key='x')
    pd.testing.assert_frame_equal(prefix.reset_index(drop=True), full.loc[full.signal_position < 85].reset_index(drop=True), check_dtype=False)
    period = Period('all', data.ts_utc.iloc[0], data.ts_utc.iloc[-1] + pd.Timedelta(hours=1))
    prefix_c, _ = confirmation_events(data.iloc[:85], prefix, [period])
    full_c, _ = confirmation_events(data, full, [period])
    pd.testing.assert_frame_equal(prefix_c.reset_index(drop=True), full_c.loc[full_c.signal_position < 85].reset_index(drop=True), check_dtype=False)
