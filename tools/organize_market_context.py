"""Mevcut endeks/kur hisse özetini kaynaklara ayırır; ölçümleri değiştirmez."""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
from contextlib import ExitStack
from pathlib import Path

GROUPS={'bist_indices':'bist-endeksleri', 'global_indices':'kuresel-gostergeler', 'fx':'doviz-kurlari'}


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def export(root: Path):
    """Verili tabloyu aynen böl, bilinmeyen kaynakları veya eski dosyaları saklama."""
    source=root/'hisse-ozet.csv'; archive=root/'kaynak-arsivi'
    with source.open(encoding='utf-8',newline='') as f:
        reader=csv.DictReader(f);fields=reader.fieldnames
        if not fields or not {'source_id','source_group','source_symbol','time_split','jump_filter','target_group'}.issubset(fields):
            raise ValueError('Özet tablo gerekli sütunları içermiyor')
        found={}
        for row in reader:
            asset=row['source_id'];group=row['source_group'];symbol=row['source_symbol']
            if group not in GROUPS or not re.fullmatch(r'[A-Z0-9_]+',asset):raise ValueError(f'Geçersiz kaynak: {group}/{asset}')
            if row['time_split']!='total' or row['jump_filter']!='all' or row['target_group']!='bist_equities':
                raise ValueError('Özet dışı satır bulundu')
            if asset in found and found[asset]!=(group,symbol):raise ValueError(f'Kaynak çelişiyor: {asset}')
            found[asset]=(group,symbol)
    if not found:raise ValueError('Özet tablosunda kaynak yok')
    expected={archive/GROUPS[group]/f'{asset}.csv' for asset,(group,_) in found.items()}
    existing={p for group in GROUPS.values() for p in (archive/group).glob('*.csv')}
    if existing-expected:raise ValueError(f'Arşivde mevcut özet tablosunda bulunmayan eski dosyalar var: {sorted(map(str,existing-expected))}')
    archive.mkdir(parents=True,exist_ok=True);counts={asset:0 for asset in found}
    with ExitStack() as stack:
        writers={}
        for asset,(group,_) in sorted(found.items()):
            path=archive/GROUPS[group]/f'{asset}.csv';path.parent.mkdir(parents=True,exist_ok=True)
            f=stack.enter_context(path.open('w',encoding='utf-8',newline=''))
            writers[asset]=csv.DictWriter(f,fieldnames=fields);writers[asset].writeheader()
        f=stack.enter_context(source.open(encoding='utf-8',newline=''))
        for row in csv.DictReader(f):
            writers[row['source_id']].writerow(row);counts[row['source_id']]+=1
    with (archive/'dosya-kontrol.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['kaynak_id','dosya','veri_satiri','sha256'])
        w.writerow(['tum_ozet','hisse-ozet.csv',sum(counts.values()),digest(source)])
        for asset,(group,_) in sorted(found.items()):
            path=archive/GROUPS[group]/f'{asset}.csv'
            w.writerow([asset,path.relative_to(root).as_posix(),counts[asset],digest(path)])
        for name in ('risk-table.csv.gz','source-windows.csv.gz','source-availability.csv','target-availability.csv','input-manifest.csv','summary.json'):
            path=root/name
            if path.exists():w.writerow(['ilgili_dosya',name,'',digest(path)])
    text='''# Endeks ve döviz kaynak arşivi

Bu klasör mevcut hisse özetini kaynaklara ayırır; hesapları yeniden yapmaz. Her CSV 100 hisseyi, 1h/4h, altı kaynak koşulunu ve aynı dönem (`same`) ile sinyal sonrası (`post_open`) sonuçlarını ayrı içerir. Özette dönem toplamı ve `jump_filter=all` vardır. **Tüm dönemler, sıçrama duyarlılığı ve boş örnekler** [tam tabloda](../risk-table.csv.gz) saklanır.

| Grup | Kaynak ID | Kaynak sembolü | Hisse sonuçları |
|---|---|---|---|
'''
    titles={'bist_indices':'BIST endeksi','global_indices':'Küresel gösterge','fx':'Döviz kuru'}
    for asset,(group,symbol) in sorted(found.items(),key=lambda x:(GROUPS[x[1][0]],x[0])):
        text+=f'| {titles[group]} | {asset} | {symbol} | [{counts[asset]:,} satır]({GROUPS[group]}/{asset}.csv) |\n'
    text+='''
## Nasıl okunur?

- `target_symbol` hisse; `interval` 1h/4h; `source_condition` kaynak yönü ve eşik; `response` zamanlamadır. `same` kaynakla aynı mumdaki geçmiş harekettir, `post_open` sinyal kapanışından sonraki 10 mumluk vekildir.
- `down0` / `up0`: kaynak <0 / >0; `down2` / `up2`: ≤−%2 / ≥+%2; `down4` / `up4`: ≤−%4 / ≥+%4. Çok küçük yön hareketleri `down0` / `up0` içinde yer alır.
- `negative_count` / `n` düşen / sonucu bilinen olaylar; `selected_source_signals` hedef sonucundan önce seçilmiş olaylardır. `0.70` = %70. `available_baseline_*` ve `baseline_*` farklı çakışmasız ızgaraları kullanır; iki baz da eşleştirilmiş kontrol değildir.
- Düşük veya sıfır n değerleri dosyalardan çıkarılmaz. Özellikle ABD endekslerinde seans uyumu nedeniyle 4h örnekleri sıfırdır; bu, etki bulunmadığını göstermez. `risk_flag` içindeki eşikler keyfidir, otomatik al/sat kararı değildir.

[Ayrıntılı yöntem, veri kapsamı ve sınırlamalar](../README.md) · [Tüm hisse özetleri](../hisse-ozet.csv) · [Dosya kontrol özeti](dosya-kontrol.csv) · [Bütün araştırma arşivleri](../../README.md)

Kaydedilen ölçümler geçmişe yöneliktir; geleceğin kesin olasılığı veya neden-sonuç kanıtı değildir. Canlı fiyat, sektör üyeliği veya birleşik indikatör ekranı içermez. Hacim analiz edilmez.

Arşivi mevcut özetten yeniden oluşturmak: `.venv/bin/python -m tools.organize_market_context`. Ana ölçüm komutu da arşivi yeniler. Özet kaydın girdi dosyaları `data/ohlcv` içindedir; proje tarafından Git'e dahil edilmez, buradaki manifest yalnız yol ve hash bilgisidir. Ham girdi dosyalarını korumak için ayrıca saklamak gerekir.
'''
    (archive/'README.md').write_text(text,encoding='utf-8')
    return counts


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path('research/measurements/market-context'))
    a=p.parse_args()
    for name,count in sorted(export(a.root).items()):print(f'{name}: {count} satır')

if __name__=='__main__':main()
