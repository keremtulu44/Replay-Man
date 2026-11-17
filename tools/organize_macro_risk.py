"""Mevcut makro risk ölçümünü değiştirmeden emtia klasörlerine dağıtır."""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
from contextlib import ExitStack
from pathlib import Path

SOURCES = {
    'OIL_BRENT': ('petrol/brent', 'Brent petrol', 'BZ=F'),
    'OIL_WTI': ('petrol/wti', 'WTI petrol', 'CL=F'),
    'METAL_GOLD': ('madenler/altin', 'Altın', 'GC=F'),
    'METAL_SILVER': ('madenler/gumus', 'Gümüş', 'SI=F'),
    'METAL_COPPER': ('madenler/bakir', 'Bakır', 'HG=F'),
    'METAL_PLATINUM': ('madenler/platin', 'Platin', 'PL=F'),
    'METAL_PALLADIUM': ('madenler/paladyum', 'Paladyum', 'PA=F'),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def export(root: Path) -> dict:
    """Sütun/satırları yeniden hesaplamadan, tam tabloyu kaynak ID'sine göre böler."""
    source = root / 'risk-table.csv.gz'
    archive = root / 'emtia-arsivi'
    with gzip.open(source, 'rt', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        required = {'source_id', 'source_symbol', 'time_split', 'jump_filter', 'target_group'}
        if not fields or not required.issubset(fields):
            raise ValueError('Tam tablo gerekli sütunları içermiyor')
        # Bilinmeyen bir kaynak olursa sessizce sonuç kaybetmek yerine dur.
        found = {row['source_id'] for row in reader}
    unknown = found - SOURCES.keys()
    if unknown or not found:
        raise ValueError(f'Bilinmeyen veya eksik kaynak: {sorted(unknown)}')
    # Eski bir kaynak mevcut tablodan kalkmışsa, eski dosyaları yanlışlıkla güncel
    # göstermemek ve kullanıcının dosyalarını kendiliğinden silmemek için dur.
    stale = [asset for asset in SOURCES.keys() - found
             if (archive / SOURCES[asset][0] / 'tum-sonuclar.csv.gz').exists()]
    if stale:
        raise ValueError(f'Arşivde mevcut tabloda bulunmayan eski kaynaklar var: {sorted(stale)}')
    archive.mkdir(parents=True, exist_ok=True)
    counts = {asset: {'full': 0, 'summary': 0} for asset in found}
    with ExitStack() as stack:
        writers = {}
        for asset in sorted(found):
            folder = archive / SOURCES[asset][0]
            folder.mkdir(parents=True, exist_ok=True)
            full = stack.enter_context(gzip.open(folder / 'tum-sonuclar.csv.gz', 'wt', encoding='utf-8', newline=''))
            summary = stack.enter_context((folder / 'ozet-hisseler.csv').open('w', encoding='utf-8', newline=''))
            fw = csv.DictWriter(full, fieldnames=fields); fw.writeheader()
            sw = csv.DictWriter(summary, fieldnames=fields); sw.writeheader()
            writers[asset] = (fw, sw)
        f = stack.enter_context(gzip.open(source, 'rt', encoding='utf-8', newline=''))
        for row in csv.DictReader(f):
            asset = row['source_id']
            writers[asset][0].writerow(row)
            counts[asset]['full'] += 1
            if row['time_split'] == 'total' and row['jump_filter'] == 'all' and row['target_group'] == 'bist_equities':
                writers[asset][1].writerow(row)
                counts[asset]['summary'] += 1
    for asset in sorted(found):
        path, name, symbol = SOURCES[asset]
        text = f'''# {name} — tarihsel BIST risk sonuçları

Kaynak: `{asset}` (`{symbol}`). Hesaplamalar yeniden yapılmadı; ana tablonun bu kaynağa ait satırları aynen ayrıldı.

- [ozet-hisseler.csv](ozet-hisseler.csv): {counts[asset]['summary']:,} satır; 100 hisse, toplam dönem, sıçrama filtresiz; iki fiyat birimi, iki periyot, altı kaynak koşulu ve iki sonuç penceresi.
- [tum-sonuclar.csv.gz](tum-sonuclar.csv.gz): {counts[asset]['full']:,} satır; hisseler ve endeksler, tüm dönemler ve sıçrama duyarlılığı. Gzip açılarak CSV filtrelenebilir.

[Sütunlar, yöntem ve uyarılar](../../README.md) · [Ayrıntılı araştırma raporu](../../../README.md)
'''
        (archive / path / 'README.md').write_text(text, encoding='utf-8')
    files = [('ana_tablo', source, sum(c['full'] for c in counts.values()))]
    for asset in sorted(found):
        folder = archive / SOURCES[asset][0]
        files.extend([(asset, folder/'ozet-hisseler.csv', counts[asset]['summary']),
                      (asset, folder/'tum-sonuclar.csv.gz', counts[asset]['full'])])
    with (archive/'dosya-kontrol.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f);writer.writerow(['kaynak_id','dosya','veri_satiri','sha256'])
        for asset, path, count in files:
            writer.writerow([asset, path.relative_to(root).as_posix(), count, sha256(path)])
    index = '''# Emtia bazında düzenlenmiş BIST risk arşivi

Bu arşiv mevcut tarihsel sonuçları **yeniden hesaplamadan** emtialara ayırır. Her klasörde hisseler için kolay filtrelenebilir CSV ve tüm bölümleri, hisseleri, endeksleri ve duyarlılıkları içeren sıkıştırılmış tam sonuç vardır.

| Emtia | Hisse özeti | Tam sonuçlar | Açıklama |
|---|---|---|---|
'''
    for asset in sorted(found, key=lambda x: SOURCES[x][0]):
        path, name, _ = SOURCES[asset]
        index += f'| {name} | [CSV]({path}/ozet-hisseler.csv) | [CSV.gz]({path}/tum-sonuclar.csv.gz) | [Oku]({path}/README.md) |\n'
    index += '''
## Hangi dosya ve filtre?

Hisse özeti `time_split=total`, `jump_filter=all`, `target_group=bist_equities` satırlarıdır. Tam dosya bunlara ek olarak 10 endeksi, `train`, `validation`, `test` dönemlerini ve `no_jump10` duyarlılığını içerir. Sıfır olaylı ve küçük örnekli kombinasyonlar da korunur. `dosya-kontrol.csv`, ana tablo ve bu dışa aktarımların satır sayılarını ve SHA-256 değerlerini kaydeder.

Örneğin altın düştükten sonraki risk için altın hisse özetinde `source_condition=down0`, `unit=USD`, `interval=4h`, `response=post_open` seçin. İstenen hisse için `target_symbol`, düşüş sayısı için `negative_count`, bilinen olay sayısı için `n` ve oran için `negative_rate` sütununa bakın. `0.7` %70 demektir; −%3 veya daha kötü düşüş ayrı `down3_count` sütunundadır.

- `down0` / `up0`: kaynak <0 / >0; `down2` / `up2`: ≤−%2 / ≥+%2; `down4` / `up4`: ≤−%4 / ≥+%4.
- `same`: aynı 10 mumdaki geçmiş eşzamanlı hareket. `post_open`: sinyal kapanışından kesinlikle sonra başlayan ilk uygun barın açılışından 10 ortak mumluk hareket. Bunlar birbirinin yerine kullanılmaz.
- `selected_source_signals` tüm seçilen kaynak olayları, `n` sonucu bilinen olayları gösterir. Sonucu eksik olaylar n dışındadır. `baseline_negative_rate` koşulsuz sabit ızgara bazıdır; `negative_rate_difference` farkı eşleştirilmiş veya nedensel değildir.
- `risk_flag`: n≥10 ve düşüş oranı ≥%70 için `tarihsel_uyari`, n<10 için `ornek_yetersiz`; bunlar keyfi tarama eşikleridir. `no_jump10` sıçrama duyarlılığıdır, veri hatası teşhisi değildir.

[Dosya kontrol listesi](dosya-kontrol.csv) · [Tam yöntem, örnekler ve sınırlamalar](../README.md) · [Plan](../PLAN.md)

**Uyarı:** Tarihsel oranlar geleceğin olasılığı, neden-sonuç ilişkisi veya yatırım tavsiyesi değildir. Çoklu tarama, küçük örnekler, dönem sınırları, örtüşen sonraki pencereler, veri/nominal zaman ve işlem maliyetleri sonuçların kullanımını sınırlar.

Arşivi ana tablodan tekrar oluşturmak için depo kökünde `.venv/bin/python -m tools.organize_macro_risk` çalıştırın. Ana ölçüm komutu da arşivi yeniler. Önceki ana dosyalar ve bağlantılar korunur.
'''
    (archive/'README.md').write_text(index, encoding='utf-8')
    return counts


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path('research/measurements/macro-risk-screen'))
    args=p.parse_args()
    for asset, counts in sorted(export(args.root).items()):
        print(f"{asset}: tam={counts['full']}, hisse özeti={counts['summary']}")


if __name__ == '__main__':
    main()
