"""Nedensel kırılım yaşam döngüsü ve ayrıca zamanlanmış karşı genişleme."""
from __future__ import annotations

import numpy as np
import pandas as pd


_EXTRA_COLUMNS = (
    "level_id", "attempt_number", "outside_duration", "old_area_depth_atr",
    "retest_approach_speed_atr", "retest_recovery_ratio",
    "counter_expansion_position", "counter_expansion_bars",
    "origin_failure_position", "origin_failure_ts", "source_break_position",
)
_CONTEXT_COLUMNS = (
    "body_ratio", "close_location", "range_atr", "path_efficiency",
    "directional_persistence", "mean_overlap", "body_decay_ratio", "progress_decay_ratio",
)


def enrich_lifecycle(
    events: pd.DataFrame,
    bars: pd.DataFrame,
    features: pd.DataFrame,
    *,
    counter_expansion_bars: int = 10,
) -> pd.DataFrame:
    """Olayları zenginleştir ve karşı genişlemeyi yalnız gerçekleştiği barda yayımla.

    Eski uygulama gelecekteki karşı genişleme konumunu doğrudan `failure` satırına
    yazıyordu. Bu bilgi failure kapanışında bilinemez. Artık failure satırı aynı
    kalır; ilk karşı kapanış gerçekleşirse `counter_expansion` adlı **ayrı** bir
    olay, kendi `event_position` ve `event_ts` değerleriyle eklenir. Hiç
    gerçekleşmez veya veri biterse bu olay üretilmez; bu iki durumun ayrımı için
    çağıran taraf takip penceresini ayrıca saymalıdır.
    """
    if counter_expansion_bars < 1:
        raise ValueError("Karşı genişleme penceresi pozitif olmalı")
    result = events.copy()
    if not result.empty and result["event"].eq("counter_expansion").any():
        raise ValueError("Girdi zaten karşı genişleme olayları içeriyor; ham yapı olayları gerekli")
    # Eski, ileri-bilgili satırlar yanlışlıkla yeniden verilirse değer taşımayın.
    # Tüm yaşam döngüsü alanları ham olaylardan nedensel olarak yeniden kurulur.
    for column in _EXTRA_COLUMNS:
        result[column] = np.nan if column not in {"level_id", "origin_failure_ts"} else None
    if result.empty:
        return result
    if len(features) != len(bars):
        raise ValueError("Özellik ve bar uzunlukları eşleşmiyor")
    result = result.sort_values(["source_pivot_position", "event_position", "event"]).reset_index(drop=True)
    result["level_id"] = [f"{row.level}:{row.source_pivot_position}:{row.direction}" for row in result.itertuples()]
    atr = features["atr"]
    confirmations: list[dict] = []
    for _, indices in result.groupby("level_id", sort=False).groups.items():
        attempts = 0
        break_pos = None
        break_price = None
        for i in indices:
            event = result.at[i, "event"]
            pos = int(result.at[i, "event_position"])
            direction = result.at[i, "direction"]
            level = float(result.at[i, "level_price"])
            a = float(atr.iloc[pos]) if pd.notna(atr.iloc[pos]) else np.nan
            if event == "probe_rejection":
                attempts += 1
                result.at[i, "attempt_number"] = attempts
            elif event == "close_break":
                attempts += 1
                result.at[i, "attempt_number"] = attempts
                break_pos = pos
                break_price = float(bars.close.iloc[pos])
                result.at[i, "source_break_position"] = pos
            elif break_pos is not None:
                result.at[i, "attempt_number"] = attempts
                result.at[i, "outside_duration"] = pos - break_pos
                result.at[i, "source_break_position"] = break_pos
                segment = bars.iloc[break_pos:pos + 1]
                extreme = float(segment.high.max() if direction == "up" else segment.low.min())
                excursion = abs(extreme - level)
                if event == "retest_hold":
                    result.at[i, "retest_approach_speed_atr"] = excursion / a / max(pos - break_pos, 1) if np.isfinite(a) and a > 0 else np.nan
                    total = abs(break_price - level)
                    result.at[i, "retest_recovery_ratio"] = abs(float(bars.close.iloc[pos]) - level) / total if total else np.nan
                if event != "failure":
                    continue
                depth = level - float(bars.close.iloc[pos]) if direction == "up" else float(bars.close.iloc[pos]) - level
                result.at[i, "old_area_depth_atr"] = depth / a if np.isfinite(a) and a > 0 else np.nan
                boundary = float(bars.low.iloc[break_pos] if direction == "up" else bars.high.iloc[break_pos])
                for j in range(pos + 1, min(pos + counter_expansion_bars + 1, len(bars))):
                    close = float(bars.close.iloc[j])
                    crossed = close < boundary if direction == "up" else close > boundary
                    if not crossed:
                        continue
                    row = result.loc[i].to_dict()
                    now_atr = float(atr.iloc[j]) if pd.notna(atr.iloc[j]) else np.nan
                    row.update({
                        "event": "counter_expansion", "event_position": j,
                        "event_ts": bars.ts_utc.iloc[j],
                        "origin_failure_position": pos, "origin_failure_ts": bars.ts_utc.iloc[pos],
                        "counter_expansion_position": j, "counter_expansion_bars": j - pos,
                        "source_break_position": break_pos,
                        "outside_duration": j - break_pos,
                        "bars_since_break": j - break_pos,
                        "level_age_bars": j - int(row["source_confirmed_position"]),
                        "distance_close_atr": (close - level) / now_atr if np.isfinite(now_atr) and now_atr > 0 else np.nan,
                    })
                    # Bağlam artık failure zamanına değil, teyidin bilindiği zamana aittir.
                    for column in _CONTEXT_COLUMNS:
                        if column in row:
                            row[column] = features.iloc[j].get(column, np.nan)
                    confirmations.append(row)
                    break
    if confirmations:
        result = pd.concat([result, pd.DataFrame(confirmations)], ignore_index=True)
    return result.sort_values(["event_position", "source_pivot_position", "event"]).reset_index(drop=True)
