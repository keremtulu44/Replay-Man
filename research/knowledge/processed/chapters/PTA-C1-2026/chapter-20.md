# PTA-C1-2026 — Bölüm 20

**PDF sayfaları:** 121–125
**Sayfa kartları:** 5

## Alt başlıklar

- 20.2 — Başlangıç ve bitiş noktaları sonucu değiştirir
- 20.4 — Pearson R bize ne anlatır?
- 20.6 — Regresyon matematiği ile ek gösterge sinyallerini ayırın
- 20.7 — Long/Short Position Tool: giriş, stop ve hedef mesafesini ölçmek
- 20.9 — Regresyon hangi araçlarla tamamlanır?

## Konu dağılımı

- `geometry_tools`: 5 sayfa
- `risk_management`: 4 sayfa
- `trend_regime`: 4 sayfa
- `volatility`: 2 sayfa
- `market_basics`: 2 sayfa
- `ohlcv_data`: 1 sayfa
- `indicator_systems`: 1 sayfa
- `strategy_design`: 1 sayfa
- `volume_flow`: 1 sayfa

## Sayfa şeritleri

### PDF s. 121 — 20.2 — Başlangıç ve bitiş noktaları sonucu değiştirir

BÖLÜM 20 Doğrusal Regresyon ve İleri Ölçüm Araçları HIZLI ROL — Ana görev: regresyonla seçtiğiniz fiyat aralığının genel yönünü ve ne kadar düzenli ilerlediğini görmek; Position ve Measure araçlarıyla giriş-stop-hedef mesafelerini ölçmek. Tek başına kazanma olasılığını veya gelecek fiyatı söylemez. Ana risk: analiz aralığını sonradan fiyata uydurmak, Pearson R’yi kazanma oranı veya iyi R:R’yi tek başına kârlılık sanmak.

**Konular:** geometry_tools, risk_management, trend_regime, volatility

**Kart:** `PTA-C1-2026.p0121`

### PDF s. 122 — 20.4 — Pearson R bize ne anlatır?

KENDİNE SOR Bu regresyon aralığını neden tam burada başlatıp bitirdim? Cevap “çizgi fiyatı daha iyi sarıyor” ise seçim geriye dönük uyuma yaklaşıyor. 20.3 — Sabit aralık regresyonu ile dönem uzunluğu kullanan sürüm aynı kullanım değildir TradingView’de kullanıcının başlangıç ve bitiş noktalarını seçtiği Regresyon Trendi (Regression Trend) gibi araçlarla, belirli bir dönem uzunluğu üzerinden sürekli yeniden hesaplanan Doğrusal Regresyon Kanalı (Linear Regression Channel) göstergeleri aynı kullanım biçimine sahip değildir.

**Konular:** geometry_tools, trend_regime, ohlcv_data

**Kart:** `PTA-C1-2026.p0122`

### PDF s. 123 — 20.6 — Regresyon matematiği ile ek gösterge sinyallerini ayırın

Aralık değişti, R değişti Seçilen aralığa duyarlılık Önceki analiz “yanlıştı” demek zorunlu değil TEKNİK SORUN Yüksek Pearson R, sistemin çok kârlı olduğu anlamına gelmez. R yalnızca seçtiğiniz fiyatların zaman içinde ne kadar düzgün bir çizgiye uyduğunu gösterir; stop, hedef, piyasa ortamındaki değişim ve işlem maliyetini hesaba katmaz. 20.5 — Regresyon kanalının dışına çıkmak otomatik dönüş değildir Üst banda çıkınca “çok pahalı, SAT”, alt banda inince “çok ucuz, AL” demek yanıltıcı olabilir.

**Konular:** geometry_tools, indicator_systems, risk_management, trend_regime, volatility

**Kart:** `PTA-C1-2026.p0123`

### PDF s. 124 — 20.7 — Long/Short Position Tool: giriş, stop ve hedef mesafesini ölçmek

Bu ek sinyaller regresyon matematiğinin zorunlu parçası değildir. Bir göstergeyi değerlendirirken hangi bölümün doğrusal regresyon hesabı, hangi bölümün geliştiricinin ek strateji mantığı olduğunu ayırın. Mevcut eğimi ileri uzatmak gelecek tahmini değildir Bazı göstergeler mevcut regresyon eğimini geleceğe doğru görsel olarak uzatır.

**Konular:** risk_management, geometry_tools, market_basics, strategy_design

**Kart:** `PTA-C1-2026.p0124`

### PDF s. 125 — 20.9 — Regresyon hangi araçlarla tamamlanır?

20.8 — Ölçüm araçları: Measure, Price Range ve Date Range Cetvel (Measure/Ruler), Price Range ve Date Range fiyat ve zaman mesafesini ölçer. “64 günlük hareket +%20 sürdü” bilgisini vermeleri, sonraki hareketin de aynı süre ve büyüklükte olacağını göstermez. Measure / Ruler (Cetvel) Fiyat değişimi, bar/zaman mesafesi Gelecek hareket tahmini Price Range (Fiyat Aralığı) İki fiyat arasındaki fark / yüzde Destek-direncin geçerliliği Date Range (Tarih Aralığı) İki nokta arasındaki zaman/bar sayısı Döngünün tekrar edeceği garantisi Long/Short Position Tool Giriş-stop-hedef senaryosu ve R:R Kazanma oranı / beklenti 20.9 — Regresyon hangi araçlarla tamamlanır?

**Konular:** trend_regime, geometry_tools, risk_management, volume_flow, market_basics

**Kart:** `PTA-C1-2026.p0125`
