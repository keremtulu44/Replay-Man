"""Cilt 2 pullback/mum ve ana kitap rejim/çoklu zaman özellikleri."""
from __future__ import annotations
import numpy as np
import pandas as pd


def pullback_events(legs: pd.DataFrame, bars: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    """Bir yönlü bacağı izleyen karşı bacağı, teyit anında pullback adayı yapar."""
    if legs.empty or "known_at_position" not in legs:
        return pd.DataFrame(columns=["event","direction","thesis_direction","known_at_position","event_ts","depth_ratio","duration_ratio","speed_ratio","efficiency_ratio","pullback_overlap","pullback_range_atr"])
    rows=[]; ordered=legs.sort_values(["known_at_position","end_position"]).to_dict("records")
    for impulse, correction in zip(ordered,ordered[1:]):
        if impulse["direction"]==correction["direction"] or impulse["end_position"]!=correction["start_position"]: continue
        known=int(correction["known_at_position"])
        def ratio(a,b): return float(a)/float(b) if pd.notna(a) and pd.notna(b) and b else np.nan
        rows.append({
            "event":"pullback_confirmed","direction":correction["direction"],"thesis_direction":impulse["direction"],
            "impulse_start_position":int(impulse["start_position"]),"impulse_end_position":int(impulse["end_position"]),
            "pullback_end_position":int(correction["end_position"]),"known_at_position":known,"event_ts":bars.iloc[known].ts_utc,
            "depth_ratio":ratio(correction["distance"],impulse["distance"]),"duration_ratio":ratio(correction["duration_bars"],impulse["duration_bars"]),
            "speed_ratio":ratio(correction["speed_per_bar"],impulse["speed_per_bar"]),"efficiency_ratio":ratio(correction["path_efficiency"],impulse["path_efficiency"]),
            "pullback_overlap":features.iloc[known].get("mean_overlap",np.nan),"pullback_range_atr":features.iloc[known].get("range_atr",np.nan),
        })
    return pd.DataFrame(rows)


def candle_and_regime_features(bars: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    """Sürekli mum geometrisinden adlandırılmış diziler ve nedensel rejim üretir."""
    out=features.copy(); o,h,l,c=(bars[x].astype(float) for x in ("open","high","low","close"))
    body=(c-o).abs(); prev_body=body.shift(1)
    out["bullish_engulfing"]=((c>o)&(c.shift(1)<o.shift(1))&(o<=c.shift(1))&(c>=o.shift(1))).astype("int8")
    out["bearish_engulfing"]=((c<o)&(c.shift(1)>o.shift(1))&(o>=c.shift(1))&(c<=o.shift(1))).astype("int8")
    out["body_expansion"]=(body/prev_body.replace(0,np.nan))
    out["strong_bull_close"]=((out.body_ratio>=.60)&(out.close_location>=.75)&(c>o)).astype("int8")
    out["strong_bear_close"]=((out.body_ratio>=.60)&(out.close_location<=.25)&(c<o)).astype("int8")
    out["doji_like"]=(out.body_ratio<=.10).astype("int8")
    out["ema20"]=c.ewm(span=20,adjust=False,min_periods=20).mean(); out["ema50"]=c.ewm(span=50,adjust=False,min_periods=50).mean()
    out["ema20_slope_atr"]=(out.ema20-out.ema20.shift(5))/(5*out.atr.replace(0,np.nan))
    trend_up=(out.ema20>out.ema50)&(out.ema20_slope_atr>.02)&(out.path_efficiency>=.30)
    trend_down=(out.ema20<out.ema50)&(out.ema20_slope_atr<-.02)&(out.path_efficiency>=.30)
    out["regime"]=np.select([trend_up,trend_down,out.path_efficiency<.30],["trend_up","trend_down","range"],default="transition")
    return out


def attach_forward(events: pd.DataFrame,bars: pd.DataFrame,horizons=(5,20,40,60)) -> pd.DataFrame:
    result=events.copy(); close=bars.close.to_numpy(float); high=bars.high.to_numpy(float); low=bars.low.to_numpy(float)
    for horizon in horizons:
        ret=[];mfe=[];mae=[]
        for e in events.to_dict("records"):
            p=int(e["known_at_position"]); sign=1 if e["thesis_direction"]=="up" else -1
            if p+horizon>=len(bars): ret.append(np.nan);mfe.append(np.nan);mae.append(np.nan);continue
            entry=close[p]; ret.append(sign*(close[p+horizon]/entry-1)); mx=high[p+1:p+horizon+1].max()/entry-1;mn=low[p+1:p+horizon+1].min()/entry-1
            mfe.append(mx if sign==1 else -mn);mae.append(mn if sign==1 else -mx)
        result[f"directional_return_{horizon}"]=ret;result[f"directional_mfe_{horizon}"]=mfe;result[f"directional_mae_{horizon}"]=mae
    return result
