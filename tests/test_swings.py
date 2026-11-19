import pandas as pd

from replayman.replay import causal_features
from replayman.swings import SwingConfig, confirmed_swings, multi_level_swings, swing_legs


def frame(highs, lows=None):
    lows = lows or [x - 2 for x in highs]
    close = [(h + l) / 2 for h, l in zip(highs, lows)]
    return pd.DataFrame({"ts_utc": pd.date_range("2026-01-01", periods=len(highs), freq="h", tz="UTC"), "open": close, "high": highs, "low": lows, "close": close, "volume": 100})


def test_pivot_is_published_only_at_confirmation_bar():
    bars = frame([1, 2, 5, 3, 2, 4, 3])
    swings = confirmed_swings(bars, config=SwingConfig(2, 2))
    high = swings.query("kind == 'high'").iloc[0]
    assert high.pivot_position == 2
    assert high.confirmed_position == 4
    assert high.confirmed_ts == bars.loc[4, "ts_utc"]


def test_equal_extrema_use_documented_rightmost_and_can_reproduce_legacy():
    bars = frame([5, 6, 8, 8, 7, 6], lows=[5, 4, 2, 2, 3, 4])
    rightmost = confirmed_swings(bars, config=SwingConfig(2, 2))
    leftmost = confirmed_swings(bars, config=SwingConfig(2, 2, tie_break="leftmost"))
    for kind in ("high", "low"):
        new = rightmost.query("kind == @kind").iloc[0]
        old = leftmost.query("kind == @kind").iloc[0]
        assert (new.pivot_position, new.confirmed_position) == (3, 5)
        assert (old.pivot_position, old.confirmed_position) == (2, 4)
    # No rightmost pivot exists at the previous bar; it cannot leak backwards.
    prefix = confirmed_swings(bars.iloc[:5], config=SwingConfig(2, 2))
    assert prefix.empty


def test_future_after_confirmation_does_not_change_old_events():
    bars = frame([1, 2, 5, 3, 2, 4, 3, 2, 8])
    prefix = confirmed_swings(bars.iloc[:7], config=SwingConfig(2, 2))
    full = confirmed_swings(bars, config=SwingConfig(2, 2))
    pd.testing.assert_frame_equal(prefix.reset_index(drop=True), full[full.confirmed_position < 7].reset_index(drop=True))


def test_high_relations_are_classified_in_confirmation_order():
    bars = frame([1, 2, 5, 3, 2, 6, 3, 2, 4, 3, 2])
    highs = confirmed_swings(bars, config=SwingConfig(1, 1)).query("kind == 'high'")
    assert list(highs.relation)[:3] == ["first", "higher_high", "lower_high"]


def test_minor_major_and_legs_have_known_time():
    bars = frame([1, 2, 5, 3, 2, 1, 2, 7, 4, 2, 1, 3, 6, 3, 2, 1, 2, 8, 4, 2])
    features = causal_features(bars)
    swings = multi_level_swings(bars, features)
    assert set(swings.level) == {"minor", "major"}
    legs = swing_legs(swings, bars)
    assert len(legs)
    assert (legs.known_at_position >= legs.end_position).all()
    assert (legs.duration_bars > 0).all()
