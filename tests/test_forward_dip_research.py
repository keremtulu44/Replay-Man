import json
from pathlib import Path

import pandas as pd
import pytest

import tools.forward_dip_research as forward


def write_series(root: Path, group: str, asset: str, dates, *, closes=None):
    series = root / group / asset / 'frozen-series'
    (series / 'bars').mkdir(parents=True, exist_ok=True)
    (series / 'series.json').write_text('{"policy":"raw"}\n')
    closes = closes or [10.0] * len(dates)
    frame = pd.DataFrame({'ts_utc': [x.isoformat() for x in dates], 'open': closes,
                          'high': [x + 1 for x in closes], 'low': [x - 1 for x in closes], 'close': closes,
                          'volume': 100, 'asset_id': asset, 'series_id': 'frozen-series', 'interval': '1d'})
    frame.to_csv(series / 'bars' / '1d.csv', index=False)
    return series / 'bars' / '1d.csv'


def test_freeze_blocked_data_future_cutoff_and_append_only_chain(tmp_path, monkeypatch):
    code = tmp_path / 'code.txt'
    code.write_text('unchanged')
    monkeypatch.setattr(forward, 'FROZEN_FILES', (str(code),))
    root, new = tmp_path / 'old', tmp_path / 'new'
    dates = pd.date_range('2026-10-15T21:00:00Z', periods=30, freq='D')
    stock = write_series(root, 'bist_equities', 'BIST_TEST', dates)
    write_series(root, 'bist_indices', 'IDX_XU100', dates)
    frozen = tmp_path / 'freeze.json'
    before = pd.Timestamp('2026-11-19T10:00:00Z')
    forward.create_freeze(root, frozen, now=before)
    with pytest.raises(FileExistsError):
        forward.create_freeze(root, frozen, now=before)
    with pytest.raises(ValueError, match='başladı'):
        forward.create_freeze(root, tmp_path / 'late.json', now=pd.Timestamp('2026-11-21T00:00Z'))
    first = tmp_path / 'one'
    result = forward.observe(frozen, root, new, first, now=before + pd.Timedelta(hours=1))
    assert result['status'] == 'blocked_data' and result['forward_equity_bars'] == 0
    with pytest.raises(ValueError, match='gelecekte'):
        forward.observe(frozen, root, new, tmp_path / 'bad', now=before,
                        as_of=before + pd.Timedelta(days=1))
    future = pd.to_datetime(['2026-11-19T21:00:00Z', '2026-11-20T21:00:00Z'])
    new_file = write_series(new, 'bist_equities', 'BIST_TEST', future)
    # Daily label for Nov 20 is not accepted until the following day at 00:00 Istanbul.
    early = forward.observe(frozen, root, new, tmp_path / 'early', previous=first,
                            now=pd.Timestamp('2026-11-20T20:00:00Z'))
    assert early['forward_equity_bars'] == 0
    later = forward.observe(frozen, root, new, tmp_path / 'two', previous=tmp_path / 'early',
                            now=pd.Timestamp('2026-11-20T22:00:00Z'))
    assert later['status'] == 'collecting' and later['forward_equity_bars'] == 1
    coverage = pd.read_csv(tmp_path / 'two' / 'series_coverage.csv')
    assert coverage.loc[coverage.asset_id == 'BIST_TEST', 'appended_rows'].iloc[0] == 1
    frame = pd.read_csv(new_file)
    frame.loc[0, ['open', 'high', 'low', 'close']] = [20, 21, 19, 20]
    frame.to_csv(new_file, index=False)
    with pytest.raises(ValueError, match='öneki değişmiş'):
        forward.observe(frozen, root, new, tmp_path / 'three', previous=tmp_path / 'two',
                        now=pd.Timestamp('2026-11-21T22:00:00Z'))
    stock.write_text(stock.read_text() + '\n')
    with pytest.raises(ValueError, match='ısınma CSV'):
        forward.verify_freeze(frozen, root)


def test_first_registration_not_backdated_and_future_rows_do_not_leak(tmp_path, monkeypatch):
    code = tmp_path / 'code.txt'; code.write_text('x')
    monkeypatch.setattr(forward, 'FROZEN_FILES', (str(code),))
    root, new = tmp_path / 'old', tmp_path / 'new'
    dates = pd.date_range('2026-10-15T21:00Z', periods=30, freq='D')
    write_series(root, 'bist_equities', 'BIST_TEST', dates)
    write_series(root, 'bist_indices', 'IDX_XU100', dates)
    freeze = tmp_path / 'freeze.json'
    forward.create_freeze(root, freeze, now=pd.Timestamp('2026-11-19T10:00Z'))
    future = pd.date_range('2026-11-19T21:00Z', periods=26, freq='D')
    new_file = write_series(new, 'bist_equities', 'BIST_TEST', future)
    raw = pd.read_csv(new_file)
    raw.loc[0, ['open', 'high', 'low', 'close']] = [9.2, 11, 8, 10]
    raw.to_csv(new_file, index=False)
    early = tmp_path / 'early'
    observed = pd.Timestamp('2026-11-20T22:00Z')
    result = forward.observe(freeze, root, new, early, now=observed)
    assert result['forward_equity_bars'] == 1
    assert result['signal_rows'] >= 1
    signals = pd.read_csv(early / 'signals.csv')
    a = signals.query("variant == 'A_all'").iloc[0]
    assert pd.Timestamp(a.first_observed_at_utc) == observed
    later = tmp_path / 'later'
    forward.observe(freeze, root, new, later, previous=early, now=pd.Timestamp('2026-12-20T00:00Z'))
    outcomes = pd.read_csv(later / 'outcomes.csv')
    choices = outcomes[(outcomes.signal_id == a.signal_id) & (outcomes.horizon == 20)]
    assert set(choices.status) == {'observed'}
    assert not bool(choices.loc[choices.entry == 'next_open', 'registered_before_entry_label'].iloc[0])
    assert bool(choices.loc[choices.entry == 'delayed_open', 'registered_before_entry_label'].iloc[0])
    assert all(pd.to_datetime(choices.first_observed_at_utc, utc=True) == observed)


def test_previous_snapshot_files_cannot_be_silently_modified(tmp_path, monkeypatch):
    code = tmp_path / 'code.txt'; code.write_text('x')
    monkeypatch.setattr(forward, 'FROZEN_FILES', (str(code),))
    root = tmp_path / 'old'; dates = pd.date_range('2026-10-01T21:00Z', periods=30, freq='D')
    write_series(root, 'bist_equities', 'BIST_TEST', dates)
    write_series(root, 'bist_indices', 'IDX_XU100', dates)
    freeze = tmp_path / 'freeze.json'; ts = pd.Timestamp('2026-11-19T12:00Z')
    forward.create_freeze(root, freeze, now=ts)
    out = tmp_path / 'first'; forward.observe(freeze, root, tmp_path / 'new', out, now=ts)
    (out / 'signals.csv').write_text('signal_id,first_observed_at_utc\nfake,2026-11-19T12:00:00Z\n')
    with pytest.raises(ValueError, match='çıktısı değişmiş'):
        forward.observe(freeze, root, tmp_path / 'new', tmp_path / 'second', previous=out,
                        now=ts + pd.Timedelta(hours=1))
    code.write_text('changed')
    with pytest.raises(ValueError, match='kod/plan'):
        forward.verify_freeze(freeze, root)
