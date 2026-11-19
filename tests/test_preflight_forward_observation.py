import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest

import tools.forward_dip_research as forward
from replayman.catalog import load_catalog
from replayman.config import PATH_FIELDS, Settings
from replayman.runner import check_plan
from replayman.series import POLICY_FIELDS, build_series
from tools.preflight_forward_observation import _raw_checks, parse_calendar, preflight, timing_windows
from tools.verify_forward_snapshot_preflight import verify as verify_snapshot_preflight


def write_series(root, group, asset, dates):
    series = root / group / asset / 'frozen-series'
    (series / 'bars').mkdir(parents=True, exist_ok=True)
    (series / 'series.json').write_text('{"policy":"raw"}\n')
    frame = pd.DataFrame({'ts_utc': [x.isoformat() for x in dates], 'open': 10., 'high': 11.,
                          'low': 9., 'close': 10., 'volume': 1, 'dividends': 0., 'stock_splits': 0.,
                          'asset_id': asset, 'series_id': 'frozen-series', 'interval': '1d'})
    path = series / 'bars/1d.csv'
    frame.to_csv(path, index=False)
    return path


def write_4h_series(root, group, asset, dates):
    series = root / group / asset / 'frozen-series'
    (series / 'bars').mkdir(parents=True, exist_ok=True)
    (series / 'series.json').write_text('{"policy":"raw"}\n')
    frame = pd.DataFrame({'ts_utc': [x.isoformat() for x in dates], 'open': 10., 'high': 11.,
                          'low': 9., 'close': 10., 'volume': 1, 'dividends': 0., 'stock_splits': 0.,
                          'asset_id': asset, 'series_id': 'frozen-series', 'interval': '4h',
                          'complete': True, 'bar_count': 4, 'expected_bars': 4, 'derived_from': '1h'})
    path = series / 'bars/4h.csv'
    frame.to_csv(path, index=False)
    return path


def setup_frozen(tmp_path, monkeypatch, *, include_4h=False):
    code = tmp_path / 'frozen-code.py'
    code.write_text('unchanged')
    monkeypatch.setattr(forward, 'FROZEN_FILES', (str(code),))
    root, new = tmp_path / 'old', tmp_path / 'new'
    dates = pd.date_range('2026-10-15T21:00Z', periods=30, freq='D')
    for group, asset in [('bist_equities', 'BIST_TEST'), ('bist_indices', 'IDX_XU100')]:
        write_series(root, group, asset, dates)
        if include_4h:
            write_4h_series(root, group, asset, dates - pd.Timedelta(hours=14, minutes=30))
    freeze = tmp_path / 'freeze.json'
    forward.create_freeze(root, freeze, now=pd.Timestamp('2026-11-19T13:00Z'))
    previous = tmp_path / 'initial'
    forward.observe(freeze, root, new, previous, now=pd.Timestamp('2026-11-19T14:00Z'))
    return freeze, root, new, previous


def make_new_and_calendar(tmp_path, new):
    dates = pd.to_datetime(['2026-11-15T21:00:00Z', '2026-11-16T21:00:00Z', '2026-11-19T21:00:00Z'])
    stock = write_series(new, 'bist_equities', 'BIST_TEST', dates)
    write_series(new, 'bist_indices', 'IDX_XU100', dates)
    calendar = tmp_path / 'calendar.json'
    calendar.write_text(json.dumps({'schema_version': 1, 'source': 'synthetic test only',
                                    'coverage_start_utc': '2026-11-12T00:00:00Z',
                                    'coverage_end_utc': '2026-11-23T00:00:00Z',
                                    'labels': {'1d': [d.isoformat() for d in dates]}}))
    return stock, calendar


def test_example_downloader_config_is_isolated_and_matches_locked_series():
    root = Path(__file__).resolve().parents[1]
    fresh = (root / 'data/forward-ohlcv').resolve()
    config = Settings.load(root / 'config/forward-settings.example.json', base_dir=root)
    baseline = Settings.load(root / 'config/settings.json', base_dir=root)
    assert all(getattr(config, field).resolve().is_relative_to(fresh) for field in PATH_FIELDS)
    assert config.output_dir.resolve() == config.derived_dir.resolve() == fresh
    assert all(getattr(config, field) == getattr(baseline, field) for field in POLICY_FIELDS)
    assert config.derive_timeframes and config.intervals == ('1h', '1d')
    plan = check_plan(config, root / 'data/universe.csv')
    freeze = json.loads((root / 'research/measurements/dip-research/forward-freeze.json').read_text())
    assert plan['network_requests'] == 0
    assert all(plan['series_ids'].get(row['asset_id']) == row['series_id'] for row in freeze['baseline_files'])
    assets, _ = load_catalog(root / 'data/universe.csv')
    assets_by_id = {asset.id: asset for asset in assets}
    for row in freeze['baseline_files']:
        manifest = build_series(assets_by_id[row['asset_id']], config).manifest
        contents = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
        assert hashlib.sha256(contents).hexdigest() == row['series_manifest_sha256']


def test_missing_new_data_and_calendar_are_not_treated_as_ready(tmp_path, monkeypatch):
    freeze, old, new, prev = setup_frozen(tmp_path, monkeypatch)
    now = pd.Timestamp('2026-11-19T18:00Z')
    result = preflight(freeze, old, new, prev, now=now)
    assert result['status'] == 'blocked_data'
    assert result['new_file_counts'] == {'valid': 0, 'missing': 2, 'invalid': 0}
    assert result['prior_prefix_mismatches'] == 0 and result['eligible_forward_equity_rows'] == 0
    assert result['expected_label_discrepancies'] is None and not result['calendar']['independently_verified']
    assert 'expected_complete_bar_calendar_not_provided' in result['blockers']
    with pytest.raises(ValueError, match='ayrı olmalı'):
        preflight(freeze, old, old, prev, now=now)
    with pytest.raises(ValueError, match='gelecekte'):
        preflight(freeze, old, new, prev, now=now, as_of=now + pd.Timedelta(seconds=1))


def test_calendar_gaps_actions_and_manual_review_are_distinct(tmp_path, monkeypatch):
    freeze, old, new, prev = setup_frozen(tmp_path, monkeypatch)
    stock, calendar = make_new_and_calendar(tmp_path, new)
    before = preflight(freeze, old, new, prev, calendar_path=calendar, now=pd.Timestamp('2026-11-19T18:00Z'))
    assert before['status'] == 'awaiting_forward_start' and before['eligible_forward_equity_rows'] == 0
    assert before['expected_label_discrepancies'] == 0
    after = preflight(freeze, old, new, prev, calendar_path=calendar, now=pd.Timestamp('2026-11-20T22:00Z'))
    assert after['status'] == 'manual_review_required' and after['eligible_forward_equity_rows'] == 1
    assert after['calendar']['status'] == 'provided_not_independently_verified'
    original = pd.read_csv(stock)
    original.iloc[1:].to_csv(stock, index=False)
    gap = preflight(freeze, old, new, prev, calendar_path=calendar, now=pd.Timestamp('2026-11-20T22:00Z'))
    assert gap['status'] == 'blocked_gaps' and gap['expected_label_discrepancies'] == 1
    changed = original.copy()
    changed.loc[0, 'dividends'] = 1.
    changed.to_csv(stock, index=False)
    actions = preflight(freeze, old, new, prev, calendar_path=calendar, now=pd.Timestamp('2026-11-20T22:00Z'))
    assert actions['status'] == 'blocked_corporate_actions' and actions['corporate_action_events'] == 1
    original.drop(columns=['stock_splits']).to_csv(stock, index=False)
    unknown = preflight(freeze, old, new, prev, calendar_path=calendar, now=pd.Timestamp('2026-11-20T22:00Z'))
    assert unknown['status'] == 'blocked_corporate_actions' and unknown['equity_series_action_status_unknown'] == 1


def test_policy_and_previous_prefix_tampering_block(tmp_path, monkeypatch):
    freeze, old, new, prev = setup_frozen(tmp_path, monkeypatch)
    stock, calendar = make_new_and_calendar(tmp_path, new)
    later = tmp_path / 'later'
    forward.observe(freeze, old, new, later, previous=prev, now=pd.Timestamp('2026-11-20T22:00Z'))
    raw = pd.read_csv(stock)
    raw.loc[0, ['open', 'high', 'low', 'close']] = [20., 21., 19., 20.]
    raw.to_csv(stock, index=False)
    result = preflight(freeze, old, new, later, calendar_path=calendar, now=pd.Timestamp('2026-11-21T22:00Z'))
    assert result['status'] == 'blocked_integrity' and result['prior_prefix_mismatches'] == 1
    (stock.parent.parent / 'series.json').write_text('{"policy":"changed"}')
    invalid = preflight(freeze, old, new, prev, calendar_path=calendar, now=pd.Timestamp('2026-11-20T22:00Z'))
    assert invalid['status'] == 'blocked_integrity' and invalid['new_file_counts']['invalid'] == 1


@pytest.mark.parametrize('problem', ['duplicate', 'unsorted', 'naive_timestamp', 'missing_ohlc', 'negative_ohlc', 'geometry'])
def test_invalid_new_price_data_is_blocked_end_to_end(tmp_path, monkeypatch, problem):
    freeze, old, new, prev = setup_frozen(tmp_path, monkeypatch)
    stock, calendar = make_new_and_calendar(tmp_path, new)
    raw = pd.read_csv(stock)
    if problem == 'duplicate':
        raw.loc[1, 'ts_utc'] = raw.loc[0, 'ts_utc']
    elif problem == 'unsorted':
        raw = raw.iloc[::-1]
    elif problem == 'naive_timestamp':
        raw['ts_utc'] = raw.ts_utc.str.replace('+00:00', '', regex=False)
    elif problem == 'missing_ohlc':
        raw.loc[0, 'close'] = None
    elif problem == 'negative_ohlc':
        raw.loc[0, ['open', 'high', 'low', 'close']] = [-10., -9., -11., -10.]
    elif problem == 'geometry':
        raw.loc[0, 'high'] = 8.
    raw.to_csv(stock, index=False)
    result = preflight(freeze, old, new, prev, calendar_path=calendar, now=pd.Timestamp('2026-11-20T22:00Z'))
    assert result['status'] == 'blocked_integrity'
    assert result['new_file_counts']['invalid'] == 1
    row = next(r for r in result['series'] if r['asset_id'] == 'BIST_TEST')
    assert row['error'] and row['new_file_status'] == 'invalid'


def test_daily_complete_flag_matches_loader_and_cannot_hide_a_gap(tmp_path, monkeypatch):
    freeze, old, new, prev = setup_frozen(tmp_path, monkeypatch)
    stock, calendar = make_new_and_calendar(tmp_path, new)
    frame = pd.read_csv(stock)
    frame['complete'] = [False, True, True]
    frame.to_csv(stock, index=False)
    result = preflight(freeze, old, new, prev, calendar_path=calendar, now=pd.Timestamp('2026-11-20T22:00Z'))
    assert result['status'] == 'blocked_gaps' and result['expected_label_discrepancies'] == 1
    row = next(r for r in result['series'] if r['asset_id'] == 'BIST_TEST')
    assert row['partial_mature_rows_excluded'] == 1 and row['eligible_rows'] == 2
    frame['complete'] = ['not-known', 'True', 'True']
    frame.to_csv(stock, index=False)
    invalid = preflight(freeze, old, new, prev, calendar_path=calendar, now=pd.Timestamp('2026-11-20T22:00Z'))
    assert invalid['status'] == 'blocked_integrity' and invalid['new_file_counts']['invalid'] == 1


@pytest.mark.parametrize('problem', ['count', 'expected', 'derived', 'missing_count', 'missing_expected', 'missing_derived', 'flag'])
def test_inconsistent_4h_derivation_is_blocked_end_to_end(tmp_path, monkeypatch, problem):
    freeze, old, new, prev = setup_frozen(tmp_path, monkeypatch, include_4h=True)
    _, calendar = make_new_and_calendar(tmp_path, new)
    dates = pd.to_datetime(['2026-11-16T06:30Z', '2026-11-16T10:30Z', '2026-11-20T06:30Z'])
    stock = write_4h_series(new, 'bist_equities', 'BIST_TEST', dates)
    write_4h_series(new, 'bist_indices', 'IDX_XU100', dates)
    calendar_data = json.loads(calendar.read_text())
    calendar_data['labels']['4h'] = [date.isoformat() for date in dates]
    calendar.write_text(json.dumps(calendar_data))
    now = pd.Timestamp('2026-11-20T22:00Z')
    assert preflight(freeze, old, new, prev, calendar_path=calendar, now=now)['status'] == 'manual_review_required'
    raw = pd.read_csv(stock)
    if problem == 'count':
        raw.loc[0, 'bar_count'] = 3
    elif problem == 'expected':
        raw.loc[0, 'expected_bars'] = 3
    elif problem == 'derived':
        raw.loc[0, 'derived_from'] = '1d'
    elif problem == 'flag':
        raw.loc[0, 'complete'] = False
    else:
        raw = raw.drop(columns={'missing_count': 'bar_count', 'missing_expected': 'expected_bars',
                                'missing_derived': 'derived_from'}[problem])
    raw.to_csv(stock, index=False)
    result = preflight(freeze, old, new, prev, calendar_path=calendar, now=now)
    assert result['status'] == 'blocked_integrity' and result['new_file_counts']['invalid'] == 1
    row = next(r for r in result['series'] if r['asset_id'] == 'BIST_TEST' and r['interval'] == '4h')
    assert 'türetim' in row['error']


def test_synthetic_two_interval_preflight_and_snapshot_chain(tmp_path, monkeypatch):
    freeze, old, new, prev = setup_frozen(tmp_path, monkeypatch, include_4h=True)
    _, calendar = make_new_and_calendar(tmp_path, new)
    dates = pd.to_datetime(['2026-11-16T06:30Z', '2026-11-16T10:30Z', '2026-11-20T06:30Z'])
    write_4h_series(new, 'bist_equities', 'BIST_TEST', dates)
    write_4h_series(new, 'bist_indices', 'IDX_XU100', dates)
    calendar_data = json.loads(calendar.read_text())
    calendar_data['labels']['4h'] = [date.isoformat() for date in dates]
    calendar.write_text(json.dumps(calendar_data))
    cutoff = pd.Timestamp('2026-11-20T22:00Z')
    checked = preflight(freeze, old, new, prev, calendar_path=calendar, now=cutoff)
    assert checked['status'] == 'manual_review_required' and checked['eligible_forward_equity_rows'] == 2
    report = tmp_path / 'preflight.json'
    report.write_text(json.dumps(checked))
    snapshot = tmp_path / 'snapshot'
    result = forward.observe(freeze, old, new, snapshot, previous=prev, as_of=cutoff, now=cutoff + pd.Timedelta(minutes=1))
    assert result['status'] == 'collecting' and result['forward_equity_bars'] == 2
    assert verify_snapshot_preflight(report, snapshot, prev, freeze, now=cutoff + pd.Timedelta(minutes=2))['series_compared'] == 4


def test_snapshot_matches_inspected_cutoff_and_inputs(tmp_path, monkeypatch):
    freeze, old, new, prev = setup_frozen(tmp_path, monkeypatch)
    stock, calendar = make_new_and_calendar(tmp_path, new)
    cutoff = pd.Timestamp('2026-11-20T22:00Z')
    checked = preflight(freeze, old, new, prev, calendar_path=calendar, now=cutoff)
    report = tmp_path / 'preflight.json'
    report.write_text(json.dumps(checked))
    snapshot = tmp_path / 'observation'
    forward.observe(freeze, old, new, snapshot, previous=prev, as_of=cutoff, now=cutoff + pd.Timedelta(minutes=1))
    verification = verify_snapshot_preflight(report, snapshot, prev, freeze, now=cutoff + pd.Timedelta(minutes=2))
    assert verification['status'] == 'consistent_manual_review_still_required'
    assert verification['series_compared'] == 2 and not verification['external_timestamp_attestation']
    assert pd.Timestamp(verification['verified_at_utc']) == cutoff + pd.Timedelta(minutes=2)
    changed = pd.read_csv(stock)
    changed.loc[0, ['open', 'high', 'low', 'close']] = [20., 21., 19., 20.]
    changed.to_csv(stock, index=False)
    altered = tmp_path / 'altered'
    forward.observe(freeze, old, new, altered, previous=prev, as_of=cutoff, now=cutoff + pd.Timedelta(minutes=3))
    with pytest.raises(ValueError, match='girdisi'):
        verify_snapshot_preflight(report, altered, prev, freeze, now=cutoff + pd.Timedelta(minutes=4))
    (snapshot / 'signals.csv').write_text('tampered')
    with pytest.raises(ValueError, match='çıktısı değişmiş'):
        verify_snapshot_preflight(report, snapshot, prev, freeze, now=cutoff + pd.Timedelta(minutes=4))


def test_snapshot_verifier_rejects_new_cutoff_and_missing_new_file(tmp_path, monkeypatch):
    freeze, old, new, prev = setup_frozen(tmp_path, monkeypatch)
    _, calendar = make_new_and_calendar(tmp_path, new)
    cutoff = pd.Timestamp('2026-11-20T22:00Z')
    report = tmp_path / 'preflight.json'
    report.write_text(json.dumps(preflight(freeze, old, new, prev, calendar_path=calendar, now=cutoff)))
    later_cutoff = tmp_path / 'later-cutoff'
    forward.observe(freeze, old, new, later_cutoff, previous=prev, now=cutoff + pd.Timedelta(minutes=1))
    with pytest.raises(ValueError, match='zaman|kesit'):
        verify_snapshot_preflight(report, later_cutoff, prev, freeze, now=cutoff + pd.Timedelta(minutes=2))
    benchmark = next(new.glob('bist_indices/IDX_XU100/*/bars/1d.csv'))
    benchmark.unlink()
    missing = tmp_path / 'missing'
    forward.observe(freeze, old, new, missing, previous=prev, as_of=cutoff, now=cutoff + pd.Timedelta(minutes=3))
    with pytest.raises(ValueError, match='seri listesi'):
        verify_snapshot_preflight(report, missing, prev, freeze, now=cutoff + pd.Timedelta(minutes=4))


def test_timing_zero_window_is_not_a_positive_window():
    daily = pd.DataFrame({'ts_utc': pd.to_datetime(['2026-01-01T00:00Z', '2026-01-02T00:00Z', '2026-01-04T00:00Z'])})
    assert timing_windows(daily, '1d', 1) == {'windows': 2, 'negative': 0, 'zero': 1, 'positive': 1}
    assert timing_windows(daily, '1d', 2) == {'windows': 1, 'negative': 0, 'zero': 0, 'positive': 1}
    hourly = pd.DataFrame({'ts_utc': pd.to_datetime(['2026-01-01T00:00Z', '2026-01-01T02:00Z'])})
    assert timing_windows(hourly, '4h', 1)['negative'] == 1


def test_partial_4h_bars_and_corporate_actions_are_not_silently_counted(tmp_path):
    path = tmp_path / '4h.csv'
    times = pd.to_datetime(['2026-11-16T06:30Z', '2026-11-16T10:30Z', '2026-11-17T06:30Z', '2026-11-18T06:30Z'])
    pd.DataFrame({'ts_utc': times, 'open': [10., 10., 10., 10.], 'high': [11.] * 4, 'low': [9.] * 4,
                  'close': [10., 10., None, 10.], 'complete': [False, True, True, True],
                  'bar_count': [3, 4, 4, 4], 'expected_bars': 4, 'derived_from': '1h',
                  'dividends': [0., 1., 0., 0.], 'stock_splits': [0., 0., 0., 0.]}).to_csv(path, index=False)
    result = _raw_checks(path, {'interval': '4h', 'kind': 'equity'}, pd.Timestamp('2026-11-13T10:30Z'),
                         pd.Timestamp('2026-11-17T12:00Z'))
    assert result['partial_mature_rows_excluded'] == 1
    assert result['bad_complete_rows'] == 1 and result['unmatured_new_rows'] == 1
    assert result['corporate_actions'][0]['field'] == 'dividends'
    assert not result['action_unknown'] and result['invalid_completion_flags'] == 0
    assert result['invalid_aggregation_rows'] == 0
    frame = pd.read_csv(path)
    frame['complete'] = frame.complete.astype(str)
    frame.loc[1, 'complete'] = 'unknown'
    frame.to_csv(path, index=False)
    invalid = _raw_checks(path, {'interval': '4h', 'kind': 'equity'}, pd.Timestamp('2026-11-13T10:30Z'),
                          pd.Timestamp('2026-11-17T12:00Z'))
    assert invalid['invalid_completion_flags'] == 1


def test_calendar_requires_coverage_unique_timezone_and_source(tmp_path):
    path = tmp_path / 'calendar.json'
    data = {'schema_version': 1, 'source': 'test', 'coverage_start_utc': '2026-01-01T00:00Z',
            'coverage_end_utc': '2026-02-01T00:00Z', 'labels': {'1d': []}}
    path.write_text(json.dumps(data))
    parsed = parse_calendar(path, intervals={'1d'}, first_baseline=pd.Timestamp('2026-01-01T00:00Z'),
                            cutoff=pd.Timestamp('2026-01-20T00:00Z'))
    assert parsed['labels']['1d'].empty
    data['labels']['1d'] = ['2026-01-02T00:00Z', '2026-01-02T00:00Z']
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match='yinelenmiş'):
        parse_calendar(path, intervals={'1d'}, first_baseline=pd.Timestamp('2026-01-01T00:00Z'), cutoff=pd.Timestamp('2026-01-20T00:00Z'))
    data['labels']['1d'] = ['2026-01-02T00:00:00']
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match='zaman dilimi'):
        parse_calendar(path, intervals={'1d'}, first_baseline=pd.Timestamp('2026-01-01T00:00Z'), cutoff=pd.Timestamp('2026-01-20T00:00Z'))
