"""Endeks veya kur hareketinde hisse tepkilerini filtrele."""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--table',type=Path,default=Path('research/measurements/market-context/risk-table.csv.gz'))
    p.add_argument('--source',default='IDX_XU100',help='Kaynak ID veya sembol')
    p.add_argument('--target',help='Hisse kodu veya ID')
    p.add_argument('--condition',choices=['down0','up0','down2','up2','down4','up4'],default='down0')
    p.add_argument('--interval',choices=['1h','4h'],default='4h')
    p.add_argument('--response',choices=['same','post_open'],default='post_open')
    p.add_argument('--split',choices=['train','validation','test','total'],default='total')
    p.add_argument('--jump-filter',choices=['all','no_jump10'],default='all')
    p.add_argument('--min-n',type=int,default=0)
    p.add_argument('--limit',type=int,default=30);p.add_argument('--csv',action='store_true')
    a=p.parse_args();data=pd.read_csv(a.table)
    mask=data.source_id.str.contains(a.source,case=False,regex=False)|data.source_symbol.str.contains(a.source,case=False,regex=False)
    for col,val in [('source_condition',a.condition),('interval',a.interval),('response',a.response),('time_split',a.split),('jump_filter',a.jump_filter)]:mask &= data[col].eq(val)
    if a.target:mask &= data.target_id.str.contains(a.target,case=False,regex=False)|data.target_symbol.str.contains(a.target,case=False,regex=False)
    mask &= data.n.ge(a.min_n)
    result=data.loc[mask].sort_values(['negative_rate','n','target_id'],ascending=[False,False,True]).head(a.limit)
    if result.empty:print('Eşleşen kayıt yok.');return
    if a.csv:print(result.to_csv(index=False),end='');return
    cols=['target_symbol','selected_source_signals','n','negative_count','negative_rate','down3_count','available_baseline_n','available_baseline_negative_rate','available_negative_rate_difference','sample_status']
    print(f'{a.source} | {a.condition} | {a.interval} | {a.response} | {a.split} | {a.jump_filter}')
    print(result[cols].to_string(index=False,float_format=lambda x:f'{x:.3f}'))
    print('\nOranlar 0–1 aralığındadır; düşük n ve sıfır olay silinmez. Bu tarihsel gözlem, emir veya tahmin değildir.')

if __name__=='__main__':main()
