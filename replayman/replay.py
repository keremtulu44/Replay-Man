"""Gelecek sızıntısız OHLCV replay ve ilk fiyat-davranışı ölçümleri."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import numpy as np
import pandas as pd

REQUIRED = ("ts_utc", "open", "high", "low", "close", "volume")


def load_bars(path: str | Path, *, complete_only: bool = True) -> pd.DataFrame:
    """Bir bar CSV'sini zaman sırasıyla, sayısal ve tekil zaman damgalı yükler."""
    frame = pd.read_csv(path)
    missing = set(REQUIRED) - set(frame.columns)
    if missing:
        raise ValueError(f"Eksik OHLCV kolonları: {sorted(missing)}")
    frame["ts_utc"] = pd.to_datetime(frame["ts_utc"], utc=True, errors="raise")
    for column in ("open", "high", "low", "close", "volume"):
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame = frame.dropna(subset=["open", "high", "low", "close"])
    if complete_only and "complete" in frame:
        complete = frame["complete"].astype(str).str.lower().isin({"true", "1"})
        frame = frame.loc[complete]
    frame = frame.sort_values("ts_utc").drop_duplicates("ts_utc", keep="last").reset_index(drop=True)
    invalid = (frame["high"] < frame[["open", "close", "low"]].max(axis=1)) | (
        frame["low"] > frame[["open", "close", "high"]].min(axis=1)
    )
    if invalid.any():
        raise ValueError(f"OHLC geometrisi bozuk {int(invalid.sum())} bar")
    return frame


def _safe_ratio(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    return numerator.div(denominator.replace(0, np.nan))


def causal_features(bars: pd.DataFrame, *, atr_window: int = 14, quality_window: int = 10) -> pd.DataFrame:
    """Yalnız mevcut ve geçmiş barları kullanarak kitap tabanlı ilk özellikleri üretir.

    Çıktı aynı indeks ve zaman damgasına sahiptir. Hiçbir negatif shift veya
    merkezlenmiş pencere kullanılmaz.
    """
    if atr_window < 2 or quality_window < 2:
        raise ValueError("Pencere uzunlukları en az 2 olmalı")
    out = bars[[c for c in bars.columns if c in REQUIRED or c in {"asset_id", "symbol", "interval", "session_date"}]].copy()
    o, h, l, c = (bars[x].astype(float) for x in ("open", "high", "low", "close"))
    previous_close = c.shift(1)
    span = h - l
    body_signed = c - o
    body = body_signed.abs()
    out["range"] = span
    out["body"] = body
    out["direction"] = np.sign(body_signed).astype("int8")
    out["body_ratio"] = _safe_ratio(body, span)
    out["upper_wick"] = h - pd.concat([o, c], axis=1).max(axis=1)
    out["lower_wick"] = pd.concat([o, c], axis=1).min(axis=1) - l
    out["close_location"] = _safe_ratio(c - l, span)
    out["gap_from_previous_close"] = _safe_ratio(o - previous_close, previous_close.abs())
    out["inside_bar"] = ((h <= h.shift(1)) & (l >= l.shift(1))).astype("int8")
    out["outside_bar"] = ((h >= h.shift(1)) & (l <= l.shift(1))).astype("int8")
    overlap = pd.concat([h, h.shift(1)], axis=1).min(axis=1) - pd.concat([l, l.shift(1)], axis=1).max(axis=1)
    union = pd.concat([h, h.shift(1)], axis=1).max(axis=1) - pd.concat([l, l.shift(1)], axis=1).min(axis=1)
    out["overlap_ratio"] = _safe_ratio(overlap.clip(lower=0), union)
    true_range = pd.concat([span, (h - previous_close).abs(), (l - previous_close).abs()], axis=1).max(axis=1)
    out["true_range"] = true_range
    out["atr"] = true_range.rolling(atr_window, min_periods=atr_window).mean()
    out["range_atr"] = _safe_ratio(span, out["atr"])
    out["return_1"] = c.pct_change(fill_method=None)
    out["volume_relative"] = _safe_ratio(bars["volume"], bars["volume"].rolling(20, min_periods=20).median())

    # Hareket kalitesi: net yer değiştirme / kapanışların kat ettiği toplam yol.
    net = (c - c.shift(quality_window)).abs()
    path = c.diff().abs().rolling(quality_window, min_periods=quality_window).sum()
    out["path_efficiency"] = _safe_ratio(net, path)
    out["directional_persistence"] = out["direction"].rolling(quality_window, min_periods=quality_window).mean().abs()
    out["mean_overlap"] = out["overlap_ratio"].rolling(quality_window, min_periods=quality_window).mean()

    # Baskı kaybı adayları: yakın dönemi bir önceki eşit pencereyle karşılaştırır.
    recent_body = body.rolling(3, min_periods=3).mean()
    prior_body = body.shift(3).rolling(3, min_periods=3).mean()
    out["body_decay_ratio"] = _safe_ratio(recent_body, prior_body)
    recent_progress = c.diff().abs().rolling(3, min_periods=3).sum()
    prior_progress = c.diff().abs().shift(3).rolling(3, min_periods=3).sum()
    out["progress_decay_ratio"] = _safe_ratio(recent_progress, prior_progress)
    return out


@dataclass(frozen=True)
class ReplayStep:
    position: int
    timestamp: pd.Timestamp
    bar: pd.Series
    features: pd.Series


class ReplayEngine:
    """Barları sırayla açan, gelecek satırlara erişim vermeyen replay imleci."""

    def __init__(self, bars: pd.DataFrame, features: pd.DataFrame | None = None):
        self._bars = bars.reset_index(drop=True).copy()
        self._features = (features if features is not None else causal_features(self._bars)).reset_index(drop=True)
        if len(self._bars) != len(self._features):
            raise ValueError("Bar ve özellik satır sayıları eşleşmiyor")
        self._position = -1

    @property
    def position(self) -> int:
        return self._position

    @property
    def history(self) -> pd.DataFrame:
        """Yalnız son açılmış bara kadar olan savunmalı kopya."""
        return self._features.iloc[: self._position + 1].copy()

    def __iter__(self) -> Iterator[ReplayStep]:
        return self

    def __next__(self) -> ReplayStep:
        position = self._position + 1
        if position >= len(self._bars):
            raise StopIteration
        self._position = position
        return ReplayStep(position, self._bars.at[position, "ts_utc"], self._bars.iloc[position].copy(), self._features.iloc[position].copy())


def forward_outcomes(bars: pd.DataFrame, horizons: tuple[int, ...] = (1, 3, 5, 10, 20)) -> pd.DataFrame:
    """Araştırma sonucu üretir; sinyal özelliği değildir ve replay kararına verilmemelidir."""
    close = bars["close"].astype(float)
    high, low = bars["high"].astype(float), bars["low"].astype(float)
    result = pd.DataFrame({"ts_utc": bars["ts_utc"]})
    for horizon in horizons:
        if horizon < 1:
            raise ValueError("Sonuç ufku pozitif olmalı")
        result[f"return_fwd_{horizon}"] = close.shift(-horizon).div(close).sub(1)
        # current bar hariç, sonraki horizon barı.
        future_high = high.shift(-1)[::-1].rolling(horizon, min_periods=horizon).max()[::-1]
        future_low = low.shift(-1)[::-1].rolling(horizon, min_periods=horizon).min()[::-1]
        result[f"mfe_{horizon}"] = future_high.div(close).sub(1)
        result[f"mae_{horizon}"] = future_low.div(close).sub(1)
    return result
