"""Seri kimliği: enstrüman ve fiyat politikası değişince ayrı, sürümlü çıktı."""
from __future__ import annotations

import hashlib
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .catalog import Asset
from .config import Settings

POLICY_FIELDS = ("auto_adjust", "back_adjust", "repair", "keepna", "actions", "prepost")


@dataclass(frozen=True)
class Series:
    id: str
    manifest: dict[str, Any]


def build_series(asset: Asset, settings: Settings) -> Series:
    manifest = {
        "schema_version": 1,
        "provider": "yahoo",
        "asset_id": asset.id,
        "symbol": asset.yahoo_symbol,
        "category": asset.category,
        "asset_type": asset.asset_type,
        "catalog_currency": asset.currency,
        "price_policy": {field: getattr(settings, field) for field in POLICY_FIELDS},
    }
    payload = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    series_id = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return Series(series_id, {**manifest, "series_id": series_id})


def price_path(settings: Settings, asset: Asset, series: Series, interval: str) -> Path:
    return settings.output_dir / asset.id / series.id / "bars" / f"{interval}.csv"


def derived_path(settings: Settings, asset: Asset, series: Series) -> Path:
    return settings.derived_dir / asset.id / series.id / "bars"


def quality_path(settings: Settings, asset: Asset, series: Series) -> Path:
    return settings.derived_dir / asset.id / series.id / "quality"


def publish_manifest(settings: Settings, asset: Asset, series: Series) -> Path:
    """Aynı kimlikli manifesti doğrula; farklı içeriği sessizce değiştirme."""
    directory = settings.output_dir / asset.id / series.id
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "series.json"
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing != series.manifest:
            raise ValueError(f"Seri manifesti uyuşmuyor: {path}")
        return path
    with tempfile.NamedTemporaryFile(dir=directory, delete=False, suffix=".tmp", mode="w", encoding="utf-8") as handle:
        tmp = Path(handle.name)
    try:
        tmp.write_text(json.dumps(series.manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.replace(path)
    finally:
        tmp.unlink(missing_ok=True)
    return path
