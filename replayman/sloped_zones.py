"""İki teyitli uçtan oluşan, geçmişi değiştirilmeyen eğimli bölge adayları.

Çizgiler sinyal değil araştırma adaylarıdır. Eğim, duvar zamanı yerine
kullanılabilir bar sırası üzerinden hesaplanır; eksik barlar kapsamda belirtilir.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math

import pandas as pd

from .swings import SwingConfig, confirmed_swings
from .zone_memory import ZoneConfig, _approach, _side


@dataclass(frozen=True)
class SlopedConfig:
    zone: ZoneConfig = ZoneConfig()
    min_anchor_distance: int = 8
    max_anchor_distance: int = 80
    max_anchors_per_kind: int = 3

    def __post_init__(self):
        if self.min_anchor_distance < 1 or self.max_anchor_distance < self.min_anchor_distance:
            raise ValueError("Uç mesafeleri geçersiz")
        if self.max_anchors_per_kind < 1:
            raise ValueError("max_anchors_per_kind pozitif olmalı")


@dataclass
class _Line:
    id: str
    kind: str
    anchor_pos: int
    anchor_price: float
    second_pos: int
    second_price: float
    slope: float
    width: float
    created: int
    source_confirmed: int
    source_kind: str
    second_kind: str
    visits: list[dict] = field(default_factory=list)
    active: dict | None = None
    outside: int = 0
    last_side: str = "unknown"
    reaction_visits: set[str] = field(default_factory=set)

    def center(self, position: int) -> float:
        return self.anchor_price + self.slope * (position - self.anchor_pos)

    @property
    def reaction_count(self) -> int:
        return 2 + len(self.reaction_visits)


def scan_sloped_zones(bars: pd.DataFrame, *, config: SlopedConfig = SlopedConfig(), series_key: str = "series"):
    """Çizgiyi iki uç teyit edilince kur; çizgiyi sonraki uçlara uydurma.

    İki kaynağın her biri yalnız bir geometrik uçtur. Bir sonraki bağımsız
    ziyaretin teyitli swing'i yeni tepki olarak, teyit anında kaydedilir.
    Bir uç birden fazla ayrı çizgiye temas edebilir: olaylar bağımlıdır.
    """
    if not series_key:
        raise ValueError("series_key boş olamaz")
    bars = bars.reset_index(drop=True)
    high, low, close = (bars[x].astype(float) for x in ("high", "low", "close"))
    previous = close.shift(1)
    tr = pd.concat([high - low, (high - previous).abs(), (low - previous).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14, min_periods=14).mean()
    swings = confirmed_swings(bars, pd.DataFrame({"atr": atr}), config=SwingConfig(config.zone.swing_left, config.zone.swing_right))
    by_confirmation: dict[int, list[dict]] = {}
    for pivot in swings.to_dict("records"):
        by_confirmation.setdefault(int(pivot["confirmed_position"]), []).append(pivot)
    highs, lows, closes, atrs = high.tolist(), low.tolist(), close.tolist(), atr.tolist()
    stamps = [str(x) for x in bars["ts_utc"]]
    prefix = f"{series_key}:sloped:{config.zone.method}:{config.zone.tolerance:g}"
    known_pivots: list[dict] = []
    lines: list[_Line] = []
    zone_events, starts, events = [], [], []

    def zone_event(line, position, event, **kwargs):
        center = line.center(position)
        zone_events.append({"zone_id": line.id, "position": position, "bar_ts": stamps[position],
                            "event": event, "line_kind": line.kind, "center": center,
                            "lower": center - line.width, "upper": center + line.width,
                            "slope_per_bar": line.slope, "first_pivot_position": line.anchor_pos,
                            "first_pivot_price": line.anchor_price, "first_pivot_kind": line.source_kind,
                            "first_confirmed_position": line.source_confirmed,
                            "second_pivot_position": line.second_pos, "second_pivot_price": line.second_price,
                            "second_pivot_kind": line.second_kind, "second_confirmed_position": line.created,
                            "reaction_count": line.reaction_count, **kwargs})

    for pos in range(len(bars)):
        for line in lines:
            if pos <= line.created:
                continue
            center = line.center(pos)
            if center + line.width <= 0:
                continue
            lower, upper = center - line.width, center + line.width
            touching = lows[pos] <= upper and highs[pos] >= lower
            side = _side(closes[pos], lower, upper)
            if line.active is None and touching:
                visit_id = f"{line.id}:v{len(line.visits)+1}"
                visit = {"visit_id": visit_id, "start": pos, "end": None}
                line.visits.append(visit)
                line.active, line.outside = visit, 0
                snap = {"visit_id": visit_id, "zone_id": line.id, "position": pos, "bar_ts": stamps[pos],
                        "line_kind": line.kind, "center": center, "lower": lower, "upper": upper,
                        "slope_per_bar": line.slope, "reaction_count": line.reaction_count,
                        "prior_visits": len(line.visits) - 1, "approach_side": line.last_side,
                        "reference_close": closes[pos], "atr": atrs[pos] if math.isfinite(atrs[pos]) else None}
                snap.update(_approach(closes, pos, atrs[pos]))
                starts.append(snap)
                events.append({"visit_id": visit_id, "position": pos, "bar_ts": stamps[pos], "event": "visit_start"})
            if line.active is not None:
                visit_id = line.active["visit_id"]
                if touching:
                    events.append({"visit_id": visit_id, "position": pos, "bar_ts": stamps[pos], "event": "touch_bar"})
                if lows[pos] < lower and highs[pos] > upper:
                    events.append({"visit_id": visit_id, "position": pos, "bar_ts": stamps[pos], "event": "both_boundaries_ambiguous"})
                elif highs[pos] > upper and closes[pos] <= upper:
                    events.append({"visit_id": visit_id, "position": pos, "bar_ts": stamps[pos], "event": "upper_wick_outside"})
                elif lows[pos] < lower and closes[pos] >= lower:
                    events.append({"visit_id": visit_id, "position": pos, "bar_ts": stamps[pos], "event": "lower_wick_outside"})
                if side in {"above", "below"}:
                    line.outside += 1
                    events.append({"visit_id": visit_id, "position": pos, "bar_ts": stamps[pos], "event": f"close_{side}"})
                else:
                    line.outside = 0
                if line.outside >= config.zone.exit_closes:
                    line.active["end"] = pos
                    events.append({"visit_id": visit_id, "position": pos, "bar_ts": stamps[pos], "event": "visit_end"})
                    line.active, line.outside = None, 0
            line.last_side = side

        for pivot in by_confirmation.get(pos, []):
            pivot_pos, price = int(pivot["pivot_position"]), float(pivot["price"])
            # Çizgiler sadece bilinen andan sonraki, ayrı bir ziyarette tepki toplar.
            for line in lines:
                if pivot_pos <= line.created or abs(price - line.center(pivot_pos)) > line.width:
                    continue
                visits = [v for v in line.visits if v["start"] <= pivot_pos and (v["end"] is None or pivot_pos <= v["end"])]
                if visits and visits[-1]["visit_id"] not in line.reaction_visits:
                    visit_id = visits[-1]["visit_id"]
                    line.reaction_visits.add(visit_id)
                    zone_event(line, pos, "reaction_confirmed", pivot_position=pivot_pos,
                               pivot_ts=str(pivot["pivot_ts"]), pivot_kind=pivot["kind"], visit_id=visit_id)
            width = (price * config.zone.tolerance if config.zone.method == "percent"
                     else atrs[pos] * config.zone.tolerance)
            if math.isfinite(width) and width > 0:
                for kind in ("high", "low"):
                    eligible = [p for p in known_pivots if p["kind"] == kind and
                                config.min_anchor_distance <= pivot_pos - int(p["pivot_position"]) <= config.max_anchor_distance]
                    for first in eligible[-config.max_anchors_per_kind:]:
                        first_pos = int(first["pivot_position"])
                        slope = (price - float(first["price"])) / (pivot_pos - first_pos)
                        line_kind = "high_high" if kind == pivot["kind"] == "high" else (
                            "low_low" if kind == pivot["kind"] == "low" else "mixed")
                        line = _Line(id=f"{prefix}:z{len(lines)+1}", kind=line_kind,
                                     anchor_pos=first_pos, anchor_price=float(first["price"]),
                                     second_pos=pivot_pos, second_price=price, slope=slope, width=width,
                                     created=pos, source_confirmed=int(first["confirmed_position"]),
                                     source_kind=kind, second_kind=pivot["kind"])
                        lines.append(line)
                        zone_event(line, pos, "zone_created", pivot_position=pivot_pos,
                                   pivot_ts=str(pivot["pivot_ts"]), pivot_kind=pivot["kind"], visit_id=None)
            known_pivots.append(pivot)
    zcols = ["zone_id", "position", "bar_ts", "event", "line_kind", "center", "lower", "upper", "slope_per_bar",
             "first_pivot_position", "first_pivot_price", "first_pivot_kind", "first_confirmed_position",
             "second_pivot_position", "second_pivot_price", "second_pivot_kind", "second_confirmed_position",
             "reaction_count", "pivot_position", "pivot_ts", "pivot_kind", "visit_id"]
    vcols = ["visit_id", "zone_id", "position", "bar_ts", "line_kind", "center", "lower", "upper", "slope_per_bar",
             "reaction_count", "prior_visits", "approach_side", "reference_close", "atr",
             "approach_return_5", "approach_speed_atr_5", "approach_efficiency_5"]
    return (pd.DataFrame(zone_events, columns=zcols), pd.DataFrame(starts, columns=vcols),
            pd.DataFrame(events, columns=["visit_id", "position", "bar_ts", "event"]))
