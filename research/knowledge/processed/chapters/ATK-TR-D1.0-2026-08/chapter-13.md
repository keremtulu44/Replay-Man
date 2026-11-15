# ATK-TR-D1.0-2026-08 — Bölüm 13

**PDF sayfaları:** 262–281
**Sayfa kartları:** 20

## Alt başlıklar

- 13.1 — Belirsizlik, Risk ve Hayatta Kalma İlkesi
- 13.2 — R Birimi ve Risk Bütçesi Hiyerarşisi
- 13.3 — Stop Seçimi: Teknik, Volatilite ve Birleşik
- 13.4 — Pozisyon Büyüklüğü Formülü
- 13.5 — Position Sizing Modelleri ve Volatilite
- 13.6 — Hedef, R:R ve İşlem Yapılabilirlik
- 13.7 — Win Rate, Başa Baş Oranı ve Expectancy
- 13.9 — Drawdown ve Toparlanma Asimetrisi
- 13.10 — Kayıp Serisi ve Risk Azaltma Protokolü
- 13.11 — Portföy Isısı, Korelasyon ve Yoğunlaşma
- 13.13 — Kaldıraç, Marjin ve Likidasyon
- 13.14 — Options Primi ve Arbitraj Operasyon
- 13.15 — Tam Sermaye Koruma İş Akışı

## Konu dağılımı

- `risk_management`: 20 sayfa
- `strategy_design`: 11 sayfa
- `execution_microstructure`: 8 sayfa
- `portfolio_correlation`: 7 sayfa
- `fundamental_derivatives`: 7 sayfa
- `volatility`: 6 sayfa
- `market_basics`: 5 sayfa
- `crypto_specific`: 4 sayfa
- `hedge_arbitrage`: 4 sayfa
- `liquidity_imbalance`: 3 sayfa
- `relative_cross_market`: 3 sayfa
- `psychology_process`: 2 sayfa
- `trend_regime`: 2 sayfa
- `derivatives_options`: 2 sayfa
- `candle_behavior`: 1 sayfa
- `support_resistance`: 1 sayfa

## Sayfa şeritleri

### PDF s. 262 — Bölüm girişi/devamı

BÖLÜM 13 Risk Yönetimi ve Pozisyon Boyutlandırma Stop seviyesinden portföy riskine uygulanabilir sermaye koruma sistemi

**Konular:** risk_management, portfolio_correlation

**Kart:** `ATK-TR-D1.0-2026-08.p0262`

### PDF s. 263 — Bölüm girişi/devamı

Bu Bölümün Amacı Bölüm 12’de setup’ın bağlamını, trigger’ını, girişini, geçersizliğini ve hedefini yazdık. Şimdi aynı fikre ne kadar sermaye ayıracağımızı hesaplayacağız. Risk yönetimi işlemin kazanıp kazanmayacağını söylemez; yanlış çıktığımızda kaybın hesap, gün, hafta ve portföy ölçeğinde kabul edilebilir kalmasını sağlar.

**Konular:** risk_management, strategy_design, portfolio_correlation, execution_microstructure, crypto_specific

**Kart:** `ATK-TR-D1.0-2026-08.p0263`

### PDF s. 264 — 13.1 — Belirsizlik, Risk ve Hayatta Kalma İlkesi

13.1 Belirsizlik, Risk ve Hayatta Kalma İlkesi Uncertainty (sonraki fiyat sonucunu önceden kesin bilememe) piyasadan kaldırılamaz. Risk (yanlış çıktığımda ne kadar kaybedeceğimi ölçme ve seçme) ise yönetilebilir. En güçlü setup bile kaybedebilir; fakat kaybeden bir setup’ın hesabı ne kadar etkileyeceğini işlemden önce belirleyebilirim.

**Konular:** risk_management, strategy_design, execution_microstructure, liquidity_imbalance, portfolio_correlation

**Kart:** `ATK-TR-D1.0-2026-08.p0264`

### PDF s. 265 — 13.2 — R Birimi ve Risk Bütçesi Hiyerarşisi

13.2 R Birimi ve Risk Bütçesi Hiyerarşisi R (işlem başına başlangıçta kabul ettiğim parasal risk birimi), farklı fiyat ve enstrümanlardaki işlemleri ortak ölçekte karşılaştırmamı sağlar. Stopta planlanan kayıp 500 TL ise −1R, 1.000 TL net kazanç +2R’dir. Gerçek kayıp slippage nedeniyle 550 TL olursa sonuç −1,10R olarak kaydedilir.

**Konular:** risk_management, portfolio_correlation, psychology_process, execution_microstructure, relative_cross_market

**Kart:** `ATK-TR-D1.0-2026-08.p0265`

### PDF s. 266 — 13.3 — Stop Seçimi: Teknik, Volatilite ve Birleşik

13.3 Stop Seçimi: Teknik, Volatilite ve Birleşik Stop-loss (setup tezi bozulduğunda pozisyonu kapatmak üzere önceden yerleştirilen emir), bütçeyi istediğim miktara uydurmak için rastgele daraltılmaz. Önce invalidation’ı belirlerim; sonra stop emrini piyasa yapısı, minimum fiyat adımı, normal volatilite ve olası slippage için uygulanabilir noktaya yerleştiririm. Ana risk Teknik stop Swing, zone, range sınırı veya pattern ekstremi ötesi.

**Konular:** risk_management, strategy_design, volatility, execution_microstructure, candle_behavior

**Kart:** `ATK-TR-D1.0-2026-08.p0266`

### PDF s. 267 — 13.3 — Stop Seçimi: Teknik, Volatilite ve Birleşik

Uygulama Görseli 13.2 – XAGTRYG 4 saatlik demand altında teknik stop, ATR tamponu ve aynı setup için aşırı dar stopun karşılaştırılması.

**Konular:** risk_management, strategy_design, support_resistance, volatility

**Kart:** `ATK-TR-D1.0-2026-08.p0267`

### PDF s. 268 — 13.4 — Pozisyon Büyüklüğü Formülü

13.4 Pozisyon Büyüklüğü Formülü Position sizing (stop gerçekleştiğinde kaybın risk bütçesini aşmaması için alınacak birim miktarını hesaplama), stop seçildikten sonra yapılır. Temel sıra değişmez: hesap özkaynağı → risk oranı → risk tutarı → etkili birim risk → pozisyon büyüklüğü. • Etkili birim risk 1,10 TL’den yaklaşık 1,60 TL’ye çıktı.

**Konular:** risk_management, execution_microstructure, strategy_design, volatility

**Kart:** `ATK-TR-D1.0-2026-08.p0268`

### PDF s. 269 — 13.5 — Position Sizing Modelleri ve Volatilite

13.5 Position Sizing Modelleri ve Volatilite Uyarlaması Şekil 13.4 – Aynı risk bütçesinde stop–pozisyon dengesi Model Uygulama Sınır Fixed fractional Güncel özkaynağın sabit yüzdesi risk edilir. Hesap büyüdükçe miktar artar, drawdown’da doğal olarak azalır. Fixed money risk Belirli dönem boyunca aynı TL tutarı risk edilir.

**Konular:** risk_management, volatility, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0269`

### PDF s. 270 — 13.6 — Hedef, R:R ve İşlem Yapılabilirlik

DOĞRU BİLİNEN YANLIŞ Mit: Kayıptan sonra miktarı büyütmek, önceki kaybı daha hızlı çıkarır. Gerçeklik: Martingale mantığı sermayenin ve işlem kapasitesinin sınırsız olduğunu varsayar. Kayıp serisi uzadığında risk geometrik büyür.

**Konular:** risk_management, trend_regime, execution_microstructure, strategy_design, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0270`

### PDF s. 271 — 13.7 — Win Rate, Başa Baş Oranı ve Expectancy

13.7 Win Rate, Başa Baş Oranı ve Expectancy Win rate (işlemlerin kaçının kazançla kapandığı oran) tek başına strateji kalitesini göstermez. Break- even win rate (maliyet öncesi sıfır beklenti için gereken minimum kazanma oranı), ortalama reward/risk oranıyla birlikte hesaplanır. Expectancy (çok sayıda benzer işlemde işlem başına beklenen ortalama sonuç), gerçek edge’i özetler.

**Konular:** risk_management, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0271`

### PDF s. 272 — 13.9 — Drawdown ve Toparlanma Asimetrisi

DOĞRU BİLİNEN YANLIŞ Mit: %70 win rate, %45 win rate’ten mutlaka daha iyidir. Gerçeklik: Yüksek win rate, küçük kazançlar ve nadir büyük kayıplarla negatif expectancy üretebilir. 13.8 Maliyet Sonrası Gerçek Edge Backtest veya grafik planında görünen brüt R, gerçek işlem sonucu değildir.

**Konular:** risk_management, execution_microstructure, crypto_specific, fundamental_derivatives, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0272`

### PDF s. 273 — 13.10 — Kayıp Serisi ve Risk Azaltma Protokolü

Hesap zirvesinden ne kadar uzakta olduğumu, hangi setup ve piyasa rejiminin kaybı ürettiğini ayrı izlerim. DOĞRU BİLİNEN YANLIŞ Mit: %50 kaybettikten sonra %50 kazanırsam başa baş olurum. Gerçeklik: 100’den 50’ye düşen hesap, tekrar 100’e çıkmak için kalan sermaye üzerinden %100 kazanmalıdır.

**Konular:** risk_management, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0273`

### PDF s. 274 — 13.11 — Portföy Isısı, Korelasyon ve Yoğunlaşma

Durum Önceden yazılacak eylem Yapılmayacak Normal varyans Aynı kurallarla, aynı risk birimiyle devam; işlemleri kaydet. Tek sonuca göre sistemi değiştirmek. Günlük limit doldu Yeni işlem açmayı durdur; açık riski plana göre yönet.

**Konular:** risk_management, strategy_design, trend_regime, portfolio_correlation, psychology_process

**Kart:** `ATK-TR-D1.0-2026-08.p0274`

### PDF s. 275 — 13.11 — Portföy Isısı, Korelasyon ve Yoğunlaşma

XAGTRYG, XAU ve metal madencisi long 1,5R Aynı metal/USD teması nedeniyle tek kümede yoğunlaşabilir. Aynı endeks içindeki üç yüksek beta hisse 1,5R Piyasa düşüşünde birlikte hareket etme riski yüksektir. Long ve karşı hedge Brüt risk iki pozisyon Net risk hedge oranı, basis ve maliyete bağlıdır; sıfır değildir.

**Konular:** risk_management, relative_cross_market, fundamental_derivatives, hedge_arbitrage, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0275`

### PDF s. 276 — 13.13 — Kaldıraç, Marjin ve Likidasyon

13.12 Stop, Hedge ve Çeşitlendirme Hedge (ana pozisyona zıt veya dengeleyici risk alarak geçici kaybı azaltma), stopun eş anlamlısı değildir. Stop tezi sonlandırır; hedge ana pozisyonu açık tutarken ek maliyet ve yeni bir yönetim kararı yaratır. Diversification (farklı risk sürücülerine dağılım) ise tek olaya bağımlılığı azaltmayı amaçlar.

**Konular:** fundamental_derivatives, risk_management, hedge_arbitrage, market_basics, portfolio_correlation

**Kart:** `ATK-TR-D1.0-2026-08.p0276`

### PDF s. 277 — 13.14 — Options Primi ve Arbitraj Operasyon

Likidasyon fiyatını stop yerine kullanmam. DOĞRU BİLİNEN YANLIŞ Mit: 5x leverage kullanmak otomatik olarak hesabın %5’ini riske atar. Gerçeklik: Gerçek risk; pozisyon büyüklüğü, stop mesafesi, marjin yapısı, maliyet ve gap/slippage ile belirlenir.

**Konular:** risk_management, derivatives_options, market_basics, fundamental_derivatives, crypto_specific

**Kart:** `ATK-TR-D1.0-2026-08.p0277`

### PDF s. 278 — 13.15 — Tam Sermaye Koruma İş Akışı

Yöntem Başlangıç risk bütçesi Görünmeyen risk Opsiyon satışı Alınan prim risk değildir; olası yükümlülük ayrıca hesaplanır. Bazı pozisyonlarda çok büyük veya asimetrik kayıp. Borsalar arası arbitraj İki taraftaki pozisyon ve işlem/transfer maliyeti.

**Konular:** risk_management, execution_microstructure, fundamental_derivatives, derivatives_options, hedge_arbitrage

**Kart:** `ATK-TR-D1.0-2026-08.p0278`

### PDF s. 279 — 13.15 — Tam Sermaye Koruma İş Akışı

VAKA ANALİZİ — XAGTRYG TAM RİSK KARTI • Temsilî hesap: 100.000 TL; plan risk bütçesi: %0,50 = 500 TL. • Entry 111,20; teknik stop 110,20; tahmini birim maliyet 0,10 TL. • Etkili birim risk 1,10 TL; teorik miktar ≈454 gram; uygulanabilir lota aşağı yuvarlanır.

**Konular:** risk_management, strategy_design, market_basics, volatility

**Kart:** `ATK-TR-D1.0-2026-08.p0279`

### PDF s. 280 — 13.15 — Tam Sermaye Koruma İş Akışı

Soru Kısa cevap R:R tek başına edge midir? Hayır; win rate, ortalama sonuç ve maliyetle birlikte expectancy gerekir. Kayıp büyüdükçe başa başa dönmek için gereken getiri hızla artar.

**Konular:** risk_management, portfolio_correlation, fundamental_derivatives, hedge_arbitrage, relative_cross_market

**Kart:** `ATK-TR-D1.0-2026-08.p0280`

### PDF s. 281 — 13.15 — Tam Sermaye Koruma İş Akışı

Terim Aksiyon tanımı Premium Opsiyon sözleşmesini almak için ödenen veya satarken alınan bedel. Slippage Emrin planlanan fiyattan farklı gerçekleşmesi. Belirsizlik ile ölçülebilir risk arasındaki fark nedir?

**Konular:** risk_management, fundamental_derivatives, market_basics, volatility, crypto_specific

**Kart:** `ATK-TR-D1.0-2026-08.p0281`
