"""Kırılım yaşam döngüsü olaylarına Cilt 2 P6 ayrıntılarını ekler."""
from __future__ import annotations
import numpy as np
import pandas as pd


def enrich_lifecycle(events: pd.DataFrame, bars: pd.DataFrame, features: pd.DataFrame, *, counter_expansion_bars: int = 10) -> pd.DataFrame:
    """Mevcut nedensel yapı olaylarını seviye yaşam döngüsü ayrıntılarıyla zenginleştirir."""
    if events.empty:
        return events.copy()
    result=events.copy().sort_values(["source_pivot_position","event_position","event"]).reset_index(drop=True)
    result["level_id"]=[f"{row.level}:{row.source_pivot_position}:{row.direction}" for row in result.itertuples()]
    for col in ("attempt_number","outside_duration","old_area_depth_atr","retest_approach_speed_atr","retest_recovery_ratio","counter_expansion_position","counter_expansion_bars"):
        result[col]=np.nan
    atr=features.atr
    for _,idx in result.groupby("level_id",sort=False).groups.items():
        ids=list(idx);attempts=0;break_pos=None;break_price=None;outside_extreme=None
        for i in ids:
            event=result.at[i,"event"];pos=int(result.at[i,"event_position"]);direction=result.at[i,"direction"];level=float(result.at[i,"level_price"]);a=float(atr.iloc[pos]) if pd.notna(atr.iloc[pos]) else np.nan
            if event=="probe_rejection":
                attempts+=1;result.at[i,"attempt_number"]=attempts
            elif event=="close_break":
                attempts+=1;result.at[i,"attempt_number"]=attempts;break_pos=pos;break_price=float(bars.close.iloc[pos]);outside_extreme=float(bars.high.iloc[pos] if direction=="up" else bars.low.iloc[pos])
            elif break_pos is not None:
                result.at[i,"attempt_number"]=attempts;result.at[i,"outside_duration"]=pos-break_pos
                segment=bars.iloc[break_pos:pos+1]
                extreme=float(segment.high.max() if direction=="up" else segment.low.min())
                excursion=abs(extreme-level)
                if event=="retest_hold":
                    result.at[i,"retest_approach_speed_atr"]=(excursion/a/max(pos-break_pos,1)) if a else np.nan
                    total=abs(break_price-level);result.at[i,"retest_recovery_ratio"]=(abs(float(bars.close.iloc[pos])-level)/total) if total else np.nan
                if event=="failure":
                    depth=(level-float(bars.close.iloc[pos])) if direction=="up" else (float(bars.close.iloc[pos])-level)
                    result.at[i,"old_area_depth_atr"]=depth/a if a else np.nan
                    boundary=float(bars.low.iloc[break_pos] if direction=="up" else bars.high.iloc[break_pos])
                    for j in range(pos+1,min(pos+counter_expansion_bars+1,len(bars))):
                        crossed=float(bars.close.iloc[j])<boundary if direction=="up" else float(bars.close.iloc[j])>boundary
                        if crossed:
                            result.at[i,"counter_expansion_position"]=j;result.at[i,"counter_expansion_bars"]=j-pos;break
    return result
