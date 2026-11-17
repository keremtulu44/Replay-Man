"""Altın-gümüş sanal işlem karşılaştırmasını filtreleyerek gösterir."""
import argparse
from pathlib import Path
import pandas as pd


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--table',type=Path,default=Path('research/measurements/metal-filter-backtest/karsilastirma.csv.gz'))
    p.add_argument('--interval',choices=['1h','4h'],default='4h')
    p.add_argument('--strategy',choices=['breakout20','failed_low5','trend_cross'],default='failed_low5')
    p.add_argument('--mode',choices=['gold','silver','either'],default='either')
    p.add_argument('--horizon',type=int,choices=[10,20],default=10)
    p.add_argument('--atr-setting',choices=['atr1_2','atr1.5_3'],default='atr1_2')
    p.add_argument('--threshold',type=float,choices=[.6,.7,.8],default=.7)
    p.add_argument('--cost',type=float,choices=[0.,.001,.0025,.005],default=.001)
    p.add_argument('--split',choices=['train','validation','test','total'],default='total')
    p.add_argument('--target',help='Hisse kodu; --table hisse-karsilastirma.csv.gz ile')
    a=p.parse_args();df=pd.read_csv(a.table)
    for col,value in [('interval',a.interval),('strategy',a.strategy),('mode',a.mode),('horizon',a.horizon),('atr_setting',a.atr_setting),('threshold',a.threshold),('roundtrip_cost',a.cost),('time_split',a.split)]:df=df[df[col].eq(value)]
    if a.target:
        if 'target_symbol' not in df.columns:p.error('--target için hisse bazlı tabloyu --table ile seçin')
        df=df[df.target_symbol.str.contains(a.target,case=False,regex=False)]
    if df.empty:print('Kayıt bulunamadı.');return
    cols=['all_n','unknown_n','paired_n','blocked_n','kept_n','paired_lower_mean','paired_upper_mean','kept_lower_mean','kept_upper_mean','blocked_lower_mean','blocked_upper_mean','kept_ambiguous']
    if 'target_symbol' in df.columns:cols=['target_symbol']+cols
    print(f'{a.interval} | {a.strategy} | {a.mode} | {a.horizon} mum | {a.atr_setting} | eşik {a.threshold:.0%} | maliyet {a.cost:.2%} | {a.split}')
    print(df[cols].to_string(index=False,float_format=lambda x:f'{x:.5f}'))
    print('Getiriler ondalıktır. paired aynı bilinen adaylarla filtresiz; kept filtreden geçen, blocked elenen adaylardır.')
    print('Alt/üst sütunlar aynı mum hedef-stop belirsizliği varsayımlarıdır; bunlar kesin işlem sonucu veya portföy getirisi değildir.')

if __name__=='__main__':main()
