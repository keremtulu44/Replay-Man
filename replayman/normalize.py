"""OHLCV doğrulama, birleştirme ve atomik CSV kaydı."""
from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

from .catalog import Asset
from .errors import InvalidData

PRICE_COLUMNS = ["open", "high", "low", "close", "adj_close", "volume"]
ACTION_COLUMNS = ["dividends", "stock_splits", "capital_gains"]
OUTPUT_COLUMNS = [
    "ts_utc", "session_date", "open", "high", "low", "close", "adj_close", "volume",
    *ACTION_COLUMNS, "asset_id", "symbol", "interval", "currency", "source", "auto_adjust", "fetched_at",
]


def timezone_for_asset(asset: Asset) -> str:
    if asset.category in {"bist100_equity", "bist_index"} or asset.yahoo_symbol.endswith(".IS"):
        return "Europe/Istanbul"
    if asset.yahoo_symbol == "^GDAXI":
        return "Europe/Berlin"
    if asset.category in {"global_index", "metals", "oil"}:
        return "America/New_York"
    return "UTC"


def normalize_prices(frame: pd.DataFrame, asset: Asset, interval: str, fetched_at: str) -> tuple[pd.DataFrame, dict]:
    stats = {"raw_rows": int(len(frame)), "dropped_all_nan": 0, "dropped_invalid": 0, "duplicates": 0}
    if frame is None or frame.empty:
        raise InvalidData("Boş fiyat tablosu")
    df = frame.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    rename = {str(c): str(c).strip().lower().replace(" ", "_") for c in df.columns}
    df = df.rename(columns=rename)
    required = {"open", "high", "low", "close"}
    if not required.issubset(df.columns):
        raise InvalidData(f"OHLC kolonları eksik: {sorted(required - set(df.columns))}")
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index, utc=True, errors="coerce")
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    else:
        df.index = df.index.tz_convert("UTC")
    df = df[~df.index.isna()]
    for column in PRICE_COLUMNS + ACTION_COLUMNS:
        if column not in df.columns:
            df[column] = np.nan
        df[column] = pd.to_numeric(df[column], errors="coerce")
    if "adj_close" not in frame.rename(columns=rename).columns:
        df["adj_close"] = df["close"]
    all_nan = df[["open", "high", "low", "close"]].isna().all(axis=1)
    stats["dropped_all_nan"] = int(all_nan.sum())
    df = df[~all_nan]
    ohlc = df[["open", "high", "low", "close"]]
    invalid = (
        ohlc.isna().any(axis=1)
        | ~np.isfinite(ohlc).all(axis=1)
        | (df["high"] < df["low"])
        | (df["high"] < df[["open", "close"]].max(axis=1))
        | (df["low"] > df[["open", "close"]].min(axis=1))
    )
    stats["dropped_invalid"] = int(invalid.sum())
    df = df[~invalid]
    duplicates = df.index.duplicated(keep="last")
    stats["duplicates"] = int(duplicates.sum())
    df = df[~duplicates].sort_index()
    if df.empty:
        raise InvalidData("Doğrulama sonrası geçerli OHLC satırı kalmadı")
    tz = timezone_for_asset(asset)
    local = df.index.tz_convert(tz)
    out = pd.DataFrame(index=df.index)
    out["ts_utc"] = df.index.strftime("%Y-%m-%dT%H:%M:%SZ")
    out["session_date"] = local.strftime("%Y-%m-%d")
    for column in PRICE_COLUMNS + ACTION_COLUMNS:
        out[column] = df[column].to_numpy()
    out["asset_id"] = asset.id
    out["symbol"] = asset.yahoo_symbol
    out["interval"] = interval
    out["currency"] = asset.currency
    out["source"] = "yahoo"
    out["auto_adjust"] = False
    out["fetched_at"] = fetched_at
    out = out.reset_index(drop=True)[OUTPUT_COLUMNS]
    return out, stats


def read_prices(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    return pd.read_csv(path)


def merge_save_prices(path: str | Path, new_df: pd.DataFrame) -> int:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    old = read_prices(path)
    combined = pd.concat([old, new_df], ignore_index=True)
    combined = combined.drop_duplicates(subset=["ts_utc"], keep="last").sort_values("ts_utc")
    combined = combined[OUTPUT_COLUMNS]
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False, suffix=".tmp", mode="w", encoding="utf-8", newline="") as handle:
        tmp = Path(handle.name)
    try:
        combined.to_csv(tmp, index=False)
        tmp.replace(path)
    finally:
        tmp.unlink(missing_ok=True)
    return int(len(combined))
