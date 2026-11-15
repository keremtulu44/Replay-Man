# ATK-TR-D1.0-2026-08 — Bölüm 23

**PDF sayfaları:** 473–490
**Sayfa kartları:** 18

## Alt başlıklar

- 23.1 — Pozisyon Yönetimi Girişten Önce Başlar
- 23.3 — Likidite, Yapı ve Volatiliteyle Hedef
- 23.4 — Partial Exit ve Scaling Out Matematiği
- 23.5 — Break-Even: Risk Azaltma mı, Erken Çıkış
- 23.6 — Normal Stop ile Trailing Stop Görev Ayrımı
- 23.8 — ATR ve Volatilite Tabanlı Trailing
- 23.9 — Yapı Tabanlı Trailing: HL, LH ve Protected
- 23.11 — Zaman, Seans Sonu ve Haber Yaklaşımı
- 23.12 — Range, Breakout, Pattern ve Gap Çıkışları
- 23.14 — Hedge Kapatma, Roll ve Tam Pozisyon
- 23.15 — Tam Pozisyon Yönetimi İş Akışı

## Konu dağılımı

- `risk_management`: 14 sayfa
- `liquidity_imbalance`: 11 sayfa
- `trend_regime`: 9 sayfa
- `strategy_design`: 7 sayfa
- `market_basics`: 6 sayfa
- `volatility`: 6 sayfa
- `fundamental_derivatives`: 5 sayfa
- `breakout_failure`: 5 sayfa
- `market_structure`: 5 sayfa
- `momentum`: 3 sayfa
- `support_resistance`: 2 sayfa
- `validation_replay`: 1 sayfa
- `volume_flow`: 1 sayfa
- `ohlcv_data`: 1 sayfa

## Sayfa şeritleri

### PDF s. 473 — Bölüm girişi/devamı

BÖLÜM 23 Pozisyon Yönetimi, Kâr Alma ve Çıkış Stratejileri Sabit hedeften partial matematiğine, trailing stoptan tam çıkışa

**Konular:** referans

**Kart:** `ATK-TR-D1.0-2026-08.p0473`

### PDF s. 474 — Bölüm girişi/devamı

Bu Bölümün Amacı İşleme doğru yerden girmek önemlidir; fakat sonuç dağılımını çoğu zaman pozisyon açıkken verdiğimiz kararlar belirler. Aynı setup, biri ilk küçük kârda tamamen çıktığında; diğeri hedef, partial ve trailing kurallarını uyguladığında farklı performans üretebilir. Bu bölümde amaç her tepeyi veya dibi yakalamak değildir.

**Konular:** risk_management, liquidity_imbalance, strategy_design, trend_regime, fundamental_derivatives

**Kart:** `ATK-TR-D1.0-2026-08.p0474`

### PDF s. 475 — 23.1 — Pozisyon Yönetimi Girişten Önce Başlar

23.1 Pozisyon Yönetimi Girişten Önce Başlar Trade management (pozisyon açıldıktan sonra stop, hedef, miktar, süre ve çıkış kararlarını uygulama), girişten sonra doğaçlama yapılacak bir faaliyet değildir. Giriş öncesinde en az üç plan yazılır: trade yanlışsa nerede çıkacağım, trade beklediğim gibi ilerlerse hangi hedefte ne yapacağım, ne fiyat ne de tez yeterince ilerlemezse ne kadar süre bekleyeceğim? Plan alanı Girişten önce yazılacak Pozisyon açıkken ölçülecek Tez ve horizon Setup neden çalışmalı; beklenen hareket kaç bar/seans/gün?

**Konular:** risk_management, strategy_design, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0475`

### PDF s. 476 — 23.3 — Likidite, Yapı ve Volatiliteyle Hedef

DOĞRU BİLİNEN YANLIŞ Mit: İyi bir giriş bulduysam çıkışı piyasa ilerledikçe belirleyebilirim. Gerçeklik: Açık kâr ve zarar karar algısını değiştirir. Önceden yazılmayan çıkış, çoğu zaman korku veya açgözlülüğe bırakılır.

**Konular:** strategy_design, support_resistance, trend_regime, liquidity_imbalance, volatility

**Kart:** `ATK-TR-D1.0-2026-08.p0476`

### PDF s. 477 — 23.4 — Partial Exit ve Scaling Out Matematiği

Likidite Equal highs/lows, session high-low, obvious stops. Fiyatın çekilebileceği fakat sweep sonrası dönebileceği alan. Zone / range Supply-demand, resistance/support, opposite range boundary.

**Konular:** support_resistance, trend_regime, volatility, liquidity_imbalance, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0477`

### PDF s. 478 — 23.4 — Partial Exit ve Scaling Out Matematiği

Stop entry’ye taşınıyorsa kalan fiyat riski sıfıra yaklaşabilir; fakat gap, slippage ve maliyet riski kalır. %40 pozisyon 106’da kapatılırsa gerçekleşen brüt kâr 2,40’tır. Kalan %60’ın ilk stopa riski 1,80’dir; maliyet öncesi toplam worst-case +0,60 olur.

**Konular:** risk_management, liquidity_imbalance, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0478`

### PDF s. 479 — 23.5 — Break-Even: Risk Azaltma mı, Erken Çıkış

DOĞRU BİLİNEN YANLIŞ Mit: Pozisyonun bir kısmını kârla kapattığım anda artık kaybedemem. Gerçeklik: Partial fiyatı, kapatılan miktar, kalan stop mesafesi ve maliyetler toplam işlem sonucunu belirler. 23.5 Break-Even: Risk Azaltma mı, Erken Çıkış mı?

**Konular:** risk_management, breakout_failure, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0479`

### PDF s. 480 — 23.6 — Normal Stop ile Trailing Stop Görev Ayrımı

23.6 Normal Stop ile Trailing Stop Görev Ayrımı Regular stop başlangıç tezinin yanlış olduğu seviyeyi korur. Trailing stop (fiyat lehe ilerledikçe belirli kural ile yalnız tek yönde sıkılaşan stop), risk kontrolünden kâr koruma ve trend taşıma görevine geçer. Aktivasyon kuralı olmadan başlangıçtan itibaren kullanılan çok sıkı trail, normal stopun yerine geçemez.

**Konular:** risk_management, trend_regime, liquidity_imbalance, market_basics, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0480`

### PDF s. 481 — 23.8 — ATR ve Volatilite Tabanlı Trailing

23.7 Sabit Yüzde ve Sabit Tutar Trailing Fixed-percentage trailing, fiyatın ulaştığı en avantajlı seviyeden sabit yüzde uzaklıkta stop tutar. Long için kavramsal formül: trail adayı = highest high since activation × (1 − yüzde). Short için lowest low × (1 + yüzde).

**Konular:** volatility, risk_management, market_basics, liquidity_imbalance, validation_replay

**Kart:** `ATK-TR-D1.0-2026-08.p0481`

### PDF s. 482 — 23.9 — Yapı Tabanlı Trailing: HL, LH ve Protected

Long pozisyonda yeni ATR adayı eski stoptan yüksekse sıkılaştırır; düşükse eski stopu korurum. Hesaplama ve emir güncelleme zamanı backtest ile aynı olmalıdır. DOĞRU BİLİNEN YANLIŞ Mit: ATR trail piyasaya uyum sağladığı için choppy piyasada da güvenilir çıkış üretir.

**Konular:** volatility, market_basics, market_structure, risk_management, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0482`

### PDF s. 483 — 23.11 — Zaman, Seans Sonu ve Haber Yaklaşımı

DOĞRU BİLİNEN YANLIŞ Mit: Her yeni higher low altında stop taşımak objektif yapı yönetimidir. Gerçeklik: Hangi swing’in confirmed sayıldığı, wick/close kuralı ve timeframe önceden tanımlanmazsa yapı sonradan seçilir. 23.10 Momentum ve Price-Action Çıkışları Momentum kaybı tam çıkışın tek başına kanıtı değildir; uyarı katmanıdır.

**Konular:** momentum, risk_management, breakout_failure, market_structure, volume_flow

**Kart:** `ATK-TR-D1.0-2026-08.p0483`

### PDF s. 484 — 23.11 — Zaman, Seans Sonu ve Haber Yaklaşımı

Zaman kapısı Soru Olası eylem Bar/horizon Setup normalde kaç bar içinde follow- through üretir? Session sonu Intraday tez bir sonraki seansa taşınacak mı? Tam çıkış veya overnight yeniden boyutlandırma.

**Konular:** risk_management, strategy_design, breakout_failure, fundamental_derivatives, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0484`

### PDF s. 485 — 23.12 — Range, Breakout, Pattern ve Gap Çıkışları

23.12 Range, Breakout, Pattern ve Gap Çıkışları Piyasa rejimi çıkış yöntemini değiştirir. Range trade’de karşı sınıra yaklaşırken mean-reversion avantajı azalabilir. Breakout trade’de range içine reclaim veya pattern invalidation tezi bozabilir.

**Konular:** liquidity_imbalance, trend_regime, breakout_failure, market_structure, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0485`

### PDF s. 486 — 23.14 — Hedge Kapatma, Roll ve Tam Pozisyon

23.13 PSAR ve Heikin Ashi ile Yardımcı Çıkış Teyidi Parabolic SAR, trend boyunca fiyatın arkasında noktalar üretip flip olduğunda olası dönüş/exit uyarısı verebilir. Heikin Ashi ise OHLC’nin ortalanmış dönüşümünü kullanarak trendi daha pürüzsüz gösterir. Her ikisi de yardımcı filtre olabilir; gerçek işlem fiyatı ve ana yapı yerine geçmez.

**Konular:** fundamental_derivatives, risk_management, trend_regime, market_structure, ohlcv_data

**Kart:** `ATK-TR-D1.0-2026-08.p0486`

### PDF s. 487 — 23.15 — Tam Pozisyon Yönetimi İş Akışı

DOĞRU BİLİNEN YANLIŞ Mit: Hedge yalnız kâra geçtiğinde kapatılmalıdır. Gerçeklik: Hedge’in görevi belirli riski azaltmaktır. Risk ortadan kalktığında, hedge tek başına zarar yazsa bile kapatma gerekebilir.

**Konular:** risk_management, fundamental_derivatives, strategy_design, liquidity_imbalance, momentum

**Kart:** `ATK-TR-D1.0-2026-08.p0487`

### PDF s. 488 — 23.15 — Tam Pozisyon Yönetimi İş Akışı

İlk supply 105, ikinci liquidity hedefi 109. Kalan risk ve maliyet matematiği yeniden hesaplanır.  105 üstü acceptance ve 2S confirmed HL oluşursa stop entry’ye değil, yeni yapısal savunmanın altına taşınır.

**Konular:** risk_management, liquidity_imbalance, trend_regime, volatility, momentum

**Kart:** `ATK-TR-D1.0-2026-08.p0488`

### PDF s. 489 — 23.15 — Tam Pozisyon Yönetimi İş Akışı

Terim Aksiyon tanımı Partial exit Pozisyonun belirli kısmını kapatıp kalanı açık tutmak. Scaling out Birden fazla hedefte miktarı kademeli azaltmak. Break-even stop Stopu entry veya maliyet düzeltilmiş entry seviyesine taşımak.

**Konular:** risk_management, volatility, breakout_failure, market_basics, market_structure

**Kart:** `ATK-TR-D1.0-2026-08.p0489`

### PDF s. 490 — 23.15 — Tam Pozisyon Yönetimi İş Akışı

PSAR range piyasasında neden zayıflar? Heikin Ashi neden gerçek emir fiyatı için tek başına kullanılmaz? Hedge ne zaman kapatılır veya roll edilir?

**Konular:** fundamental_derivatives, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0490`
