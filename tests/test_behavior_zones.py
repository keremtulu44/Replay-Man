import pandas as pd
import pytest

from replayman.behavior_zones import BehaviorConfig, scan_behavior_zones
from replayman.zone_memory import ZoneConfig


def bars():
    closes = [100.0] * 20 + [101., 102., 103., 104., 105., 105., 100., 98., 98., 100., 102., 102., 100., 98., 98.]
    return pd.DataFrame({'ts_utc': pd.date_range('2026-01-01', periods=len(closes), freq='h', tz='UTC'),
                         'open': closes, 'high': [x + .2 for x in closes], 'low': [x - .2 for x in closes],
                         'close': closes, 'volume': [500.] * len(closes)})


def cfg(kind):
    return BehaviorConfig(kind=kind, zone=ZoneConfig(method='atr', tolerance=.25))


def test_dwell_candidate_only_when_known_and_visits_follow_departure():
    zones, visits, events = scan_behavior_zones(bars(), config=cfg('dwell'), series_key='X')
    first = zones.iloc[0]
    assert first.position == 13  # ilk ATR14
    assert first.source_start_position == 4
    assert first.source_end_position == 13
    relevant = visits[visits.zone_id == first.zone_id].reset_index(drop=True)
    assert relevant.iloc[0].position == 26  # kaynak içi barlar ziyaret sayılmaz
    assert relevant.iloc[0].prior_completed_visits == 0
    assert relevant.iloc[0].approach_side == 'above'
    first_end = events[(events.visit_id == relevant.iloc[0].visit_id) & (events.event == 'visit_end')].iloc[0]
    assert first_end.position == 28
    assert first_end.outcome == 'opposite_side'
    assert relevant.iloc[1].position == 29
    assert relevant.iloc[1].prior_opposite_side == 1
    assert relevant.iloc[1].prior_completed_visits == 1


def test_impulse_is_only_published_when_threshold_met_not_at_origin():
    zones, visits, _ = scan_behavior_zones(bars(), config=cfg('impulse'))
    first = zones.iloc[0]
    assert first.source_direction == 'up'
    assert first.source_start_position == first.position - 5
    assert first.position == 20
    assert (visits.position > first.source_end_position).all()


@pytest.mark.parametrize('kind', ['dwell', 'impulse'])
def test_truncation_and_future_mutation_do_not_change_history(kind):
    original = bars()
    changed = original.copy()
    changed.loc[30:, ['open', 'high', 'low', 'close']] *= 3
    result = [scan_behavior_zones(frame, config=cfg(kind), series_key='X') for frame in (original, changed, original.iloc[:30])]
    for full, altered, prefix in zip(*result):
        def clean(frame):
            frame = frame[frame.position < 30].reset_index(drop=True).astype(object)
            return frame.where(pd.notna(frame), None)
        pd.testing.assert_frame_equal(clean(full), clean(altered))
        pd.testing.assert_frame_equal(clean(full), clean(prefix))


def test_invalid_and_empty_results():
    with pytest.raises(ValueError):
        BehaviorConfig(kind='other')
    zones, visits, events = scan_behavior_zones(bars().iloc[:5], config=cfg('dwell'))
    assert zones.empty and visits.empty and events.empty
    assert 'zone_id' in zones and 'visit_id' in visits
