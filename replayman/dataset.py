"""Birleşik OHLCV veri ağacı için doğrulanmış global indeks üretimi."""
from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path

import pandas as pd

from .config import Settings
from .errors import InvalidData

INTERVALS = ("1h", "2h", "4h", "1d")
REQUIRED = {"open", "high", "low", "close", "volume", "asset_id", "series_id", "symbol", "interval"}


def build_dataset_index(settings: Settings) -> Path:
    """Fiziksel CSV'leri okuyup şema, kimlik ve OHLC tutarlılığını doğrula."""
    roots = {Path(settings.output_dir), Path(settings.derived_dir)}
    rows: list[dict] = []
    for root in sorted(roots, key=str):
        if not root.exists():
            continue
        for path in sorted(root.glob("*/*/bars/*.csv")):
            interval = path.stem
            if interval not in INTERVALS:
                continue
            frame = pd.read_csv(path)
            missing = REQUIRED - set(frame.columns)
            if missing:
                raise InvalidData(f"OHLCV indeks şeması eksik: {path}; {sorted(missing)}")
            if frame.empty:
                raise InvalidData(f"Boş OHLCV dosyası: {path}")
            for column in ("asset_id", "series_id", "symbol", "interval"):
                if frame[column].nunique(dropna=False) != 1:
                    raise InvalidData(f"Tek kimlik gerekli: {path}; {column}")
            if str(frame["interval"].iloc[0]) != interval:
                raise InvalidData(f"Dosya/periyot uyuşmazlığı: {path}")
            invalid = ((frame["high"] < frame["low"]) |
                       (frame["high"] < frame[["open", "close"]].max(axis=1)) |
                       (frame["low"] > frame[["open", "close"]].min(axis=1)))
            if invalid.any():
                raise InvalidData(f"Geçersiz OHLC satırı: {path}; adet={int(invalid.sum())}")
            complete = frame["complete"].astype(bool) if "complete" in frame else pd.Series(True, index=frame.index)
            payload = path.read_bytes()
            rows.append({
                "asset_id": frame["asset_id"].iloc[0],
                "symbol": frame["symbol"].iloc[0],
                "series_id": frame["series_id"].iloc[0],
                "interval": interval,
                "rows": len(frame),
                "complete_rows": int(complete.sum()),
                "partial_rows": int((~complete).sum()),
                "start_ts_utc": frame["ts_utc"].iloc[0],
                "end_ts_utc": frame["ts_utc"].iloc[-1],
                "sha256": hashlib.sha256(payload).hexdigest(),
                "path": path.as_posix(),
            })
    if not rows:
        raise InvalidData("İndekslenecek OHLCV dosyası bulunamadı")
    index = pd.DataFrame(rows).sort_values(["asset_id", "interval"])
    target = Path(settings.output_dir) / "index.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False, suffix=".tmp", mode="w", encoding="utf-8", newline="") as handle:
        tmp = Path(handle.name)
    try:
        index.to_csv(tmp, index=False)
        tmp.replace(target)
    finally:
        tmp.unlink(missing_ok=True)
    return target
