"""Teyitli swing seviyeleri için nedensel kırılım/kabul/failure durum makinesi."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class StructureConfig:
    tolerance_atr: float = 0.10
    acceptance_closes: int = 2
    follow_through_bars: int = 3
    failure_bars: int = 10
    max_level_age: int = 100

    def __post_init__(self) -> None:
        if self.tolerance_atr < 0 or self.acceptance_closes < 1 or self.follow_through_bars < 1 or self.failure_bars < 1 or self.max_level_age < 1:
            raise ValueError("Yapı motoru parametreleri pozitif olmalı")


def structure_events(bars: pd.DataFrame, features: pd.DataFrame, swings: pd.DataFrame, *, level: str = "minor", config: StructureConfig = StructureConfig()) -> pd.DataFrame:
    """Her teyitli swing seviyesinin ilk kırılım yaşam döngüsünü üretir.

    Seviye pivot barında değil `confirmed_position` barından sonra aktiftir.
    Her olay yalnız o bar kapanınca bilinen OHLC/ATR ile oluşur.
    """
    required = {"open", "high", "low", "close", "ts_utc"}
    if required - set(bars):
        raise ValueError(f"Eksik bar kolonları: {sorted(required - set(bars))}")
    selected = swings.loc[swings.level == level].sort_values("confirmed_position")
    activations: dict[int, list[dict]] = {}
    for swing in selected.to_dict("records"):
        # Teyit barının kendi aralığı pivotu zaten içeriyor olabilir; seviye bir sonraki barda sınanabilir.
        activations.setdefault(int(swing["confirmed_position"]) + 1, []).append(swing)
    active: list[dict] = []
    rows: list[dict] = []
    atr = features["atr"] if "atr" in features else pd.Series(np.nan, index=bars.index)
    for position in range(len(bars)):
        active.extend({"swing": s, "state": "active", "break_position": None, "outside_closes": 0, "retest_emitted": False, "follow_emitted": False} for s in activations.get(position, []))
        bar = bars.iloc[position]
        tolerance = float(atr.iloc[position]) * config.tolerance_atr if pd.notna(atr.iloc[position]) else 0.0
        feature_row = features.iloc[position]
        context_features = {name: feature_row.get(name, np.nan) for name in ("body_ratio", "close_location", "range_atr", "path_efficiency", "directional_persistence", "mean_overlap", "body_decay_ratio", "progress_decay_ratio")}
        survivors: list[dict] = []
        for item in active:
            swing = item["swing"]
            age = position - int(swing["confirmed_position"])
            if age > config.max_level_age:
                continue
            price = float(swing["price"])
            direction = "up" if swing["kind"] == "high" else "down"
            extreme_outside = float(bar.high) > price + tolerance if direction == "up" else float(bar.low) < price - tolerance
            close_outside = float(bar.close) > price + tolerance if direction == "up" else float(bar.close) < price - tolerance
            close_inside = float(bar.close) < price - tolerance if direction == "up" else float(bar.close) > price + tolerance
            event_base = {
                "level": level, "direction": direction, "level_price": price,
                "source_pivot_position": int(swing["pivot_position"]), "source_confirmed_position": int(swing["confirmed_position"]),
                "event_position": position, "event_ts": bar.ts_utc, "level_age_bars": age,
                "distance_close_atr": ((float(bar.close) - price) / float(atr.iloc[position])) if pd.notna(atr.iloc[position]) and atr.iloc[position] else np.nan,
            }
            event_base.update(context_features)
            if item["state"] == "active":
                if extreme_outside and not close_outside:
                    rows.append({**event_base, "event": "probe_rejection", "bars_since_break": np.nan})
                if close_outside:
                    item["state"] = "broken"
                    item["break_position"] = position
                    item["outside_closes"] = 1
                    rows.append({**event_base, "event": "close_break", "bars_since_break": 0})
            else:
                since = position - int(item["break_position"])
                event_base["bars_since_break"] = since
                if close_outside:
                    item["outside_closes"] += 1
                    if not item["follow_emitted"] and since <= config.follow_through_bars:
                        rows.append({**event_base, "event": "follow_through"})
                        item["follow_emitted"] = True
                    if item["outside_closes"] == config.acceptance_closes:
                        rows.append({**event_base, "event": "acceptance"})
                # Retest: fiyat seviyeye dokunur, kapanış kırılım tarafında/çevresinde kalır.
                touched = float(bar.low) <= price + tolerance if direction == "up" else float(bar.high) >= price - tolerance
                retained = float(bar.close) >= price - tolerance if direction == "up" else float(bar.close) <= price + tolerance
                if since > 0 and touched and retained and not item["retest_emitted"]:
                    rows.append({**event_base, "event": "retest_hold"})
                    item["retest_emitted"] = True
                if since > 0 and close_inside:
                    rows.append({**event_base, "event": "failure", "bars_since_break": since})
                    continue
                if since > config.failure_bars:
                    continue
            survivors.append(item)
        active = survivors
    columns = ["level", "direction", "event", "level_price", "source_pivot_position", "source_confirmed_position", "event_position", "event_ts", "level_age_bars", "bars_since_break", "distance_close_atr", "body_ratio", "close_location", "range_atr", "path_efficiency", "directional_persistence", "mean_overlap", "body_decay_ratio", "progress_decay_ratio"]
    return pd.DataFrame(rows, columns=columns)


def attach_event_outcomes(events: pd.DataFrame, bars: pd.DataFrame, horizons: tuple[int, ...] = (1, 3, 5, 10, 20)) -> pd.DataFrame:
    """Yapı olaylarına yön düzeltilmiş ileri getiri, MFE ve MAE ekler."""
    result = events.copy()
    # Counter expansion is a separate event known at its own closing bar.
    reversal_events = {"probe_rejection", "failure", "counter_expansion"}
    result["thesis_direction"] = [
        ("down" if row["direction"] == "up" else "up") if row["event"] in reversal_events else row["direction"]
        for row in events.to_dict("records")
    ]
    close = bars.close.to_numpy(float)
    high, low = bars.high.to_numpy(float), bars.low.to_numpy(float)
    for horizon in horizons:
        if horizon < 1:
            raise ValueError("Sonuç ufku pozitif olmalı")
        returns, mfe, mae, end_times = [], [], [], []
        for event in events.to_dict("records"):
            pos = int(event["event_position"])
            thesis_direction = ("down" if event["direction"] == "up" else "up") if event["event"] in reversal_events else event["direction"]
            sign = 1 if thesis_direction == "up" else -1
            if pos + horizon >= len(bars):
                returns.append(np.nan); mfe.append(np.nan); mae.append(np.nan); end_times.append(pd.NaT); continue
            entry = close[pos]
            returns.append(sign * (close[pos + horizon] / entry - 1))
            future_high = high[pos + 1:pos + horizon + 1].max() / entry - 1
            future_low = low[pos + 1:pos + horizon + 1].min() / entry - 1
            mfe.append(future_high if sign == 1 else -future_low)
            mae.append(future_low if sign == 1 else -future_high)
            end_times.append(bars.ts_utc.iloc[pos + horizon])
        result[f"directional_return_{horizon}"] = returns
        result[f"directional_mfe_{horizon}"] = mfe
        result[f"directional_mae_{horizon}"] = mae
        result[f"outcome_end_ts_{horizon}"] = pd.to_datetime(end_times, utc=True)
    return result
