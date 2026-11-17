"""Tarihsel makro risk tablosunu kaynak ve hedefe göre süzer."""
import argparse
from pathlib import Path
import pandas as pd


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--table',type=Path,default=Path('research/measurements/macro-risk-screen/risk-table.csv.gz'))
    p.add_argument('--source',default='METAL_GOLD',help='Kaynak ID veya sembol, örn. METAL_GOLD')
    p.add_argument('--target',help='Hedef ID veya sembolde aranan metin, örn. TUPRS')
    p.add_argument('--condition',choices=['down0','up0','down2','up2','down4','up4'],default='down0')
    p.add_argument('--interval',choices=['1h','4h'],default='4h')
    p.add_argument('--unit',choices=['USD','TRY_proxy'],default='USD')
    p.add_argument('--response',choices=['same','post_open'],default='post_open')
    p.add_argument('--split',choices=['train','validation','test','total'],default='total')
    p.add_argument('--jump-filter',choices=['all','no_jump10'],default='all')
    p.add_argument('--min-n',type=int,default=0);p.add_argument('--warning-only',action='store_true')
    p.add_argument('--limit',type=int,default=30);p.add_argument('--csv',action='store_true',help='Filtreyi CSV olarak yaz')
    a=p.parse_args();df=pd.read_csv(a.table)
    mask=(df.source_id.str.contains(a.source,case=False,regex=False)|df.source_symbol.str.contains(a.source,case=False,regex=False))
    for col,value in [('source_condition',a.condition),('interval',a.interval),('unit',a.unit),('response',a.response),('time_split',a.split),('jump_filter',a.jump_filter)]:mask &= df[col].eq(value)
    if a.target:mask &= (df.target_id.str.contains(a.target,case=False,regex=False)|df.target_symbol.str.contains(a.target,case=False,regex=False))
    mask &= df.n.ge(a.min_n)
    if a.warning_only:mask &= df.risk_flag.eq('tarihsel_uyari')
    result=df.loc[mask].sort_values(['negative_rate','n','target_id'],ascending=[False,False,True]).head(a.limit)
    if result.empty:
        print('Eşleşen kayıt yok. Filtreleri kontrol edin.');return
    if a.csv:print(result.to_csv(index=False),end='');return
    cols=['target_symbol','selected_source_signals','n','negative_count','negative_rate','down3_count','baseline_n','baseline_negative_rate','negative_rate_difference','risk_flag']
    print(f'{a.source} {a.condition} | {a.unit} {a.interval} | {a.response} | {a.split} | {a.jump_filter}')
    print(result[cols].to_string(index=False,float_format=lambda x:f'{x:.3f}'))
    print('\nOranlar 0–1 aralığındadır; uyarı betimleyicidir, işlem önerisi değildir.')

if __name__=='__main__':main()
