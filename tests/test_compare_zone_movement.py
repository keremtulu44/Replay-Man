import pandas as pd
import pytest

from tools.compare_zone_movement import FLAGS, KINDS, make_events, path_labels, predictions, paired_scores, weekly_intervals


def row(kind, pos, split='train', side=1, y=.01, progress='rising', ts=None):
    return {'asset_id':'A', 'interval':'1d', 'position':pos, 'kind':kind, 'split':split,
            'approach_direction':side, 'directional_excess':y, 'return_5bar':.02,
            'bar_ts':pd.Timestamp(ts or '2026-01-01', tz='UTC'), 'progress_group':progress}


def test_deduplicates_prioritizes_and_keeps_same_side_only():
    f = pd.DataFrame([row('oyalanma', 1), row('yatay', 1), row('egimli', 1, side=-1, y=-.01),
                      row('yatay', 2), row('oyalanma', 2, split='test')])
    result, conflicts = make_events(f)
    assert conflicts == 1 and len(result) == 1
    assert result.iloc[0].anchor_kind == 'yatay'
    assert result.iloc[0][FLAGS].tolist() == [1, 1, 0, 0]
    rev, _ = make_events(f, list(reversed(KINDS)))
    assert rev.iloc[0].anchor_kind == 'egimli'
    assert rev.iloc[0][FLAGS].tolist() == [0, 0, 0, 1]


def test_inconsistent_same_bar_result_rejected():
    f = pd.DataFrame([row('yatay', 1), row('oyalanma', 1, y=.03)])
    with pytest.raises(ValueError, match='sonuç farklı'):
        make_events(f)


def test_train_only_and_fallback_and_paired_comparisons():
    rows = []
    for split, val in [('train', .01), ('validation', .2), ('test', -.2)]:
        for i, side in enumerate([1, -1]):
            for pos in range(2):
                rows.append({'interval':'1d', 'split':split, 'asset_id':f'A{i}', 'position':pos,
                             'bar_ts':pd.Timestamp('2026-01-01', tz='UTC'), 'approach_direction':side,
                             'progress_group':'rising', 'path_group':'direct', 'directional_excess':val * side,
                             **dict(zip(FLAGS, [1,0,0,0]))})
    pred, score = predictions(pd.DataFrame(rows), min_train=3)
    assert (score.fallback_fraction == 1).all()
    assert (pred.prediction_combined == pred.approach_direction * .01).all()
    assert (paired_scores(pred).mae_improvement == 0).all()
    expanded = pd.concat([pred.assign(bar_ts=pd.Timestamp('2026-01-01', tz='UTC') + pd.Timedelta(weeks=i))
                          for i in range(6)], ignore_index=True)
    ci = weekly_intervals(expanded, draws=20, seed=1)
    assert len(ci) == 18
    pd.testing.assert_frame_equal(ci, weekly_intervals(expanded, draws=20, seed=1))
    assert (ci[['low', 'high']] == 0).all().all()


def test_path_uses_only_pre_touch_closes_and_unknown_for_no_path():
    prices = pd.Series([100.0 + i for i in range(20)])
    base = path_labels(prices)
    assert base.loc[11, 'path_group'] == 'direct'
    changed = prices.copy()
    changed.iloc[11:] = -100
    pd.testing.assert_series_equal(base.iloc[11], path_labels(changed).iloc[11])
    assert path_labels(pd.Series([100.] * 20)).iloc[15].path_group == 'unknown'
