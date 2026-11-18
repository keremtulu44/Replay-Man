"""Temsilî lifecycle olaylarını daha küçük XZ CSV'ye dönüştür.

Yalnız türetilebilir/sabit kolonlar çıkarılır; kimlik, zaman, konum, bant,
senaryo ve ham/yönlü sonuçlar korunur. Orijinal biçim çalıştırıcıyla üretilebilir.
"""
import argparse
from pathlib import Path
import pandas as pd

DROP = ['prior_start_side','prior_scenario','duration_bars','representative','end_label_5','end_label_10']


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path('research/measurements/zone-memory'))
    args=p.parse_args(argv)
    for kind in ['horizontal','dwell','impulse','sloped']:
        for suffix in ['', '-hourly']:
            folder=args.root/f'lifecycle-{kind}{suffix}'
            gz=folder/'events.csv.gz'; xz=folder/'events.csv.xz'; temp=folder/'events.tmp.csv.xz'
            source=gz if gz.exists() else xz
            if not source.exists():raise FileNotFoundError(source)
            df=pd.read_csv(source)
            slim=df.drop(columns=DROP,errors='ignore')
            slim.to_csv(temp,index=False,compression={'method':'xz','preset':6})
            # Satır/kolon ve senaryo özeti kontrol edilir, yazılan değerler okunabilir olmalı.
            check=pd.read_csv(temp)
            if check.shape!=slim.shape or list(check.columns)!=list(slim.columns):
                raise ValueError(f'Çıktı biçimi uyuşmuyor: {temp}')
            pd.testing.assert_frame_equal(slim,check,check_dtype=False,rtol=1e-12,atol=1e-12)
            temp.replace(xz)
            if gz.exists():gz.unlink()
            print(f'{folder.name}: {len(slim)} satır {xz.stat().st_size} bytes',flush=True)


if __name__=='__main__':main()
