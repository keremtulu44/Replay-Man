"""Nedensel yatay swing bölgesi araştırmasının ilk dilimi.

Zaman damgaları bar etiketidir; piyasa kapanış zamanı olarak yorumlanmaz.
Bölge olayları ve ziyaret başlangıcı özellikleri, ileri sonuçlardan ayrıdır.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math

import pandas as pd

from .swings import SwingConfig, confirmed_swings


@dataclass(frozen=True)
class ZoneConfig:
    method: str = "atr"
    tolerance: float = 0.25
    exit_closes: int = 2
    swing_left: int = 2
    swing_right: int = 2

    def __post_init__(self) -> None:
        if self.method not in {"atr", "percent"}:
            raise ValueError("method atr veya percent olmalı")
        if not math.isfinite(self.tolerance) or self.tolerance <= 0:
            raise ValueError("tolerance sonlu ve pozitif olmalı")
        if self.exit_closes < 1 or self.swing_left < 1 or self.swing_right < 1:
            raise ValueError("Pencere değerleri pozitif olmalı")


@dataclass
class _Zone:
    id: str
    center: float
    width: float
    created_pos: int
    last_pivot: int
    reactions: int = 1
    high_reactions: int = 0
    low_reactions: int = 0
    visited_reactions: set[str] = field(default_factory=set)
    visits: list[dict] = field(default_factory=list)
    active: dict | None = None
    outside: int = 0
    last_side: str = "unknown"

    @property
    def role(self) -> str:
        if self.high_reactions and self.low_reactions:
            return "mixed"
        return "resistance_candidate" if self.high_reactions else "support_candidate"


def _side(close: float, lower: float, upper: float) -> str:
    return "above" if close > upper else "below" if close < lower else "inside"


def _approach(closes: list[float], pos: int, atr: float, window: int = 5) -> dict:
    """Temas barından önceki kapanışlarla yaklaşımı ölç."""
    if pos < window + 1:
        return {"approach_return_5": None, "approach_speed_atr_5": None, "approach_efficiency_5": None}
    segment = closes[pos - window - 1:pos]
    change = segment[-1] - segment[0]
    path = sum(abs(b - a) for a, b in zip(segment, segment[1:]))
    return {
        "approach_return_5": change / segment[0] if segment[0] else None,
        "approach_speed_atr_5": change / (window * atr) if math.isfinite(atr) and atr > 0 else None,
        "approach_efficiency_5": abs(change) / path if path else None,
    }


def scan_zones(bars: pd.DataFrame, *, config: ZoneConfig = ZoneConfig(), series_key: str = "series") -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Teyitli uçları sırayla aç ve sabit genişlikli yatay bölgeleri takip et.

    İlk uç bir aday açar; daha sonra farklı bir ziyaretteki teyitli uç aynı
    adaya eşleşirse tepki sayısı artar. Ziyaret başlangıç snapshot'ı olaydan
    önceki bilinen tepki sayısını taşır. Her kaynak uç yalnız bir adaya atanır.
    Dönüşün teyit barındaki bölge güncellemesi o barın ziyaretinden sonradır.
    """
    if not series_key:
        raise ValueError("series_key boş olamaz")
    bars = bars.reset_index(drop=True)
    previous_close = bars["close"].astype(float).shift(1)
    high = bars["high"].astype(float)
    low = bars["low"].astype(float)
    true_range = pd.concat([high - low, (high - previous_close).abs(), (low - previous_close).abs()], axis=1).max(axis=1)
    features = pd.DataFrame({"atr": true_range.rolling(14, min_periods=14).mean()})
    swings = confirmed_swings(bars, features, config=SwingConfig(config.swing_left, config.swing_right))
    by_confirmation: dict[int, list[dict]] = {}
    for pivot in swings.to_dict("records"):
        by_confirmation.setdefault(int(pivot["confirmed_position"]), []).append(pivot)
    closes = bars["close"].astype(float).tolist()
    highs = bars["high"].astype(float).tolist()
    lows = bars["low"].astype(float).tolist()
    atrs = features["atr"].astype(float).tolist()
    stamps = [str(value) for value in bars["ts_utc"]]
    zones: list[_Zone] = []
    zone_events: list[dict] = []
    visit_starts: list[dict] = []
    visit_events: list[dict] = []
    prefix = f"{series_key}:{config.method}:{config.tolerance:g}"

    def emit(zone: _Zone, position: int, name: str, **extra) -> None:
        zone_events.append({"zone_id": zone.id, "position": position, "bar_ts": stamps[position],
                            "event": name, "center": zone.center, "lower": zone.center - zone.width,
                            "upper": zone.center + zone.width, "reaction_count": zone.reactions,
                            "role": zone.role, **extra})

    for pos in range(len(bars)):
        high, low, close = highs[pos], lows[pos], closes[pos]
        for zone in zones:
            if pos <= zone.created_pos:
                continue
            lower, upper = zone.center - zone.width, zone.center + zone.width
            touching = low <= upper and high >= lower
            side = _side(close, lower, upper)
            if zone.active is None and touching:
                visit_id = f"{zone.id}:v{len(zone.visits) + 1}"
                visit = {"visit_id": visit_id, "start": pos, "end": None}
                zone.visits.append(visit)
                zone.active = visit
                zone.outside = 0
                start = {"visit_id": visit_id, "zone_id": zone.id, "position": pos,
                         "bar_ts": stamps[pos], "center": zone.center, "lower": lower, "upper": upper,
                         "reaction_count": zone.reactions, "high_reactions": zone.high_reactions,
                         "low_reactions": zone.low_reactions, "role": zone.role,
                         "prior_visits": len(zone.visits) - 1, "approach_side": zone.last_side,
                         "reference_close": close, "atr": atrs[pos] if math.isfinite(atrs[pos]) else None}
                start.update(_approach(closes, pos, atrs[pos]))
                visit_starts.append(start)
                visit_events.append({"visit_id": visit_id, "position": pos, "bar_ts": stamps[pos], "event": "visit_start"})
            if zone.active is not None:
                visit_id = zone.active["visit_id"]
                if touching:
                    visit_events.append({"visit_id": visit_id, "position": pos, "bar_ts": stamps[pos], "event": "touch_bar"})
                # İki sınır aynı barda aşılırsa sıra bilinmez.
                if low < lower and high > upper:
                    visit_events.append({"visit_id": visit_id, "position": pos, "bar_ts": stamps[pos], "event": "both_boundaries_ambiguous"})
                elif high > upper and close <= upper:
                    visit_events.append({"visit_id": visit_id, "position": pos, "bar_ts": stamps[pos], "event": "upper_wick_outside"})
                elif low < lower and close >= lower:
                    visit_events.append({"visit_id": visit_id, "position": pos, "bar_ts": stamps[pos], "event": "lower_wick_outside"})
                if side in {"above", "below"}:
                    zone.outside += 1
                    visit_events.append({"visit_id": visit_id, "position": pos, "bar_ts": stamps[pos], "event": f"close_{side}"})
                else:
                    zone.outside = 0
                if zone.outside >= config.exit_closes:
                    zone.active["end"] = pos
                    visit_events.append({"visit_id": visit_id, "position": pos, "bar_ts": stamps[pos], "event": "visit_end"})
                    zone.active = None
                    zone.outside = 0
            zone.last_side = side

        # Geometri veya tepki hafızası yalnız teyit barı kapandıktan sonra güncellenir.
        for pivot in by_confirmation.get(pos, []):
            price, pivot_pos = float(pivot["price"]), int(pivot["pivot_position"])
            choices = []
            for zone in zones:
                if pivot_pos <= zone.created_pos or abs(price - zone.center) > zone.width:
                    continue
                # Aynı ziyaret birden fazla teyitli uç üretebilir; yalnız bir tepki say.
                matching = [v for v in zone.visits if v["start"] <= pivot_pos and (v["end"] is None or pivot_pos <= v["end"])]
                if matching and matching[-1]["visit_id"] not in zone.visited_reactions:
                    choices.append((abs(price - zone.center) / zone.width, zone.created_pos, zone.id, zone, matching[-1]))
            if choices:
                _, _, _, zone, visit = min(choices, key=lambda item: item[:3])
                zone.reactions += 1
                zone.high_reactions += int(pivot["kind"] == "high")
                zone.low_reactions += int(pivot["kind"] == "low")
                zone.last_pivot = pivot_pos
                zone.visited_reactions.add(visit["visit_id"])
                emit(zone, pos, "reaction_confirmed", pivot_position=pivot_pos,
                     pivot_ts=str(pivot["pivot_ts"]), pivot_kind=pivot["kind"], visit_id=visit["visit_id"])
            else:
                atr = atrs[pos]
                width = price * config.tolerance if config.method == "percent" else atr * config.tolerance
                if not math.isfinite(width) or width <= 0:
                    continue
                zone = _Zone(id=f"{prefix}:z{len(zones) + 1}", center=price, width=width,
                             created_pos=pos, last_pivot=pivot_pos,
                             high_reactions=int(pivot["kind"] == "high"), low_reactions=int(pivot["kind"] == "low"))
                zones.append(zone)
                emit(zone, pos, "zone_created", pivot_position=pivot_pos,
                     pivot_ts=str(pivot["pivot_ts"]), pivot_kind=pivot["kind"], visit_id=None)
    zone_columns = ["zone_id", "position", "bar_ts", "event", "center", "lower", "upper",
                    "reaction_count", "role", "pivot_position", "pivot_ts", "pivot_kind", "visit_id"]
    visit_columns = ["visit_id", "zone_id", "position", "bar_ts", "center", "lower", "upper",
                     "reaction_count", "high_reactions", "low_reactions", "role", "prior_visits",
                     "approach_side", "reference_close", "atr", "approach_return_5",
                     "approach_speed_atr_5", "approach_efficiency_5"]
    event_columns = ["visit_id", "position", "bar_ts", "event"]
    return (pd.DataFrame(zone_events, columns=zone_columns), pd.DataFrame(visit_starts, columns=visit_columns),
            pd.DataFrame(visit_events, columns=event_columns))


def visit_outcomes(bars: pd.DataFrame, visits: pd.DataFrame, horizons: tuple[int, ...] = (1, 3, 5, 10, 20)) -> pd.DataFrame:
    """Ziyaret anından sonraki fiyat sonuçları; asla özellik tablosuna eklenmez."""
    rows = []
    for visit in visits.to_dict("records"):
        pos, entry = int(visit["position"]), float(visit["reference_close"])
        for horizon in horizons:
            if horizon < 1:
                raise ValueError("Ufuk pozitif olmalı")
            end = pos + horizon
            row = {"visit_id": visit["visit_id"], "horizon": horizon, "end_position": end,
                   "status": "censored" if end >= len(bars) else "observed",
                   "return": None, "mfe": None, "mae": None, "end_bar_ts": None}
            if end < len(bars) and entry != 0:
                future = bars.iloc[pos + 1:end + 1]
                row.update({"return": float(bars.iloc[end]["close"]) / entry - 1,
                            "mfe": float(future["high"].max()) / entry - 1,
                            "mae": float(future["low"].min()) / entry - 1,
                            "end_bar_ts": str(bars.iloc[end]["ts_utc"])})
            elif entry == 0:
                row["status"] = "unknown"
            rows.append(row)
    return pd.DataFrame(rows, columns=["visit_id", "horizon", "end_position", "status", "return", "mfe", "mae", "end_bar_ts"])
