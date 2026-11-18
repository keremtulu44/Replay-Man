"""Bölge başına nedensel ziyaret ve iki aşamalı senaryo motoru.

Her ziyaret için temas tarafı önceki kapanışa dayanır; iki ardışık aynı taraf
kapanışla biter. Etiket sadece o an bilinen önceki tamamlanmış ziyareti kullanır.
Aralıklar bar sırasıyladır, çoklu periyot/seans kapanışları varsayılmaz.
"""
from __future__ import annotations

import math
import pandas as pd


def side(close: float, lower: float, upper: float) -> str:
    return 'above' if close > upper else 'below' if close < lower else 'inside'


def track_zone(bars: pd.DataFrame, zone: dict) -> list[dict]:
    """Bilinen bir bölge için ziyareti izler; son açık ziyaret sansürlüdür.

    Bölge oluşumundan sonra dış kapanış görülmeden yeni ziyaret başlamaz.
    Hareketli alanın merkezi oluşturulduğu barın konumundan eğimle ilerler.
    """
    start = int(zone['position'])
    lower, upper = float(zone['lower']), float(zone['upper'])
    raw_slope = zone.get('slope_per_bar', 0.0)
    slope = float(raw_slope) if pd.notna(raw_slope) else 0.0
    if start < 0 or start >= len(bars) or not all(map(math.isfinite, (lower, upper, slope))) or lower > upper:
        raise ValueError('Bölge geometrisi geçersiz')
    close = bars.close.to_numpy(dtype=float)
    high = bars.high.to_numpy(dtype=float)
    low = bars.low.to_numpy(dtype=float)
    timestamps = bars.ts_utc.to_numpy()
    armed, active, previous = False, None, None
    last_outside = None
    run = 0
    visits = []
    for pos in range(start + 1, len(bars)):
        off = slope * (pos - start)
        lo, hi = lower + off, upper + off
        if hi <= 0:
            # Geçersiz geometride geleceğe dair yargıda bulunulmaz.
            break
        current = side(close[pos], lo, hi)
        touching = low[pos] <= hi and high[pos] >= lo
        if not armed:
            if current != 'inside':
                armed = True
            continue
        if active is None and touching:
            prev_off = slope * (pos - 1 - start)
            approach = side(close[pos-1], lower + prev_off, upper + prev_off)
            active = {'zone_id':zone['zone_id'], 'visit_number':len(visits)+1, 'start_position':pos,
                      'start_bar_ts':str(timestamps[pos]), 'start_side':approach,
                      'lower_at_start':lo, 'upper_at_start':hi, 'touch_bars':0, 'ambiguous_bars':0,
                      'prior_visit_number': previous['visit_number'] if previous else None,
                      'prior_end_position': previous['end_position'] if previous else None,
                      'prior_start_side': previous['start_side'] if previous else None,
                      'prior_end_side': previous['end_side'] if previous else None,
                      'prior_path': previous['path'] if previous else None,
                      'prior_scenario': previous['scenario'] if previous else None}
            last_outside, run = None, 0
        if active is None:
            continue
        active['touch_bars'] += int(touching)
        active['ambiguous_bars'] += int(low[pos] < lo and high[pos] > hi)
        if current == 'inside':
            last_outside, run = None, 0
        else:
            run = run + 1 if current == last_outside else 1
            last_outside = current
        if run >= 2:
            approach = active['start_side']
            path = 'unknown' if approach not in ('above', 'below') else ('same' if current == approach else 'cross')
            scenario = ('up_candidate' if current == 'above' else 'down_candidate') if path == 'cross' else ('unknown' if path == 'unknown' else 'none')
            if previous and previous['path'] == 'cross' and approach == previous['end_side']:
                if path == 'same':
                    scenario = 'up_retest' if current == 'above' else 'down_retest'
                elif path == 'cross':
                    scenario = 'mixed'
            row = {**active, 'end_position':pos, 'end_bar_ts':str(timestamps[pos]), 'end_side':current,
                   'status':'completed', 'path':path, 'scenario':scenario,
                   'duration_bars':pos-active['start_position']+1}
            visits.append(row)
            previous = row
            active = None
            last_outside, run = None, 0
    if active is not None:
        visits.append({**active, 'end_position':None, 'end_bar_ts':None, 'end_side':None,
                       'status':'censored', 'path':'unknown', 'scenario':'unknown', 'duration_bars':None})
    return visits
