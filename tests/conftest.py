from __future__ import annotations

import csv
from pathlib import Path

import pytest

from replayman.config import Settings


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(
        min_request_interval_seconds=0.0,
        jitter_seconds=0.0,
        max_requests_per_hour=10000,
        max_requests_per_run=10000,
        retry_base_seconds=0.01,
        retry_max_seconds=0.02,
        max_sweeps=4,
        rate_limit_cooldown_seconds=0.01,
        cache_dir=tmp_path / "cache",
        output_dir=tmp_path / "prices",
        derived_dir=tmp_path / "derived",
        report_dir=tmp_path / "reports",
        state_path=tmp_path / "state.sqlite3",
        lock_path=tmp_path / "state.lock",
        log_dir=tmp_path / "logs",
    )


@pytest.fixture
def catalog_path(tmp_path: Path) -> Path:
    path = tmp_path / "universe.csv"
    fields = ["id", "category", "name", "local_symbol", "yahoo_symbol", "asset_type", "currency", "enabled"]
    rows = [
        ["BIST_ASELS", "bist100_equity", "Aselsan", "ASELS", "ASELS.IS", "equity", "TRY", "true"],
        ["IDX_XU100", "bist_index", "BIST 100", "XU100", "XU100.IS", "index", "TRY", "true"],
        ["METAL_GOLD", "metals", "Altın", "GOLD", "GC=F", "future", "USD", "true"],
        ["DISABLED", "fx", "Kapalı", "OFF", "OFF=X", "fx", "TRY", "false"],
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(fields)
        writer.writerows(rows)
    return path
