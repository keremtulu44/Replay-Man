import pandas as pd
import pytest

from tools.analyze_zone_philosophy import overlaps, surface, weekly_bootstrap


def event(kind, pos, direction, progress, memory='1+', value=.02, split='test'):
    return {'kind': kind, 'asset_id': 'A', 'interval': '1d', 'position': pos,
            'bar_ts': pd.Timestamp('2026-01-01', tz='UTC') + pd.Timedelta(days=pos * 7),
            'memory_group': memory, 'progress_group': progress, 'approach_direction': direction,
            'return_5bar': value, 'directional_excess': direction * value, 'split': split}


def test_surface_counts_assets_and_directional_return():
    data = pd.DataFrame([event('yatay', n, 1, 'rising') for n in range(3)])
    row = surface(data).iloc[0]
    assert row['n'] == 3 and row.assets == 1 and row.assets_3plus == 1
    assert row.asset_positive == 1
    assert row.median_directional_return == pytest.approx(.02)


def test_overlap_same_bar_same_direction_and_mismatch_detection():
    rows = [event('yatay', 0, 1, 'rising'), event('oyalanma', 0, 1, 'rising'),
            event('yatay', 1, 1, 'rising'), event('oyalanma', 1, -1, 'falling')]
    df = pd.DataFrame(rows)
    row = overlaps(df).iloc[0]
    assert row.same_bar == 2 and row.same_side == 1 and row.same_side_and_progress == 1
    df.loc[1, 'return_5bar'] = .03
    with pytest.raises(ValueError, match='ileri hisse sonucu farklı'):
        overlaps(df)


def test_weekly_bootstrap_is_seeded_and_keeps_groups():
    rows = []
    for week in range(8):
        rows.extend([event('oyalanma', week, 1, 'rising', value=.03),
                     event('oyalanma', week, 1, 'falling', value=.01),
                     event('oyalanma', week, 1, 'rising', memory='0', value=.02)])
    data = pd.DataFrame(rows)
    first = weekly_bootstrap(data, draws=25, seed=3)
    pd.testing.assert_frame_equal(first, weekly_bootstrap(data, draws=25, seed=3))
    row = first[first.comparison == 'rising_minus_falling_memory_1plus'].iloc[0]
    assert row.n_left == 8 and row.n_right == 8 and row.weeks == 8
    assert row.median_difference == pytest.approx(.02)
    assert row.week_bootstrap_2_5pct == pytest.approx(.02)
