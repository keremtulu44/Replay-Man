import numpy as np
import pandas as pd
import pytest

from replayman.dip_research import Period
from replayman.general_review import block_bootstrap_mean, prior_bull_controls
import tools.review_general_results as review


def sample_bars():
    bars = pd.DataFrame({'ts_utc': pd.date_range('2026-01-05', periods=24, freq='h', tz='UTC'),
                         'open': 10., 'high': 11., 'low': 9., 'close': 10.})
    bars.loc[18, ['open', 'close']] = [9.5, 10.]  # eligible prior control
    bars.loc[19, ['open', 'high', 'low', 'close']] = [9.5, 11., 8., 10.]  # raw A, not a control
    bars.loc[20, ['open', 'high', 'low', 'close']] = [9.5, 11., 7.5, 10.]  # chosen A
    bars.loc[22, ['open', 'high', 'low', 'close']] = [9., 11., 7., 9.5]  # another A; control 18 already used
    return bars


def test_previous_control_is_earlier_non_a_same_week_and_not_reused():
    bars = sample_bars()
    period = Period('p', bars.ts_utc.iloc[0] - pd.Timedelta(days=1), bars.ts_utc.iloc[-1] + pd.Timedelta(days=1))
    signals = pd.DataFrame([{'signal_id': 'a1', 'signal_position': 20, 'signal_ts': bars.ts_utc.iloc[20], 'period': 'p'},
                            {'signal_id': 'a2', 'signal_position': 22, 'signal_ts': bars.ts_utc.iloc[22], 'period': 'p'}])
    chosen = prior_bull_controls(bars, signals, [period])
    assert chosen.iloc[0].control_position == 18
    assert chosen.iloc[0].bar_gap == 2
    assert chosen.iloc[1].control_status == 'no_prior_control'
    changed = bars.copy()
    changed.loc[21:, ['open', 'high', 'low', 'close']] = [100, 102, 99, 101]
    prefix = prior_bull_controls(bars.iloc[:21], signals.iloc[:1], [period])
    future_changed = prior_bull_controls(changed, signals.iloc[:1], [period])
    pd.testing.assert_frame_equal(prefix, future_changed, check_dtype=False)


def test_control_cannot_cross_period_or_week_boundary():
    bars = sample_bars()
    p = Period('p', bars.ts_utc.iloc[19], bars.ts_utc.iloc[-1] + pd.Timedelta(days=1))
    signal = pd.DataFrame([{'signal_id': 'a', 'signal_position': 20, 'signal_ts': bars.ts_utc.iloc[20], 'period': 'p'}])
    assert prior_bull_controls(bars, signal, [p]).iloc[0].control_status == 'no_prior_control'
    with pytest.raises(ValueError, match='failed_low5'):
        prior_bull_controls(bars, signal.assign(signal_position=18), [p])


def test_block_bootstrap_reproducible_and_insufficient_weeks_are_unknown():
    times = pd.Series(pd.date_range('2025-01-06', periods=24, freq='W-MON', tz='UTC'))
    values = pd.Series(np.full(24, .03))
    a = block_bootstrap_mean(values, times, draws=200)
    b = block_bootstrap_mean(values, times, draws=200)
    assert a == b and a['observed_weeks'] == 24 and a['calendar_weeks'] == 24
    assert a['ci_low'] == pytest.approx(.03) and a['ci_high'] == pytest.approx(.03)
    short = block_bootstrap_mean(values[:19], times[:19], draws=100)
    assert short['valid_draws'] == 0 and np.isnan(short['ci_low'])


def test_market_data_must_match_original_input_manifest(tmp_path, monkeypatch):
    pd.DataFrame([{'kind':'benchmark','interval':'4h','sha256':'original'}]).to_csv(tmp_path / 'input_manifest.csv', index=False)
    monkeypatch.setattr(review, 'load_benchmarks', lambda root: ({'4h':'market'}, [{'interval':'4h','sha256':'original'}]))
    assert review.verified_markets(tmp_path, tmp_path) == {'4h':'market'}
    monkeypatch.setattr(review, 'load_benchmarks', lambda root: ({'4h':'other'}, [{'interval':'4h','sha256':'changed'}]))
    with pytest.raises(ValueError, match='hash'):
        review.verified_markets(tmp_path, tmp_path)
