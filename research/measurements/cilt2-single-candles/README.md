# Cilt 2 P2 — Tek Mum Geometrisi

> **Tarihsel arşiv uyarısı (19.11.2026):** Olay-sıralı bölümler sonuç ufkunu bölüm içinde zorunlu tutmaz ve XU100 bağımsız satır kaydırmasıyla eşlenir; özellikle günlük bitiş etiketleri farklı olabilir. Sonuçlar kapanış başlangıçlı/maliyetsiz keşiftir, bağımsız ileri test veya gerçek işlem değildir. [Genel denetim](../general-review/README.md).

## Kapsam

125 varlık ve dört periyotta 912.810 örtüşebilen geometrik varyant olayı ölçüldü. Olaylar bağımsız değildir; aynı mum farklı pin eşiklerine ve fitil reddi tanımına aynı anda girebilir.

Ölçülenler: gövde/aralık, kapanış konumu, üst/alt fitil oranı, range/ATR, doji envanteri, 0,40/0,50/0,60 fitil ve 0,20/0,30 gövde eşikli pin varyantları, marubozu, uzun güçlü kapanış ve fitil reddi.

## Ana sonuç

4h/60 bar BIST testinde bull marubozu `%3,18`, long bull `%1,22`, alt fitil reddi `%1,04` ve pin(0,50/0,20) `%1,32` XU100-aşırı medyan verdi. Aynı kurallar eğitimde yaklaşık `-%3,2` ile `-%4,3` arasındadır. Ayı karşılıkları eğitimde pozitifken doğrulama/testte negatiftir.

Bu nedenle tek mum adı bağımsız ve zaman-kararlı avantaj değildir. Kitabın “mumun adı değil davranışı ve bağlamı” ilkesi desteklenmiştir. Parametre varyantlarının çokluğu ayrı avantajlar olarak sayılmayacaktır; olay örtüşme matrisi P12'de üretilecektir.

## Veri bütünlüğü

- `inventory.csv`: Her seri için bütün olay ve doji sayımları
- `event_study.csv`: Grup/periyot/zaman bölümü/olay/yön/gövde bandı/range bandı için eksiksiz sonuçlar
- `summary.json`: Toplam olay sayıları

912.810 satırlık olay tablosu yaklaşık 487 MB olduğu ve sıkıştırılmış hâli GitHub tek dosya sınırını aştığı için depoya ikili kopya olarak eklenmedi. Üretim kodu, kaynak OHLCV ve bütün agregasyon tabloları sürümlüdür; aynı tablo `python -m tools.measure_cilt2_single_candles` ile deterministik olarak yeniden üretilir. Bu sınırlama sonuç satırlarının veya varyantların agregasyonlardan çıkarıldığı anlamına gelmez.
