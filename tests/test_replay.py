import pandas as pd
import pytest

from replayman.replay import ReplayEngine, causal_features, forward_outcomes, load_bars


def bars(n=30):
    close = [100 + i + (i % 3) for i in range(n)]
    return pd.DataFrame({
        "ts_utc": pd.date_range("2026-01-01", periods=n, freq="h", tz="UTC"),
        "open": [x - 0.5 for x in close], "high": [x + 1 for x in close],
        "low": [x - 1 for x in close], "close": close, "volume": [1000 + i for i in range(n)],
    })


def test_features_are_causal_when_future_changes():
    original = bars()
    changed = original.copy()
    changed.loc[20:, ["open", "high", "low", "close"]] *= 10
    left = causal_features(original).iloc[:20]
    right = causal_features(changed).iloc[:20]
    pd.testing.assert_frame_equal(left, right)


def test_replay_exposes_only_opened_history():
    engine = ReplayEngine(bars(5))
    first = next(engine)
    assert first.position == 0
    assert len(engine.history) == 1
    history = engine.history
    history.loc[0, "close"] = -1
    assert engine.history.loc[0, "close"] != -1
    list(engine)
    assert len(engine.history) == 5


def test_forward_results_are_separate_and_correct():
    frame = bars(25)
    result = forward_outcomes(frame, (1, 3))
    assert result.loc[0, "return_fwd_1"] == pytest.approx(frame.loc[1, "close"] / frame.loc[0, "close"] - 1)
    assert result.loc[0, "mfe_3"] == pytest.approx(frame.loc[1:3, "high"].max() / frame.loc[0, "close"] - 1)
    assert result.loc[0, "mae_3"] == pytest.approx(frame.loc[1:3, "low"].min() / frame.loc[0, "close"] - 1)
    assert pd.isna(result.iloc[-1]["return_fwd_1"])


def test_load_rejects_invalid_geometry(tmp_path):
    frame = bars(2)
    frame.loc[0, "high"] = 1
    path = tmp_path / "bars.csv"
    frame.to_csv(path, index=False)
    with pytest.raises(ValueError, match="geometrisi"):
        load_bars(path)


def test_incomplete_derived_bars_are_removed(tmp_path):
    frame = bars(2)
    frame["complete"] = [True, False]
    path = tmp_path / "bars.csv"
    frame.to_csv(path, index=False)
    assert len(load_bars(path)) == 1
