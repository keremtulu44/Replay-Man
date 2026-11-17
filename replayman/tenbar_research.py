"""Ortak 10 BIST mumunda emtia ve hisse hareketlerini nedensel hizalar."""
from __future__ import annotations

import numpy as np
import pandas as pd

TRAIN_END='2026-07-01T00:00:00Z'
VALIDATION_END='2026-09-01T00:00:00Z'
CONDITIONS=('all','up4','down4','up2','down2','up0','down0','flat1')


def times(frame):
    idx=pd.DatetimeIndex(pd.to_datetime(frame.ts_utc,utc=True,errors='raise'))
    if idx.hasnans or idx.has_duplicates or not idx.is_monotonic_increasing:
        raise ValueError('Bar zamanları eksiksiz, sıralı ve tekil olmalı')
    return idx


def split_label(t,train_end=TRAIN_END,validation_end=VALIDATION_END):
    vals=pd.DatetimeIndex(pd.to_datetime(t,utc=True));a=pd.Timestamp(train_end);b=pd.Timestamp(validation_end)
    if a.tzinfo is None or b.tzinfo is None or a>=b:raise ValueError('UTC sınırları yanlış')
    return np.where(vals.isna(),None,np.where(vals<a,'train',np.where(vals<b,'validation','test')))


def make_windows(benchmark,interval='4h',bars=10,train_end=TRAIN_END,validation_end=VALIDATION_END):
    if interval not in ('1h','4h') or bars<1:raise ValueError('Geçersiz periyot veya bar sayısı')
    ts=times(benchmark);dur=pd.Timedelta(interval);end=np.arange(bars-1,len(ts));start=end-bars+1
    known=ts.take(end)+dur;starttime=ts.take(start)
    startsplit=split_label(starttime,train_end,validation_end);end_split=split_label(known,train_end,validation_end)
    good=startsplit==end_split;start=start[good];end=end[good];known=known[good];starttime=starttime[good];split=end_split[good]
    x=pd.DataFrame({'start_pos':start,'end_pos':end,'window_start':starttime,'end_bar_ts':ts.take(end),
                    'signal_close_proxy':known,'time_split':split})
    x['fixed_nonoverlap']=nonoverlap(x,np.ones(len(x),dtype=bool))
    return x


def nonoverlap(windows,eligible):
    """Biten sinyale kadar bilinen uygunlukla, her split başında kronolojik seçim."""
    if len(windows)!=len(eligible):raise ValueError('Uygunluk uzunluğu yanlış')
    selected=np.zeros(len(windows),dtype=bool);last={}
    for j,row in enumerate(windows.itertuples(index=False)):
        if eligible[j] and int(row.start_pos)>last.get(row.time_split,-1):
            selected[j]=True;last[row.time_split]=int(row.end_pos)
    return selected


def asof_hour(targets,source,max_age='90min'):
    target=pd.DatetimeIndex(pd.to_datetime(targets,utc=True));end=times(source)+pd.Timedelta(hours=1)
    close=pd.to_numeric(source.close,errors='coerce').to_numpy(float)
    index=end.searchsorted(target,side='right')-1;available=(index>=0)&~target.isna();ii=np.flatnonzero(available)
    match=pd.Series(pd.NaT,index=range(len(target)),dtype='datetime64[ns, UTC]');price=np.full(len(target),np.nan)
    match.iloc[ii]=end.take(index[ii]);price[ii]=close[index[ii]]
    age=target-pd.DatetimeIndex(match)
    good=available & (age>=pd.Timedelta(0)) & (age<=pd.Timedelta(max_age)) & np.isfinite(price) & (price>0)
    price[~good]=np.nan
    return pd.DataFrame({'price':price,'close_time':match,'age_minutes':age.total_seconds()/60})


def source_features(windows,commodity,fx):
    """Kaynağın yalnız aralık uçlarında bilinen USD / yaklaşık TRY değişimi."""
    source_start=asof_hour(windows.window_start,commodity);source_end=asof_hour(windows.signal_close_proxy,commodity)
    fx_start=asof_hour(windows.window_start,fx);fx_end=asof_hour(windows.signal_close_proxy,fx)
    start=source_start.price.to_numpy();end=source_end.price.to_numpy()
    # Kapanmış kaynak barlarında, başlangıçtan sona kadar gözlenen en büyük sıçrama.
    # Bu yalnız kaynak anında bilinen son barları kullanır; gap/roll hatası teşhisi değildir.
    closes=pd.to_numeric(commodity.close,errors='coerce').to_numpy(float)
    ends=times(commodity)+pd.Timedelta(hours=1)
    si=ends.get_indexer(pd.DatetimeIndex(source_start.close_time))
    ei=ends.get_indexer(pd.DatetimeIndex(source_end.close_time))
    maxjump=np.full(len(windows),np.nan)
    for j,(a,b) in enumerate(zip(si,ei)):
        if a<0 or b<=a or not np.isfinite(start[j]) or not np.isfinite(end[j]):continue
        seq=closes[a:b+1]
        if not np.isfinite(seq).all() or (seq<=0).any():continue
        maxjump[j]=np.max(np.abs(seq[1:]/seq[:-1]-1))
    with np.errstate(divide='ignore',invalid='ignore'):
        usd=end/start-1
        local=(end*fx_end.price.to_numpy())/(start*fx_start.price.to_numpy())-1
    sync0=abs(pd.DatetimeIndex(source_start.close_time)-pd.DatetimeIndex(fx_start.close_time))<=pd.Timedelta(hours=1)
    sync1=abs(pd.DatetimeIndex(source_end.close_time)-pd.DatetimeIndex(fx_end.close_time))<=pd.Timedelta(hours=1)
    local[~(sync0&sync1)]=np.nan
    frames=[]
    for unit,change in [('USD',usd),('TRY_proxy',local)]:
        x=windows.copy();x['unit']=unit;x['source_return']=change
        x['source_start_price']=start;x['source_end_price']=end
        x['source_max_hourly_jump']=maxjump
        x['source_start_time']=source_start.close_time;x['source_end_time']=source_end.close_time
        x['fx_start_price']=fx_start.price;x['fx_end_price']=fx_end.price
        x['fx_start_time']=fx_start.close_time;x['fx_end_time']=fx_end.close_time
        for cond in CONDITIONS[1:]:
            x[f'episode_{cond}']=nonoverlap(windows,condition_mask(change,cond))
            x[f'episode_{cond}_no_jump10']=nonoverlap(windows,condition_mask(change,cond) & np.isfinite(maxjump) & (maxjump<=.10))
        frames.append(x)
    return pd.concat(frames,ignore_index=True)


def condition_mask(change,condition):
    a=np.asarray(change,dtype=float);valid=np.isfinite(a)
    conditions={'all':valid,'up4':valid & (a>=.04),'down4':valid & (a<=-.04),
                'up2':valid & (a>=.02),'down2':valid & (a<=-.02),'up0':valid & (a>0),'down0':valid & (a<0),
                'flat1':valid & (np.abs(a)<.01)}
    if condition not in conditions:raise ValueError('Bilinmeyen koşul')
    return conditions[condition]


def target_labels(windows,benchmark,target,interval='4h',bars=10,train_end=TRAIN_END,validation_end=VALIDATION_END):
    """10 ortak barın tamamı ve gelecekteki 10 ortak bar eşleşmesini kontrol eder."""
    if interval not in ('1h','4h') or bars<1:raise ValueError('Geçersiz periyot')
    bt=times(benchmark);tt=times(target);lookup=tt.get_indexer(bt)
    op=target.open.to_numpy(float);cl=target.close.to_numpy(float)
    bo=benchmark.open.to_numpy(float);bc=benchmark.close.to_numpy(float)
    target_ohlc=target[['open','high','low','close']].to_numpy(float)
    bench_ohlc=benchmark[['open','high','low','close']].to_numpy(float)
    n=len(windows)
    same=np.full(n,np.nan);after=np.full(n,np.nan);post=np.full(n,np.nan)
    same_ex=np.full(n,np.nan);after_ex=np.full(n,np.nan);post_ex=np.full(n,np.nan)
    outcome_end=pd.Series(pd.NaT,index=range(n),dtype='datetime64[ns, UTC]')
    entry_time=pd.Series(pd.NaT,index=range(n),dtype='datetime64[ns, UTC]')
    post_end=pd.Series(pd.NaT,index=range(n),dtype='datetime64[ns, UTC]')
    def exact_valid(start,end):
        if start<0 or end>=len(bt): return False
        ix=lookup[start:end+1]
        if len(ix)!=end-start+1 or np.any(ix<0) or np.any(np.diff(ix)!=1): return False
        return bool(np.isfinite(target_ohlc[ix]).all() and (target_ohlc[ix]>0).all() and
                    np.isfinite(bench_ohlc[start:end+1]).all() and (bench_ohlc[start:end+1]>0).all())
    for j,w in enumerate(windows.itertuples(index=False)):
        sp=int(w.start_pos);ep=int(w.end_pos)
        same_valid=ep-sp+1==bars and exact_valid(sp,ep)
        if same_valid:
            i0,ie=int(lookup[sp]),int(lookup[ep])
            same[j]=cl[ie]/op[i0]-1;same_ex[j]=same[j]-(bc[ep]/bo[sp]-1)
        end=ep+bars
        if same_valid and end<len(bt) and exact_valid(ep,end):
            endclose=bt[end]+pd.Timedelta(interval);outcome_end.iloc[j]=endclose
            if split_label([endclose],train_end,validation_end)[0]==w.time_split:
                target_end=int(lookup[end])
                after[j]=cl[target_end]/cl[ie]-1;after_ex[j]=after[j]-(bc[end]/bc[ep]-1)
        # Sinyal kapanışıyla aynı ana denk gelen açılış kullanılamaz.
        enter=int(bt.searchsorted(w.signal_close_proxy,side='right'))
        finish=enter+bars-1
        if enter<len(bt) and finish<len(bt) and exact_valid(enter,finish):
            entry_time.iloc[j]=bt[enter];endclose=bt[finish]+pd.Timedelta(interval);post_end.iloc[j]=endclose
            if split_label([endclose],train_end,validation_end)[0]==w.time_split:
                target_entry=int(lookup[enter]);target_end=int(lookup[finish])
                post[j]=cl[target_end]/op[target_entry]-1;post_ex[j]=post[j]-(bc[finish]/bo[enter]-1)
    out=windows[['end_pos']].copy();out['same_return']=same;out['same_excess']=same_ex
    out['after_return']=after;out['after_excess']=after_ex;out['after_close_proxy']=outcome_end
    out['post_open_return']=post;out['post_open_excess']=post_ex
    out['post_open_entry_ts']=entry_time;out['post_open_close_proxy']=post_end
    return out


def metrics(mask,returns,excess):
    mask=np.asarray(mask,dtype=bool);r=np.asarray(returns,dtype=float);e=np.asarray(excess,dtype=float)
    valid=mask & np.isfinite(r);paired=mask & np.isfinite(e);n=int(valid.sum());v=r[valid]
    return {'n':n,'negative_count':int((v<0).sum()),'negative_rate':float((v<0).mean()) if n else np.nan,
            'positive_count':int((v>0).sum()),'flat_count':int((v==0).sum()),
            'flat_rate':float((v==0).mean()) if n else np.nan,'down3_count':int((v<=-.03).sum()),'down3_rate':float((v<=-.03).mean()) if n else np.nan,
            'up3_count':int((v>=.03).sum()),'up3_rate':float((v>=.03).mean()) if n else np.nan,
            'median_return':float(np.median(v)) if n else np.nan,
            'positive_rate':float((v>0).mean()) if n else np.nan,
            'excess_n':int(paired.sum()),'median_excess':float(np.median(e[paired])) if paired.any() else np.nan,
            'sample_status':'betimleyici_yeterli' if n>=10 else 'ornek_yetersiz'}
