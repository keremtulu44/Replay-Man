# PTA-C1-2026 — Bölüm 17

**PDF sayfaları:** 104–110
**Sayfa kartları:** 7

## Alt başlıklar

- 17.1 — Retracement aslında neyi hesaplar?
- 17.4 — Başlangıç noktası seçimi: en öznel karar
- 17.5 — 0,618’e temas neden giriş işareti değildir?
- 17.7 — Trend-Based Extension: hedef değil, projeksiyon
- 17.9 — Fibonacci zaman araçları: fiyat değil zaman ekseni
- 17.10 — En iyi kombinasyonlar ve tekrar riski

## Konu dağılımı

- `geometry_tools`: 6 sayfa
- `pullback`: 4 sayfa
- `trend_regime`: 3 sayfa
- `support_resistance`: 2 sayfa
- `volatility`: 2 sayfa
- `candle_behavior`: 2 sayfa
- `risk_management`: 1 sayfa
- `psychology_process`: 1 sayfa
- `volume_flow`: 1 sayfa
- `indicator_systems`: 1 sayfa
- `momentum`: 1 sayfa

## Sayfa şeritleri

### PDF s. 104 — 17.1 — Retracement aslında neyi hesaplar?

BÖLÜM 17 Fibonacci Ailesi: Oran, Başlangıç Noktası ve Projeksiyon Fibonacci tek başına al-sat sinyali üretmez. Seçtiğiniz belirgin fiyat hareketini belirli oranlara böler. Bu nedenle asıl analiz, çizgiden önce “hangi fiyat hareketini neden ölçüyorum?” sorusuyla başlar.

**Konular:** geometry_tools, pullback, risk_management, support_resistance, trend_regime

**Kart:** `PTA-C1-2026.p0104`

### PDF s. 105 — 17.1 — Retracement aslında neyi hesaplar?

Özet cümlesi otomatik ayrılamadı; tam kaynak şeridi kart JSONL kaydında korunuyor.

**Konular:** pullback

**Kart:** `PTA-C1-2026.p0105`

### PDF s. 106 — 17.4 — Başlangıç noktası seçimi: en öznel karar

17.2 — Fibonacci oranları matematiksel olarak nereden gelir? Fibonacci dizisi şu mantıkla ilerler: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89... Her yeni sayı kendisinden önceki iki sayının toplamıdır.

**Konular:** pullback, geometry_tools, volatility, trend_regime

**Kart:** `PTA-C1-2026.p0106`

### PDF s. 107 — 17.5 — 0,618’e temas neden giriş işareti değildir?

Başlangıç Yapıyı başlatan anlamlı dip/tepe İstenen Fib seviyesi çıksın diye birkaç bar kaydırılır Bitiş Ana hareketin önceden belirlenebilir karşı uç noktası Sonraki fiyatı daha iyi yakalayan fitil seçilir Test Sağ taraf kapalıyken aynı başlangıç noktası seçilebilir Gelecek fiyat görüldükten sonra ayarlanır Şekil 17.2 — Başlangıç noktasının yalnız birkaç bar veya fiyat birimi kayması bile 0,618 seviyesini değiştirir. KENDİNE SOR Grafiğin sağ tarafını kapatsaydım bu iki başlangıç noktasını yine seçer miydim? Cevap hayırsa, çizim analizden çok geriye dönük uyuma yaklaşmıştır.

**Konular:** candle_behavior, geometry_tools

**Kart:** `PTA-C1-2026.p0107`

### PDF s. 108 — 17.7 — Trend-Based Extension: hedef değil, projeksiyon

YANLIŞ / DOĞRU YANLIŞ: “0,618 geldi, AL.” DOĞRU: “Ana yapı yükseliş; anlamlı hareketin 0,50–0,618 bölgesindeyiz. Şimdi fiyat burada yeniden yukarı yönlü yapı veya hareket gücü üretiyor mu?” 17.6 — Fibonacci kümelenmesi: farklı ölçümlerin aynı bölgede buluşması Farklı, önceden gerekçelendirilmiş fiyat hareketlerine çizilen Fibonacci seviyeleri aynı bölgeye yaklaşabilir. Örneğin bir hareketin %50 seviyesi ile başka bir hareketin %78,6 seviyesi birbirine yakınsa Fibonacci kümelenmesi oluşur.

**Konular:** geometry_tools, trend_regime, psychology_process

**Kart:** `PTA-C1-2026.p0108`

### PDF s. 109 — 17.9 — Fibonacci zaman araçları: fiyat değil zaman ekseni

SAYISAL ÖRNEK A=100, B=160, C=130 olsun. 1,272 projeksiyon: 130 + (60×1,272) = 206,32. 1,618 projeksiyon: 130 + (60×1,618) = 227,08.

**Konular:** geometry_tools, volatility, pullback, support_resistance

**Kart:** `PTA-C1-2026.p0109`

### PDF s. 110 — 17.10 — En iyi kombinasyonlar ve tekrar riski

TEKNİK SORUN Fiyat seviyesi ile zaman bölgesini aynı şeymiş gibi yorumlamak hatadır. Fibonacci zaman aracı yalnız belirli bar/tarih çevresini gözlem penceresi olarak işaretler; kesin olay üretmez. 17.10 — En iyi kombinasyonlar ve tekrar riski Kombinasyon Rol ayrımı Değerlendirme Fib + Fiyat yapısı Fib = konum; Fiyat yapısı = davranış/bozulma Güçlü tamamlayıcı Fib + AVWAP Fib = oran; AVWAP = hacim ağırlıklı maliyet/konum Faydalı örtüşme; giriş işareti ayrı Fib + Volume Profile Fib = geometri; VP = fiyat seviyelerine göre hacim yoğunluğu Farklı veri sınıfları Fib + RSI / hareket gücü Fib = nerede; RSI = hareket gücü ne yapıyor Giriş işareti desteği olabilir Fib + Pitchfork İkisi de çizim ve hedef bölgesi üretir Kesişim faydalı olabilir ama iki bağımsız teyit değildir TEKRAR RİSKİ Retracement + Extension + Fib Fan aynı fiyat hareketinden türetiliyorsa, aynı bölgede birleşmeleri üç bağımsız teyit değildir.

**Konular:** geometry_tools, volume_flow, indicator_systems, momentum, candle_behavior

**Kart:** `PTA-C1-2026.p0110`
