"""Oyalanma ve hızlı uzaklaşma kaynaklı nedensel bölge adayları.

OHLC temelli tanımlar emir akışı veya gizli alış/satış iddiası değildir.
Kaynak aralık sadece oluştuğu bar kapandığında öğrenilir; sınırlar sabittir.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math

import pandas as pd

from .zone_memory import ZoneConfig, _approach, _side


@dataclass(frozen=True)
class BehaviorConfig:
    kind: str
    zone: ZoneConfig = ZoneConfig()
    dwell_window: int = 10
    dwell_width_atr: float = 2.0
    impulse_bars: int = 5
    impulse_distance_atr: float = 2.0

    def __post_init__(self):
        if self.kind not in {'dwell', 'impulse'}:
            raise ValueError('kind dwell veya impulse olmalı')
        if self.dwell_window < 2 or self.impulse_bars < 1:
            raise ValueError('Pencere boyutları geçersiz')
        if not all(math.isfinite(x) and x > 0 for x in (self.dwell_width_atr, self.impulse_distance_atr)):
            raise ValueError('Eşikler sonlu ve pozitif olmalı')


@dataclass
class _BehaviorZone:
    id: str
    kind: str
    lower: float
    upper: float
    created: int
    direction: str
    armed: bool = False
    last_side: str = 'unknown'
    active: dict | None = None
    outside_sides: list[str] = field(default_factory=list)
    visit_count: int = 0
    completed: int = 0
    bounces: int = 0
    crosses: int = 0
    unknowns: int = 0


def scan_behavior_zones(bars: pd.DataFrame, *, config: BehaviorConfig, series_key: str = 'series'):
    """Kaynak olayı ilk bilindiğinde bölge kur; sonraki ziyaretleri izle.

    Önce bölgeden dışarı kapanış beklenir. Sonraki temas bir ziyaret açar;
    böylece kaynak sıkışması veya çıkışı kendini ziyaret olarak saymaz. Ziyaret
    çıkışı ve geçmiş sayaçlar yalnız çıkış kapanışında bilinir.
    """
    if not series_key:
        raise ValueError('series_key boş olamaz')
    bars = bars.reset_index(drop=True)
    high, low, close = (bars[x].astype(float) for x in ('high', 'low', 'close'))
    previous = close.shift(1)
    tr = pd.concat([high-low, (high-previous).abs(), (low-previous).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14, min_periods=14).mean().tolist()
    highs, lows, closes = high.tolist(), low.tolist(), close.tolist()
    stamps = [str(ts) for ts in bars['ts_utc']]
    zones: list[_BehaviorZone] = []
    zone_events, starts, events = [], [], []
    last_signal: str | None = None
    prefix = f'{series_key}:{config.kind}:{config.zone.method}:{config.zone.tolerance:g}'

    for pos in range(len(bars)):
        for zone in zones:
            if pos <= zone.created:
                continue
            side = _side(closes[pos], zone.lower, zone.upper)
            touching = lows[pos] <= zone.upper and highs[pos] >= zone.lower
            if not zone.armed:
                if side in {'above', 'below'}:
                    zone.armed = True
                zone.last_side = side
                continue
            if zone.active is None and touching:
                zone.visit_count += 1
                visit_id = f'{zone.id}:v{zone.visit_count}'
                zone.active = {'visit_id': visit_id, 'approach_side': zone.last_side}
                zone.outside_sides.clear()
                center = (zone.lower + zone.upper) / 2
                start = {'visit_id': visit_id, 'zone_id': zone.id, 'position': pos, 'bar_ts': stamps[pos],
                         'zone_kind': zone.kind, 'source_direction': zone.direction,
                         'center': center, 'lower': zone.lower, 'upper': zone.upper,
                         'prior_visits': zone.visit_count-1, 'prior_completed_visits': zone.completed,
                         'prior_same_side': zone.bounces, 'prior_opposite_side': zone.crosses,
                         'prior_unknowns': zone.unknowns, 'approach_side': zone.last_side,
                         'reference_close': closes[pos], 'atr': atr[pos] if math.isfinite(atr[pos]) else None}
                start.update(_approach(closes, pos, atr[pos]))
                starts.append(start)
                events.append({'visit_id': visit_id, 'position': pos, 'bar_ts': stamps[pos], 'event': 'visit_start', 'outcome': None})
            if zone.active is not None:
                visit_id = zone.active['visit_id']
                def emit(event, outcome=None):
                    events.append({'visit_id': visit_id, 'position': pos, 'bar_ts': stamps[pos], 'event': event, 'outcome': outcome})
                if touching:
                    emit('touch_bar')
                if lows[pos] < zone.lower and highs[pos] > zone.upper:
                    emit('both_boundaries_ambiguous')
                elif highs[pos] > zone.upper and closes[pos] <= zone.upper:
                    emit('upper_wick_outside')
                elif lows[pos] < zone.lower and closes[pos] >= zone.lower:
                    emit('lower_wick_outside')
                if side in {'above', 'below'}:
                    zone.outside_sides.append(side)
                    emit(f'close_{side}')
                else:
                    zone.outside_sides.clear()
                if len(zone.outside_sides) >= config.zone.exit_closes:
                    approach = zone.active['approach_side']
                    # Karşı kenarlar aynı barlarda geçilmiş olabilir; kapanış
                    # vekili yalnız tutarlı dış kapanış ve bilinen gelişte etiketlenir.
                    if approach not in {'above', 'below'} or len(set(zone.outside_sides)) != 1:
                        result = 'unknown'
                    else:
                        result = 'same_side' if side == approach else 'opposite_side'
                    zone.completed += 1
                    zone.bounces += result == 'same_side'
                    zone.crosses += result == 'opposite_side'
                    zone.unknowns += result == 'unknown'
                    emit('visit_end', result)
                    zone.active = None
                    zone.outside_sides.clear()
            zone.last_side = side

        # Yalnız kapanmış geçmiş pencerenin ilk koşul barında aday oluşturulur.
        signal = None
        origin = None
        direction = 'unknown'
        if config.kind == 'dwell' and pos >= config.dwell_window - 1:
            start = pos - config.dwell_window + 1
            scale = atr[pos]
            if math.isfinite(scale) and scale > 0 and max(closes[start:pos+1]) - min(closes[start:pos+1]) <= config.dwell_width_atr * scale:
                signal = 'dwell'
                origin = (start, min(lows[start:pos+1]), max(highs[start:pos+1]), scale)
        elif config.kind == 'impulse' and pos >= config.impulse_bars:
            start = pos - config.impulse_bars
            scale = atr[start]
            distance = closes[pos] - closes[start]
            if math.isfinite(scale) and scale > 0 and abs(distance) >= config.impulse_distance_atr * scale:
                direction = 'up' if distance > 0 else 'down'
                signal = direction
                origin = (start, lows[start], highs[start], atr[pos])
        if signal is not None and signal != last_signal and origin is not None:
            start, source_low, source_high, width_atr = origin
            center = (source_low + source_high) / 2
            padding = center * config.zone.tolerance if config.zone.method == 'percent' else width_atr * config.zone.tolerance
            if math.isfinite(padding) and padding > 0 and source_low > 0:
                zone = _BehaviorZone(id=f'{prefix}:z{len(zones)+1}', kind=config.kind,
                                     lower=source_low-padding, upper=source_high+padding,
                                     created=pos, direction=direction)
                zones.append(zone)
                zone_events.append({'zone_id': zone.id, 'position': pos, 'bar_ts': stamps[pos],
                                    'event': 'zone_created', 'zone_kind': config.kind,
                                    'source_start_position': start, 'source_end_position': pos,
                                    'source_direction': direction, 'center': center, 'lower': zone.lower,
                                    'upper': zone.upper, 'source_low': source_low, 'source_high': source_high,
                                    'source_scale_atr': atr[start] if config.kind == 'impulse' else atr[pos]})
        last_signal = signal
    zcols = ['zone_id', 'position', 'bar_ts', 'event', 'zone_kind', 'source_start_position', 'source_end_position',
             'source_direction', 'center', 'lower', 'upper', 'source_low', 'source_high', 'source_scale_atr']
    vcols = ['visit_id', 'zone_id', 'position', 'bar_ts', 'zone_kind', 'source_direction', 'center', 'lower', 'upper',
             'prior_visits', 'prior_completed_visits', 'prior_same_side', 'prior_opposite_side', 'prior_unknowns',
             'approach_side', 'reference_close', 'atr', 'approach_return_5', 'approach_speed_atr_5', 'approach_efficiency_5']
    ecols = ['visit_id', 'position', 'bar_ts', 'event', 'outcome']
    return (pd.DataFrame(zone_events, columns=zcols), pd.DataFrame(starts, columns=vcols),
            pd.DataFrame(events, columns=ecols))
