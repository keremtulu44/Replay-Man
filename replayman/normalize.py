"""OHLCV doğrulama, açık seri/politika metadata'sı ve atomik CSV kaydı."""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Mapping
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import numpy as np
import pandas as pd

from .catalog import Asset
from .config import Settings
from .errors import InvalidData

PRICE_COLUMNS = ["open", "high", "low", "close", "adj_close", "volume"]
ACTION_COLUMNS = ["dividends", "stock_splits", "capital_gains"]
OUTPUT_COLUMNS = [
    "ts_utc", "session_date", "open", "high", "low", "close", "adj_close", "volume",
    *ACTION_COLUMNS, "asset_id", "series_id", "symbol", "interval", "currency", "source",
    "auto_adjust", "back_adjust", "repair", "adj_close_source", "exchange_timezone",
    "timestamp_basis", "session_date_basis", "fetched_at",
]


def timezone_for_asset(asset: Asset) -> str:
    if asset.category in {"bist100_equity", "bist_index"} or asset.yahoo_symbol.endswith(".IS"):
        return "Europe/Istanbul"
    if asset.yahoo_symbol == "^GDAXI":
        return "Europe/Berlin"
    if asset.category in {"global_index", "metals", "oil"}:
        return "America/New_York"
    return "UTC"


def _validate_metadata(asset: Asset, metadata: Mapping) -> None:
    symbol = metadata.get("symbol")
    if symbol and str(symbol).upper() != asset.yahoo_symbol.upper():
        raise InvalidData(f"Sembol uyuşmazlığı: katalog={asset.yahoo_symbol}, sağlayıcı={symbol}")
    currency = metadata.get("currency")
    # POINTS bir ISO para birimi değil; vadeli/endeks birimi E11'de ayrıca doğrulanacak.
    if currency and asset.currency != "POINTS" and str(currency).upper() != asset.currency.upper():
        raise InvalidData(f"Para birimi uyuşmazlığı: katalog={asset.currency}, sağlayıcı={currency}")
    expected_type = {"equity": "EQUITY", "index": "INDEX", "future": "FUTURE", "fx": "CURRENCY"}.get(asset.asset_type)
    instrument = metadata.get("instrumentType")
    if expected_type and instrument and str(instrument).upper() != expected_type:
        raise InvalidData(f"Enstrüman türü uyuşmazlığı: katalog={expected_type}, sağlayıcı={instrument}")


def normalize_prices(
    frame: pd.DataFrame,
    asset: Asset,
    interval: str,
    fetched_at: str,
    *,
    settings: Settings,
    series_id: str,
    metadata: Mapping | None = None,
) -> tuple[pd.DataFrame, dict]:
    """Politikayı açıkça alır; bilinmeyen naive zamanları UTC varsaymaz."""
    stats = {"raw_rows": int(len(frame)), "dropped_all_nan": 0, "dropped_invalid": 0, "duplicates": 0}
    if frame is None or frame.empty:
        raise InvalidData("Boş fiyat tablosu")
    if not series_id:
        raise InvalidData("Seri kimliği olmadan fiyat kaydedilemez")
    metadata = metadata or {}
    _validate_metadata(asset, metadata)
    df = frame.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    rename = {str(c): str(c).strip().lower().replace(" ", "_") for c in df.columns}
    df = df.rename(columns=rename)
    required = {"open", "high", "low", "close"}
    if not required.issubset(df.columns):
        raise InvalidData(f"OHLC kolonları eksik: {sorted(required - set(df.columns))}")
    exchange_timezone = metadata.get("exchangeTimezoneName")
    if exchange_timezone:
        try:
            ZoneInfo(str(exchange_timezone))
        except (ZoneInfoNotFoundError, ValueError) as exc:
            raise InvalidData(f"Sağlayıcı zaman dilimi geçersiz: {exchange_timezone}") from exc
        tz = str(exchange_timezone)
    else:
        tz = timezone_for_asset(asset)
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index, errors="coerce")
    if df.index.tz is None:
        if not exchange_timezone:
            raise InvalidData("Naive timestamp için sağlayıcı borsa zaman dilimi yok; UTC varsayılmadı")
        try:
            df.index = df.index.tz_localize(tz, ambiguous="raise", nonexistent="raise")
        except (TypeError, ValueError) as exc:
            raise InvalidData(f"Naive timestamp borsa saatine güvenle yorumlanamadı: {exc}") from exc
        timestamp_basis = "provider_exchange_timezone"
    else:
        timestamp_basis = "provider_aware_timestamp"
    df.index = df.index.tz_convert("UTC")
    df = df[~df.index.isna()]
    for column in PRICE_COLUMNS + ACTION_COLUMNS:
        if column not in df.columns:
            df[column] = np.nan
        df[column] = pd.to_numeric(df[column], errors="coerce")
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
    local = df.index.tz_convert(tz)
    out = pd.DataFrame(index=df.index)
    out["ts_utc"] = df.index.strftime("%Y-%m-%dT%H:%M:%SZ")
    # Takvim günü etiketi; doğrulanmış borsa işlem günü/seansı olduğu iddia edilmez.
    out["session_date"] = local.strftime("%Y-%m-%d")
    for column in PRICE_COLUMNS + ACTION_COLUMNS:
        out[column] = df[column].to_numpy()
    valid_adj_close = np.isfinite(df["adj_close"].to_numpy())
    out["adj_close"] = np.where(valid_adj_close, df["adj_close"].to_numpy(), np.nan)
    stats["missing_adj_close"] = int((~valid_adj_close).sum())
    out["asset_id"] = asset.id
    out["series_id"] = series_id
    out["symbol"] = asset.yahoo_symbol
    out["interval"] = interval
    out["currency"] = asset.currency
    out["source"] = "yahoo"
    out["auto_adjust"] = settings.auto_adjust
    out["back_adjust"] = settings.back_adjust
    out["repair"] = settings.repair
    # Kolonun bulunması tek başına kanıt değil: NaN/sonsuz değerler de eksik sayılır.
    out["adj_close_source"] = np.where(valid_adj_close, "provider", "missing")
    out["exchange_timezone"] = tz
    out["timestamp_basis"] = timestamp_basis
    out["session_date_basis"] = "exchange_civil_date_unverified"
    out["fetched_at"] = fetched_at
    return out.reset_index(drop=True)[OUTPUT_COLUMNS], stats


def read_prices(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    return pd.read_csv(path)


def merge_save_prices(path: str | Path, new_df: pd.DataFrame) -> int:
    path = Path(path)
    identity_columns = ["series_id", "symbol", "auto_adjust", "back_adjust", "repair"]
    if new_df.empty or any(c not in new_df.columns for c in identity_columns):
        raise InvalidData("Seri kimliği/politikası olmayan fiyatlar birleştirilemez")
    for column in identity_columns:
        if new_df[column].astype(str).nunique(dropna=False) != 1 or new_df[column].isna().any():
            raise InvalidData(f"Tek bir seri/politika gerekli: {column}")
    path.parent.mkdir(parents=True, exist_ok=True)
    old = read_prices(path)
    if not old.empty:
        missing = set(OUTPUT_COLUMNS) - set(old.columns)
        if missing:
            raise InvalidData(f"Eski/uyumsuz fiyat şeması; yeni çıktı dizini kullanın: {path}; eksik={sorted(missing)}")
        for column in identity_columns:
            if set(old[column].astype(str)) != set(new_df[column].astype(str)):
                raise InvalidData(f"Farklı seri/politika aynı dosyaya yazılamaz: {column}, {path}")
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
