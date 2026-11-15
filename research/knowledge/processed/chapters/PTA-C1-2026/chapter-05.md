# PTA-C1-2026 — Bölüm 5

**PDF sayfaları:** 28–36
**Sayfa kartları:** 9

## Alt başlıklar

- 5.1 — MACD’nin üç parçası
- 5.3 — Sinyal çizgisi neden EMA’dır?
- 5.4 — MACD sütunları (histogram) aslında neyi gösterir?
- 5.6 — MACD / Sinyal kesişimi ne zaman anlamlı, ne zaman gürültü?
- 5.9 — Uyumsuzluk: hareket gücü zayıflıyor, kesin zaman vermiyor
- 5.10 — MACD uyumsuzluğunda hız ve fiyat yapısı
- 5.12 — MACD hangi araçlarla tamamlanır, hangileriyle tekrar eder?
- 5.13 — MACD için pratik karar akışı

## Konu dağılımı

- `momentum`: 9 sayfa
- `trend_regime`: 7 sayfa
- `volatility`: 5 sayfa
- `risk_management`: 4 sayfa
- `breakout_failure`: 4 sayfa
- `volume_flow`: 2 sayfa
- `pullback`: 2 sayfa
- `ohlcv_data`: 1 sayfa
- `psychology_process`: 1 sayfa
- `multi_timeframe`: 1 sayfa

## Sayfa şeritleri

### PDF s. 28 — 5.1 — MACD’nin üç parçası

BÖLÜM 5 MACD: Trend ve Hareket Gücü MACD’de çizgi isimlerini ezberlemek yerine şu basit fikri anlayın: kısa dönemli fiyat ortalaması ile daha uzun dönemli ortalama arasındaki fark izlenir. Sütunlar (histogram) ise MACD çizgisi ile sinyal çizgisi arasındaki farkı gösterir; fiyatın ne kadar geniş dalgalandığını ölçmez. HIZLI ROL — Ana görev: kısa ve uzun EMA arasındaki farkın açılıp kapanmasını izlemek; hareketin hızlanıp yavaşladığını görmek.

**Konular:** momentum, trend_regime, volatility, volume_flow, risk_management

**Kart:** `PTA-C1-2026.p0028`

### PDF s. 29 — 5.3 — Sinyal çizgisi neden EMA’dır?

Üstte EMA 12/26; altta onların farkından oluşan MACD, onun yumuşatılmış sinyal çizgisi ve aradaki farkı gösteren histogram. 5.2 — Formül işareti neden önemlidir? Standart hesap MACD = EMA(12) − EMA(26)’dır.

**Konular:** momentum, trend_regime

**Kart:** `PTA-C1-2026.p0029`

### PDF s. 30 — 5.4 — MACD sütunları (histogram) aslında neyi gösterir?

EMA son gözleme daha yüksek ağırlık verir. Sinyal çizgisinin hesap türünü değiştirirseniz kesişim zamanları ve MACD sütunları değerleri de değişebilir. Matematik değiştiğinde gösterge aynı gösterge olarak kalmaz.

**Konular:** momentum, volatility, ohlcv_data, breakout_failure, psychology_process

**Kart:** `PTA-C1-2026.p0030`

### PDF s. 31 — 5.6 — MACD / Sinyal kesişimi ne zaman anlamlı, ne zaman gürültü?

5.5 — Histogramı dört ayrı hareket durumu olarak okuyun MACD sütunlarında yalnız pozitif veya negatif işaret değil, sütunların büyüyüp küçülmesi de bilgi taşır. Histogram durumu Çizgiler arasındaki fark Daha doğru okuma Pozitif + büyüyor Pozitif fark genişliyor Yukarı yönlü hareket gücü artıyor Pozitif + küçülüyor Pozitif fark daralıyor Yukarı yönlü hareket gücü yavaşlıyor Negatif + büyüyor Negatif fark genişliyor Aşağı yönlü hareket gücü artıyor Negatif + küçülüyor Negatif fark daralıyor Aşağı yönlü hareket gücü yavaşlıyor Bu nedenle histogramın sıfır çizgisini geçmesini beklemeden hareket gücündeki hızlanma veya yavaşlama görülebilir. Fakat histogramın küçülmesi fiyatın mutlaka tersine döneceği anlamına gelmez; sonuç dönüş de olabilir, yataylaşma da.

**Konular:** trend_regime, momentum, risk_management

**Kart:** `PTA-C1-2026.p0031`

### PDF s. 32 — 5.9 — Uyumsuzluk: hareket gücü zayıflıyor, kesin zaman vermiyor

Piyasa bağlamı Kesişimin yorumu Ana risk Yatay piyasa Çok sayıda kısa ömürlü kesişim Sık yanlış sinyal / aşırı işlem Yapısal seviye yakınında Fiyat davranışına hareket gücü katmanı eklemek Kesişimi fiyat teyidinin yerine koymak Üst zaman dilimi filtresi Operasyonel yön/hareket gücü filtresi Zaman dilimi seçimine aşırı bağımlılık 5.7 — Sıfır çizgisinin doğru anlamı MACD’nin sıfıra gelmesi hızlı ve yavaş EMA’nın birbirine yaklaşması anlamına gelir. MACD sıfırdan yukarı geçtiğinde hızlı EMA yavaş EMA’nın üzerine geçmiş olur. Fakat bu, fiyatın otomatik olarak yeni bir yapısal yükseliş trendine geçtiğini kanıtlamaz; çünkü iki EMA da geçmiş fiyatlardan türetilir ve yatay piyasada sıfır çizgisi etrafında sık gidip gelebilir.

**Konular:** momentum, pullback, risk_management, trend_regime, multi_timeframe

**Kart:** `PTA-C1-2026.p0032`

### PDF s. 33 — 5.10 — MACD uyumsuzluğunda hız ve fiyat yapısı

Bu uyuşmazlık dönüşün tam zamanını vermez. DOĞRU SIRALAMA Uyumsuzluk → “hareket gücü teyidi zayıfladı” uyarısı. Ardından fiyat yapısı / önemli seviye / kırılım veya yeniden test gibi doğrudan fiyat teyidi aranır.

**Konular:** momentum, trend_regime, breakout_failure

**Kart:** `PTA-C1-2026.p0033`

### PDF s. 34 — 5.12 — MACD hangi araçlarla tamamlanır, hangileriyle tekrar eder?

Aynı hesap zincirine ait olsalar da uyumsuzluk iki görünümde aynı anda oluşmak zorunda değildir. Hem MACD çizgisinde hem histogramda aynı bölgede uyumsuzluk görülmesi daha seçici bir gözlem olabilir; ancak bunu iki bağımsız teyit saymak doğru değildir. İkisi de aynı MACD hesap zincirinden türetilir.

**Konular:** momentum, trend_regime, volatility, volume_flow, pullback

**Kart:** `PTA-C1-2026.p0034`

### PDF s. 35 — 5.12 — MACD hangi araçlarla tamamlanır, hangileriyle tekrar eder?

Kesin dönüş noktası, doğrudan fiyat hareketliliği, kesin kırılım yönü, tek başına beklenen başarı olasılığı veya uyumsuzluk sonrası dönüş zamanı. MACD’nin en güçlü rolü hareket gücünün hızlanması/yavaşlaması ve iki EMA hızının ayrışmasını görünür kılmaktır.

**Konular:** momentum, breakout_failure, volatility

**Kart:** `PTA-C1-2026.p0035`

### PDF s. 36 — 5.13 — MACD için pratik karar akışı

5.13 — MACD için pratik karar akışı Adım Soru MACD’nin rolü 1. Konum Fiyat önemli yapı/konum bölgesinde mi? Hareket gücü MACD/Sinyal/MACD sütunları nasıl değişiyor?

**Konular:** momentum, trend_regime, risk_management, volatility, breakout_failure

**Kart:** `PTA-C1-2026.p0036`
