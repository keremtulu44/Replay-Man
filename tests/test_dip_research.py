import pandas as pd
import pytest

import replayman.dip_research as dip


def bars(n=35):
    return pd.DataFrame({
        'ts_utc': pd.date_range('2026-01-01', periods=n, freq='h', tz='UTC'),
        'open': [10.0] * n, 'high': [11.0] * n, 'low': [9.0] * n, 'close': [10.0] * n,
        'volume': [1] * n,
    })


def period():
    return dip.Period('all', pd.Timestamp('2025-12-01', tz='UTC'), pd.Timestamp('2027-01-01', tz='UTC'))


def fake_zone(position):
    row = {'zone_id': 'z1', 'position': position, 'role': 'support_candidate', 'center': 9.0,
           'lower': 8.5, 'upper': 9.5, 'reaction_count': 1}
    return pd.DataFrame([row]), pd.DataFrame(), pd.DataFrame()


def test_support_must_be_known_before_candidate_bar(monkeypatch):
    data = bars()
    data.loc[20, ['open', 'high', 'low', 'close']] = [9.3, 11.0, 8.0, 10.0]
    monkeypatch.setattr(dip, 'scan_zones', lambda *a, **k: fake_zone(20))
    same_bar = dip.scan_candidates(data)
    assert len(same_bar) == 1 and not same_bar.iloc[0].support
    monkeypatch.setattr(dip, 'scan_zones', lambda *a, **k: fake_zone(19))
    earlier = dip.scan_candidates(data)
    assert earlier.iloc[0].support
    assert earlier.iloc[0].zone_created_position < earlier.iloc[0].signal_position


def test_confirmation_only_exists_when_later_bar_closes_and_censors():
    data = bars()
    data.loc[22, ['open', 'high', 'low', 'close']] = [10.0, 11.5, 9.0, 11.2]
    base = pd.DataFrame([{'signal_position': 20, 'signal_ts': data.ts_utc.iloc[20], 'atr': 2.0,
                          'signal_open': 9.3, 'signal_high': 11.0, 'signal_low': 8.0, 'signal_close': 10.0,
                          'prior_low5': 9.0, 'support': True, 'zone_id': 'z', 'zone_created_position': 19,
                          'zone_lower': 8.5, 'zone_upper': 9.5, 'zone_reactions': 1}])
    full, status = dip.confirmation_events(data, base, [period()])
    assert full.iloc[0].signal_position == 22
    assert full.iloc[0].origin_position == 20
    assert status.iloc[0].status == 'confirmed'
    prefix, censored = dip.confirmation_events(data.iloc[:22], base, [period()])
    assert prefix.empty and censored.iloc[0].status == 'censored'
    early_end = dip.Period('short', data.ts_utc.iloc[0], data.ts_utc.iloc[22])
    assert dip.confirmation_events(data, base, [early_end])[1].iloc[0].status == 'censored'


def test_same_bar_stop_target_is_ambiguous_and_no_lookahead_entry():
    data = bars(6)
    data.loc[1, ['open', 'high', 'low', 'close']] = [100., 103., 98., 101.]
    data.loc[2, ['open', 'high', 'low', 'close']] = [105., 106., 104., 105.]
    signal = {'signal_position': 0, 'atr': 1.0}
    result = dip.evaluate_trade(data, signal, period(), horizon=2, entry_lag=1)
    assert result['entry_position'] == 1 and result['exit_reason'] == 'ambiguous'
    assert result['trade_lower'] == pytest.approx(-.01)
    assert result['trade_upper'] == pytest.approx(.02)
    delayed = dip.evaluate_trade(data, signal, period(), horizon=2, entry_lag=2)
    assert delayed['entry_position'] == 2 and delayed['entry_price'] == 105


def test_exact_benchmark_end_and_censoring_are_preserved():
    data = bars(8)
    signal = {'signal_position': 1, 'atr': 1.0}
    benchmark = data[['ts_utc', 'open', 'close']].copy()
    benchmark = benchmark.drop(index=4)
    missing = dip.evaluate_trade(data, signal, period(), horizon=3, entry_lag=1, benchmark=benchmark)
    assert missing['status'] == 'observed' and missing['benchmark_return'] is None
    exact = dip.evaluate_trade(data, signal, period(), horizon=2, entry_lag=1, benchmark=benchmark)
    assert exact['benchmark_return'] == 0 and exact['excess_return'] == 0
    boundary = dip.Period('short', data.ts_utc.iloc[0], data.ts_utc.iloc[4])
    assert dip.evaluate_trade(data, signal, boundary, horizon=3, entry_lag=1)['status'] == 'censored'


def test_pivot_label_cannot_use_incomplete_future_window():
    data = bars(30)
    pivots = pd.DataFrame([{'pivot_position': 18, 'pivot_ts': data.ts_utc.iloc[18], 'known_at_position': 23,
                            'pivot_low': 9.5, 'period': 'all'}])
    signal = {'signal_position': 20, 'signal_close': 10.0, 'atr': 1.0}
    observed = dip.label_signal(signal, data, pivots, period())
    assert observed == {'label_status': 'matched', 'matched_pivot_position': 18, 'pivot_delay': 2}
    assert dip.label_signal(signal, data.iloc[:27], pivots, period())['label_status'] == 'censored'
