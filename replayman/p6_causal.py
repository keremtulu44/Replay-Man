"""P6 karşı genişleme sınıflaması ve eşzamanlı olay sonuçları."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .dip_research import Period


def classify_failure(bars: pd.DataFrame, position: int, confirmation: int | None,
                     period: Period, *, window: int = 10) -> str:
    """Dönemde gerçekleşen teyit / tam gözlenmiş yokluk / sansür ayrımı."""
    if window < 1 or position < 0 or position >= len(bars):
        raise ValueError("Geçersiz failure veya takip penceresi")
    if not period.start <= bars.ts_utc.iloc[position] < period.end:
        raise ValueError("Failure belirtilen dönemde değil")
    if confirmation is not None:
        if not position < confirmation <= position + window or confirmation >= len(bars):
            raise ValueError("Karşı genişleme failure sonrası pencerede olmalı")
        if bars.ts_utc.iloc[confirmation] < period.end:
            return "confirmed"
    end = position + window
    if end >= len(bars) or bars.ts_utc.iloc[end] >= period.end:
        return "censored"
    return "not_confirmed"


def event_result(bars: pd.DataFrame, position: int, *, entry: str, sign: int, horizon: int,
                 period: Period, benchmark: pd.DataFrame | None = None) -> dict:
    """Failure/teyit kapanışı veya teyit sonrası açılıştan yönlü sonuç.

    Ufuk `position + horizon` kapanışında biter: next_open için horizon adet
    bar (position+1 ... position+horizon) kullanılır. Hisse/endeks giriş ve
    bitiş etiketleri eşit değilse benchmark bilinmiyor kalır.
    """
    if entry not in {"close", "next_open"} or sign not in {-1, 1} or horizon < 1:
        raise ValueError("Geçersiz olay sonucu parametresi")
    if position < 0 or position >= len(bars) or not period.start <= bars.ts_utc.iloc[position] < period.end:
        raise ValueError("Olay verilen dönem dışında")
    start = position + (entry == "next_open")
    end = position + horizon
    result = {"status": "censored", "start_ts": None, "end_ts": None, "start_price": None,
              "directional_return": None, "mfe": None, "mae": None,
              "benchmark_return": None, "directional_excess": None,
              "old_independent_end_ts": None, "old_end_mismatch": None}
    if start >= len(bars) or end >= len(bars) or bars.ts_utc.iloc[end] >= period.end:
        return result
    column = "open" if entry == "next_open" else "close"
    price, exit_price = float(bars[column].iloc[start]), float(bars.close.iloc[end])
    segment = bars.iloc[position + 1:end + 1]
    if (not np.isfinite(price) or not np.isfinite(exit_price) or price <= 0 or exit_price <= 0
            or not np.isfinite(segment[["high", "low"]].to_numpy(dtype=float)).all()):
        result["status"] = "unknown"
        return result
    high = float(segment.high.max()) / price - 1
    low = float(segment.low.min()) / price - 1
    directional = sign * (exit_price / price - 1)
    result.update({"status": "observed", "start_ts": bars.ts_utc.iloc[start], "end_ts": bars.ts_utc.iloc[end],
                   "start_price": price, "directional_return": directional,
                   "mfe": high if sign == 1 else -low, "mae": low if sign == 1 else -high})
    if benchmark is None or benchmark.empty:
        return result
    market = benchmark if benchmark.index.name == "ts_utc" else benchmark.set_index("ts_utc")
    if not market.index.is_unique or not market.index.is_monotonic_increasing:
        raise ValueError("Endeks etiketleri tekil ve sıralı olmalı")
    start_ts, end_ts = result["start_ts"], result["end_ts"]
    if start_ts not in market.index:
        return result
    # Tarihsel kodun bağımsız shift(-h) sonucunun hangi tarihe ulaştığını sakla.
    market_start_position = market.index.get_loc(start_ts)
    old_end = market_start_position + (horizon if entry == "close" else horizon - 1)
    if old_end < len(market):
        result["old_independent_end_ts"] = market.index[old_end]
        result["old_end_mismatch"] = bool(market.index[old_end] != end_ts)
    if end_ts in market.index:
        market_start, market_end = float(market.at[start_ts, column]), float(market.at[end_ts, "close"])
        if np.isfinite(market_start) and np.isfinite(market_end) and market_start > 0 and market_end > 0:
            market_return = market_end / market_start - 1
            result["benchmark_return"] = market_return
            result["directional_excess"] = directional - sign * market_return
    return result
