import pandas as pd
import pytest

from replayman.zone_memory import ZoneConfig, scan_zones, visit_outcomes


def sample_bars():
    close = [9, 10, 12, 10, 9, 10, 12.05, 10, 9, 10, 12.1, 10, 9, 8, 9, 10, 11, 10, 9, 8]
    return pd.DataFrame({"ts_utc": pd.date_range("2026-01-01", periods=len(close), freq="h", tz="UTC"),
                         "open": close, "high": [x + .1 for x in close],
                         "low": [x - .1 for x in close], "close": close,
                         "volume": [100] * len(close)})


def config():
    return ZoneConfig(method="percent", tolerance=0.02, swing_left=1, swing_right=1, exit_closes=2)


def test_pivots_and_memory_only_visible_after_confirmation():
    zones, visits, events = scan_zones(sample_bars(), config=config(), series_key="X")
    first = zones.iloc[0]
    assert first["event"] == "zone_created"
    assert first["pivot_position"] == 2
    assert first["position"] == 3
    assert first["role"] == "resistance_candidate"
    relevant = visits[visits.zone_id == first.zone_id].reset_index(drop=True)
    assert relevant.iloc[0]["position"] == 6
    assert relevant.iloc[0]["reaction_count"] == 1
    assert relevant.iloc[1]["position"] == 10
    assert relevant.iloc[1]["reaction_count"] == 2
    confirmation = zones[(zones.zone_id == first.zone_id) & (zones.event == "reaction_confirmed")].iloc[0]
    assert confirmation["pivot_position"] == 6
    assert confirmation["position"] == 7
    assert confirmation["reaction_count"] == 2
    first_events = events[events.visit_id == relevant.iloc[0].visit_id]
    assert len(first_events[first_events.event == "touch_bar"]) == 1
    assert first_events[first_events.event == "visit_end"].iloc[0]["position"] == 8


def test_future_mutation_and_truncation_do_not_change_past():
    bars = sample_bars()
    original = scan_zones(bars, config=config(), series_key="X")
    changed = bars.copy()
    changed.loc[13:, ["open", "high", "low", "close"]] *= 3
    altered = scan_zones(changed, config=config(), series_key="X")
    prefix = scan_zones(bars.iloc[:13], config=config(), series_key="X")
    for a, b, c in zip(original, altered, prefix):
        a = a[a.position < 13].reset_index(drop=True)
        b = b[b.position < 13].reset_index(drop=True)
        def normalize(frame):
            return frame.reset_index(drop=True).astype(object).where(pd.notna(frame.reset_index(drop=True)), None)
        pd.testing.assert_frame_equal(normalize(a), normalize(b), check_dtype=False)
        pd.testing.assert_frame_equal(normalize(a), normalize(c), check_dtype=False)


def test_outcomes_separate_and_censored():
    bars = sample_bars()
    _, visits, _ = scan_zones(bars, config=config())
    results = visit_outcomes(bars, visits, (1, 100))
    first = results[(results.visit_id == visits.iloc[0].visit_id) & (results.horizon == 1)].iloc[0]
    pos = int(visits.iloc[0].position)
    assert first['return'] == pytest.approx(bars.iloc[pos + 1]['close'] / bars.iloc[pos]['close'] - 1)
    assert first['mfe'] == pytest.approx(bars.iloc[pos + 1]['high'] / bars.iloc[pos]['close'] - 1)
    assert (results[results.horizon == 100].status == 'censored').all()
    assert results[results.horizon == 100]['return'].isna().all()
    assert 'return' not in visits


def test_atr_warmup_and_no_volume_influence():
    bars = sample_bars()
    cfg = ZoneConfig(method="atr", tolerance=0.25, swing_left=1, swing_right=1)
    first = scan_zones(bars, config=cfg)
    assert first[0].position.min() >= 13
    changed = bars.copy()
    changed['volume'] *= 1000
    second = scan_zones(changed, config=cfg)
    for a, b in zip(first, second):
        pd.testing.assert_frame_equal(a, b)


def test_configuration_validation():
    with pytest.raises(ValueError):
        ZoneConfig(tolerance=0)
    with pytest.raises(ValueError):
        ZoneConfig(method='invalid')
