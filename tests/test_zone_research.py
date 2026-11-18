import json

import pandas as pd
import pytest

from tools.measure_zone_memory import discover, main
from tools.measure_movement_character import main as movement_main
from tools.summarize_behavior_pilot import main as summarize_main
from tools.measure_zone_universe import main as universe_main


def make_dataset(root):
    path = root / 'bist_equities' / 'BIST_TEST' / 'abc' / 'bars' / '4h.csv'
    path.parent.mkdir(parents=True)
    close = [9, 10, 12, 10, 9, 10, 12, 10, 9, 10, 12, 10, 9, 8, 9, 10, 11, 10, 9, 8] * 2
    frame = pd.DataFrame({'ts_utc': pd.date_range('2026-01-01', periods=len(close), freq='4h', tz='UTC'),
                          'open': close, 'high': [x+.1 for x in close], 'low': [x-.1 for x in close],
                          'close': close, 'volume': [1] * len(close), 'asset_id': 'BIST_TEST',
                          'series_id': 'abc', 'interval': '4h', 'complete': True})
    frame.loc[0, 'complete'] = False
    frame.to_csv(path, index=False)
    return path


def test_pilot_produces_traceable_separate_outputs(tmp_path):
    root, output = tmp_path / 'data', tmp_path / 'result'
    make_dataset(root)
    assert main(['--root', str(root), '--output', str(output), '--symbols', 'BIST_TEST',
                 '--intervals', '4h', '--method', 'percent', '--tolerance', '0.02']) == 0
    manifest = pd.read_csv(output / 'input-manifest.csv')
    assert manifest.loc[0, 'input_rows'] == 40
    assert manifest.loc[0, 'usable_rows'] == 39
    assert len(manifest.loc[0, 'sha256']) == 64
    visits = pd.read_csv(output / 'visits.csv.gz')
    outcomes = pd.read_csv(output / 'outcomes.csv.gz')
    assert len(visits) > 0
    assert 'return' not in visits
    assert len(outcomes) == 5 * len(visits)
    assert set(outcomes.visit_id) == set(visits.visit_id)
    assert json.loads((output / 'experiment-config.json').read_text())['code_sha256']['zone_memory.py']


def test_sloped_and_movement_pipeline_and_hash_guard(tmp_path):
    root, pilot, output = tmp_path / 'data', tmp_path / 'pilot', tmp_path / 'movement'
    path = make_dataset(root)
    assert main(['--root', str(root), '--output', str(pilot), '--symbols', 'BIST_TEST',
                 '--geometry', 'sloped', '--method', 'percent', '--tolerance', '0.02']) == 0
    assert not pd.read_csv(pilot / 'visits.csv.gz').empty
    assert movement_main(['--pilot', str(pilot), '--output', str(output)]) == 0
    features = pd.read_csv(output / 'movement-features.csv.gz')
    assert len(features) == len(pd.read_csv(pilot / 'visits.csv.gz'))
    assert 'return' not in features
    summary = pd.read_csv(output / 'descriptive-5bar.csv')
    assert 'median_approach_direction_return_5bar' in summary
    path.write_bytes(path.read_bytes() + b'\n')
    with pytest.raises(ValueError, match='Girdi değişmiş'):
        movement_main(['--pilot', str(pilot), '--output', str(output)])


def test_behavior_pilot_summary_and_input_integrity(tmp_path):
    root, pilot, movement, summary = (tmp_path / x for x in ['data', 'pilot', 'movement', 'summary'])
    make_dataset(root)
    assert main(['--root', str(root), '--output', str(pilot), '--symbols', 'BIST_TEST',
                 '--geometry', 'dwell', '--method', 'percent', '--tolerance', '0.02']) == 0
    assert movement_main(['--pilot', str(pilot), '--output', str(movement)]) == 0
    assert summarize_main(['--pilot', str(pilot), '--movement', str(movement), '--output', str(summary)]) == 0
    data = pd.read_csv(summary / 'splits.csv')
    assert set(data['mode']) == {'all_visits', 'one_visit_per_bar'}
    assert (data.eligible <= data.visits).all()
    meta = json.loads((summary / 'summary.json').read_text())
    assert meta['unique_asset_interval_positions'] <= meta['input_visits']
    output_file = pilot / 'outcomes.csv.gz'
    output_file.write_bytes(output_file.read_bytes() + b' ')
    with pytest.raises(ValueError, match='değişmiş'):
        summarize_main(['--pilot', str(pilot), '--movement', str(movement), '--output', str(summary)])


def test_universe_research_keeps_bounds_and_missing_benchmark(tmp_path):
    root, output = tmp_path / 'data', tmp_path / 'universe'
    make_dataset(root)
    assert universe_main(['--root', str(root), '--output', str(output), '--kind', 'dwell',
                          '--intervals', '4h']) == 0
    events = pd.read_csv(output / 'events.csv.gz')
    assert not events.empty
    assert events.benchmark_return_5bar.isna().all()
    chosen = events[events.one_per_bar]
    assert not chosen.duplicated(['asset_id', 'interval', 'position']).any()
    metadata = json.loads((output / 'summary.json').read_text())
    assert metadata['benchmark_eligible'] == 0
    bounds = {'train': metadata['boundary_train_end'], 'validation': metadata['boundary_validation_end'],
              'test': metadata['boundary_test_end']}
    for split, group in events[events.eligible].groupby('split'):
        assert (pd.to_datetime(group.end_bar_ts, utc=True) < pd.Timestamp(bounds[split])).all()


def test_universe_representative_and_percent_variant(tmp_path):
    root, output = tmp_path / 'data', tmp_path / 'universe'
    make_dataset(root)
    assert universe_main(['--root', str(root), '--output', str(output), '--kind', 'dwell', '--intervals', '4h',
                          '--method', 'percent', '--tolerance', '0.02', '--representative-only']) == 0
    meta = json.loads((output / 'summary.json').read_text())
    events = pd.read_csv(output / 'events.csv.gz')
    assert meta['zone_method'] == 'percent' and meta['tolerance'] == .02
    assert meta['representative_only'] is True
    assert meta['stored_visits'] == len(events) == meta['one_per_bar']
    assert meta['visits'] >= meta['stored_visits']
    assert set(pd.read_csv(output / 'group-results.csv')['mode']) == {'one_visit_per_bar'}


def test_universe_benchmark_aligns_exact_start_and_end(tmp_path):
    root, output = tmp_path / 'data', tmp_path / 'universe'
    source = make_dataset(root)
    benchmark = root / 'bist_indices' / 'IDX_XU100' / 'series' / 'bars' / '4h.csv'
    benchmark.parent.mkdir(parents=True)
    benchmark.write_bytes(source.read_bytes())
    assert universe_main(['--root', str(root), '--output', str(output), '--kind', 'dwell',
                          '--intervals', '4h']) == 0
    events = pd.read_csv(output / 'events.csv.gz')
    comparable = events[events.eligible & events.benchmark_return_5bar.notna()]
    assert not comparable.empty
    assert comparable.directional_excess.abs().max() < 1e-10


def test_ambiguous_series_is_not_silently_selected(tmp_path):
    path = make_dataset(tmp_path)
    other = path.parents[1].parent / 'other' / 'bars' / '4h.csv'
    other.parent.mkdir(parents=True)
    other.write_bytes(path.read_bytes())
    with pytest.raises(ValueError, match='tam bir seri'):
        discover(tmp_path, ['BIST_TEST'], ['4h'])
