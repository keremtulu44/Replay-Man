# OHLCV Replay Ölçüm Arşivi

Bu klasör 125 varlık ve 500 seride çalışan ilk nedensel replay ölçümlerini içerir.

## Kapsam

- 558.121 tamamlanmış OHLCV barı
- Mum geometrisi, volatilite, örtüşme, hareket kalitesi ve baskı kaybı
- 151.450 minor, 67.705 major swing ve 113.778 swing bacağı
- Swing seviyelerinde probe, kapanış kırılımı, takip, kabul, retest ve failure
- Karar özelliklerinden ayrı ileri getiri, MFE ve MAE

## Dosyalar

- `summary.json`: Toplam kapsam ve olay sayıları
- `series_inventory.csv`: 500 seri bazında ölçüm ve olay envanteri
- `structure_event_study.csv`: Grup/periyot/olay/yön bazında havuzlanmış finansal sonuçlar
- `structure_symbol_results.csv`: Her sembolde olay sonucu ve semboller arası tutarlılık girdisi
- `FINANCIAL_RESULTS.md`: BIST hisseleri 1h için okunabilir ilk finansal değerlendirme

## Zaman ve yön sözleşmesi

Pivot geometrik barında değil teyit barında bilinir; seviye ancak teyitten sonraki barda aktiftir. Failure ve probe rejection sonuçları ilk denemenin ters yönünde; kırılım, takip, kabul ve retest sonuçları kırılım yönünde ölçülür.

Bu çıktılar işlem maliyetsiz keşifsel olay çalışmasıdır; yürütülebilir strateji veya portföy backtesti değildir.
