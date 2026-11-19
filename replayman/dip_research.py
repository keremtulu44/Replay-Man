"""Hacimsiz ve bilinebilirlik zamanı açık dip adayı araştırması.

Sinyal üretimi ile sonradan bilinen dip/gelecek sonuçları ayrı fonksiyonlardır.
Bu modül emir göndermez; açılış, stop ve maliyetler fiyat vekilleridir.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd

from .swings import SwingConfig, confirmed_swings
from .zone_memory import ZoneConfig, scan_zones


@dataclass(frozen=True)
class Period:
    name: str
    start: pd.Timestamp
    end: pd.Timestamp  # exclusive; bar labels, not verified exchange closes


def local_boundary(date: str) -> pd.Timestamp:
    """BIST yerel takvim gününün başlangıcı; seans kapanışı iddiası değildir."""
    return pd.Timestamp(date, tz="Europe/Istanbul").tz_convert("UTC")


def period_at(timestamp: pd.Timestamp, periods: Iterable[Period]) -> Period | None:
    stamp = pd.Timestamp(timestamp)
    for period in periods:
        if period.start <= stamp < period.end:
            return period
    return None


def atr14(bars: pd.DataFrame) -> pd.Series:
    """Yalnız o ana dek kapanmış OHLC; hacim hesaplanmaz."""
    high, low, close = (pd.to_numeric(bars[c], errors="coerce") for c in ("high", "low", "close"))
    prev = close.shift(1)
    true_range = pd.concat([high - low, (high - prev).abs(), (low - prev).abs()], axis=1).max(axis=1)
    return true_range.rolling(14, min_periods=14).mean()


def scan_candidates(bars: pd.DataFrame, *, series_key: str = "series") -> pd.DataFrame:
    """A adaylarını ve önceden bilinen B destek bağlamını üret.

    A dayanaklı cooldown dahil tüm girdiler sinyal kapanışında veya öncesinde
    bilinir. `zone_created`/`reaction_confirmed` olayı aynı barın ziyaretine
    geriye taşınmaz: yalnızca `zone.position < signal.position` kabul edilir.
    """
    data = bars.reset_index(drop=True)
    atr = atr14(data)
    open_, high, low, close = (data[c].astype(float) for c in ("open", "high", "low", "close"))
    previous_low = low.shift(1).rolling(5, min_periods=5).min()
    failed = (low < previous_low) & (close > previous_low) & (close > open_)
    zone_events, _, _ = scan_zones(data, config=ZoneConfig(method="atr", tolerance=0.25), series_key=series_key)
    zone_records = zone_events.to_dict("records")
    zone_index = 0
    known: dict[str, dict] = {}
    created_order = 0
    last_signal = -10
    result: list[dict] = []
    for pos in range(len(data)):
        while zone_index < len(zone_records) and int(zone_records[zone_index]["position"]) < pos:
            event = zone_records[zone_index]
            key = event["zone_id"]
            if key not in known:
                known[key] = {"created_position": int(event["position"]), "created_order": created_order}
                created_order += 1
            known[key].update({name: event[name] for name in ("role", "center", "lower", "upper", "reaction_count")})
            zone_index += 1
        a = float(atr.iloc[pos]) if pd.notna(atr.iloc[pos]) else np.nan
        if not bool(failed.iloc[pos]) or not np.isfinite(a) or a <= 0 or pos - last_signal < 10:
            continue
        last_signal = pos
        candidates = []
        for key, zone in known.items():
            if zone["role"] != "support_candidate":
                continue
            lower, upper = float(zone["lower"]), float(zone["upper"])
            if (float(low.iloc[pos]) <= upper and float(high.iloc[pos]) >= lower
                    and float(close.iloc[pos]) >= lower and float(close.iloc[pos - 1]) >= lower):
                width = (upper - lower) / 2
                if width > 0:
                    candidates.append((abs(float(low.iloc[pos]) - float(zone["center"])) / width,
                                       int(zone["created_order"]), key, zone))
        chosen = min(candidates, key=lambda x: x[:3]) if candidates else None
        zone = chosen[3] if chosen else None
        result.append({
            "signal_position": pos, "signal_ts": data.ts_utc.iloc[pos], "atr": a,
            "signal_open": float(open_.iloc[pos]), "signal_high": float(high.iloc[pos]),
            "signal_low": float(low.iloc[pos]), "signal_close": float(close.iloc[pos]),
            "prior_low5": float(previous_low.iloc[pos]), "support": bool(zone),
            "zone_id": chosen[2] if chosen else None,
            "zone_created_position": int(zone["created_position"]) if zone else None,
            "zone_lower": float(zone["lower"]) if zone else None,
            "zone_upper": float(zone["upper"]) if zone else None,
            "zone_reactions": int(zone["reaction_count"]) if zone else None,
        })
    columns = ["signal_position", "signal_ts", "atr", "signal_open", "signal_high", "signal_low", "signal_close",
               "prior_low5", "support", "zone_id", "zone_created_position", "zone_lower", "zone_upper", "zone_reactions"]
    return pd.DataFrame(result, columns=columns)


def confirmation_events(
    bars: pd.DataFrame, base: pd.DataFrame, periods: list[Period], *, window: int = 5
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """B için karşı teyidi ancak o kapanışta üret; B sonucu ayrı kaydet."""
    data = bars.reset_index(drop=True)
    atr = atr14(data)
    confirmed: list[dict] = []
    statuses: list[dict] = []
    used_positions: set[int] = set()
    for source in base.loc[base.support].sort_values("signal_position").to_dict("records"):
        origin = int(source["signal_position"])
        period = period_at(data.ts_utc.iloc[origin], periods)
        if period is None:
            continue
        outcome = "not_confirmed"
        for pos in range(origin + 1, origin + window + 1):
            if pos >= len(data) or data.ts_utc.iloc[pos] >= period.end:
                outcome = "censored"
                break
            if float(data.close.iloc[pos]) > float(source["signal_high"]):
                if pos in used_positions:
                    outcome = "duplicate_confirmation"
                    break
                a = float(atr.iloc[pos]) if pd.notna(atr.iloc[pos]) else np.nan
                if not np.isfinite(a) or a <= 0:
                    outcome = "unknown_atr"
                    break
                used_positions.add(pos)
                current = dict(source)
                current.update({
                    "origin_position": origin, "origin_ts": source["signal_ts"],
                    "confirmation_delay": pos - origin, "signal_position": pos,
                    "signal_ts": data.ts_utc.iloc[pos], "atr": a,
                    "signal_open": float(data.open.iloc[pos]), "signal_high": float(data.high.iloc[pos]),
                    "signal_low": float(data.low.iloc[pos]), "signal_close": float(data.close.iloc[pos]),
                })
                confirmed.append(current)
                outcome = "confirmed"
                break
        statuses.append({"origin_position": origin, "origin_ts": source["signal_ts"],
                         "period": period.name, "status": outcome})
    cols = list(base.columns) + ["origin_position", "origin_ts", "confirmation_delay"]
    return pd.DataFrame(confirmed, columns=cols), pd.DataFrame(statuses, columns=["origin_position", "origin_ts", "period", "status"])


def reference_lows(bars: pd.DataFrame, periods: list[Period]) -> pd.DataFrame:
    """Sonradan bilinen 5+5 yerel dip etiketleri; sinyal girdisi değildir."""
    data = bars.reset_index(drop=True)
    swings = confirmed_swings(data, config=SwingConfig(5, 5, tie_break="rightmost"), level="reference")
    rows = []
    for row in swings.loc[swings.kind == "low"].itertuples():
        p = int(row.pivot_position)
        period = period_at(data.ts_utc.iloc[p], periods)
        if period is None or p - 2 < 13 or p + 5 >= len(data):
            continue
        if data.ts_utc.iloc[p - 2] < period.start or data.ts_utc.iloc[p + 5] >= period.end:
            continue
        rows.append({"pivot_position": p, "pivot_ts": data.ts_utc.iloc[p],
                     "known_at_position": int(row.confirmed_position), "pivot_low": float(row.price), "period": period.name})
    return pd.DataFrame(rows, columns=["pivot_position", "pivot_ts", "known_at_position", "pivot_low", "period"])


def label_signal(signal: dict, bars: pd.DataFrame, pivots: pd.DataFrame, period: Period) -> dict:
    """Sadece değerlendirme etiketi: dip etiketi henüz oluşmamışsa bilinmiyor."""
    pos = int(signal["signal_position"])
    if pos + 7 >= len(bars) or bars.ts_utc.iloc[pos + 7] >= period.end:
        return {"label_status": "censored", "matched_pivot_position": None, "pivot_delay": None}
    choices = []
    for pivot in pivots.loc[pivots.period == period.name].to_dict("records"):
        p = int(pivot["pivot_position"])
        if p - 2 <= pos <= p + 3:
            price_gap = float(signal["signal_close"]) - float(pivot["pivot_low"])
            if 0 <= price_gap <= float(signal["atr"]):
                choices.append((abs(pos - p), p))
    if not choices:
        return {"label_status": "not_matched", "matched_pivot_position": None, "pivot_delay": None}
    _, pivot_pos = min(choices)
    return {"label_status": "matched", "matched_pivot_position": pivot_pos, "pivot_delay": pos - pivot_pos}


def evaluate_trade(
    bars: pd.DataFrame,
    signal: dict,
    period: Period,
    *,
    horizon: int,
    entry_lag: int,
    benchmark: pd.DataFrame | None = None,
) -> dict:
    """Girişteki 1 ATR stop/2 ATR hedef ve sabit ufuk; iki sıra ayrı.

    `entry_lag=1` sonraki kullanılabilir bar; 2 ek gecikme duyarlılığıdır.
    Gerçek seans ve emir gerçekleşme saati bu yaklaşımda doğrulanmış değildir.
    """
    if horizon < 1 or entry_lag < 1:
        raise ValueError("Ufuk ve gecikme pozitif olmalı")
    pos = int(signal["signal_position"])
    entry = pos + entry_lag
    end = entry + horizon - 1
    result = {
        "status": "censored", "entry_position": None, "end_position": None,
        "entry_ts": None, "end_ts": None, "entry_price": None,
        "fixed_return": None, "benchmark_return": None, "excess_return": None,
        "mfe": None, "mae": None, "trade_lower": None, "trade_upper": None,
        "exit_reason": None, "exit_position": None, "bars_held": None,
    }
    if end >= len(bars) or entry >= len(bars):
        return result
    if bars.ts_utc.iloc[entry] >= period.end or bars.ts_utc.iloc[end] >= period.end:
        return result
    entry_price = float(bars.open.iloc[entry])
    a = float(signal["atr"])
    if not np.isfinite(entry_price) or entry_price <= 0 or not np.isfinite(a) or a <= 0 or entry_price - a <= 0:
        result["status"] = "unknown"
        return result
    future = bars.iloc[entry:end + 1]
    values = future[["open", "high", "low", "close"]].to_numpy(dtype=float)
    if not np.isfinite(values).all() or (values <= 0).any():
        result["status"] = "unknown"
        return result
    fixed = float(bars.close.iloc[end]) / entry_price - 1
    result.update({
        "status": "observed", "entry_position": entry, "end_position": end,
        "entry_ts": bars.ts_utc.iloc[entry], "end_ts": bars.ts_utc.iloc[end], "entry_price": entry_price,
        "fixed_return": fixed, "mfe": float(future.high.max()) / entry_price - 1,
        "mae": float(future.low.min()) / entry_price - 1,
    })
    if benchmark is not None and not benchmark.empty:
        lookup = benchmark if benchmark.index.name == "ts_utc" else benchmark.set_index("ts_utc")
        if not lookup.index.is_unique:
            raise ValueError("Benchmark zaman etiketleri tekil olmalı")
        start_time, end_time = bars.ts_utc.iloc[entry], bars.ts_utc.iloc[end]
        if start_time in lookup.index and end_time in lookup.index:
            market_open, market_close = float(lookup.at[start_time, "open"]), float(lookup.at[end_time, "close"])
            if np.isfinite(market_open) and np.isfinite(market_close) and market_open > 0:
                result["benchmark_return"] = market_close / market_open - 1
                result["excess_return"] = fixed - result["benchmark_return"]
    stop, target = entry_price - a, entry_price + 2 * a
    for p in range(entry, end + 1):
        o, hi, lo = (float(bars.iloc[p][name]) for name in ("open", "high", "low"))
        if p > entry and o <= stop:
            lower = upper = o; reason = "gap_stop"
        elif p > entry and o >= target:
            lower = upper = o; reason = "gap_target"
        elif lo <= stop and hi >= target:
            lower, upper, reason = stop, target, "ambiguous"
        elif lo <= stop:
            lower = upper = stop; reason = "stop"
        elif hi >= target:
            lower = upper = target; reason = "target"
        elif p == end:
            lower = upper = float(bars.close.iloc[p]); reason = "time"
        else:
            continue
        result.update({"trade_lower": lower / entry_price - 1, "trade_upper": upper / entry_price - 1,
                       "exit_reason": reason, "exit_position": p, "bars_held": p - entry + 1})
        break
    return result
