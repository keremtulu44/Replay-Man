import pandas as pd
import pytest

from tools.summarize_dip_sensitivity import daily_action_flags, paired_delay


def test_delay_sensitivity_only_uses_same_completed_signals():
    rows = []
    for signal, next_return, delayed_return, delayed_status in [('s1', .02, .01, 'observed'), ('s2', -.03, 0, 'censored')]:
        common = {'signal_id': signal, 'horizon': 20, 'asset_id': 'X', 'interval': '4h', 'period': 'test', 'variant': 'A_all'}
        rows.append({**common, 'entry': 'next_open', 'status': 'observed', 'fixed_return': next_return,
                     'excess_return': None, 'trade_lower': next_return})
        rows.append({**common, 'entry': 'delayed_open', 'status': delayed_status, 'fixed_return': delayed_return,
                     'excess_return': None, 'trade_lower': delayed_return})
    summary = paired_delay(pd.DataFrame(rows)).iloc[0]
    assert summary.paired_signals == 1
    assert summary.fixed_return_next_median == pytest.approx(.02)
    assert summary.fixed_return_delay_median == pytest.approx(.01)
    assert summary.fixed_return_median_paired_change == pytest.approx(-.01)
    assert summary.excess_return_paired == 0


def test_corporate_action_flags_are_not_treated_as_known_no_action(tmp_path):
    root = tmp_path / 'ohlcv'
    folder = root / 'bist_equities' / 'BIST_X' / 'series' / 'bars'
    folder.mkdir(parents=True)
    prices = [10.0] * 8 + [6.0] * 17
    frame = pd.DataFrame({'ts_utc': pd.date_range('2026-01-01', periods=25, freq='D', tz='UTC'),
                          'open': prices, 'high': [p + 1 for p in prices], 'low': [p - 1 for p in prices],
                          'close': prices, 'volume': 100, 'stock_splits': 0., 'dividends': 0.})
    frame.loc[5, 'stock_splits'] = 2.
    frame.loc[7, 'dividends'] = 1.
    frame.loc[4, 'dividends'] = None
    frame.to_csv(folder / '1d.csv', index=False)
    outcomes = pd.DataFrame([{'signal_id': 'x', 'asset_id': 'BIST_X', 'interval': '1d', 'period': 'test',
                              'variant': 'A_all', 'entry': 'next_open', 'horizon': 20, 'status': 'observed',
                              'entry_position': 2, 'end_position': 21, 'fixed_return': -.4, 'trade_lower': -.1}])
    flags, summary = daily_action_flags(outcomes, root)
    assert flags.iloc[0].action_unknown and flags.iloc[0].split_recorded
    assert flags.iloc[0].dividend_recorded and flags.iloc[0].close_jump_30pct
    assert summary.iloc[0].known_no_action_count == 0
    assert summary.iloc[0].no_jump_count == 0
