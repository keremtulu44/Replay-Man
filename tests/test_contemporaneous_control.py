import numpy as np
import pandas as pd

from replayman.contemporaneous_control import bar_context, match_at_same_bar
from tools.compare_dip_contemporaneous import summarize


def test_same_timestamp_calipers_and_one_to_one_control():
    t = pd.Timestamp('2026-01-01T10:30Z')
    rows = [
        {'asset_id': 'A', 'interval': '4h', 'position': 20, 'ts_utc': t, 'atr': 2., 'bullish': True, 'raw_a': True, 'prior_move_atr': -.1, 'prior_atr_fraction': .05},
        {'asset_id': 'B', 'interval': '4h', 'position': 21, 'ts_utc': t, 'atr': 2., 'bullish': True, 'raw_a': True, 'prior_move_atr': .1, 'prior_atr_fraction': .05},
        {'asset_id': 'X', 'interval': '4h', 'position': 24, 'ts_utc': t, 'atr': 1., 'bullish': True, 'raw_a': False, 'prior_move_atr': 0., 'prior_atr_fraction': .05},
        {'asset_id': 'Y', 'interval': '4h', 'position': 25, 'ts_utc': t, 'atr': 1., 'bullish': True, 'raw_a': False, 'prior_move_atr': .2, 'prior_atr_fraction': .06},
        {'asset_id': 'Z', 'interval': '4h', 'position': 25, 'ts_utc': t, 'atr': 1., 'bullish': True, 'raw_a': False, 'prior_move_atr': 5., 'prior_atr_fraction': .05},
        {'asset_id': 'W', 'interval': '4h', 'position': 25, 'ts_utc': t + pd.Timedelta(hours=4), 'atr': 1., 'bullish': True, 'raw_a': False, 'prior_move_atr': -.1, 'prior_atr_fraction': .05},
    ]
    signals = pd.DataFrame([{'signal_id': 'a', 'asset_id': 'A', 'interval': '4h', 'period': 'p', 'signal_position': 20, 'signal_ts': t},
                            {'signal_id': 'b', 'asset_id': 'B', 'interval': '4h', 'period': 'p', 'signal_position': 21, 'signal_ts': t}])
    result = match_at_same_bar(signals, pd.DataFrame(rows)).set_index('signal_id')
    assert result.loc['a', 'control_asset_id'] == 'X'
    assert result.loc['b', 'control_asset_id'] == 'Y'
    assert result.control_asset_id.is_unique
    assert result.trend_distance.le(1).all()
    assert result.volatility_ratio.between(.5, 2).all()


def test_context_is_prefix_stable_and_uses_only_previous_bars():
    rng = np.random.default_rng(12)
    price = 100 + np.cumsum(rng.normal(size=50))
    bars = pd.DataFrame({'ts_utc': pd.date_range('2026-01-01', periods=50, freq='h', tz='UTC'),
                         'open': price, 'high': price+2, 'low': price-2, 'close': price+1})
    prefix = bar_context(bars.iloc[:35], 'A', '4h')
    full = bar_context(bars, 'A', '4h')
    pd.testing.assert_frame_equal(prefix.reset_index(drop=True), full.iloc[:35].reset_index(drop=True))
    revised = bars.copy()
    revised.loc[34, 'close'] = 10000
    previous = bar_context(revised, 'A', '4h')
    assert previous.prior_move_atr.iloc[34] == full.prior_move_atr.iloc[34]
    assert previous.prior_atr_fraction.iloc[34] == full.prior_atr_fraction.iloc[34]


def test_different_exit_dates_and_censored_pairs_are_excluded():
    matches = pd.DataFrame([{'source':'internal','interval':'4h','period':'test','signal_id':str(i), 'control_status':'matched'} for i in range(3)])
    rows = []
    for i, timing in enumerate(('same', 'different', 'censored_or_unknown')):
        for entry in ('next_open', 'delayed_open'):
            rows.append({'source':'internal','interval':'4h','period':'test','asset_id':str(i),
                         'signal_id':str(i),'entry':entry,'timing':timing,'signal_ts':'2026-01-01T00:00:00Z',
                         'a_label':'censored' if i == 2 else 'matched','control_label':'not_matched',
                         'a_fixed_return':.1,'control_fixed_return':.03,
                         'a_excess_return':.05,'control_excess_return':-.02,
                         'a_trade_lower':.01,'control_trade_lower':-.01})
    result = summarize(matches, pd.DataFrame(rows))
    row = result.query("entry == 'next_open' and metric == 'fixed_return'").iloc[0]
    assert row.n == 1 and row.timing_mismatch == 1 and row.censored_or_unknown == 1
    assert row.paired_difference_mean == .07
    label = result.query("metric == 'dip_match'").iloc[0]
    assert label.n == 2 and label.censored_or_unknown == 1
