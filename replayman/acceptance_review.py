"""Geçmiş 4s aşağı acceptance adayını daha sıkı zaman sözleşmesiyle denetle."""
from __future__ import annotations

import pandas as pd

from .dip_research import Period
from .p6_causal import event_result


def down_acceptance_representatives(events: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Aynı hisse/bar'da sayılan birden fazla seviyeden ilk pivotu seç."""
    raw = events.loc[(events.event == "acceptance") & (events.direction == "down")].sort_values(
        ["event_position", "source_pivot_position"], kind="stable").copy()
    unique = raw.drop_duplicates("event_position", keep="first").copy()
    return raw, unique


def open_result(bars: pd.DataFrame, position: int, *, entry_lag: int, horizon: int, period: Period,
                benchmark: pd.DataFrame | None) -> dict:
    """Aşağı yönlü olayda bir veya iki bar sonraki açılış -> horizon kapanış."""
    if entry_lag < 1:
        raise ValueError("Giriş gecikmesi en az bir bar olmalı")
    if position < 0 or position >= len(bars) or not period.start <= bars.ts_utc.iloc[position] < period.end:
        raise ValueError("Sinyal dönemi hatalı")
    anchor = position + entry_lag - 1
    if anchor >= len(bars) or bars.ts_utc.iloc[anchor] >= period.end:
        return {"status": "censored", "start_ts": None, "end_ts": None, "directional_return": None,
                "directional_excess": None, "benchmark_return": None, "mfe": None, "mae": None}
    return event_result(bars, anchor, entry="next_open", sign=-1, horizon=horizon, period=period, benchmark=benchmark)
