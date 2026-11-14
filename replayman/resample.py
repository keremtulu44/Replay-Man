"""1s veriden 2s/4s ve türetilmiş günlük üretimi; eksik son bar işaretlenir."""
from __future__ import annotations

import tempfile
from pathlib import Path

import pandas as pd

from .catalog import Asset
from .normalize import timezone_for_asset

AGG = {
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last",
    "adj_close": "last",
    "volume": lambda s: s.sum(min_count=1),
    "dividends": lambda s: s.sum(min_count=1),
    "stock_splits": "last",
    "capital_gains": lambda s: s.sum(min_count=1),
}


def _finish(groups: pd.core.groupby.DataFrameGroupBy, counts: pd.Series, expected: pd.Series | int, asset: Asset, label: str, tz: str) -> pd.DataFrame:
    out = groups.agg(AGG)
    out["bar_count"] = counts
    out["expected_bars"] = expected
    out["complete"] = out["bar_count"] == out["expected_bars"]
    out["derived_from"] = "1h"
    out["asset_id"] = asset.id
    out["symbol"] = asset.yahoo_symbol
    out["interval"] = label
    out["currency"] = asset.currency
    out = out.dropna(subset=["open", "high", "low", "close"])
    local = out.index.tz_convert(tz)
    out["session_date"] = local.strftime("%Y-%m-%d")
    out["ts_utc"] = out.index.tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%SZ")
    return out.reset_index(drop=True)


def _bist_derive(df: pd.DataFrame, asset: Asset, hours: int, label: str) -> pd.DataFrame:
    tz = "Europe/Istanbul"
    local = df.index.tz_convert(tz)
    boundaries = [10, 12, 14, 16] if hours == 2 else [10, 14]
    expected_map = {10: 2, 12: 1, 14: 2, 16: 2} if hours == 2 else {10: 3, 14: 4}
    keys = []
    expected = []
    labels = []
    for ts in local:
        hour = ts.hour + ts.minute / 60.0
        if not (10 <= hour < 18):
            keys.append(None)
            expected.append(0)
            labels.append(pd.NaT)
            continue
        boundary = max(b for b in boundaries if b <= hour)
        keys.append((ts.strftime("%Y-%m-%d"), boundary))
        expected.append(expected_map[boundary])
        labels.append(pd.Timestamp(f"{ts.strftime('%Y-%m-%d')} {boundary:02d}:00:00", tz=tz))
    work = df.copy()
    work["_key"] = keys
    work["_expected"] = expected
    work["_label"] = labels
    work = work[work["_key"].notna()]
    if work.empty:
        return pd.DataFrame()
    grouped = work.groupby("_label", sort=True)
    out = grouped.agg(AGG)
    out["bar_count"] = grouped.size()
    out["expected_bars"] = grouped["_expected"].first()
    out["complete"] = out["bar_count"] == out["expected_bars"]
    out["derived_from"] = "1h"
    out["asset_id"] = asset.id
    out["symbol"] = asset.yahoo_symbol
    out["interval"] = label
    out["currency"] = asset.currency
    out.index = out.index.tz_convert("UTC")
    local_out = out.index.tz_convert(tz)
    out["session_date"] = local_out.strftime("%Y-%m-%d")
    out["ts_utc"] = out.index.strftime("%Y-%m-%dT%H:%M:%SZ")
    return out.reset_index(drop=True)


def _bist_daily(df: pd.DataFrame, asset: Asset) -> pd.DataFrame:
    tz = "Europe/Istanbul"
    local = df.index.tz_convert(tz)
    work = df.copy()
    work["_date"] = local.strftime("%Y-%m-%d")
    work["_label"] = pd.to_datetime(local.strftime("%Y-%m-%d")).tz_localize(tz)
    grouped = work.groupby("_label", sort=True)
    out = grouped.agg(AGG)
    out["bar_count"] = grouped.size()
    out["expected_bars"] = 7
    out["complete"] = out["bar_count"] == out["expected_bars"]
    out["derived_from"] = "1h"
    out["asset_id"] = asset.id
    out["symbol"] = asset.yahoo_symbol
    out["interval"] = "1d_from_1h"
    out["currency"] = asset.currency
    out.index = out.index.tz_convert("UTC")
    out["session_date"] = out.index.tz_convert(tz).strftime("%Y-%m-%d")
    out["ts_utc"] = out.index.strftime("%Y-%m-%dT%H:%M:%SZ")
    return out.reset_index(drop=True)


def derive_timeframes(hourly: pd.DataFrame, asset: Asset) -> dict[str, pd.DataFrame]:
    if hourly.empty:
        return {}
    df = hourly.copy()
    df["ts_utc"] = pd.to_datetime(df["ts_utc"], utc=True)
    df = df.set_index("ts_utc").sort_index()
    tz = timezone_for_asset(asset)
    result: dict[str, pd.DataFrame] = {}
    is_bist = asset.category in {"bist100_equity", "bist_index"} or asset.yahoo_symbol.endswith(".IS")
    if is_bist:
        result["2h"] = _bist_derive(df, asset, 2, "2h")
        result["4h"] = _bist_derive(df, asset, 4, "4h")
        result["1d_from_1h"] = _bist_daily(df, asset)
    else:
        for rule, hours, label in [("2h", 2, "2h"), ("4h", 4, "4h"), ("1D", 24, "1d_from_1h")]:
            grouped = df.resample(rule, origin="start_day")
            counts = grouped.size()
            result[label] = _finish(grouped, counts, hours, asset, label, tz)
    return {key: value for key, value in result.items() if not value.empty}


def save_derived(path: str | Path, frame: pd.DataFrame) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False, suffix=".tmp", mode="w", encoding="utf-8", newline="") as handle:
        tmp = Path(handle.name)
    try:
        frame.to_csv(tmp, index=False)
        tmp.replace(path)
    finally:
        tmp.unlink(missing_ok=True)


def daily_comparison(native: pd.DataFrame, derived: pd.DataFrame) -> pd.DataFrame:
    if native.empty or derived.empty:
        return pd.DataFrame()
    left = native[["session_date", "close", "volume"]].rename(columns={"close": "native_close", "volume": "native_volume"})
    right = derived[["session_date", "close", "volume"]].rename(columns={"close": "derived_close", "volume": "derived_volume"})
    merged = left.merge(right, on="session_date", how="inner")
    if merged.empty:
        return merged
    denom = merged["native_close"].abs().replace(0, float("nan"))
    merged["close_rel_diff"] = (merged["derived_close"] - merged["native_close"]).abs() / denom
    merged["volume_diff"] = merged["derived_volume"] - merged["native_volume"]
    merged["match"] = (merged["close_rel_diff"] <= 0.001) & (
        merged["volume_diff"].isna() | (merged["volume_diff"].abs() < 1e-9)
    )
    return merged
