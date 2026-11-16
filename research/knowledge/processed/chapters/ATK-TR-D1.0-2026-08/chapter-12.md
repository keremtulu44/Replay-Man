# ATK-TR-D1.0-2026-08 — Bölüm 12

**PDF sayfaları:** 239–261
**Sayfa kartları:** 23

## Alt başlıklar

- 12.1 — Strateji, Setup, Tetik ve İşlem Ayrımı
- 12.2 — İşlem Kurulumunun Dokuz Parçası
- 12.3 — İşlem Tezi ve No-Trade Koşulları
- 12.4 — Konum: Yapı, Bölge ve Likidite Rotası
- 12.5 — Confluence ve Bağımsız Kanıt
- 12.6 — Tetik ve Teyit Hiyerarşisi
- 12.7 — Agresif, Teyitli ve Retest Girişleri
- 12.8 — Geçersizlik, Stop, Hedef ve İşlem
- 12.9 — Pullback Devam Setup’ı
- 12.10 — Breakout–Retest ve Momentum Setup’ı
- 12.11 — Range, Failure Test ve False Breakout
- 12.12 — Trend Reversal Setup’ı
- 12.13 — Zone, FVG, Inside Bar, Gap, Indicator ve
- 12.15 — Backtest, Replay, Forward/Paper Test ve

## Konu dağılımı

- `strategy_design`: 22 sayfa
- `breakout_failure`: 11 sayfa
- `support_resistance`: 11 sayfa
- `trend_regime`: 10 sayfa
- `liquidity_imbalance`: 9 sayfa
- `market_structure`: 8 sayfa
- `risk_management`: 6 sayfa
- `validation_replay`: 5 sayfa
- `momentum`: 5 sayfa
- `volume_flow`: 4 sayfa
- `candle_behavior`: 4 sayfa
- `indicator_systems`: 3 sayfa
- `execution_microstructure`: 3 sayfa
- `volatility`: 2 sayfa
- `pullback`: 2 sayfa
- `automation_ai`: 2 sayfa
- `follow_through`: 1 sayfa
- `journal_review`: 1 sayfa
- `multi_timeframe`: 1 sayfa

## Sayfa şeritleri

### PDF s. 239 — Bölüm girişi/devamı

BÖLÜM 12 İşlem Kurulumu, Strateji Tasarımı ve Doğrulama Bağlamdan emre, modelden doğrulamaya tekrar edilebilir işlem sistemi

**Konular:** strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0239`

### PDF s. 240 — 12.1 — Strateji, Setup, Tetik ve İşlem Ayrımı

Bu Bölümün Amacı İlk on bir bölümde grafiğin parçalarını öğrendik: piyasa ve emirler, mum davranışı, market structure, önemli bölgeler, likidite, formasyonlar, hacim, indikatörler, Fibonacci/Elliott, top-down analiz ve çalışma stili. Fakat bu parçalar tek bir karar sistemine bağlanmadığında grafik yalnız işaretlerle dolar. Bölüm 12’nin görevi, “ne görüyorum?” sorusunu “hangi koşul gerçekleşirse işlem yaparım; hangi koşulda hiçbir şey yapmam?” sorusuna dönüştürmektir.

**Konular:** strategy_design, validation_replay, breakout_failure, liquidity_imbalance, volume_flow

**Kart:** `ATK-TR-D1.0-2026-08.p0240`

### PDF s. 241 — 12.1 — Strateji, Setup, Tetik ve İşlem Ayrımı

Trigger (setup’ı gerçek işleme dönüştüren kesin fiyat olayı), “şimdi aktif” dediğim noktadır. Trade ise gerçek emir, stop, hedef ve kayıtla birlikte uygulanan pozisyondur. Yükseliş trendinde demand/FVG pullback’i ve bullish yapı teyidi.

**Konular:** strategy_design, liquidity_imbalance, momentum, risk_management, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0241`

### PDF s. 242 — 12.2 — İşlem Kurulumunun Dokuz Parçası

Uygulama Görseli 12.2 – Aynı grafikte “ipucu”, “setup adayı”, “trigger” ve “gerçek işlem” etiketlerinin farklı renklerle ayrılması. 12.2 İşlem Kurulumunun Dokuz Parçası “Level–trigger–confirmation–risk” dört sütunu, önceki bölümlerde kurulan yapı ve top-down sistemiyle dokuz operasyon parçasına genişletilir. Böylece yalnız giriş anı değil, işlem fikrinin doğuşundan kayıt aşamasına kadar bütün yol kontrol edilir.

**Konular:** strategy_design, trend_regime, risk_management, volatility

**Kart:** `ATK-TR-D1.0-2026-08.p0242`

### PDF s. 243 — 12.3 — İşlem Tezi ve No-Trade Koşulları

VAKA ANALİZİ — XAGTRYG / TEMSİLİ • Günlük grafik yükseliş yapısını koruyor; fiyat 110,00–110,60 demand alanına dönüyor. • 4 saatlik grafikte pullback yavaşlıyor ve önceki BOS bölgesiyle bullish FVG çakışıyor. • 1 saatlik grafikte 109,90 altı kısa sweep sonrası 110,80 üstü bullish CHoCH kapanışı oluşuyor.

**Konular:** strategy_design, liquidity_imbalance, market_structure, support_resistance, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0243`

### PDF s. 244 — 12.4 — Konum: Yapı, Bölge ve Likidite Rotası

Gerçeklik: Stratejinin önemli bir çıktısı da “bugün benim modelim yok” diyebilmektir. No-trade, kaçırılmış fırsat değil; kuralın çalışmasıdır. 12.4 Konum: Yapı, Bölge ve Likidite Rotası Location (işlem fikrinin grafikte anlam kazandığı fiyat alanı), setup’ın en sık ihmal edilen parçasıdır.

**Konular:** strategy_design, liquidity_imbalance, trend_regime, support_resistance, breakout_failure

**Kart:** `ATK-TR-D1.0-2026-08.p0244`

### PDF s. 245 — 12.5 — Confluence ve Bağımsız Kanıt

Uygulama Görseli 12.3 – Range ortasındaki bullish engulfing ile demand+sweep sonrasındaki aynı engulfing’in karşılaştırılması. 12.5 Confluence ve Bağımsız Kanıt Confluence (aynı işlem tezini farklı veri ailelerinin desteklemesi), grafiğe mümkün olduğunca çok araç eklemek değildir. Kanıtları beş aileye ayırırım: bağlam, konum, fiyat davranışı, katılım/hacim ve zamanlama.

**Konular:** momentum, indicator_systems, liquidity_imbalance, strategy_design, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0245`

### PDF s. 246 — 12.6 — Tetik ve Teyit Hiyerarşisi

Konum Demand, support, external liquidity, FVG. İşlemin nerede aranacağını açıklar. Fiyat davranışı Sweep, close, BOS/CHoCH, retest, displacement.

**Konular:** strategy_design, volume_flow, breakout_failure, liquidity_imbalance, market_structure

**Kart:** `ATK-TR-D1.0-2026-08.p0246`

### PDF s. 247 — 12.7 — Agresif, Teyitli ve Retest Girişleri

Aşama Örnek olay Karar Gözlem Fiyat zone’a girdi veya liquidity seviyesine yaklaştı. Uyarı Fitil, momentum kaybı, divergence veya absorption. Teyit Gövdeli reclaim, BOS/CHoCH, breakout close veya güçlü reversal mum.

**Konular:** strategy_design, breakout_failure, support_resistance, candle_behavior, market_structure

**Kart:** `ATK-TR-D1.0-2026-08.p0247`

### PDF s. 248 — 12.7 — Agresif, Teyitli ve Retest Girişleri

Zone doğrudan kırılabilir; teyit azdır. Çok net HTF bağlamı, fresh zone ve önceden test edilmiş model. Teyitli close Fiyat davranışı görünür hâle gelir.

**Konular:** breakout_failure, risk_management, strategy_design, support_resistance, execution_microstructure

**Kart:** `ATK-TR-D1.0-2026-08.p0248`

### PDF s. 249 — 12.8 — Geçersizlik, Stop, Hedef ve İşlem

Uygulama Görseli 12.4 – Aynı pullback setup’ında zone touch, CHoCH close ve retest entry noktalarının tek grafikte karşılaştırılması. 12.8 Geçersizlik, Stop, Hedef ve İşlem Yapılabilirlik Invalidation (işlem tezinin artık doğru kabul edilemeyeceği fiyat veya davranış), stop-loss emrinden önce tanımlanır. Stop emri invalidation’ın uygulanabilir hâlidir.

**Konular:** strategy_design, risk_management, support_resistance, market_structure, volatility

**Kart:** `ATK-TR-D1.0-2026-08.p0249`

### PDF s. 250 — 12.9 — Pullback Devam Setup’ı

• Stopun arkasında gerçekten “tez bozuldu” diyebileceğim yapı var mı? • Fiyat stopa gitmeden önce setup’ı iptal eden erken davranış kuralım var mı? • İlk hedefe kadar karşı zone veya range ortası engeli var mı?

**Konular:** strategy_design, pullback, risk_management, market_structure, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0250`

### PDF s. 251 — 12.10 — Breakout–Retest ve Momentum Setup’ı

Adım Bullish pullback standardı No-trade işareti Invalidation Pullback swing dibi / demand altında kabul. Stop yalnız küçük trigger mumunun içine konuyor. Hedef Önceki tepe, BSL, measured move veya major zone.

**Konular:** strategy_design, breakout_failure, pullback, support_resistance, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0251`

### PDF s. 252 — 12.10 — Breakout–Retest ve Momentum Setup’ı

hacim ve follow-through birlikte değerlendirilir. Retest, breakout’ın yeni alanda kalıp kalamadığını sınar. Bileşen Güçlü işaret Zayıf / false breakout riski Sınır Birden fazla görünür reaksiyon, range/pattern boundary.

**Konular:** breakout_failure, support_resistance, trend_regime, volume_flow, candle_behavior

**Kart:** `ATK-TR-D1.0-2026-08.p0252`

### PDF s. 253 — 12.11 — Range, Failure Test ve False Breakout

Uygulama Görseli 12.6 – Breakout quality karşılaştırması: fitil aşımı, zayıf close, güçlü close+volume ve başarılı retest. 12.11 Range, Failure Test ve False Breakout Setup’ı Range setup’ında avantaj orta bölgede tahmin yapmak değil, sınırdaki asimetrik davranışı işlemektir. Failure test (range veya önemli seviyenin kısa süre aşılması ve yeniden içeri kapanış), breakout traderlarını yanlış tarafta bırakabilen bir trigger’dır.

**Konular:** breakout_failure, trend_regime, strategy_design, candle_behavior, follow_through

**Kart:** `ATK-TR-D1.0-2026-08.p0253`

### PDF s. 254 — 12.12 — Trend Reversal Setup’ı

VAKA ANALİZİ — XAGTRYG RANGE • TEMSİLİ: 2 saatlik range 108,80–111,40; fiyat 108,65’e iğne atıp 109,10’da kapanıyor. • Alt zaman bullish engulfing ve 109,35 üstü micro BOS geliyor. • Entry retestte; invalidation 108,60 altı kabul.

**Konular:** trend_regime, market_structure, strategy_design, breakout_failure, momentum

**Kart:** `ATK-TR-D1.0-2026-08.p0254`

### PDF s. 255 — 12.13 — Zone, FVG, Inside Bar, Gap, Indicator ve

Dönüş zinciri Gözlenebilir kanıt 6. Hedef rotası Karşı major zone’a kadar açık alan ve net invalidation. • Yalnız minor CHoCH: pullback içi tepki olabilir.

**Konular:** liquidity_imbalance, strategy_design, support_resistance, market_structure, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0255`

### PDF s. 256 — 12.13 — Zone, FVG, Inside Bar, Gap, Indicator ve

Araç / kavram Ana görevi Tek başına neden yetmez? Örnek birleşim RSI/MACD/CCI Momentum veya divergence confirmation. Fiyattan türetilir; location ve trigger yerine geçmez.

**Konular:** volume_flow, strategy_design, momentum, indicator_systems, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0256`

### PDF s. 257 — 12.15 — Backtest, Replay, Forward/Paper Test ve

12.14 Kural Tabanlı Strateji Kartı Rules-based strategy (girişten önce bütün karar alanları yazılmış ve farklı grafiklerde aynı biçimde uygulanabilen sistem), yoruma tamamen kapalı olmak zorunda değildir; fakat karar noktaları gözlenebilir ve kaydedilebilir olmalıdır. “Güçlü trend” dersem güçlü trendin ölçütünü, “iyi mum” dersem mumun kapanış ve gövde koşulunu tanımlarım. Kart alanı Yazılacak kural Piyasa / enstrüman Hangi semboller, minimum likidite ve spread koşulu?

**Konular:** strategy_design, breakout_failure, market_structure, validation_replay, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0257`

### PDF s. 258 — 12.15 — Backtest, Replay, Forward/Paper Test ve

canlıymış gibi ilerletme), forward test (kuralları yeni gelen piyasa verisinde izleme) ve paper trading (gerçek para riske etmeden sanal emirle uygulama) farklı soruları cevaplar. Geçmiş grafik taraması Model farklı dönemlerde gerçekten görülüyor mu? Setup örneği, bağlam, sonuç, no-trade.

**Konular:** strategy_design, validation_replay, execution_microstructure, journal_review, automation_ai

**Kart:** `ATK-TR-D1.0-2026-08.p0258`

### PDF s. 259 — 12.15 — Backtest, Replay, Forward/Paper Test ve

DOĞRU BİLİNEN YANLIŞ Mit: Backtest kârlıysa strateji gerçek piyasada çalışmaya hazırdır. Gerçeklik: Backtest yalnız geçmiş kuralların sonucudur; geleceği garanti etmez. Replay karar disiplinini, paper/forward test ise canlı akış ve emir uygulanabilirliğini sınar.

**Konular:** validation_replay, strategy_design, trend_regime, automation_ai, execution_microstructure

**Kart:** `ATK-TR-D1.0-2026-08.p0259`

### PDF s. 260 — 12.15 — Backtest, Replay, Forward/Paper Test ve

Bölüm Özeti Bölüm 12’nin ana sonucu, grafikteki teknik araçların tek tek “sinyal” üretmesi değil; her birinin bağlamdan hedefe uzanan karar zincirinde belirli bir görev üstlenmesidir. Strateji tekrarlanan sistem, setup güncel düzen, trigger kesin aktivasyon olayı ve trade gerçek uygulamadır. Kontrol alanı Kısa soru Bağlam Hangi piyasa hâli ve hangi üst zaman senaryosu?

**Konular:** strategy_design, breakout_failure, trend_regime, multi_timeframe, candle_behavior

**Kart:** `ATK-TR-D1.0-2026-08.p0260`

### PDF s. 261 — 12.15 — Backtest, Replay, Forward/Paper Test ve

Terim Aksiyon tanımı Invalidation İşlem tezinin artık geçerli olmadığı fiyat/davranış. No-trade Kurallar nedeniyle bilinçli olarak işlem yapılmayan durum. Confluence Farklı veri ailelerinin aynı tezi desteklemesi.

**Konular:** strategy_design, validation_replay, indicator_systems, momentum, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0261`
