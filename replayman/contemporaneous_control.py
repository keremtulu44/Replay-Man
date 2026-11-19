"""Aynı bar etiketinde fiyat-temelli başka-hisse kontrolü (gözlemsel)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .dip_research import atr14


def bar_context(bars: pd.DataFrame, asset: str, interval: str) -> pd.DataFrame:
    """Eşleşme için yalnız sinyal barına kadar bilinen OHLC özellikleri."""
    data = bars.reset_index(drop=True)
    if data.ts_utc.duplicated().any() or not data.ts_utc.is_monotonic_increasing:
        raise ValueError("Seride zaman sıralı ve tekil olmalı")
    close = data.close.astype(float)
    atr = atr14(data)
    previous_atr = atr.shift(1)
    previous_close = close.shift(1)
    low5 = data.low.astype(float).shift(1).rolling(5, min_periods=5).min()
    bullish = close > data.open.astype(float)
    failed = (data.low.astype(float) < low5) & (close > low5) & bullish
    return pd.DataFrame({"asset_id": asset, "interval": interval, "position": np.arange(len(data)),
                         "ts_utc": data.ts_utc, "atr": atr, "bullish": bullish, "raw_a": failed,
                         "prior_move_atr": (previous_close - close.shift(6)) / previous_atr.replace(0, np.nan),
                         "prior_atr_fraction": previous_atr / previous_close.replace(0, np.nan)})


def match_at_same_bar(signals: pd.DataFrame, contexts: pd.DataFrame) -> pd.DataFrame:
    """Kontrolü aynı etiketli farklı hisseden seç; hiçbir sonuç/gelecek okunmaz.

    Kontrol raw A değildir ve yükseliş mumu olmalıdır. Önceki 5 bar hareketi
    ATR cinsinden en fazla 1 farklı, önceki ATR/kapanış ölçeği 0,5–2 kat
    olmalıdır. Her kontrol aynı bar etiketinde yalnız bir A'ya atanır.
    """
    ctx = contexts.copy()
    ctx["ts_utc"] = pd.to_datetime(ctx.ts_utc, utc=True)
    key = ["asset_id", "interval", "ts_utc"]
    if ctx.duplicated(key).any():
        raise ValueError("Aynı hisse/periyot/etikette birden fazla bar var")
    sig = signals.copy()
    sig["signal_ts"] = pd.to_datetime(sig.signal_ts, utc=True)
    if sig.signal_id.duplicated().any():
        raise ValueError("Sinyal kimlikleri tekil olmalı")
    candidates = ctx.loc[ctx.bullish & ~ctx.raw_a & np.isfinite(ctx.atr) & (ctx.atr > 0)
                         & np.isfinite(ctx.prior_move_atr) & np.isfinite(ctx.prior_atr_fraction)
                         & (ctx.prior_atr_fraction > 0)]
    grouped = {(interval, ts): group for (interval, ts), group in candidates.groupby(["interval", "ts_utc"], sort=False)}
    indexed = ctx.set_index(key)
    rows = []
    for (interval, ts), group in sig.groupby(["interval", "signal_ts"], sort=True):
        used: set[str] = set()
        pool = grouped.get((interval, ts))
        for signal in group.sort_values(["asset_id", "signal_id"]).to_dict("records"):
            base = {"signal_id": signal["signal_id"], "asset_id": signal["asset_id"], "interval": interval,
                    "period": signal["period"], "signal_position": int(signal["signal_position"]), "signal_ts": ts,
                    "control_asset_id": None, "control_position": None, "control_atr": None,
                    "a_prior_move_atr": None, "control_prior_move_atr": None,
                    "a_prior_atr_fraction": None, "control_prior_atr_fraction": None,
                    "trend_distance": None, "volatility_ratio": None, "control_status": "no_control"}
            signal_key = (signal["asset_id"], interval, ts)
            if signal_key not in indexed.index:
                raise ValueError(f"Sinyal barı bağlamda yok: {signal_key}")
            origin = indexed.loc[signal_key]
            if int(origin.position) != int(signal["signal_position"]) or not bool(origin.raw_a):
                raise ValueError("A sinyali raw failed_low5 ile uyuşmuyor")
            move, volatility = float(origin.prior_move_atr), float(origin.prior_atr_fraction)
            if not np.isfinite(move) or not np.isfinite(volatility) or volatility <= 0:
                base["control_status"] = "unknown_context"
                rows.append(base)
                continue
            base.update({"a_prior_move_atr": move, "a_prior_atr_fraction": volatility})
            if pool is None:
                rows.append(base)
                continue
            valid = pool.loc[(pool.asset_id != signal["asset_id"]) & ~pool.asset_id.isin(used)].copy()
            valid["distance"] = (valid.prior_move_atr - move).abs()
            valid["ratio"] = volatility / valid.prior_atr_fraction
            valid = valid.loc[(valid.distance <= 1.0) & valid.ratio.between(.5, 2., inclusive="both")].copy()
            if valid.empty:
                rows.append(base)
                continue
            valid["log_ratio_distance"] = np.log(valid.ratio).abs()
            chosen = valid.sort_values(["distance", "log_ratio_distance", "asset_id"], kind="stable").iloc[0]
            used.add(str(chosen.asset_id))
            base.update({"control_asset_id": chosen.asset_id, "control_position": int(chosen.position),
                         "control_atr": float(chosen.atr), "control_prior_move_atr": float(chosen.prior_move_atr),
                         "control_prior_atr_fraction": float(chosen.prior_atr_fraction),
                         "trend_distance": float(chosen.distance), "volatility_ratio": float(chosen.ratio),
                         "control_status": "matched"})
            rows.append(base)
    return pd.DataFrame(rows)
