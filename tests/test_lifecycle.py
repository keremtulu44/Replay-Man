import pandas as pd
import pytest

from replayman.lifecycle import enrich_lifecycle
from replayman.structure import attach_event_outcomes


def sample():
    bars = pd.DataFrame({
        'open': [9] * 8,
        'high': [9.5, 10.5, 9.5, 11, 12, 10, 8, 7],
        'low': [8.5, 8.8, 8.5, 9, 10, 8, 7, 6],
        'close': [9, 9.5, 9, 10.8, 11, 8.8, 7.5, 7],
        'volume': 100,
        'ts_utc': pd.date_range('2026-01-01', periods=8, freq='h', tz='UTC'),
    })
    features = pd.DataFrame({'atr': [1.0] * 8})
    common = {
        'level': 'minor', 'direction': 'up', 'level_price': 10.0,
        'source_pivot_position': 0, 'source_confirmed_position': 0,
        'level_age_bars': 1, 'distance_close_atr': 0,
    }
    events = pd.DataFrame([
        {**common, 'event': 'probe_rejection', 'event_position': 1, 'event_ts': bars.ts_utc.iloc[1], 'bars_since_break': None},
        {**common, 'event': 'close_break', 'event_position': 3, 'event_ts': bars.ts_utc.iloc[3], 'bars_since_break': 0},
        {**common, 'event': 'retest_hold', 'event_position': 4, 'event_ts': bars.ts_utc.iloc[4], 'bars_since_break': 1},
        {**common, 'event': 'failure', 'event_position': 5, 'event_ts': bars.ts_utc.iloc[5], 'bars_since_break': 2},
    ])
    return events, bars, features


def test_counter_expansion_is_separate_and_known_only_at_confirmation():
    events, bars, features = sample()
    full = enrich_lifecycle(events, bars, features)
    prefix = enrich_lifecycle(events, bars.iloc[:6], features.iloc[:6])
    failure = full[full.event == 'failure'].iloc[0]
    confirmation = full[full.event == 'counter_expansion'].iloc[0]
    assert list(full.attempt_number) == [1, 2, 2, 2, 2]
    assert failure.old_area_depth_atr > 1
    assert pd.isna(failure.counter_expansion_position)
    assert (confirmation.event_position, confirmation.origin_failure_position) == (6, 5)
    assert confirmation.counter_expansion_bars == 1
    assert confirmation.event_ts == bars.ts_utc.iloc[6]
    assert 'counter_expansion' not in set(prefix.event)
    assert pd.isna(prefix[prefix.event == 'failure'].iloc[0].counter_expansion_position)
    assert full[full.event == 'retest_hold'].iloc[0].outside_duration == 1

    # Outcomes start at the confirmation's close, not the earlier failure close.
    actual = attach_event_outcomes(full[full.event == 'counter_expansion'], bars, (1,)).iloc[0]
    assert actual.thesis_direction == 'down'
    assert actual.directional_return_1 == pytest.approx(-(bars.close.iloc[7] / bars.close.iloc[6] - 1))
    assert actual.outcome_end_ts_1 == bars.ts_utc.iloc[7]


def test_future_mutation_cannot_change_past_lifecycle_rows():
    events, bars, features = sample()
    changed = bars.copy()
    changed.loc[6:, 'close'] = 11.0  # prevent future counter expansion
    a = enrich_lifecycle(events, bars, features)
    b = enrich_lifecycle(events, changed, features)
    columns = ['event', 'event_position', 'attempt_number', 'outside_duration', 'old_area_depth_atr', 'counter_expansion_position']
    pd.testing.assert_frame_equal(a.loc[a.event_position <= 5, columns].reset_index(drop=True),
                                  b.loc[b.event_position <= 5, columns].reset_index(drop=True),
                                  check_dtype=False)
    assert 'counter_expansion' in set(a.event)
    assert 'counter_expansion' not in set(b.event)


def test_invalid_counter_window_rejected():
    events, bars, features = sample()
    with pytest.raises(ValueError):
        enrich_lifecycle(events, bars, features, counter_expansion_bars=0)


def test_old_future_columns_are_never_retained_on_failure():
    events, bars, features = sample()
    events['counter_expansion_position'] = 999
    current = enrich_lifecycle(events, bars, features)
    assert pd.isna(current.loc[current.event == 'failure', 'counter_expansion_position'].iloc[0])
    with pytest.raises(ValueError, match='ham yapı'):
        enrich_lifecycle(current, bars, features)
