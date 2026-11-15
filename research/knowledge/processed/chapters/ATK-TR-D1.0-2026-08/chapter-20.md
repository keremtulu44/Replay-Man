# ATK-TR-D1.0-2026-08 — Bölüm 20

**PDF sayfaları:** 419–438
**Sayfa kartları:** 20

## Alt başlıklar

- 20.1 — Tahvil Piyasası Neden İzlenir?
- 20.2 — Tahvil Sözleşmesi: Issuer, Principal,
- 20.3 — Devlet ve Şirket Tahvilleri: Yield Riskin
- 20.4 — Coupon Rate, Current Yield ve Yield to
- 20.6 — Faiz Değişimi, Maturity ve Duration
- 20.7 — Kısa ve Uzun Vadeli Getiriler
- 20.8 — Yield Curve: Seviye, Eğim ve Değişim
- 20.9 — Nominal Yield, Inflation ve Real Yield
- 20.11 — Faizlerin Hisse Senetlerine Aktarım
- 20.12 — Döviz, Altın, Gümüş ve Kripto Bağlantısı
- 20.13 — Çapraz Varlık Vaka Analizleri ve
- 20.14 — Correlation, Diversification ve Rejim
- 20.15 — Tam Intermarket İzleme İş Akışı

## Konu dağılımı

- `macro_rates`: 18 sayfa
- `relative_cross_market`: 17 sayfa
- `risk_management`: 10 sayfa
- `execution_microstructure`: 10 sayfa
- `support_resistance`: 6 sayfa
- `market_basics`: 6 sayfa
- `fundamental_derivatives`: 5 sayfa
- `trend_regime`: 4 sayfa
- `liquidity_imbalance`: 2 sayfa
- `market_structure`: 2 sayfa
- `strategy_design`: 2 sayfa
- `crypto_specific`: 1 sayfa

## Sayfa şeritleri

### PDF s. 419 — Bölüm girişi/devamı

BÖLÜM 20 Tahviller, Faizler ve Piyasalar Arası İlişkiler Tahvil nakit akışından faiz rejimi ve çapraz varlık karar sistemine

**Konular:** macro_rates, relative_cross_market

**Kart:** `ATK-TR-D1.0-2026-08.p0419`

### PDF s. 420 — 20.1 — Tahvil Piyasası Neden İzlenir?

Bu Bölümün Amacı Tahvil piyasasını öğrenmek yalnız tahvil almak isteyen yatırımcılar için gerekli değildir. Yield; finansman maliyetini, gelecekteki nakit akışlarının bugünkü değerini, para birimleri arasındaki getiri farkını ve riskli varlıkların fırsat maliyetini etkileyen ana değişkenlerden biridir. Bununla birlikte “yield yükseldi, şu varlık düşer” şeklindeki otomatik kurallar güvenilir değildir.

**Konular:** macro_rates, relative_cross_market, risk_management, fundamental_derivatives, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0420`

### PDF s. 421 — 20.2 — Tahvil Sözleşmesi: Issuer, Principal,

Issuer (ihraççı), parayı kullanan devlet, şirket veya başka kurumdur. Principal ya da face value (anapara/nominal değer), sözleşmenin vade sonunda geri ödemeyi vaat ettiği tutardır. Coupon (kupon), sözleşmeye göre yapılan faiz ödemesidir.

**Konular:** macro_rates, relative_cross_market, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0421`

### PDF s. 422 — 20.3 — Devlet ve Şirket Tahvilleri: Yield Riskin

Yatırımcı tahvili 1.000 yerine 900’e alırsa sözleşme couponu 40 olarak kalır; fakat 40/900 current yield’i yaklaşık %4,44’e çıkarır. 20.3 Devlet ve Şirket Tahvilleri: Yield Riskin Fiyatıdır Devlet tahvili ile şirket tahvili aynı nakit akışı diliyle fiyatlanır; fakat taşıdıkları riskler farklıdır. Bir devlet kendi para biriminde borçlanıyor olabilir, başka para biriminde borçlanabilir veya politik ve inflation riski taşıyabilir.

**Konular:** macro_rates, risk_management, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0422`

### PDF s. 423 — 20.4 — Coupon Rate, Current Yield ve Yield to

Risk Devlet tahvilinde Şirket tahvilinde Duration Uzun vadeli devlet tahvilleri faiz şokuna hassas olabilir. Maturity ve coupon yanında credit spread de hareket eder. Liquidity Derinlik ülke ve vadeye göre değişir.

**Konular:** execution_microstructure, macro_rates, risk_management, fundamental_derivatives, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0423`

### PDF s. 424 — 20.6 — Faiz Değişimi, Maturity ve Duration

20.5 Bond Price–Yield Ters İlişkisi Mevcut sabit couponlu bir tahvilin cash flow’ları değişmeden market price’ı düşerse, yeni alıcı aynı ödemeleri daha düşük fiyatla elde eder; yield yükselir. Price yükselirse aynı ödemeler için daha fazla para ödenir; yield düşer. Ters ilişki bu sabit cash flow mantığından doğar.

**Konular:** macro_rates, relative_cross_market

**Kart:** `ATK-TR-D1.0-2026-08.p0424`

### PDF s. 425 — 20.6 — Faiz Değişimi, Maturity ve Duration

açıklandığı anda tahvilin mutlaka düşmesi gerekmez; karar önceden fiyatlanmış veya beklenenden daha yumuşak algılanmış olabilir. Duration (faiz duyarlılığı süresi), tahvil cash flow’larının zamanlamasını tek ölçüde özetleyerek yield değişimine karşı yaklaşık price hassasiyetini anlatır. Maturity uzadıkça duration çoğu sabit couponlu tahvilde artma eğilimindedir; ancak coupon oranı ve ödeme yapısı da önemlidir.

**Konular:** macro_rates, relative_cross_market, execution_microstructure

**Kart:** `ATK-TR-D1.0-2026-08.p0425`

### PDF s. 426 — 20.7 — Kısa ve Uzun Vadeli Getiriler

Uygulama Görseli 20.1 – Aynı gün 2 yıllık ve 20/30 yıllık bond ETF veya tahvil price hareketlerini yan yana gösteren gerçek grafik; faiz şoku, yüzdesel price tepkisi ve tarih işaretlenecek.. 20.7 Kısa ve Uzun Vadeli Getiriler Kısa vadeli yield’ler merkez bankasının yakın dönem policy yoluna ve para piyasası beklentilerine daha duyarlıdır. Uzun vadeli yield’ler ise beklenen kısa oranların bileşimi yanında long-term growth, inflation ve term premium gibi daha uzun ufuklu değişkenleri taşır.

**Konular:** fundamental_derivatives, macro_rates, market_basics, relative_cross_market, execution_microstructure

**Kart:** `ATK-TR-D1.0-2026-08.p0426`

### PDF s. 427 — 20.8 — Yield Curve: Seviye, Eğim ve Değişim

20.8 Yield Curve: Seviye, Eğim ve Değişim Yield curve (getiri eğrisi), aynı issuer’ın farklı vadelerdeki yield’lerini birlikte gösterir. Yalnız curve’ün “normal” veya “inverted” olduğunu yazmak yetersizdir. Üç ayrı bilgi kaydederim: genel seviye, kısa– uzun vade arasındaki eğim ve bu eğimin hangi uçtan değiştiği.

**Konular:** market_basics, macro_rates, relative_cross_market, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0427`

### PDF s. 428 — 20.9 — Nominal Yield, Inflation ve Real Yield

Uygulama Görseli 20.2 – 2Y ve 10Y yield çizgileri ile 10Y 2Y spread paneli; inversion, re-steepening, equity− trend ve tarih işaretleri birlikte gösterilecek.. 20.9 Nominal Yield, Inflation ve Real Yield Nominal yield, ekranda görülen sözleşme veya piyasa getirisidir. Investorın satın alma gücü açısından asıl soru, bu getirinin inflation sonrasında ne bıraktığıdır.

**Konular:** execution_microstructure, macro_rates, relative_cross_market, risk_management, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0428`

### PDF s. 429 — 20.11 — Faizlerin Hisse Senetlerine Aktarım

DOĞRU BİLİNEN YANLIŞ “Yüksek nominal yield kesin olarak değerli metalleri düşürür.” Değerli metal için real yield, USD, inflation, risk, physical demand ve positioning birlikte değerlendirilir. 20.10 Credit Spread, Default, Liquidity ve Currency Riski Corporate bond veya riskli sovereign bond incelerken government benchmark üzerindeki ek yield’e credit spread denir. Spread genişlemesi, piyasanın default veya liquidity için daha fazla tazminat istediğini gösterebilir.

**Konular:** execution_microstructure, market_basics, macro_rates, risk_management, relative_cross_market

**Kart:** `ATK-TR-D1.0-2026-08.p0429`

### PDF s. 430 — 20.11 — Faizlerin Hisse Senetlerine Aktarım

Buna rağmen yüksek yield bütün hisseleri aynı şekilde etkilemez. Yield güçlü nominal growth nedeniyle yükseliyorsa şirket earnings’i de güçlenebilir. Finansal şirketlerde curve ve credit quality; growth hisselerinde uzun durationlı earnings; borçlu şirketlerde refinancing takvimi farklı sonuç üretir.

**Konular:** macro_rates, relative_cross_market, crypto_specific

**Kart:** `ATK-TR-D1.0-2026-08.p0430`

### PDF s. 431 — 20.12 — Döviz, Altın, Gümüş ve Kripto Bağlantısı

Uygulama Görseli 20.3 – 10Y yield, NASDAQ/growth endeksi ve banka endeksi aynı tarih aralığında; yield hareketinin kaynağı ve earnings dönemleri işaretlenecek.. 20.12 Döviz, Altın, Gümüş ve Kripto Bağlantısı Dövizde önemli kanal iki para birimi arasındaki beklenen faiz farkıdır. Ancak yüksek yield tek başına currency talebi garantilemez; inflation, fiscal risk, current account, güvenli liman talebi ve piyasanın daha önce ne fiyatladığı sonucu değiştirebilir.

**Konular:** risk_management, support_resistance, relative_cross_market, macro_rates, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0431`

### PDF s. 432 — 20.13 — Çapraz Varlık Vaka Analizleri ve

• Nominal yield mi, real yield mi değişiyor? • DXY veya ilgili currency aynı yönde mi? • Riskli varlıkların tamamı mı etkileniyor, yalnız belirli sektör mü?

**Konular:** market_structure, macro_rates, relative_cross_market, risk_management, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0432`

### PDF s. 433 — 20.14 — Correlation, Diversification ve Rejim

VAKA 2 — LONG YIELD YÜKSELİYOR, HİSSE DE YÜKSELİYOR • Yield hareketi yüksek inflation yerine güçlü growth ve earnings beklentisinden geliyor olabilir. • Equity breadth ve earnings revision iyiyse “yield yükseldi = short” kuralı çalışmayabilir. • Long end yükselirken credit spread daralıyorsa risk stresi hipotezi zayıflar.

**Konular:** macro_rates, market_basics, risk_management, execution_microstructure, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0433`

### PDF s. 434 — 20.15 — Tam Intermarket İzleme İş Akışı

Kontrol Sorulacak soru Hata önleme Lookback 20 gün mü, 1 yıl mı? Farklı karar ufuklarını karıştırma. Regime Inflation, growth, crisis veya easing dönemi mi?

**Konular:** market_basics, relative_cross_market, execution_microstructure, fundamental_derivatives, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0434`

### PDF s. 435 — 20.15 — Tam Intermarket İzleme İş Akışı

Nedeni adaylaştır: Policy, growth, inflation, term premium, supply, credit veya safety demand. Çapraz teyit ara: FX, equity breadth, credit spread, gold/silver, crypto ve volatility ne yapıyor? İşlem varlığını ayır: Makro hipotez, kendi grafiğinin structure ve zone’unu destekliyor mu?

**Konular:** strategy_design, execution_microstructure, relative_cross_market, support_resistance, market_structure

**Kart:** `ATK-TR-D1.0-2026-08.p0435`

### PDF s. 436 — 20.15 — Tam Intermarket İzleme İş Akışı

Hızlı Başvuru: Tahvil ve Faiz Okuma Tablosu Gözlem İlk hipotez Kontrol edilmeden karar verilmez Bond price düşüyor, yield yükseliyor Piyasa daha yüksek getiri talep ediyor. Maturity, duration, policy, inflation, credit. 2Y hızlı yükseliyor Yakın policy yolu daha sıkı fiyatlanıyor olabilir.

**Konular:** relative_cross_market, macro_rates, execution_microstructure, support_resistance, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0436`

### PDF s. 437 — 20.15 — Tam Intermarket İzleme İş Akışı

Terim Kısa anlam Duration Yield değişimine karşı yaklaşık fiyat duyarlılığı ölçüsü. Yield curve Aynı issuer’ın farklı vadelerdeki yield yapısı. Term premium Uzun vadeli belirsizlik için talep edilen ek getiri bileşeni.

**Konular:** macro_rates, execution_microstructure, fundamental_derivatives, relative_cross_market, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0437`

### PDF s. 438 — 20.15 — Tam Intermarket İzleme İş Akışı

Gold ve silver için yield dışında hangi sürücüler izlenir? Crypto faiz ve liquidity rejimine hangi kanallardan tepki verebilir? XAGTRYG’de XAGUSD ile USDTRY neden ayrı okunur?

**Konular:** macro_rates, relative_cross_market, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0438`
