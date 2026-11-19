"""Önceden görülmüş sonuçlar için ek gözlemsel kontrol ve blok belirsizliği.

Kontrol seçiminde yalnız daha önce kapanmış barlar kullanılır. Eşleşmenin kendisi
ve takip sonuçları nedensel karşı-olgusal, gerçek işlem veya ileri test değildir.
"""
from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from .dip_research import Period, atr14, period_at


def prior_bull_controls(bars: pd.DataFrame, signals: pd.DataFrame, periods: Iterable[Period]) -> pd.DataFrame:
    """Her A için aynı hisse/haftada önceki en yakın farklı yükseliş barı.

    Ham failed_low5 barları ve ATR'si bilinmeyen barlar aday değildir. Seçim
    kronolojiktir; bir kontrol barı en fazla bir kez kullanılır. `signals`
    yalnız aynı seriye ait A kayıtları içermelidir.
    """
    data = bars.reset_index(drop=True)
    if data.ts_utc.duplicated().any() or not data.ts_utc.is_monotonic_increasing:
        raise ValueError("Bar zamanları tekil ve sıralı olmalı")
    if signals.signal_id.duplicated().any():
        raise ValueError("A sinyal kimlikleri tekil olmalı")
    periods = list(periods)
    atr = atr14(data)
    low5 = data.low.astype(float).shift(1).rolling(5, min_periods=5).min()
    bullish = data.close.astype(float) > data.open.astype(float)
    raw_a = (data.low.astype(float) < low5) & (data.close.astype(float) > low5) & bullish
    weeks = pd.to_datetime(data.ts_utc, utc=True).dt.tz_convert("Europe/Istanbul").dt.strftime("%G-W%V").tolist()
    used: set[int] = set()
    rows = []
    for signal in signals.sort_values("signal_position").to_dict("records"):
        pos = int(signal["signal_position"])
        if pos < 0 or pos >= len(data) or not bool(raw_a.iloc[pos]):
            raise ValueError(f"Geçersiz failed_low5 konumu: {pos}")
        if pd.Timestamp(signal["signal_ts"]) != data.ts_utc.iloc[pos]:
            raise ValueError("Sinyal barı konumu/zamanı uyuşmuyor")
        period = period_at(data.ts_utc.iloc[pos], periods)
        if period is None or period.name != signal["period"]:
            raise ValueError("Sinyal bölümü uyuşmuyor")
        chosen = None
        for candidate in range(pos - 1, -1, -1):
            if weeks[candidate] != weeks[pos] or data.ts_utc.iloc[candidate] < period.start:
                break
            a = float(atr.iloc[candidate]) if pd.notna(atr.iloc[candidate]) else np.nan
            if candidate not in used and bool(bullish.iloc[candidate]) and not bool(raw_a.iloc[candidate]) and np.isfinite(a) and a > 0:
                chosen = candidate
                used.add(candidate)
                break
        rows.append({"signal_id": signal["signal_id"], "signal_position": pos, "signal_ts": data.ts_utc.iloc[pos],
                     "period": period.name, "control_position": chosen,
                     "control_ts": data.ts_utc.iloc[chosen] if chosen is not None else None,
                     "control_atr": float(atr.iloc[chosen]) if chosen is not None else None,
                     "bar_gap": pos - chosen if chosen is not None else None,
                     "control_status": "matched" if chosen is not None else "no_prior_control"})
    return pd.DataFrame(rows, columns=["signal_id", "signal_position", "signal_ts", "period", "control_position",
                                       "control_ts", "control_atr", "bar_gap", "control_status"])


def week_starts(values: pd.Series) -> pd.Series:
    """İstanbul yerel haftasının pazartesi tarihleri (saat dilimsiz takvim)."""
    local = pd.to_datetime(values, utc=True).dt.tz_convert("Europe/Istanbul").dt.tz_localize(None)
    return (local.dt.normalize() - pd.to_timedelta(local.dt.day_of_week, unit="D"))


def block_bootstrap_mean(values: pd.Series, times: pd.Series, *, draws: int = 2000, block_weeks: int = 5,
                         seed: int = 20261119) -> dict:
    """Ardışık 5 takvim haftasını (boş haftalar dahil) yeniden örnekle.

    Aynı hafta içindeki bütün varlıkları birlikte tutar. Dönemler arasındaki
    kalıntı bağımlılık ve çoklu keşif sorununu çözmez. En az 20 gözlem haftası
    ve en az dört blokluk takvim aralığı yoksa güven aralığı üretilmez.
    """
    if draws < 1 or block_weeks < 1:
        raise ValueError("Blok ve çekim sayıları pozitif olmalı")
    frame = pd.DataFrame({"value": pd.to_numeric(values, errors="coerce").to_numpy(),
                          "time": pd.to_datetime(times, utc=True).to_numpy()})
    frame = frame.loc[frame.value.notna() & frame.time.notna()].copy()
    result = {"count": len(frame), "observed_weeks": 0, "calendar_weeks": 0,
              "mean": np.nan, "ci_low": np.nan, "ci_high": np.nan, "valid_draws": 0}
    if frame.empty:
        return result
    frame["week"] = week_starts(frame.time)
    n_observed = int(frame.week.nunique())
    calendar = pd.date_range(frame.week.min(), frame.week.max(), freq="W-MON")
    result.update({"observed_weeks": n_observed, "calendar_weeks": len(calendar), "mean": float(frame.value.mean())})
    minimum_weeks = max(20, 4 * block_weeks)
    if n_observed < minimum_weeks or len(calendar) < minimum_weeks:
        return result
    grouped = frame.groupby("week").value.agg(["sum", "count"]).reindex(calendar, fill_value=0)
    sums = grouped["sum"].to_numpy(float)
    counts = grouped["count"].to_numpy(float)
    n = len(calendar)
    n_blocks = (n + block_weeks - 1) // block_weeks
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n - block_weeks + 1, size=(draws, n_blocks))
    indices = (starts[..., None] + np.arange(block_weeks)).reshape(draws, -1)[:, :n]
    sampled_sum = sums[indices].sum(axis=1)
    sampled_count = counts[indices].sum(axis=1)
    averages = sampled_sum[sampled_count > 0] / sampled_count[sampled_count > 0]
    if len(averages):
        result.update({"ci_low": float(np.quantile(averages, .025)), "ci_high": float(np.quantile(averages, .975)),
                       "valid_draws": len(averages)})
    return result
