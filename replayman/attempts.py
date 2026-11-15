"""Kitaptaki ilk/ikinci deneme ve beklenen yeni uç ölçümleri."""
from __future__ import annotations

import numpy as np
import pandas as pd


def compare_directional_legs(legs: pd.DataFrame, bars: pd.DataFrame, features: pd.DataFrame, *, extreme_tolerance_atr: float = 0.10) -> pd.DataFrame:
    """Her hareket bacağını önceki aynı yönlü bacakla nedensel olarak karşılaştırır.

    Olay, ikinci bacağın bitiş swing'i teyit edildiğinde bilinir. Yeni uç kararı
    geometrik bitiş fiyatlarını karşılaştırır; tolerans olay anındaki ATR'dir.
    """
    if extreme_tolerance_atr < 0:
        raise ValueError("Uç toleransı negatif olamaz")
    columns = [
        "direction", "event", "thesis_direction", "previous_start_position", "previous_end_position",
        "current_start_position", "current_end_position", "known_at_position", "event_ts",
        "previous_distance", "current_distance", "distance_ratio", "previous_duration", "current_duration",
        "duration_ratio", "speed_ratio", "efficiency_ratio", "extreme_delta", "extreme_delta_atr",
    ]
    if legs.empty:
        return pd.DataFrame(columns=columns)
    last_by_direction: dict[str, dict] = {}
    rows: list[dict] = []
    atr = features["atr"] if "atr" in features else pd.Series(np.nan, index=features.index)
    ordered = legs.sort_values(["known_at_position", "end_position"])
    for current in ordered.to_dict("records"):
        direction = current["direction"]
        previous = last_by_direction.get(direction)
        if previous is not None:
            known = int(current["known_at_position"])
            tolerance = float(atr.iloc[known]) * extreme_tolerance_atr if known < len(atr) and pd.notna(atr.iloc[known]) else 0.0
            if direction == "up":
                delta = float(current["end_price"] - previous["end_price"])
                success = delta > tolerance
            else:
                delta = float(previous["end_price"] - current["end_price"])
                success = delta > tolerance
            event = "new_extreme_success" if success else "new_extreme_failure"
            thesis = direction if success else ("down" if direction == "up" else "up")
            def ratio(a, b):
                return float(a) / float(b) if pd.notna(a) and pd.notna(b) and float(b) != 0 else np.nan
            rows.append({
                "direction": direction, "event": event, "thesis_direction": thesis,
                "previous_start_position": int(previous["start_position"]), "previous_end_position": int(previous["end_position"]),
                "current_start_position": int(current["start_position"]), "current_end_position": int(current["end_position"]),
                "known_at_position": known, "event_ts": bars.iloc[known]["ts_utc"],
                "previous_distance": float(previous["distance"]), "current_distance": float(current["distance"]),
                "distance_ratio": ratio(current["distance"], previous["distance"]),
                "previous_duration": int(previous["duration_bars"]), "current_duration": int(current["duration_bars"]),
                "duration_ratio": ratio(current["duration_bars"], previous["duration_bars"]),
                "speed_ratio": ratio(current["speed_per_bar"], previous["speed_per_bar"]),
                "efficiency_ratio": ratio(current["path_efficiency"], previous["path_efficiency"]),
                "extreme_delta": delta, "extreme_delta_atr": delta / float(atr.iloc[known]) if pd.notna(atr.iloc[known]) and atr.iloc[known] else np.nan,
            })
        last_by_direction[direction] = current
    return pd.DataFrame(rows, columns=columns)


def attach_attempt_outcomes(events: pd.DataFrame, bars: pd.DataFrame, horizons: tuple[int, ...] = (5, 20, 40, 60)) -> pd.DataFrame:
    """İkinci deneme olaylarına hipotez yönünde ileri sonuç ekler."""
    result = events.copy()
    close, high, low = (bars[name].to_numpy(float) for name in ("close", "high", "low"))
    for horizon in horizons:
        returns, mfe, mae = [], [], []
        for event in events.to_dict("records"):
            position = int(event["known_at_position"])
            sign = 1 if event["thesis_direction"] == "up" else -1
            if position + horizon >= len(bars):
                returns.append(np.nan); mfe.append(np.nan); mae.append(np.nan); continue
            entry = close[position]
            returns.append(sign * (close[position + horizon] / entry - 1))
            maximum = high[position + 1:position + horizon + 1].max() / entry - 1
            minimum = low[position + 1:position + horizon + 1].min() / entry - 1
            mfe.append(maximum if sign == 1 else -minimum)
            mae.append(minimum if sign == 1 else -maximum)
        result[f"directional_return_{horizon}"] = returns
        result[f"directional_mfe_{horizon}"] = mfe
        result[f"directional_mae_{horizon}"] = mae
    return result
