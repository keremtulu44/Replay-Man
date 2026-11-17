"""Altın/gümüş uyarısı için nedensel, olay bazlı sanal işlem araştırması."""
from __future__ import annotations
import numpy as np
import pandas as pd
from replayman.tenbar_research import times, split_label, nonoverlap, asof_hour

_TRAIN=pd.Timestamp('2026-07-01T00:00:00Z')
_VALIDATION=pd.Timestamp('2026-09-01T00:00:00Z')

def period(t):
    return 'train' if t<_TRAIN else ('validation' if t<_VALIDATION else 'test')


def signal_features(aligned):
    """Yalnız kapanmış/geçmiş barlar; NaN barlar gerekli geçmişi geçersiz kılar."""
    o,h,l,c=(aligned[x].astype(float) for x in ('open','high','low','close'))
    tr=pd.concat([h-l,(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1,skipna=False)
    atr=tr.rolling(14,min_periods=14).mean()
    prev_high=h.shift(1).rolling(20,min_periods=20).max()
    prev_low=l.shift(1).rolling(5,min_periods=5).min()
    ma20=c.rolling(20,min_periods=20).mean();ma50=c.rolling(50,min_periods=50).mean()
    return pd.DataFrame({'atr':atr,
        'breakout20':(c>prev_high),
        'failed_low5':(l<prev_low)&(c>prev_low)&(c>o),
        'trend_cross':(ma20>ma50)&(ma20.shift(1)<=ma50.shift(1)),
    })


def metal_windows(windows,source):
    """Sinyal anında erişilebilir, kesinlikle %2 üstündeki değişim ve kaynak-öncelikli seçim."""
    a=asof_hour(windows.window_start,source).price.to_numpy(float)
    b=asof_hour(windows.signal_close_proxy,source).price.to_numpy(float)
    ret=b/a-1
    result=windows.copy();result['source_return']=ret
    for name,mask in [('up',ret>.02),('down',ret<-.02)]:
        result['episode_'+name]=nonoverlap(windows,mask & np.isfinite(ret))
    return result


def post_labels(windows,benchmark,aligned,interval):
    """İlk gecikmeli giriş açılışından 10. ortak kapanış; dönem sınırı dışlanır."""
    bt=times(benchmark); dur=pd.Timedelta(interval);n=len(bt)
    entry=bt.searchsorted(pd.DatetimeIndex(windows.signal_close_proxy),side='right')
    end=entry+9;inrange=end<n
    good=np.isfinite(aligned[['open','high','low','close']].to_numpy(float)).all(axis=1)&(aligned[['open','high','low','close']].to_numpy(float)>0).all(axis=1)
    bvals=benchmark[['open','high','low','close']].to_numpy(float)
    good &= np.isfinite(bvals).all(axis=1)&(bvals>0).all(axis=1)
    invalid=np.r_[0,np.cumsum(~good)]
    pos=np.flatnonzero(inrange); ee=entry[pos];xx=end[pos]
    result=np.full(len(windows),np.nan)
    end_ts=pd.Series(pd.NaT,index=range(len(windows)),dtype='datetime64[ns, UTC]')
    end_times=bt.take(xx)+dur
    ok=(invalid[xx+1]-invalid[ee]==0)&(split_label(end_times)==windows.time_split.to_numpy()[pos])
    p=pos[ok];es=entry[p];ends=end[p]
    result[p]=aligned.close.to_numpy(float)[ends]/aligned.open.to_numpy(float)[es]-1
    end_ts.iloc[p]=bt.take(ends)+dur
    return result,end_ts


def expanding_history(windows,source,post,post_end):
    """Sonuç kapanışı sinyale kadar bilinen seçili olayların sayı ve düşüşleri."""
    t=pd.DatetimeIndex(windows.signal_close_proxy).as_unit("ns").asi8
    output={}
    for direction in ('up','down'):
        selected=source['episode_'+direction].to_numpy(bool)&np.isfinite(post)&post_end.notna().to_numpy()
        stamps=pd.DatetimeIndex(post_end[selected]).as_unit("ns").asi8
        vals=post[selected]<0
        order=np.argsort(stamps,kind='stable');stamps=stamps[order];vals=vals[order]
        cum=np.r_[0,np.cumsum(vals,dtype=int)]
        count=np.searchsorted(stamps,t,side='right')
        output[direction+'_n']=count
        output[direction+'_down']=cum[count]
    return pd.DataFrame(output)


def simulate(aligned,bt,signal_pos,atr,interval,horizon,stop_mult,target_mult):
    """Tek adayın iki olası OHLC sonucunu üretir; ileri bilgi girişe verilmez."""
    known=bt[signal_pos]+pd.Timedelta(interval);entry=int(bt.searchsorted(known,side='right'))
    if entry>=len(bt) or not np.isfinite(atr) or atr<=0:return None
    s0=period(known)
    if period(bt[entry])!=s0:return None
    o,h,l,c=(aligned[x].to_numpy(float) for x in ('open','high','low','close'))
    price=o[entry]
    if not np.isfinite(price) or price<=0:return None
    stop=price-stop_mult*atr;target=price+target_mult*atr
    if stop<=0:return None
    last=min(entry+horizon,len(bt))
    for pos in range(entry,last):
        if not np.isfinite([o[pos],h[pos],l[pos],c[pos]]).all() or min(o[pos],h[pos],l[pos],c[pos])<=0:return None
        close_time=bt[pos]+pd.Timedelta(interval)
        if period(close_time)!=s0:return None
        # Açılış seviyeyi aşmışsa sıranın belirsizliği yoktur; fiyat açılıştır.
        if pos>entry and o[pos]<=stop: lo=hi=o[pos];reason='gap_stop'
        elif pos>entry and o[pos]>=target: lo=hi=o[pos];reason='gap_target'
        elif l[pos]<=stop and h[pos]>=target: lo,hi=stop,target;reason='ambiguous'
        elif l[pos]<=stop:lo=hi=stop;reason='stop'
        elif h[pos]>=target:lo=hi=target;reason='target'
        elif pos==entry+horizon-1:lo=hi=c[pos];reason='time'
        else:continue
        return {'entry_ts':bt[entry], 'exit_ts':close_time,'entry_price':price,'stop_price':stop,'target_price':target,
                'exit_reason':reason,'gross_lower':lo/price-1,'gross_upper':hi/price-1,'bars_held':pos-entry+1}
    return None


def classify(source_return,n,down,threshold):
    if not np.isfinite(source_return):return 'unknown'
    if abs(source_return)<=.02:return 'no_signal'
    if n<10:return 'unknown'
    return 'warning' if down/n>=threshold else 'clear'


def combine(a,b):
    if 'warning' in (a,b):return 'warning'
    if 'unknown' in (a,b):return 'unknown'
    return 'clear'
