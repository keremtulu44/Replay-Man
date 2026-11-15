import csv
import sqlite3
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest

from replayman.catalog import load_catalog
from replayman.errors import InvalidData
from replayman.normalize import merge_save_prices, normalize_prices
from replayman.runner import Downloader
from replayman.series import POLICY_FIELDS, build_series, derived_path, price_path, publish_manifest, quality_path
from replayman.state import State, TaskScope


class RecordingProvider:
    def __init__(self):
        self.calls = []

    def fetch(self, asset, interval, start, end, before_request=None):
        self.calls.append((asset.id, asset.yahoo_symbol, interval))
        if before_request:
            before_request()
        frame = pd.DataFrame(
            {"Open": [10], "High": [11], "Low": [9], "Close": [10.5], "Volume": [100]},
            index=pd.DatetimeIndex([pd.Timestamp(start) + pd.Timedelta(hours=1)], tz="UTC"),
        )
        return SimpleNamespace(frame=frame, from_cache=False, metadata={})


def clock_pair():
    now = [1_000_000.0]
    return lambda: now[0], lambda seconds: now.__setitem__(0, now[0] + seconds)


def snapshot(state):
    return {
        (r["asset_id"], r["series_id"], r["interval"], r["start"], r["end"]): dict(r)
        for r in state.all_tasks()
    }


def test_selected_run_and_retry_do_not_touch_old_queue(settings, catalog_path):
    clock, sleep = clock_pair()
    provider = RecordingProvider()
    first = Downloader(settings, catalog_path, provider=provider, clock=clock, sleep=sleep).run(
        limit=2, intervals=("1h", "1d"), max_requests=1,
    )
    assert first["status"] == "limited"
    with State(settings.state_path, clock=clock) as state:
        pairs = dict.fromkeys((r["asset_id"], r["series_id"]) for r in state.all_tasks()
                              if r["asset_id"] in {"BIST_ASELS", "IDX_XU100"} and r["interval"] == "1h")
        scope = TaskScope(tuple(pairs), ("1h",))
        due = state.due_tasks(clock(), 3, scope=scope)
        wanted = {("BIST_ASELS", "1h"), ("IDX_XU100", "1h")}
        failures = [next(task for task in due if (task.asset_id, task.interval) == key) for key in wanted]
        selected_scope = TaskScope(((("IDX_XU100"), scope.asset_series[1][1]),), ("1d",))
        failures.extend(state.due_tasks(clock(), 3, scope=selected_scope)[:1])
        assert len(failures) == 3
        for task in failures:
            state.mark_failed(task, "transient", "test failure")
        before = snapshot(state)
    provider.calls.clear()
    selected = Downloader(settings, catalog_path, provider=provider, clock=clock, sleep=sleep).run(
        symbols=["XU100"], intervals=("1d",), retry_failed=True,
    )
    assert selected["status"] == "completed"
    assert provider.calls and all(call[0] == "IDX_XU100" and call[2] == "1d" for call in provider.calls)
    assert selected["task_counts"] == {"complete": 1}
    assert selected["queue_task_counts"]["failed"] == 2
    with State(settings.state_path, clock=clock) as state:
        after = snapshot(state)
    selected_ids = set(selected["scope"]["asset_ids"])
    for key, row in before.items():
        if key[0] not in selected_ids or key[2] != "1d":
            assert after[key] == row


def test_symbol_and_policy_changes_create_separate_series(settings, catalog_path):
    clock, sleep = clock_pair()
    provider = RecordingProvider()
    assets, _ = load_catalog(catalog_path, limit=1)
    asset = assets[0]
    original = build_series(asset, settings)
    Downloader(settings, catalog_path, provider=provider, clock=clock, sleep=sleep).run(limit=1, intervals=("1d",))
    original_path = price_path(settings, asset, original, "1d")
    original_bytes = original_path.read_bytes()

    rows = list(csv.DictReader(catalog_path.open(encoding="utf-8")))
    fields = list(rows[0])
    rows[0]["yahoo_symbol"] = "THYAO.IS"
    with catalog_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)
    changed_asset = load_catalog(catalog_path, limit=1)[0][0]
    changed = build_series(changed_asset, settings)
    Downloader(settings, catalog_path, provider=provider, clock=clock, sleep=sleep).run(limit=1, intervals=("1d",))
    assert changed.id != original.id
    assert original_path.read_bytes() == original_bytes
    assert pd.read_csv(price_path(settings, changed_asset, changed, "1d"))["symbol"].iloc[0] == "THYAO.IS"

    for field in POLICY_FIELDS:
        alternate = settings.with_overrides(**{field: not getattr(settings, field)})
        assert build_series(changed_asset, alternate).id != changed.id
    adjusted_settings = settings.with_overrides(auto_adjust=True)
    adjusted = build_series(changed_asset, adjusted_settings)
    Downloader(adjusted_settings, catalog_path, provider=provider, clock=clock, sleep=sleep).run(limit=1, intervals=("1d",))
    assert adjusted.id not in {original.id, changed.id}
    frame = pd.read_csv(price_path(settings, changed_asset, adjusted, "1d"))
    assert bool(frame["auto_adjust"].iloc[0])
    with State(settings.state_path) as state:
        assert len({r["series_id"] for r in state.all_tasks()}) == 3


def test_manifest_conflict_does_not_overwrite_existing_series(settings, catalog_path):
    asset = load_catalog(catalog_path, limit=1)[0][0]
    series = build_series(asset, settings)
    path = publish_manifest(settings, asset, series)
    before = path.read_bytes()
    path.write_text('{"series_id": "different", "schema_version": 1}\n', encoding="utf-8")
    conflict = path.read_bytes()
    with pytest.raises(ValueError, match="manifesti uyuşmuyor"):
        publish_manifest(settings, asset, series)
    assert path.read_bytes() == conflict
    path.write_bytes(before)
    assert publish_manifest(settings, asset, series) == path


def test_derived_files_follow_source_series(settings, catalog_path):
    clock, sleep = clock_pair()
    provider = RecordingProvider()
    downloader = Downloader(settings, catalog_path, provider=provider, clock=clock, sleep=sleep)
    summary = downloader.run(symbols=["GOLD"], intervals=("1h", "1d"))
    asset = load_catalog(catalog_path, symbols=["GOLD"])[0][0]
    series_id = summary["scope"]["series_ids"]["METAL_GOLD"]
    directory = derived_path(settings, asset, build_series(asset, settings))
    assert directory == settings.derived_dir / "metals" / "METAL_GOLD" / series_id / "bars"
    assert (directory / "2h.csv").exists()
    assert (pd.read_csv(directory / "2h.csv")["series_id"] == series_id).all()
    assert (quality_path(settings, asset, build_series(asset, settings)) / "daily_comparison.csv").exists()
    original_bytes = {path.name: path.read_bytes() for path in directory.glob("*.csv")}

    adjusted = settings.with_overrides(auto_adjust=True)
    changed = Downloader(adjusted, catalog_path, provider=provider, clock=clock, sleep=sleep).run(
        symbols=["GOLD"], intervals=("1h", "1d"),
    )
    changed_id = changed["scope"]["series_ids"]["METAL_GOLD"]
    changed_directory = derived_path(adjusted, asset, build_series(asset, adjusted))
    assert changed_id != series_id
    assert changed_directory != directory
    assert (pd.read_csv(changed_directory / "2h.csv")["series_id"] == changed_id).all()
    assert {path.name: path.read_bytes() for path in directory.glob("*.csv")} == original_bytes


def test_legacy_tasks_are_preserved_not_assigned_to_new_series(settings):
    settings.state_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(settings.state_path) as conn:
        conn.execute("CREATE TABLE tasks(asset_id TEXT, interval TEXT, start TEXT, end TEXT, status TEXT)")
        conn.execute("INSERT INTO tasks VALUES('A','1d','s','e','complete')")
    with State(settings.state_path) as state:
        assert state.migrated_legacy_tasks
        assert state.global_task_counts() == {}
        assert state.conn.execute("SELECT status FROM tasks_legacy_v1").fetchone()[0] == "complete"


def test_metadata_policy_and_missing_adjusted_close(settings):
    assets, _ = load_catalog(Path(__file__).resolve().parents[1] / "data/universe.csv", symbols=["ASELS"])
    frame = pd.DataFrame({"Open": [10], "High": [11], "Low": [9], "Close": [10.5]},
                         index=pd.DatetimeIndex([pd.Timestamp("2026-01-05 07:00", tz="UTC")]))
    adjusted = settings.with_overrides(auto_adjust=True)
    metadata = {"symbol": "ASELS.IS", "currency": "TRY", "exchangeTimezoneName": "Europe/Istanbul"}
    out, stats = normalize_prices(frame, assets[0], "1h", "now", settings=adjusted, series_id="s",
                                  metadata=metadata)
    assert bool(out["auto_adjust"].iloc[0])
    assert out["adj_close"].isna().all()
    assert out["adj_close_source"].iloc[0] == "missing"
    assert stats["missing_adj_close"] == 1
    for values, expected in [([float("nan")], "missing"), ([float("inf")], "missing"), ([10.25], "provider")]:
        supplied = frame.assign(**{"Adj Close": values})
        result, _ = normalize_prices(supplied, assets[0], "1h", "now", settings=settings,
                                     series_id="s", metadata=metadata)
        assert result["adj_close_source"].iloc[0] == expected
        if expected == "missing":
            assert result["adj_close"].isna().all()
        else:
            assert result["adj_close"].iloc[0] == 10.25
    with pytest.raises(InvalidData, match="Para birimi"):
        normalize_prices(frame, assets[0], "1h", "now", settings=settings, series_id="s", metadata={"currency": "USD"})
    with pytest.raises(InvalidData, match="Sembol"):
        normalize_prices(frame, assets[0], "1h", "now", settings=settings, series_id="s", metadata={"symbol": "THYAO.IS"})
    naive = frame.copy()
    naive.index = pd.DatetimeIndex([pd.Timestamp("2026-01-05 10:00")])
    with pytest.raises(InvalidData, match="Naive timestamp"):
        normalize_prices(naive, assets[0], "1h", "now", settings=settings, series_id="s")
    localized, _ = normalize_prices(naive, assets[0], "1h", "now", settings=settings,
                                    series_id="s", metadata=metadata)
    assert localized["ts_utc"].iloc[0] == "2026-01-05T07:00:00Z"
    assert localized["timestamp_basis"].iloc[0] == "provider_exchange_timezone"


def test_merge_rejects_mixed_series(tmp_path, settings):
    frame = pd.DataFrame({"Open": [10], "High": [11], "Low": [9], "Close": [10.5]},
                         index=pd.DatetimeIndex([pd.Timestamp("2026-01-05 07:00", tz="UTC")]))
    asset = load_catalog(Path(__file__).resolve().parents[1] / "data/universe.csv", symbols=["ASELS"])[0][0]
    first, _ = normalize_prices(frame, asset, "1h", "now", settings=settings, series_id="series-a")
    second, _ = normalize_prices(frame, asset, "1h", "now", settings=settings, series_id="series-b")
    path = tmp_path / "series.csv"
    merge_save_prices(path, first)
    with pytest.raises(InvalidData, match="Farklı seri"):
        merge_save_prices(path, second)
