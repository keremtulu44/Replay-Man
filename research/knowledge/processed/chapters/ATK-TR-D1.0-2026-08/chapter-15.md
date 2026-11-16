# ATK-TR-D1.0-2026-08 — Bölüm 15

**PDF sayfaları:** 302–328
**Sayfa kartları:** 27

## Alt başlıklar

- 15.1 — Platformu Stratejiden Ayırmak
- 15.2 — Watchlist, Sembol ve Veri Kaynağı
- 15.3 — Chart Type, Zaman Dilimi, Ölçek ve
- 15.4 — Layout, Workspace ve Temiz Grafik
- 15.5 — Çizim Araçları: Seviye, Bölge, Trendline ve
- 15.6 — Fibonacci, Ölçüm ve Koordinat Disiplini
- 15.7 — İndikatör Kurulumu, Ayarları ve Şablon
- 15.8 — Community Script, Repaint ve Otomatik
- 15.9 — Long–Short Position Araçlarıyla İşlem
- 15.10 — Alarm Tasarımı: Koşul, Sıklık, Mesaj ve
- 15.11 — Bar Replay ile Kör Karar Pratiği
- 15.12 — Paper Trading, Emir Paneli ve Broker
- 15.13 — Dual/Multi-Chart Görev Ayrımı
- 15.14 — Otomatik Pattern, Range ve Session
- 15.15 — Tam TradingView Test ve Çalışma İş Akışı

## Konu dağılımı

- `strategy_design`: 18 sayfa
- `validation_replay`: 14 sayfa
- `automation_ai`: 12 sayfa
- `market_basics`: 11 sayfa
- `risk_management`: 10 sayfa
- `trend_regime`: 8 sayfa
- `breakout_failure`: 7 sayfa
- `chart_transformations`: 5 sayfa
- `volume_flow`: 4 sayfa
- `liquidity_imbalance`: 4 sayfa
- `ohlcv_data`: 3 sayfa
- `position_management`: 3 sayfa
- `execution_microstructure`: 3 sayfa
- `geometry_tools`: 3 sayfa
- `sessions_timing`: 2 sayfa
- `support_resistance`: 2 sayfa
- `psychology_process`: 2 sayfa
- `pullback`: 1 sayfa
- `volatility`: 1 sayfa
- `market_structure`: 1 sayfa
- `multi_timeframe`: 1 sayfa
- `crypto_specific`: 1 sayfa
- `candle_behavior`: 1 sayfa
- `patterns`: 1 sayfa

## Sayfa şeritleri

### PDF s. 302 — Bölüm girişi/devamı

BÖLÜM 15 TradingView, Grafik Araçları ve Test İş Akışı Sembol doğrulamadan replay ve paper trading’e kadar görev bazlı platform sistemi

**Konular:** validation_replay

**Kart:** `ATK-TR-D1.0-2026-08.p0302`

### PDF s. 303 — Bölüm girişi/devamı

Bu Bölümün Amacı Önceki bölümlerde fiyatı okumayı, setup kurmayı, riski hesaplamayı ve duygusal süreç kapıları oluşturmayı öğrendik. Bu bölümde aynı sistemi TradingView ekranına taşırız. Grafiği açtığım anda önce sembolü ve veri kaynağını doğrular, sonra bağlam–setup–tetik katmanlarını ayırır, işlem planını çizer, alarm kurar ve fikri replay ile paper trading ortamında sınarım.

**Konular:** validation_replay, strategy_design, automation_ai, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0303`

### PDF s. 304 — 15.1 — Platformu Stratejiden Ayırmak

15.1 Platformu Stratejiden Ayırmak TradingView (grafik, analiz, alarm, test ve bazı broker bağlantılarını tek çalışma alanında birleştiren platform), bana veri ve araç sunar. Hangi koşulda işlem alacağımı platform değil, Bölüm 12’deki strateji kartım belirler. Platformun görevi, stratejiyi görünür ve uygulanabilir hâle getirmektir.

**Konular:** automation_ai, market_basics, strategy_design, validation_replay, volume_flow

**Kart:** `ATK-TR-D1.0-2026-08.p0304`

### PDF s. 305 — 15.2 — Watchlist, Sembol ve Veri Kaynağı

Analiz Çizim, indikatör, ölçüm ve çoklu grafik. Kavramı doğru yorumlama veya edge üretme garantisi vermez. Alarmdan sonra setup’ın tamamlandığını kanıtlamaz.

**Konular:** validation_replay, automation_ai, market_basics, strategy_design, ohlcv_data

**Kart:** `ATK-TR-D1.0-2026-08.p0305`

### PDF s. 306 — 15.2 — Watchlist, Sembol ve Veri Kaynağı

Benzer isimli başka şirket/coin/kontrat. Borsa / feed Fiyat hangi kaynak veya piyasadan geliyor? Farklı seans, likidite ve fiyat basamakları.

**Konular:** liquidity_imbalance, market_basics, sessions_timing, automation_ai, breakout_failure

**Kart:** `ATK-TR-D1.0-2026-08.p0306`

### PDF s. 307 — 15.3 — Chart Type, Zaman Dilimi, Ölçek ve

DOĞRU BİLİNEN YANLIŞ Mit: Ticker aynıysa grafik de aynıdır. Gerçeklik: Aynı varlık farklı borsa, broker, quote currency veya kontratta farklı fiyat, hacim, seans ve geçmiş veri üretebilir. Uygulama Görseli 15.2 – XAGTRYG sembol aramasında ticker, sağlayıcı/feed, ürün türü ve para biriminin çerçevelendiği sembol doğrulama ekranı.

**Konular:** chart_transformations, liquidity_imbalance, market_basics, ohlcv_data, position_management

**Kart:** `ATK-TR-D1.0-2026-08.p0307`

### PDF s. 308 — 15.3 — Chart Type, Zaman Dilimi, Ölçek ve

Dikkat Auto scale Mevcut görünümü ekrandaki veri ve çizimlere sığdırma. Uzak çizimler fiyatı sıkıştırabilir. Timeframe Bağlam, setup veya tetik görevi.

**Konular:** position_management, strategy_design, chart_transformations

**Kart:** `ATK-TR-D1.0-2026-08.p0308`

### PDF s. 309 — 15.4 — Layout, Workspace ve Temiz Grafik

15.4 Layout, Workspace ve Temiz Grafik Standardı Layout/workspace (grafik sayısı, sembol, timeframe, çizim, indikatör ve görünüm düzenini kaydedip yeniden kullanma çalışma alanı), karar rutinimi standardize eder. Her strateji için ayrı bir görev şablonu oluştururum; tek grafiği bütün piyasalar ve bütün amaçlar için kalabalıklaştırmam. Mikro tetik ve çok sayıda oscillator.

**Konular:** strategy_design, risk_management, trend_regime, validation_replay, execution_microstructure

**Kart:** `ATK-TR-D1.0-2026-08.p0309`

### PDF s. 310 — 15.5 — Çizim Araçları: Seviye, Bölge, Trendline ve

VAKA ANALİZİ — ÜÇ WORKSPACE XAGTRYG için “1G Bağlam”, “2S Setup” ve “30D Tetik” adlı üç layout kurarım. Günlükte yalnız major yapı ve bölgeler; 2 saatte pullback, FVG ve hacim; 30 dakikada trigger, stop ve hedef görünür. Aynı çizgiyi üç grafikte çoğaltmak yerine yalnız görev için gerekli referansları taşırım.

**Konular:** strategy_design, support_resistance, liquidity_imbalance, pullback, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0310`

### PDF s. 311 — 15.6 — Fibonacci, Ölçüm ve Koordinat Disiplini

Araç Doğru kullanım Yaygın hata Channel Paralel yön/volatilite koridoru. Paralelliği kaybolmuş yapıyı kanal diye sürdürmek. Path / brush Eğitim, olası rota veya serbest açıklama.

**Konular:** strategy_design, geometry_tools, trend_regime, volatility

**Kart:** `ATK-TR-D1.0-2026-08.p0311`

### PDF s. 312 — 15.7 — İndikatör Kurulumu, Ayarları ve Şablon

Aynı şekilde price range, date range ve measure araçları da yalnız seçtiğim koordinatları hesaplar. Araç İlk tıklama / ikinci tıklama Çıktı Fib retracement Impulse başlangıcı → impulse sonu Pullback derinliği ve retracement alanları. Fib extension Tanımlı swing yapısına göre anchor noktaları Projection ve extension referansları.

**Konular:** trend_regime, strategy_design, automation_ai, geometry_tools, market_structure

**Kart:** `ATK-TR-D1.0-2026-08.p0312`

### PDF s. 313 — 15.7 — İndikatör Kurulumu, Ayarları ve Şablon

Kontrol alanı Soracağım soru Örnek hata Session Hangi seans verisi kullanılıyor? VWAP/session aracını yanlış oturumda çalıştırmak. Görsel Hangi plot karar için gerekli?

**Konular:** sessions_timing, trend_regime, volume_flow

**Kart:** `ATK-TR-D1.0-2026-08.p0313`

### PDF s. 314 — 15.8 — Community Script, Repaint ve Otomatik

15.8 Community Script, Repaint ve Otomatik Araç Sınırları Community script, yararlı fikirler ve özel araçlar sağlayabilir; ancak yayınlanmış veya popüler olması metodolojiyi doğrulamaz. Repaint (geçmişte görünen sinyalin yeni veri geldikçe değişmesi, silinmesi veya konum değiştirmesi), özellikle MTF, pivot, future-looking veya açık bar kullanan araçlarda test sonucunu yanıltabilir. Denetim Kontrol edeceğim Açıklama Araç ne ölçüyor, sinyal hangi bar kapanışında kesinleşiyor?

**Konular:** validation_replay, automation_ai, multi_timeframe, volume_flow

**Kart:** `ATK-TR-D1.0-2026-08.p0314`

### PDF s. 315 — 15.9 — Long–Short Position Araçlarıyla İşlem

15.9 Long–Short Position Araçlarıyla İşlem Planı Long/short position tool (giriş, stop ve hedef seviyelerini görsel olarak yerleştirip fiyat mesafesi ve R:R taslağını gösterme), emir değildir. Önce teknik seviyeleri belirlerim; aracı bu seviyelere yerleştirir, sonra Bölüm 13 formülüyle gerçek quantity hesaplarım. Order type, spread ve olası slippage.

**Konular:** market_basics, risk_management, execution_microstructure, strategy_design, breakout_failure

**Kart:** `ATK-TR-D1.0-2026-08.p0315`

### PDF s. 316 — 15.10 — Alarm Tasarımı: Koşul, Sıklık, Mesaj ve

Uygulama Görseli 15.6 – XAGTRYG grafiğinde long position tool; entry, invalidation, target, R:R, ilk engel ve tahmini maliyet notlarının birlikte gösterimi. 15.10 Alarm Tasarımı: Koşul, Sıklık, Mesaj ve Eylem Alert (tanımladığım fiyat, çizim veya uygun indikatör koşulu gerçekleştiğinde bildirim üretme), ekrana sürekli bakma ihtiyacını azaltır. Alarm kurarken “fiyat 112 olunca” gibi eksik bir cümle yerine hangi serinin hangi seviyeyi hangi yönde ve hangi doğrulama sıklığında geçeceğini yazarım.

**Konular:** automation_ai, market_basics, risk_management, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0316`

### PDF s. 317 — 15.10 — Alarm Tasarımı: Koşul, Sıklık, Mesaj ve

Alarm bileşeni Örnek Neden gerekli? Reference / geçilen şey 112,00 yatay seviye Neyin aşıldığı açık. Direction Crossing up Yukarı ve aşağı olay ayrılır.

**Konular:** automation_ai, strategy_design, breakout_failure, psychology_process, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0317`

### PDF s. 318 — 15.11 — Bar Replay ile Kör Karar Pratiği

Uygulama Görseli 15.7 – TradingView alert oluşturma penceresinde condition, crossing direction, frequency, expiration, message ve notification alanlarının numaralandırılması. 15.11 Bar Replay ile Kör Karar Pratiği Bar Replay (grafiği geçmişte seçtiğim tarihe götürüp sonraki barları adım adım açarak geleceği görmeden karar pratiği yapma), geçmiş grafiğe bakıp “burada alırdım” deme yanılgısını azaltır. Replay başlamadan geleceği ele veren çizimleri, otomatik sinyalleri ve notları temizlerim.

**Konular:** validation_replay

**Kart:** `ATK-TR-D1.0-2026-08.p0318`

### PDF s. 319 — 15.11 — Bar Replay ile Kör Karar Pratiği

2 Kör başlangıç Setup öncesine git; gelecek barları ve sonuç notlarını gizle. 3 Karar kaydı Bağlam, setup, trigger, entry, stop, target ve no-trade. 4 Bar ilerletme Sabit hız veya tek bar; karar sonradan değiştirilmez.

**Konular:** validation_replay, strategy_design, execution_microstructure, risk_management, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0319`

### PDF s. 320 — 15.12 — Paper Trading, Emir Paneli ve Broker

VAKA ANALİZİ — BREAKOUT/RETEST REPLAY XAGTRYG 2S breakout–retest modelini 2024 başından başlayan geçmiş bölümde test ettiğimi varsayalım. Her valid breakout’tan önce grafiği durdurur, entry–stop–target çizimini kaydederim. Retest gelmeyen örnekleri “kaçtı” diye silmem; no-fill olarak kaydederim.

**Konular:** validation_replay, breakout_failure, risk_management, market_basics, crypto_specific

**Kart:** `ATK-TR-D1.0-2026-08.p0320`

### PDF s. 321 — 15.12 — Paper Trading, Emir Paneli ve Broker

Desteklenen ürünler, emir tipleri, veri, ücret, yetki ve güvenlik bağlı kuruma göre değişir. • Trading panelde Paper Trading mi, gerçek broker hesabı mı bağlı? • Hesap para birimi, balance, leverage ve quantity gerçekçi mi?

**Konular:** validation_replay, market_basics, risk_management, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0321`

### PDF s. 322 — 15.13 — Dual/Multi-Chart Görev Ayrımı

Uygulama Görseli 15.9 – Paper Trading panelinde account, order ticket, market/limit/stop seçimi, quantity, take-profit, stop-loss, positions, orders ve history alanları. 15.13 Dual/Multi-Chart Görev Ayrımı Dual-chart veya multi-chart layout (aynı ya da farklı sembol/timeframe’leri eşzamanlı panellerde gösterme), ancak her panelin görevi farklıysa değerlidir. Üst zaman bağlamı, orta zaman setup’ı ve alt zaman tetik grafiğini ayırabilirim.

**Konular:** strategy_design, chart_transformations, trend_regime, volume_flow, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0322`

### PDF s. 323 — 15.14 — Otomatik Pattern, Range ve Session

DOĞRU BİLİNEN YANLIŞ Mit: Daha fazla grafik aynı anda daha fazla teyit sağlar. Gerçeklik: Aynı veri farklı panellerde tekrar ediliyorsa teyit sayısı artmaz. Multi-chart yalnız görev, veri kaynağı veya zaman ufku ayrımı sağladığında değerlidir.

**Konular:** trend_regime, strategy_design, breakout_failure, candle_behavior, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0323`

### PDF s. 324 — 15.14 — Otomatik Pattern, Range ve Session

Araç ailesi Aday olarak gösterir Manuel doğrulama Heikin Ashi/auto filter Trend streak veya dönüş adayı. Gerçek OHLC, fiyat ve standart mum teyidi. Adayın önceki trendini, tamamlanma çizgisini, kapanışını, invalidation’ını ve hedefe kalan alanı kontrol ederim.

**Konular:** trend_regime, patterns, strategy_design, breakout_failure, chart_transformations

**Kart:** `ATK-TR-D1.0-2026-08.p0324`

### PDF s. 325 — 15.15 — Tam TradingView Test ve Çalışma İş Akışı

15.15 Tam TradingView Test ve Çalışma İş Akışı Platformu verimli kullanmak tek tek araçları bilmekten değil, her gün aynı sırayı tekrarlamaktan gelir. Aşağıdaki akışta watchlist analiz evrenini, layout bağlamı, çizimler setup’ı, alarm beklemeyi, replay geçmiş karar pratiğini, paper trading canlı operasyonu ve günlük öğrenmeyi yönetir. Aşama TradingView eylemi Çıktı 1 Evren Watchlist ve filtrelenmiş sembol grupları.

**Konular:** strategy_design, validation_replay, risk_management, automation_ai, breakout_failure

**Kart:** `ATK-TR-D1.0-2026-08.p0325`

### PDF s. 326 — 15.15 — Tam TradingView Test ve Çalışma İş Akışı

Uygulama Görseli 15.12 – Bölüm 15’in tam iş akışını gösteren gerçek TradingView ekran serisi: watchlist → günlük bağlam 2S setup alarm 30D tetik replay/paper günlük. Temsilî eğitim şeması.→ → → → → Hızlı Başvuru Sorun Kontrol Varsayılan eylem Fiyat başka grafikten farklı Feed/quote/contract/session Sembol kimliğini doğrula; çizimi güncellemeden karşılaştır. Grafik sıkışık veya okunmuyor Auto scale, uzak çizim, indikatör sayısı İlgisiz katmanı kaldır; göreve özel layout aç.

**Konular:** validation_replay, strategy_design, automation_ai, psychology_process, position_management

**Kart:** `ATK-TR-D1.0-2026-08.p0326`

### PDF s. 327 — 15.15 — Tam TradingView Test ve Çalışma İş Akışı

 İndikatör source, length, timeframe, session ve sürümü kayıtlı.  Community script repaint ve canlı/replay davranışı açısından denetlendi.  Long/short tool seviyeleri teknik; gerçek quantity ayrıca hesaplandı.

**Konular:** market_basics, validation_replay, risk_management, automation_ai, ohlcv_data

**Kart:** `ATK-TR-D1.0-2026-08.p0327`

### PDF s. 328 — 15.15 — Tam TradingView Test ve Çalışma İş Akışı

Standart mum ile Heikin Ashi hangi farklı görevleri yapar? Lineer ve log ölçek ne zaman ayrılır? Auto scale hangi durumda grafiği sıkıştırabilir?

**Konular:** validation_replay, market_basics, automation_ai, chart_transformations, geometry_tools

**Kart:** `ATK-TR-D1.0-2026-08.p0328`
