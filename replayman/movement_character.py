"""Bölgeye gelişin kendi önceki bölümüyle karşılaştırılması; hacimsiz."""
from __future__ import annotations

import math
import pandas as pd


def approach_character(bars: pd.DataFrame, visits: pd.DataFrame) -> pd.DataFrame:
    """Temastan önceki 10 barın ilk ve son 5 barını karşılaştır.

    Yalnız temas barından önceki kapanışlar ve ATR kullanılır. Yaklaşım yönü,
    bir önceki barda bilinen bölge merkezine göre tanımlanır. Bu özellikler
    hareket sonundaki veya gelecekteki tepkiyi kullanmaz.
    """
    data = bars.reset_index(drop=True)
    close, high, low = (data[x].astype(float) for x in ("close", "high", "low"))
    previous = close.shift(1)
    atr = pd.concat([high - low, (high - previous).abs(), (low - previous).abs()], axis=1).max(axis=1).rolling(14, min_periods=14).mean()
    prices = close.tolist()
    rows = []
    for visit in visits.to_dict("records"):
        pos = int(visit['position'])
        if pos < 0 or pos >= len(data):
            raise ValueError(f"Ziyaret konumu veri dışında: {pos}")
        row = {"visit_id": visit['visit_id'], "known_at_position": pos - 1,
               "status": "insufficient_history", "approach_direction": None,
               "prior_progress_atr": None, "recent_progress_atr": None, "progress_change_atr": None,
               "prior_efficiency": None, "recent_efficiency": None,
               "direction_changes_10": None, "max_pullback_atr_10": None}
        if pos >= 11:
            seq = prices[pos-11:pos]
            slope = visit.get('slope_per_bar', 0.0)
            slope = float(slope) if pd.notna(slope) else 0.0
            previous_center = float(visit['center']) - slope
            direction = 1 if seq[-1] < previous_center else -1 if seq[-1] > previous_center else 0
            scale = float(atr.iloc[pos - 1])
            first = [b-a for a, b in zip(seq[:5], seq[1:6])]
            last = [b-a for a, b in zip(seq[5:10], seq[6:11])]
            def efficiency(delta):
                path = sum(abs(x) for x in delta)
                return abs(sum(delta)) / path if path else None
            changes = [x for x in first + last if x != 0]
            row.update({'status': 'observed' if direction and math.isfinite(scale) and scale > 0 else 'unknown',
                        'approach_direction': direction or None,
                        'prior_efficiency': efficiency(first), 'recent_efficiency': efficiency(last),
                        'direction_changes_10': sum(a*b < 0 for a, b in zip(changes, changes[1:]))})
            if direction and math.isfinite(scale) and scale > 0:
                prior, recent = direction * sum(first) / scale, direction * sum(last) / scale
                oriented = [direction * (x - seq[0]) for x in seq]
                peak, drawdown = oriented[0], 0.0
                for value in oriented:
                    peak = max(peak, value)
                    drawdown = max(drawdown, peak - value)
                row.update({'prior_progress_atr': prior, 'recent_progress_atr': recent,
                            'progress_change_atr': recent - prior, 'max_pullback_atr_10': drawdown / scale})
        rows.append(row)
    columns = ['visit_id', 'known_at_position', 'status', 'approach_direction', 'prior_progress_atr',
               'recent_progress_atr', 'progress_change_atr', 'prior_efficiency', 'recent_efficiency',
               'direction_changes_10', 'max_pullback_atr_10']
    return pd.DataFrame(rows, columns=columns)
