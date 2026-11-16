import pandas as pd

from replayman.replay import causal_features
from replayman.structure import StructureConfig, attach_event_outcomes, structure_events
from replayman.swings import confirmed_swings, SwingConfig


def bars(close):
    return pd.DataFrame({"ts_utc": pd.date_range("2026-01-01", periods=len(close), freq="h", tz="UTC"), "open": close, "high": [x + .4 for x in close], "low": [x - .4 for x in close], "close": close, "volume": 100})


def manual_swing(price=10, kind="high", confirmed=2):
    return pd.DataFrame([{"level": "minor", "kind": kind, "relation": "first", "price": price, "pivot_position": 1, "pivot_ts": pd.Timestamp("2026-01-01T01:00Z"), "confirmed_position": confirmed, "confirmed_ts": pd.Timestamp("2026-01-01T02:00Z"), "confirmation_delay_bars": 1, "price_from_confirmation_close_atr": 0}])


def test_level_cannot_trigger_before_confirmation():
    frame = bars([9, 11, 9, 11, 12, 12])
    features = causal_features(frame)
    events = structure_events(frame, features, manual_swing(10, confirmed=2), config=StructureConfig(tolerance_atr=0))
    assert events.event_position.min() == 3
    assert not (events.event_position <= 2).any()


def test_break_follow_accept_retest_failure_lifecycle():
    frame = bars([9, 9, 9, 11, 12, 10, 8, 8])
    features = causal_features(frame)
    events = structure_events(frame, features, manual_swing(10), config=StructureConfig(tolerance_atr=0, acceptance_closes=2))
    names = list(events.event)
    assert names[:3] == ["close_break", "follow_through", "acceptance"]
    assert "retest_hold" in names
    assert names[-1] == "failure"
    assert events.query("event == 'failure'").iloc[0].bars_since_break == 3


def test_down_break_directional_outcomes_are_signed():
    frame = bars([11, 11, 11, 9, 8, 7, 6, 5])
    features = causal_features(frame)
    events = structure_events(frame, features, manual_swing(10, "low"), config=StructureConfig(tolerance_atr=0))
    attached = attach_event_outcomes(events.query("event == 'close_break'"), frame, (1, 3))
    assert attached.iloc[0].directional_return_1 > 0
    assert attached.iloc[0].directional_return_3 > attached.iloc[0].directional_return_1


def test_generated_swing_events_stay_causal():
    frame = bars([8, 9, 11, 9, 8, 10, 12, 11, 9, 8, 13, 12, 11])
    features = causal_features(frame)
    swings = confirmed_swings(frame, features, config=SwingConfig(1, 1))
    events = structure_events(frame, features, swings, config=StructureConfig(tolerance_atr=0))
    assert (events.event_position > events.source_confirmed_position).all()
