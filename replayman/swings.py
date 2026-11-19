"""Teyit zamanı açık, gelecek sızıntısız swing/pivot olayları."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SwingConfig:
    left: int = 2
    right: int = 2
    price_tolerance_atr: float = 0.10
    tie_break: str = "rightmost"

    def __post_init__(self) -> None:
        if self.left < 1 or self.right < 1:
            raise ValueError("Swing sol/sağ gücü en az 1 olmalı")
        if self.price_tolerance_atr < 0:
            raise ValueError("Fiyat toleransı negatif olamaz")
        if self.tie_break not in {"rightmost", "leftmost"}:
            raise ValueError("tie_break rightmost veya leftmost olmalı")


def confirmed_swings(bars: pd.DataFrame, features: pd.DataFrame | None = None, *, config: SwingConfig = SwingConfig(), level: str = "minor") -> pd.DataFrame:
    """Pivotları ancak sağ taraftaki teyit barları kapandıktan sonra yayımlar.

    `pivot_position` geometrik tepe/dip barıdır; `confirmed_position` olayın ilk
    bilinebildiği bardır. Varsayılan `rightmost` eşit uçların en sağdakini seçer:
    pivot sol pencereye eşit olabilir, sağ pencereden kesin üstün olmalıdır.
    Önceki araştırmaları yeniden üretmek için `tie_break="leftmost"` seçilebilir;
    eski sürümün açıklamasına rağmen uyguladığı kural buydu.
    """
    required = {"ts_utc", "high", "low", "close"}
    missing = required - set(bars.columns)
    if missing:
        raise ValueError(f"Swing için eksik kolonlar: {sorted(missing)}")
    n = len(bars)
    if n < config.left + config.right + 1:
        return _empty()
    atr = features["atr"] if features is not None and "atr" in features else pd.Series(np.nan, index=bars.index)
    rows: list[dict] = []
    last_price: dict[str, float | None] = {"high": None, "low": None}
    highs, lows = bars["high"].to_numpy(float), bars["low"].to_numpy(float)
    for confirmed in range(config.left + config.right, n):
        pivot = confirmed - config.right
        left_slice = slice(pivot - config.left, pivot)
        right_slice = slice(pivot + 1, confirmed + 1)
        candidates: list[tuple[str, float]] = []
        if config.tie_break == "rightmost":
            is_high = highs[pivot] >= highs[left_slice].max() and highs[pivot] > highs[right_slice].max()
            is_low = lows[pivot] <= lows[left_slice].min() and lows[pivot] < lows[right_slice].min()
        else:
            is_high = highs[pivot] > highs[left_slice].max() and highs[pivot] >= highs[right_slice].max()
            is_low = lows[pivot] < lows[left_slice].min() and lows[pivot] <= lows[right_slice].min()
        if is_high:
            candidates.append(("high", highs[pivot]))
        if is_low:
            candidates.append(("low", lows[pivot]))
        for kind, price in candidates:
            previous = last_price[kind]
            tolerance = float(atr.iloc[confirmed]) * config.price_tolerance_atr if pd.notna(atr.iloc[confirmed]) else 0.0
            if previous is None:
                relation = "first"
            elif abs(price - previous) <= tolerance:
                relation = "equal_high" if kind == "high" else "equal_low"
            elif kind == "high":
                relation = "higher_high" if price > previous else "lower_high"
            else:
                relation = "higher_low" if price > previous else "lower_low"
            rows.append({
                "level": level, "kind": kind, "relation": relation, "price": price,
                "pivot_position": pivot, "pivot_ts": bars.iloc[pivot]["ts_utc"],
                "confirmed_position": confirmed, "confirmed_ts": bars.iloc[confirmed]["ts_utc"],
                "confirmation_delay_bars": config.right,
                "price_from_confirmation_close_atr": ((price - float(bars.iloc[confirmed]["close"])) / float(atr.iloc[confirmed])) if pd.notna(atr.iloc[confirmed]) and atr.iloc[confirmed] != 0 else np.nan,
            })
            last_price[kind] = price
    return pd.DataFrame(rows, columns=_columns())


def multi_level_swings(bars: pd.DataFrame, features: pd.DataFrame | None = None, *, tie_break: str = "rightmost") -> pd.DataFrame:
    """Minor (2+2) ve major (5+5) swing; eski eşitlik kuralı seçilebilir."""
    minor = confirmed_swings(bars, features, config=SwingConfig(2, 2, tie_break=tie_break), level="minor")
    major = confirmed_swings(bars, features, config=SwingConfig(5, 5, tie_break=tie_break), level="major")
    return pd.concat([minor, major], ignore_index=True).sort_values(["confirmed_position", "level", "kind"]).reset_index(drop=True)


def swing_legs(swings: pd.DataFrame, bars: pd.DataFrame) -> pd.DataFrame:
    """Ardışık karşıt minor swingler arasındaki mesafe, süre ve hız."""
    source = swings.loc[swings["level"] == "minor"].sort_values(["pivot_position", "confirmed_position"])
    rows: list[dict] = []
    previous = None
    for current in source.to_dict("records"):
        if previous is not None and current["kind"] != previous["kind"] and current["pivot_position"] > previous["pivot_position"]:
            duration = int(current["pivot_position"] - previous["pivot_position"])
            signed = float(current["price"] - previous["price"])
            start = int(previous["pivot_position"])
            end = int(current["pivot_position"])
            close_path = bars["close"].iloc[start:end + 1].diff().abs().sum()
            rows.append({
                "direction": "up" if signed > 0 else "down", "start_kind": previous["kind"],
                "start_position": start, "end_position": end,
                "start_ts": previous["pivot_ts"], "end_ts": current["pivot_ts"],
                "known_at_position": int(current["confirmed_position"]), "known_at_ts": current["confirmed_ts"],
                "start_price": float(previous["price"]), "end_price": float(current["price"]),
                "distance": abs(signed), "return": signed / float(previous["price"]),
                "duration_bars": duration, "speed_per_bar": abs(signed) / duration,
                "path_efficiency": abs(signed) / close_path if close_path else np.nan,
            })
        previous = current
    return pd.DataFrame(rows)


def _columns() -> list[str]:
    return ["level", "kind", "relation", "price", "pivot_position", "pivot_ts", "confirmed_position", "confirmed_ts", "confirmation_delay_bars", "price_from_confirmation_close_atr"]


def _empty() -> pd.DataFrame:
    return pd.DataFrame(columns=_columns())
