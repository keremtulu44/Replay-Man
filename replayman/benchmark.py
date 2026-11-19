"""Olay sonuçlarını endeksin aynı başlangıç ve bitiş etiketlerine hizala."""
from __future__ import annotations

import numpy as np
import pandas as pd


def attach_exact_close_benchmark(
    events: pd.DataFrame, benchmark: pd.DataFrame, horizons: tuple[int, ...]
) -> pd.DataFrame:
    """Her ufukta olay kapanışı -> hisse sonuç kapanışı ile endeksi eşleştir.

    Endekste hisseyle aynı başlangıç *ve* bitiş etiketi yoksa sonuç NaN'dır.
    Ayrı endeks satır sayısı üzerinden `shift(-h)` yapılmaz ve eksikler
    doldurulmaz. Bu fark, gerçek işlem veya portföy getirisi değildir.
    """
    required = {"interval", "event_ts", "thesis_direction"}
    for h in horizons:
        required |= {f"outcome_end_ts_{h}", f"directional_return_{h}"}
    missing = required - set(events.columns)
    if missing:
        raise ValueError(f"Olay sonuç kolonları eksik: {sorted(missing)}")
    if {"interval", "ts_utc", "close"} - set(benchmark.columns):
        raise ValueError("Endeks interval, ts_utc ve close içermeli")
    market = benchmark[["interval", "ts_utc", "close"]].copy()
    market["ts_utc"] = pd.to_datetime(market.ts_utc, utc=True)
    if market.duplicated(["interval", "ts_utc"]).any():
        raise ValueError("Endeks zaman etiketleri periyot içinde tekil olmalı")
    market["close"] = pd.to_numeric(market.close, errors="coerce")
    market.loc[~np.isfinite(market.close) | (market.close <= 0), "close"] = np.nan
    lookup = market.set_index(["interval", "ts_utc"])["close"]
    result = events.copy()
    start_ts = pd.to_datetime(result.event_ts, utc=True)
    start_keys = pd.MultiIndex.from_arrays([result.interval, start_ts], names=lookup.index.names)
    start_price = lookup.reindex(start_keys).to_numpy()
    sign = result.thesis_direction.map({"up": 1, "down": -1}).to_numpy(float)
    for h in horizons:
        end_ts = pd.to_datetime(result[f"outcome_end_ts_{h}"], utc=True)
        end_keys = pd.MultiIndex.from_arrays([result.interval, end_ts], names=lookup.index.names)
        end_price = lookup.reindex(end_keys).to_numpy()
        bench = end_price / start_price - 1
        result[f"bench_{h}"] = bench
        result[f"excess_{h}"] = result[f"directional_return_{h}"].to_numpy(float) - sign * bench
    return result
