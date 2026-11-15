# ATK-TR-D1.0-2026-08 — Bölüm 22

**PDF sayfaları:** 457–472
**Sayfa kartları:** 16

## Alt başlıklar

- 22.1 — Zamanı Bağımsız Sinyal Değil Piyasa
- 22.2 — UTC, Yerel Saat, DST ve Resmî Takvim
- 22.4 — Sydney/Pacific ve Asya/Tokyo Penceresi
- 22.5 — Londra Seansı: Açılış, Likidite ve İlk
- 22.7 — Overlap ve Seans Geçişleri
- 22.8 — Açılış, Opening Range ve Kapanış
- 22.9 — Session High–Low ve Likidite Rotası
- 22.11 — Session VWAP, Reset ve Anchor
- 22.12 — Strateji–Seans Uyumu
- 22.13 — Forex, Hisse, Kripto ve XAGTRYG
- 22.14 — Kişisel İşlem Penceresi ve Zaman
- 22.15 — Tam Gün İçi Zamanlama İş Akışı

## Konu dağılımı

- `liquidity_imbalance`: 16 sayfa
- `trend_regime`: 12 sayfa
- `volume_flow`: 11 sayfa
- `breakout_failure`: 11 sayfa
- `strategy_design`: 9 sayfa
- `risk_management`: 5 sayfa
- `market_basics`: 3 sayfa
- `relative_cross_market`: 2 sayfa
- `psychology_process`: 2 sayfa
- `candle_behavior`: 1 sayfa
- `fundamental_derivatives`: 1 sayfa
- `momentum`: 1 sayfa
- `market_structure`: 1 sayfa
- `volatility`: 1 sayfa

## Sayfa şeritleri

### PDF s. 457 — Bölüm girişi/devamı

BÖLÜM 22 İşlem Seansları, Likidite ve Gün İçi Zamanlama UTC doğrulamasından session VWAP ve kişisel işlem penceresine

**Konular:** liquidity_imbalance, volume_flow

**Kart:** `ATK-TR-D1.0-2026-08.p0457`

### PDF s. 458 — Bölüm girişi/devamı

Bu Bölümün Amacı Piyasa zamanı yalnız saatin kaç olduğunu göstermez. Hangi finans merkezlerinin açık olduğunu, hangi katılımcıların emir gönderdiğini, spread ve işlem hızının nasıl değişebileceğini, haber akışının ne zaman yoğunlaştığını ve seçtiğimiz setup’ın uygulanabilir olup olmadığını etkiler. Bu bölümde seansları mekanik yön sinyali olarak değil, karar bağlamı olarak kullanacağız.

**Konular:** liquidity_imbalance, strategy_design, trend_regime, volume_flow, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0458`

### PDF s. 459 — 22.1 — Zamanı Bağımsız Sinyal Değil Piyasa

22.1 Zamanı Bağımsız Sinyal Değil Piyasa Değişkeni Olarak Okumak Trading session (belirli piyasa merkezinin, borsanın veya kullanıcı tanımlı katılım penceresinin aktif olduğu zaman aralığı), “bu saatte al” kuralı değildir. Zaman; katılım, spread, işlem hızı, haber ve likidite havuzlarının ne zaman daha görünür hâle gelebileceğini anlatır. Zaman bilgisi Cevapladığı soru Cevaplamadığı soru Seans Hangi merkez ve katılımcı grubu daha aktif olabilir?

**Konular:** liquidity_imbalance, volume_flow, breakout_failure, candle_behavior, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0459`

### PDF s. 460 — 22.2 — UTC, Yerel Saat, DST ve Resmî Takvim

DOĞRU BİLİNEN YANLIŞ Mit: Doğru işlem saatini bulursam yön analizi yapmama gerek kalmaz. Gerçeklik: Seans yalnız uygulanabilirlik ve katılım bağlamıdır. Yapı, setup, geçersizlik, maliyet ve risk hâlâ gereklidir.

**Konular:** liquidity_imbalance, risk_management, strategy_design, volume_flow

**Kart:** `ATK-TR-D1.0-2026-08.p0460`

### PDF s. 461 — 22.4 — Sydney/Pacific ve Asya/Tokyo Penceresi

UYGULAMA GÖREVİ Aynı işlem günü için UTC’yi, borsanın yerel saatini ve kendi yerel saatinizi ekonomik takvim ve grafik ayarlarında yan yana doğrulayın. 22.3 Piyasa Türlerine Göre Seans Mantığı Her piyasa aynı şekilde “açık” değildir. Hisse borsalarında resmî ana seans, auction ve extended hours bulunabilir.

**Konular:** trend_regime, liquidity_imbalance, fundamental_derivatives, volume_flow, breakout_failure

**Kart:** `ATK-TR-D1.0-2026-08.p0461`

### PDF s. 462 — 22.5 — Londra Seansı: Açılış, Likidite ve İlk

Bu dönem yüksek likidite, trend ve breakout fırsatlarıyla ilişkilendirilebilir; ilk saatte fakeout riski de bulunur. Bu nedenle açılış hareketi “gerçek yön” değil, test edilmesi gereken ilk emir dalgasıdır. Londra açılışında gördüğüm Kontrol Karar Asya high/low aşımı Kapanış dışarıda mı; hızlı reclaim mi?

**Konular:** breakout_failure, liquidity_imbalance, trend_regime, volume_flow, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0462`

### PDF s. 463 — 22.7 — Overlap ve Seans Geçişleri

22.6 New York Seansı: Haber, Hisse Açılışı ve Katılım New York penceresi USD pair’leri, ABD hisseleri, endeksler, değerli metaller ve kriptoda önemli bir katılım değişimi yaratabilir. Makro veri, merkez bankası iletişimi veya ABD hisse açılışı aynı pencereye yığıldığında hız, spread ve slippage artabilir. Bu durum fırsat kadar uygulama riski de üretir.

**Konular:** liquidity_imbalance, risk_management, momentum, relative_cross_market, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0463`

### PDF s. 464 — 22.8 — Açılış, Opening Range ve Kapanış

Venue volume, tick volume veya order- book verisi. Session sınırı dışında close ve follow- through. “Breakout setup’ım Londra–New York overlap’inde, haber dışı günlerde, spread eşik altında ve range dışı kapanış + retest oluşursa aktif olur” gibi ölçülebilir pencere yazarım.

**Konular:** trend_regime, breakout_failure, volume_flow, liquidity_imbalance, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0464`

### PDF s. 465 — 22.9 — Session High–Low ve Likidite Rotası

Gerçeklik: Açılış aynı zamanda gap, auction, geniş spread ve yanlış ilk hareket riski taşır. Edge, stratejinin bu koşullarda test edilmiş sonucudur. 22.9 Session High–Low ve Likidite Rotası Session high ve session low (önceden tanımlanmış seans penceresinde görülen en yüksek ve en düşük fiyat), görünür likidite referanslarıdır.

**Konular:** liquidity_imbalance, breakout_failure, trend_regime, market_basics, market_structure

**Kart:** `ATK-TR-D1.0-2026-08.p0465`

### PDF s. 466 — 22.11 — Session VWAP, Reset ve Anchor

22.10 Haber Pencereleri ve No-Trade Kararı Ekonomik calendar (planlı veri, merkez bankası, şirket açıklaması ve diğer olayların zamanını gösterme), yön tahmin aracından önce risk takvimidir. Yüksek etkili olaylar spread, gap, slippage ve bar range’ini büyütebilir. Haber stratejisi olmayan trader için en iyi karar bazen olay öncesi veya hemen sonrasında işlem almamaktır.

**Konular:** risk_management, volume_flow, liquidity_imbalance, strategy_design, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0466`

### PDF s. 467 — 22.12 — Strateji–Seans Uyumu

Farklı reset’leri aynı VWAP sanmak. Regular vs extended Pre/after-market dahil mi? Hisse ana seans benchmark’ını extended volume ile karıştırmak.

**Konular:** volume_flow, strategy_design, trend_regime, breakout_failure, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0467`

### PDF s. 468 — 22.13 — Forex, Hisse, Kripto ve XAGTRYG

Strateji İhtiyaç Seans testi Breakout Yeterli katılım, range dışı close, follow- through. Açılış/overlap ile normal saat performansını karşılaştır. Trend pullback Yönlü kabul, kontrollü pullback, VWAP/yapı uyumu.

**Konular:** strategy_design, liquidity_imbalance, trend_regime, breakout_failure, relative_cross_market

**Kart:** `ATK-TR-D1.0-2026-08.p0468`

### PDF s. 469 — 22.14 — Kişisel İşlem Penceresi ve Zaman

22.14 Kişisel İşlem Penceresi ve Zaman Günlüğü Kişisel işlem penceresi (traderın strateji, piyasa, yaşam düzeni ve risk kapasitesine göre önceden belirlediği aktif analiz/işlem saatleri), bütün gün ekran başında kalmayı önler. Pencere “en hareketli saat” değil, doğru karar verebildiğim ve edge’imi test ettiğim saat olmalıdır. Günlük alan Kayıt Tarih / sembol / venue Doğru ürün ve veri kaynağı.

**Konular:** strategy_design, liquidity_imbalance, psychology_process, trend_regime, breakout_failure

**Kart:** `ATK-TR-D1.0-2026-08.p0469`

### PDF s. 470 — 22.15 — Tam Gün İçi Zamanlama İş Akışı

22.15 Tam Gün İçi Zamanlama İş Akışı Şekil 22.7 – Tam gün içi zamanlama iş akışı Aşama Eylem Çıktı 1 Takvim Venue tatili/erken kapanış ve ekonomik olayları kontrol et. 2 Saat UTC, yerel offset, DST ve grafik timezone’unu doğrula. 3 Bağlam Üst TF yapı, günlük bias ve beklenen gün tipini yaz.

**Konular:** strategy_design, liquidity_imbalance, risk_management, breakout_failure, psychology_process

**Kart:** `ATK-TR-D1.0-2026-08.p0470`

### PDF s. 471 — 22.15 — Tam Gün İçi Zamanlama İş Akışı

UYGULAMA GÖREVİ Ekonomik takvim → UTC session overlay → Asya high–low → Londra sweep → New York retest → VWAP → işlem günlüğü sırasıyla tek bir vaka kaydı oluşturun. Hızlı Başvuru Gördüğüm İlk kontrol Varsayılan eylem Session saatleri uyuşmuyor UTC, DST, exchange calendar, chart timezone Saati doğrulamadan analiz yapma. Overlap’te hız arttı Haber, spread, range ve acceptance Boyutu/maliyeti yeniden değerlendir.

**Konular:** volume_flow, strategy_design, trend_regime, liquidity_imbalance, breakout_failure

**Kart:** `ATK-TR-D1.0-2026-08.p0471`

### PDF s. 472 — 22.15 — Tam Gün İçi Zamanlama İş Akışı

Terim Aksiyon tanımı Extended hours Ana seans öncesi/sonrası işlem penceresini ve düşük likidite riskini kontrol etmek. Time edge Stratejinin belirli zaman penceresinde ölçülmüş performans farkını kaydetmek. Seans bilgisi hangi soruyu cevaplar, hangi soruyu cevaplamaz?

**Konular:** liquidity_imbalance, volume_flow, trend_regime, breakout_failure, volatility

**Kart:** `ATK-TR-D1.0-2026-08.p0472`
