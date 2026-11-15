# ATK-TR-D1.0-2026-08 — Bölüm 24

**PDF sayfaları:** 491–530
**Sayfa kartları:** 40

## Alt başlıklar

- 24.2 — Fiyat Farkı Neden Oluşur ve Nasıl
- 24.3 — Aynı Varlık mı? Ürün, Pair, Ağ ve
- 24.4 — Gross Spread, Net Edge ve Başabaş Eşiği
- 24.5 — Exchange Arbitrage: Önceden Fonlanmış
- 24.7 — Triangular Arbitrage ve Döngü Matematiği
- 24.8 — DEX Arbitrage: Pool, Gas, Price Impact ve
- 24.9 — Veri, Timestamp ve Stale Quote Riski
- 24.11 — Tam Maliyet Yığını ve Güvenlik Tamponu
- 24.13 — Platform, Ağ, Withdrawal ve
- 24.14 — No-Trade Eşiği, Kill Switch ve Operasyon
- 24.15 — Tam Arbitraj İş Akışı ve Vaka Analizleri
- 0.65 — zorunlu oran değildir.

## Konu dağılımı

- `fundamental_derivatives`: 24 sayfa
- `execution_microstructure`: 21 sayfa
- `market_basics`: 18 sayfa
- `risk_management`: 18 sayfa
- `hedge_arbitrage`: 17 sayfa
- `trend_regime`: 9 sayfa
- `crypto_specific`: 8 sayfa
- `strategy_design`: 8 sayfa
- `support_resistance`: 7 sayfa
- `derivatives_options`: 7 sayfa
- `liquidity_imbalance`: 5 sayfa
- `automation_ai`: 5 sayfa
- `volume_flow`: 5 sayfa
- `breakout_failure`: 4 sayfa
- `momentum`: 4 sayfa
- `market_structure`: 4 sayfa
- `candle_behavior`: 4 sayfa
- `relative_cross_market`: 3 sayfa
- `pullback`: 2 sayfa
- `macro_rates`: 2 sayfa
- `patterns`: 2 sayfa
- `follow_through`: 2 sayfa
- `indicator_systems`: 2 sayfa
- `psychology_process`: 1 sayfa
- `volatility`: 1 sayfa
- `chart_transformations`: 1 sayfa
- `multi_timeframe`: 1 sayfa
- `ohlcv_data`: 1 sayfa
- `wave_cycle_models`: 1 sayfa
- `fundamental_valuation`: 1 sayfa
- `position_management`: 1 sayfa

## Sayfa şeritleri

### PDF s. 491 — Bölüm girişi/devamı

BÖLÜM 24 Arbitraj, Piyasa Verimliliği ve Operasyon Riski Görünen fiyat farkından uygulanabilir net edge ve operasyon kontrolüne

**Konular:** fundamental_derivatives, hedge_arbitrage

**Kart:** `ATK-TR-D1.0-2026-08.p0491`

### PDF s. 492 — Bölüm girişi/devamı

Bu Bölümün Amacı Arbitraj, bir varlığın veya dönüşüm döngüsünün farklı piyasalarda geçici olarak uyumsuz fiyatlanmasından yararlanmayı amaçlar. Yönlü trade’de “fiyat nereye gidecek?” sorusu öndeyken arbitrajda “aynı ekonomik maruziyet şu anda iki yerde gerçekten farklı uygulanabilir fiyatla mı işlem görüyor?” sorusu öne çıkar. Bu ayrım arbitrajı otomatik olarak risksiz yapmaz.

**Konular:** execution_microstructure, fundamental_derivatives, hedge_arbitrage, market_basics, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0492`

### PDF s. 493 — 24.2 — Fiyat Farkı Neden Oluşur ve Nasıl

24.1 Arbitrajı Yönlü Trading’den Ayırmak Arbitrage (aynı ekonomik varlık veya bağlı dönüşüm döngüsündeki geçici fiyat uyumsuzluğunu, eşleşen alım–satım bacaklarıyla değerlendirme), klasik long/short tahmininden farklı bir edge kaynağıdır. Ancak “fiyatın yönünü tahmin etmiyorum” demek “zarar ihtimali yok” demek değildir. Karar alanı Yönlü trade Arbitraj Edge Trend, mean reversion, yapı veya olay sonrası yön.

**Konular:** market_basics, execution_microstructure, risk_management, fundamental_derivatives, hedge_arbitrage

**Kart:** `ATK-TR-D1.0-2026-08.p0493`

### PDF s. 494 — 24.3 — Aynı Varlık mı? Ürün, Pair, Ağ ve

Gerçeklik: Küçük fark hız ve maliyet nedeniyle uygulanamaz olabilir; büyük fark ise likidite, withdrawal, veri veya counterparty riskinin fiyatıdır. Ürün, Pair, Ağ ve Settlement Kimliği Ticker benzerliği fiyat karşılaştırması için yeterli değildir. BTC/USDT spot ile BTC perpetual; ağ üzerindeki BTC ile wrapped token; USD ile USDT quote; aynı sembolün farklı contract adresleri ekonomik olarak farklı risk ve settlement taşır.

**Konular:** crypto_specific, fundamental_derivatives, hedge_arbitrage, execution_microstructure, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0494`

### PDF s. 495 — 24.4 — Gross Spread, Net Edge ve Başabaş Eşiği

 İki venue’de tam symbol ve product türü aynı mı?  Base ve quote aynı mı; quote conversion gerekiyor mu?  Network ve contract address eşleşiyor mu?

**Konular:** execution_microstructure, market_basics, relative_cross_market, crypto_specific, fundamental_derivatives

**Kart:** `ATK-TR-D1.0-2026-08.p0495`

### PDF s. 496 — 24.5 — Exchange Arbitrage: Önceden Fonlanmış

DOĞRU BİLİNEN YANLIŞ Mit: İki last price arasındaki fark arbitraj kârıdır. Gerçeklik: Alış ask’tan, satış bid’den ve miktara göre depth tüketilerek gerçekleşir. Last price uygulanabilir emir fiyatı değildir.

**Konular:** execution_microstructure, market_basics, fundamental_derivatives, hedge_arbitrage, pullback

**Kart:** `ATK-TR-D1.0-2026-08.p0496`

### PDF s. 497 — 24.7 — Triangular Arbitrage ve Döngü Matematiği

24.6 Transfer Tabanlı Arbitraj, Envanter ve Rebalans Transfer tabanlı modelde trader önce ucuz venue’den varlık alır, sonra pahalı venue’ye gönderip satar. Bu işlem iki bacağı eşzamanlı kilitlemez. Transfer süresince spread kapanabilir, ağ sıkışabilir veya withdrawal durabilir.

**Konular:** execution_microstructure, fundamental_derivatives, hedge_arbitrage, risk_management, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0497`

### PDF s. 498 — 24.8 — DEX Arbitrage: Pool, Gas, Price Impact ve

Her leg %0,10 fee ise fee çarpanı yaklaşık 0,997 olur ve teorik sonuç yaklaşık 10.014,9 USDT’ye iner. Rounding ve toplam 12 USDT slippage sonrası yalnız 2,9 USDT kalır. Sistem güvenlik tamponu 10 USDT ise döngü no-trade’dir.

**Konular:** execution_microstructure, crypto_specific, market_basics, fundamental_derivatives, hedge_arbitrage

**Kart:** `ATK-TR-D1.0-2026-08.p0498`

### PDF s. 499 — 24.9 — Veri, Timestamp ve Stale Quote Riski

DEX alanı Kontrol Net edge etkisi Slippage tolerance Kabul edilen maksimum fiyat sapması. Çok yüksekse kötü fill; çok düşükse revert. Gas İki/çoklu transaction ve onay maliyeti.

**Konular:** execution_microstructure, market_basics, fundamental_derivatives, hedge_arbitrage, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0499`

### PDF s. 500 — 24.11 — Tam Maliyet Yığını ve Güvenlik Tamponu

 İki fiyatın exchange timestamp’i ve local receive time’ı.  Last değil bid/ask ve miktar bazlı depth.  Feed bağlantısı, son update süresi ve outlier uyarısı.

**Konular:** execution_microstructure, market_basics, crypto_specific, fundamental_derivatives, hedge_arbitrage

**Kart:** `ATK-TR-D1.0-2026-08.p0500`

### PDF s. 501 — 24.13 — Platform, Ağ, Withdrawal ve

Gerçeklik: Spread, slippage, idle capital, rebalans ve failure buffer; doğrudan komisyonun birkaç katı olabilir. VAKA ANALİZİ — NET EDGE EŞİĞİ Sistem için ortalama toplam doğrudan maliyet %0,24; beklenen slippage %0,12; rebalans %0,08 ve güvenlik tamponu %0,15 olsun. Brüt fark %0,50 ise pozitif görünse de işlem yapılmaz.

**Konular:** automation_ai, fundamental_derivatives, hedge_arbitrage, execution_microstructure, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0501`

### PDF s. 502 — 24.14 — No-Trade Eşiği, Kill Switch ve Operasyon

Risk Kontrol No-trade / limit Stablecoin / quote risk Quote parity ve redemption. Account/KYC limit Withdrawal ve günlük transfer limiti. Miktar operasyon kapasitesini aşmaz.

**Konular:** strategy_design, fundamental_derivatives, hedge_arbitrage, risk_management, psychology_process

**Kart:** `ATK-TR-D1.0-2026-08.p0502`

### PDF s. 503 — 24.15 — Tam Arbitraj İş Akışı ve Vaka Analizleri

24.15 Tam Arbitraj İş Akışı ve Vaka Analizleri Şekil 24.7 – Tam arbitraj operasyon akışı Aşama Eylem Çıktı 1 Kimlik Asset, product, pair, quote, network ve settlement doğrula. 2 Veri Bid/ask, timestamp, source ve health kontrol et. 3 Miktar İki/üç bacağın depth ve precision hesabı.

**Konular:** execution_microstructure, fundamental_derivatives, hedge_arbitrage, market_basics, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0503`

### PDF s. 504 — 24.15 — Tam Arbitraj İş Akışı ve Vaka Analizleri

Arbitraj sinyali doğru olsa bile leg failure operasyon zararıdır. Kayıt Timeout, API response, reject nedeni, open exposure ve unwind slippage kaydedilir. Timestamp Küçük venue feed’i 18 saniye eski.

**Konular:** execution_microstructure, market_basics, fundamental_derivatives, hedge_arbitrage, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0504`

### PDF s. 505 — 24.15 — Tam Arbitraj İş Akışı ve Vaka Analizleri

Terim Aksiyon tanımı Leg Arbitraj işleminin ayrı alım, satım veya dönüşüm adımı. Leg risk Bir bacak dolarken diğerinin dolmamasıyla oluşan açık maruziyet. Pre-funded İki venue’de trade öncesi gerekli nakit ve varlığı hazır tutmak.

**Konular:** fundamental_derivatives, hedge_arbitrage, execution_microstructure, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0505`

### PDF s. 506 — 24.15 — Tam Arbitraj İş Akışı ve Vaka Analizleri

Volume-weighted executable price nasıl kullanılır? Filled quantity mismatch hangi riski doğurur? Tam maliyet yığınına hangi kalemler girer?

**Konular:** fundamental_derivatives, hedge_arbitrage, automation_ai, risk_management, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0506`

### PDF s. 507 — 24.15 — Tam Arbitraj İş Akışı ve Vaka Analizleri

ANA SÖZLÜK 24 bölümün ortak terim ve kavram başvuru rehberi 407 madde • alfabetik düzen • ilgili bölüm yönlendirmeleri

**Konular:** referans

**Kart:** `ATK-TR-D1.0-2026-08.p0507`

### PDF s. 508 — 24.15 — Tam Arbitraj İş Akışı ve Vaka Analizleri

Ana Sözlük Hakkında Bu sözlük, kitabın 24 bölümündeki bölüm sonu sözlüklerinden çıkarılan 453 terim satırının birleştirilmesiyle hazırlanmıştır. Aynı kavramın tekrarları ve açık yazım eşdeğerleri tek maddede toplanmış; farklı bağlam taşıyan benzer terimler ayrı bırakılmıştır. Tanımlar, terimlerin bu kitapta kullanılan işlevsel anlamını verir.

**Konular:** support_resistance, trend_regime, volume_flow, automation_ai, breakout_failure

**Kart:** `ATK-TR-D1.0-2026-08.p0508`

### PDF s. 509 — 24.15 — Tam Arbitraj İş Akışı ve Vaka Analizleri

Terim Bu kitaptaki temel anlamı Bölüm Arbitrage Aynı veya bağlantılı ekonomik ürünlerdeki eşzamanlı fiyat uyumsuzluğunu eşleşen işlem bacaklarıyla değerlendirme. 11, 24 Ask Satıcıların kabul ettiği en düşük bekleyen satış fiyatı. 1 ATR True range’in ortalaması; yönsüz volatilite ölçümü.

**Konular:** volatility, market_basics, execution_microstructure, risk_management, derivatives_options

**Kart:** `ATK-TR-D1.0-2026-08.p0509`

### PDF s. 510 — 24.15 — Tam Arbitraj İş Akışı ve Vaka Analizleri

Terim Bu kitaptaki temel anlamı Bölüm Break-even stop Stopu entry veya maliyet düzeltilmiş entry seviyesine taşımak. 23 Broker Müşteri emirlerinin piyasaya iletilmesine ve işlemlerin yürütülmesine aracılık eden kurum. 1 Broker connection Desteklenen kurum hesabından emirleri TradingView paneliyle iletmek.

**Konular:** derivatives_options, market_basics, trend_regime, execution_microstructure, momentum

**Kart:** `ATK-TR-D1.0-2026-08.p0510`

### PDF s. 511 — 24.15 — Tam Arbitraj İş Akışı ve Vaka Analizleri

Terim Bu kitaptaki temel anlamı Bölüm Community script Başka kullanıcı tarafından yayımlanan özel göstergenin mantık ve riskini denetlemek. 15 Compile Kodun dil/sentaks kurallarına uygunluğunu kontrol etmek. 16 Composite Operator Büyük katılımcıların birleşik etkisini düşünmek için analitik metafor kullanmak.

**Konular:** crypto_specific, macro_rates, execution_microstructure, fundamental_derivatives, patterns

**Kart:** `ATK-TR-D1.0-2026-08.p0511`

### PDF s. 512 — 24.15 — Tam Arbitraj İş Akışı ve Vaka Analizleri

Terim Bu kitaptaki temel anlamı Bölüm CVD Deltanın seçilen başlangıçtan kümülatif toplamı. 7 D Terim Bu kitaptaki temel anlamı Bölüm Data feed Fiyat ve hacmin geldiği borsa/broker/veri kaynağını kontrol etmek. 15 Day trading Pozisyonu tanımlı işlem günü/seans içinde açıp kapatma.

**Konular:** support_resistance, market_basics, automation_ai, crypto_specific, derivatives_options

**Kart:** `ATK-TR-D1.0-2026-08.p0512`

### PDF s. 513 — 24.15 — Tam Arbitraj İş Akışı ve Vaka Analizleri

Terim Bu kitaptaki temel anlamı Bölüm Doji Açılış ile kapanışın birbirine çok yakın olduğu kararsızlık mumu. 2 Drawdown Hesap zirvesinden sonraki dip seviyesine düşüş. 13 Drawing tool Seviye, bölge, eğim, mesafe veya notu görünür kılmak.

**Konular:** risk_management, execution_microstructure, follow_through, macro_rates, market_structure

**Kart:** `ATK-TR-D1.0-2026-08.p0513`

### PDF s. 514 — 24.15 — Tam Arbitraj İş Akışı ve Vaka Analizleri

Terim Bu kitaptaki temel anlamı Bölüm EQH / EQL Birbirine tolerans içinde yakın eşit tepe veya dip. 3 Equality İki dalganın benzer fiyat mesafesi üretmesi. 9 Equal highs/lows Yaklaşık aynı fiyat çevresinde oluşan birden fazla tepe veya dip.

**Konular:** liquidity_imbalance, breakout_failure, execution_microstructure, pullback, relative_cross_market

**Kart:** `ATK-TR-D1.0-2026-08.p0514`

### PDF s. 515 — 24.15 — Tam Arbitraj İş Akışı ve Vaka Analizleri

Terim Bu kitaptaki temel anlamı Bölüm Fair value estimate Model ve varsayımlara bağlı tahmini değer çıktısı. 16 Fair value / İçsel değer Temel analiz varsayımlarıyla tahmin edilen ekonomik değer. 1 Fakeout Bir sınır ya da seviyenin aşılmasının kabul görmeyip fiyatın eski alana geri dönmesi.

**Konular:** market_basics, breakout_failure, support_resistance, execution_microstructure, follow_through

**Kart:** `ATK-TR-D1.0-2026-08.p0515`

### PDF s. 516 — 0.65 — zorunlu oran değildir.

G Terim Bu kitaptaki temel anlamı Bölüm Gap fill Fiyatın klasik gap veya işaretli dengesizlik alanına geri dönerek alanı işlemesi. 5 Given-back profit MFE ile gerçekleşen çıkış sonucu arasındaki geri verilen kâr. 23 Golden pocket 0.618–0.65 dar trader konvansiyonu; 0.65 zorunlu oran değildir.

**Konular:** fundamental_derivatives, hedge_arbitrage, liquidity_imbalance, market_structure, chart_transformations

**Kart:** `ATK-TR-D1.0-2026-08.p0516`

### PDF s. 517 — 0.65 — zorunlu oran değildir.

Terim Bu kitaptaki temel anlamı Bölüm HVN / LVN Yerel yüksek / düşük hacim düğümü. 7 I Terim Bu kitaptaki temel anlamı Bölüm Ichimoku / Kumo Denge çizgileri ve ileri kaydırılmış bulut içeren trend sistemi. 8 Imbalance Footprint hücrelerinde bir tarafın tanımlı oranla baskın olması.

**Konular:** volume_flow, strategy_design, candle_behavior, fundamental_derivatives, indicator_systems

**Kart:** `ATK-TR-D1.0-2026-08.p0517`

### PDF s. 518 — 0.65 — zorunlu oran değildir.

Terim Bu kitaptaki temel anlamı Bölüm ITM / ATM / OTM Dayanak ile strike konumunu intrinsic value açısından sınıflandırmak. 21 K Terim Bu kitaptaki temel anlamı Bölüm Kaldıraç (Leverage) Ayrılan teminattan daha büyük piyasa maruziyeti kontrol edilmesini sağlayan ve hem kazanç hem kayıp etkisini büyüten mekanizma. 1, 19 Kill switch Tanımlı veri, bağlantı, kayıp veya hata koşulunda otomasyonu ve yeni emirleri hızlı biçimde durduran güvenlik mekanizması.

**Konular:** liquidity_imbalance, risk_management, derivatives_options, execution_microstructure, fundamental_derivatives

**Kart:** `ATK-TR-D1.0-2026-08.p0518`

### PDF s. 519 — 0.65 — zorunlu oran değildir.

Terim Bu kitaptaki temel anlamı Bölüm Liquidity sweep Seviye ötesindeki emirler tetiklendikten sonra fiyatın eski yapıya dönmesi; grab’a göre daha geniş süreç olabilir. 5 Liquidity void Fiyatın az overlap ve güçlü momentumla hızlı geçtiği ince alan. 5 Logarithmic scale Uzun dönem yüzdesel hareketleri eşit oran mantığıyla göstermek.

**Konular:** market_basics, trend_regime, market_structure, risk_management, momentum

**Kart:** `ATK-TR-D1.0-2026-08.p0519`

### PDF s. 520 — 0.65 — zorunlu oran değildir.

Terim Bu kitaptaki temel anlamı Bölüm Market cap Price × circulating supply ile yaklaşık mevcut piyasa değerini görmek. 19 Market cycle Trend–range–trend geçişlerini fazlar üzerinden koşullu olarak haritalamak. 17 Market emir Mevcut en iyi fiyatlardan hızlı gerçekleşme talimatı.

**Konular:** trend_regime, market_structure, momentum, liquidity_imbalance, multi_timeframe

**Kart:** `ATK-TR-D1.0-2026-08.p0520`

### PDF s. 521 — 0.65 — zorunlu oran değildir.

N Terim Bu kitaptaki temel anlamı Bölüm Neckline Double/triple ve OBO/TOBO yapılarını tamamlayan ara swing sınırı. 6 Net edge Bütün maliyet ve risk tamponu sonrası kalan avantaj. 24 Net income / bottom line Tüm gider ve vergiler sonrası muhasebe kârını izlemek.

**Konular:** ohlcv_data, risk_management, strategy_design, derivatives_options, fundamental_derivatives

**Kart:** `ATK-TR-D1.0-2026-08.p0521`

### PDF s. 522 — 0.65 — zorunlu oran değildir.

P Terim Bu kitaptaki temel anlamı Bölüm Paper Trading Gerçek para riske etmeden sanal bakiye ve emirlerle işlem sürecini uygulama. 12, 15 Parabolic SAR Trend takip ve stop-and-reverse noktaları. 8 Parite Bir varlığın başka bir para veya varlık cinsinden fiyatı.

**Konular:** automation_ai, risk_management, trend_regime, candle_behavior, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0522`

### PDF s. 523 — 0.65 — zorunlu oran değildir.

Terim Bu kitaptaki temel anlamı Bölüm Principal / Face value Vade sonunda geri ödenmesi vaat edilen nominal tutar. 20 Private key / seed phrase Self-custody erişim sırrını korumak ve kimseyle paylaşmamak. 19 Process thinking Tek sonucu değil plan uygulamasını değerlendirmek.

**Konular:** derivatives_options, market_basics, risk_management, support_resistance, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0523`

### PDF s. 524 — 0.65 — zorunlu oran değildir.

Terim Bu kitaptaki temel anlamı Bölüm Reaccumulation Markup içindeki range’in trend devamı üretip üretmediğini test etmek. 17 Reaction candle Bir yöndeki fiyat denemesinin kapanışa kadar geri çevrildiğini gösteren mum. 2 Realized P&L Kapatılan miktarda gerçekleşmiş kâr/zarar.

**Konular:** trend_regime, wave_cycle_models, breakout_failure, candle_behavior, patterns

**Kart:** `ATK-TR-D1.0-2026-08.p0524`

### PDF s. 525 — 0.65 — zorunlu oran değildir.

Terim Bu kitaptaki temel anlamı Bölüm Risk acceptance Stop sonucunu emirden önce parasal ve zihinsel olarak kabul etme. 14 Risk budget Tek işlem, gün, hafta ve portföy için önceden ayrılan kayıp sınırı. 13 RMA Wilder tipi yumuşatılmış hareketli ortalama.

**Konular:** risk_management, fundamental_derivatives, strategy_design, volume_flow, hedge_arbitrage

**Kart:** `ATK-TR-D1.0-2026-08.p0525`

### PDF s. 526 — 0.65 — zorunlu oran değildir.

Terim Bu kitaptaki temel anlamı Bölüm Setup family Pullback, breakout veya range gibi fırsat modelinin ailesi. 11 Short Düşüşten yararlanmayı amaçlayan pozisyon. 1 Signal Setup lehine veya aleyhine tek bilgi parçası.

**Konular:** indicator_systems, execution_microstructure, momentum, market_basics, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0526`

### PDF s. 527 — 0.65 — zorunlu oran değildir.

Terim Bu kitaptaki temel anlamı Bölüm Strike Hakkın kullanılabileceği fiyatı belirlemek. 21 Structure trail Stopu confirmed swing veya protected level arkasına taşımak. 23 Supply zone Güçlü düşüş departure’ının başladığı alan.

**Konular:** support_resistance, derivatives_options, fundamental_derivatives, volume_flow, fundamental_valuation

**Kart:** `ATK-TR-D1.0-2026-08.p0527`

### PDF s. 528 — 0.65 — zorunlu oran değildir.

Terim Bu kitaptaki temel anlamı Bölüm Timeframe conflict Farklı ölçeklerdeki görünüm farkının pullback/range/reversal bilgisi üretmesi. 10 Timeout Bir bacağın tamamlanması için izin verilen maksimum süre. 24 Time edge Stratejinin belirli zaman penceresinde ölçülmüş performans farkını kaydetmek.

**Konular:** risk_management, trend_regime, position_management, crypto_specific, fundamental_derivatives

**Kart:** `ATK-TR-D1.0-2026-08.p0528`

### PDF s. 529 — 0.65 — zorunlu oran değildir.

U Terim Bu kitaptaki temel anlamı Bölüm Uncertainty Sonraki sonucun kesin bilinmemesi. 13 Underlying Option değerinin bağlı olduğu varlık veya sözleşmeyi doğrulamak. 21 Unrealized P&L Açık pozisyonun mevcut fiyata göre değişen fakat henüz kapanmamış sonucu.

**Konular:** volume_flow, crypto_specific, market_basics, relative_cross_market, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0529`

### PDF s. 530 — 0.65 — zorunlu oran değildir.

Terim Bu kitaptaki temel anlamı Bölüm Watchlist Aynı filtrelerle izlenecek sembolleri sınırlı gruplarda toplama listesi. 11, 15 Wave count Olası dalga sırasını aynı degree içinde etiketleme. 9 Wave degree Dalganın zaman/ölçek seviyesi.

**Konular:** candle_behavior, support_resistance, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0530`
