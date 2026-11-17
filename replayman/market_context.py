"""Endeks ve kur kaynakları için ortak mumlarda yerel birimli özellikler."""
from __future__ import annotations
import numpy as np
import pandas as pd
from replayman.tenbar_research import asof_hour, condition_mask, nonoverlap, times

CONDITIONS=('down0','up0','down2','up2','down4','up4')


def native_source_features(windows, source):
    """Yalnız bilinen fiyatlarla kaynak penceresi; kur çarpanı veya hedef kullanılmaz."""
    start=asof_hour(windows.window_start,source)
    end=asof_hour(windows.signal_close_proxy,source)
    p0=start.price.to_numpy(float);p1=end.price.to_numpy(float)
    change=p1/p0-1
    timestamps=times(source)+pd.Timedelta(hours=1)
    ix0=timestamps.get_indexer(pd.DatetimeIndex(start.close_time));ix1=timestamps.get_indexer(pd.DatetimeIndex(end.close_time))
    closes=pd.to_numeric(source.close,errors='coerce').to_numpy(float)
    jump=np.full(len(windows),np.nan)
    for j,(a,b) in enumerate(zip(ix0,ix1)):
        if a<0 or b<=a or not np.isfinite(p0[j]) or not np.isfinite(p1[j]):continue
        seq=closes[a:b+1]
        if np.isfinite(seq).all() and (seq>0).all():jump[j]=np.max(np.abs(seq[1:]/seq[:-1]-1))
    result=windows.copy()
    result['source_return']=change;result['source_max_hourly_jump']=jump
    result['source_start_price']=p0;result['source_end_price']=p1
    result['source_start_time']=start.close_time;result['source_end_time']=end.close_time
    # Fixed grid selected after source availability, but without looking at the target.
    result['source_fixed']=nonoverlap(windows,np.isfinite(change))
    result['source_fixed_no_jump10']=nonoverlap(windows,np.isfinite(change)&np.isfinite(jump)&(jump<=.10))
    for cond in CONDITIONS:
        eligible=condition_mask(change,cond)
        result['episode_'+cond]=nonoverlap(windows,eligible)
        result['episode_'+cond+'_no_jump10']=nonoverlap(windows,eligible & np.isfinite(jump) & (jump<=.10))
    return result
