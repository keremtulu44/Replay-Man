import pandas as pd
import pytest

from replayman.movement_character import approach_character


def bars():
    c = [float(x) for x in range(10, 50)]
    return pd.DataFrame({'ts_utc': pd.date_range('2026-01-01', periods=len(c), freq='h', tz='UTC'),
                         'high': [x + 1 for x in c], 'low': [x - 1 for x in c], 'close': c})


def test_movement_features_use_only_bars_before_touch():
    frame = bars()
    visits = pd.DataFrame([{'visit_id': 'v1', 'position': 20, 'center': 35, 'slope_per_bar': .1}])
    result = approach_character(frame, visits).iloc[0]
    assert result.status == 'observed'
    assert result.known_at_position == 19
    assert result.approach_direction == 1
    assert result.prior_efficiency == 1
    assert result.recent_efficiency == 1
    assert result.progress_change_atr == pytest.approx(0)
    assert result.direction_changes_10 == 0
    assert result.max_pullback_atr_10 == 0
    changed = frame.copy()
    changed.loc[20:, ['high', 'low', 'close']] *= 10
    pd.testing.assert_frame_equal(approach_character(frame, visits), approach_character(changed, visits))
    pd.testing.assert_frame_equal(approach_character(frame, visits), approach_character(frame.iloc[:21], visits))


def test_insufficient_and_invalid_positions():
    visits = pd.DataFrame([{'visit_id': 'v', 'position': 3, 'center': 12}])
    assert approach_character(bars(), visits).iloc[0].status == 'insufficient_history'
    visits.loc[0, 'position'] = 99
    with pytest.raises(ValueError, match='veri dışında'):
        approach_character(bars(), visits)
