import pandas as pd
import pytest

from replayman.sloped_zones import SlopedConfig, scan_sloped_zones
from replayman.zone_memory import ZoneConfig


def bars():
    c = [9, 10, 12, 10, 9, 10, 12.05, 10, 9, 10, 12.1, 10, 9, 8, 9, 10, 11, 10, 9, 8]
    return pd.DataFrame({'ts_utc': pd.date_range('2026-01-01', periods=len(c), freq='h', tz='UTC'),
                         'open': c, 'high': [x + .1 for x in c], 'low': [x - .1 for x in c],
                         'close': c, 'volume': [100] * len(c)})


def cfg():
    return SlopedConfig(zone=ZoneConfig(method='percent', tolerance=.02, swing_left=1, swing_right=1),
                        min_anchor_distance=2, max_anchor_distance=8, max_anchors_per_kind=3)


def test_line_created_only_after_both_confirmed_and_third_reaction_is_later():
    zones, visits, _ = scan_sloped_zones(bars(), config=cfg(), series_key='X')
    created = zones[(zones.event == 'zone_created') & (zones.first_pivot_position == 2) & (zones.second_pivot_position == 6)].iloc[0]
    assert created['line_kind'] == 'high_high'
    assert created.first_confirmed_position == 3
    assert created.second_confirmed_position == 7
    assert created.position == 7
    assert created.slope_per_bar == pytest.approx((12.15 - 12.1) / 4)
    visits_for_line = visits[visits.zone_id == created.zone_id]
    assert visits_for_line.position.min() > 7
    assert visits_for_line.iloc[0].reaction_count == 2
    later = zones[(zones.zone_id == created.zone_id) & (zones.event == 'reaction_confirmed')].iloc[0]
    assert later.pivot_position == 10
    assert later.position == 11
    assert later.reaction_count == 3


def test_no_future_leak_or_refitting_from_later_bars():
    original = bars()
    changed = original.copy()
    changed.loc[13:, ['open', 'high', 'low', 'close']] *= 3
    results = [scan_sloped_zones(frame, config=cfg(), series_key='X') for frame in (original, changed, original.iloc[:13])]
    for full, mutated, prefix in zip(*results):
        def clean(frame):
            frame = frame[frame.position < 13].reset_index(drop=True).astype(object)
            return frame.where(pd.notna(frame), None)
        pd.testing.assert_frame_equal(clean(full), clean(mutated))
        pd.testing.assert_frame_equal(clean(full), clean(prefix))


def test_invalid_anchor_configuration():
    with pytest.raises(ValueError):
        SlopedConfig(min_anchor_distance=10, max_anchor_distance=5)
