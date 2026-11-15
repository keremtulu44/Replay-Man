# ATK-TR-D1.0-2026-08 — Bölüm 19

**PDF sayfaları:** 395–418
**Sayfa kartları:** 24

## Alt başlıklar

- 19.1 — Kripto İşlemini Katmanlarına Ayırmak
- 19.3 — Bitcoin, Ethereum, Coin, Token ve
- 19.4 — Tokenomics, Supply, Market Cap ve FDV
- 19.5 — Trading Pair: Base, Quote ve Fiyat
- 19.6 — CEX, DEX, Broker ve Analiz Platformu
- 19.7 — Hesap, KYC, Yetki ve Borsa Seçimi
- 19.8 — Fonlama, Deposit–Withdrawal ve Network
- 19.9 — Wallet, Custody, Private Key ve Seed
- 19.10 — Hesap ve Cüzdan Güvenlik Protokolü
- 19.11 — Spot Trading: Varlık, Bakiye ve Emir
- 19.12 — Futures, Perpetual, Margin ve Funding
- 19.13 — Leverage, Liquidation ve Stop İlişkisi
- 19.14 — Kriptoda Emir, Likidite, Volatilite ve Feed
- 19.15 — Tam Kripto İşlem ve Operasyon İş Akışı

## Konu dağılımı

- `market_basics`: 24 sayfa
- `fundamental_derivatives`: 24 sayfa
- `risk_management`: 14 sayfa
- `support_resistance`: 10 sayfa
- `strategy_design`: 4 sayfa
- `liquidity_imbalance`: 3 sayfa
- `volume_flow`: 2 sayfa
- `relative_cross_market`: 2 sayfa
- `automation_ai`: 2 sayfa
- `patterns`: 1 sayfa
- `pullback`: 1 sayfa

## Sayfa şeritleri

### PDF s. 395 — Bölüm girişi/devamı

BÖLÜM 19 Kripto Piyasaları, Borsalar, Cüzdanlar ve Kaldıraç Ağ ve varlık mantığından güvenli emir, custody ve kaldıraç yönetimine

**Konular:** market_basics, fundamental_derivatives

**Kart:** `ATK-TR-D1.0-2026-08.p0395`

### PDF s. 396 — 19.1 — Kripto İşlemini Katmanlarına Ayırmak

Bu Bölümün Amacı Kripto grafiği diğer finansal grafikler gibi fiyat, hacim ve yapı üretir; fakat işlemin operasyon katmanı belirgin biçimde farklıdır. Aynı BTC etiketi bir borsada spot varlık, başka bir panelde perpetual futures sözleşmesi, bir wallet’ta on-chain bakiye veya bir ETF içinde dolaylı maruz kalma anlamına gelebilir. Bu bölümün amacı blockchain mühendisliği öğretmek veya coin tavsiyesi vermek değildir.

**Konular:** fundamental_derivatives, market_basics, risk_management, support_resistance, volume_flow

**Kart:** `ATK-TR-D1.0-2026-08.p0396`

### PDF s. 397 — 19.1 — Kripto İşlemini Katmanlarına Ayırmak

DOĞRU BİLİNEN YANLIŞ Mit: BTC grafiği her platformda aynı ürünü ve aynı fiyatı gösterir. Gerçeklik: Exchange feed, quote asset, spot/futures sözleşmesi ve likidite yapısı fiyatı ve uygulamayı değiştirebilir.

**Konular:** fundamental_derivatives, market_basics, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0397`

### PDF s. 398 — 19.3 — Bitcoin, Ethereum, Coin, Token ve

19.2 Blockchain, Ağ ve Merkeziyetsizlik Derecesi Blockchain (işlemleri sıralı kayıt yapısında tutan ve network katılımcıları tarafından doğrulanan dijital ledger), kripto varlığın hangi kayıt ve transfer ortamında yaşadığını açıklar. Cryptography (bilgiyi ve yetkiyi matematiksel anahtarlarla doğrulama) kayıt güvenliğinin parçalarından biridir; fakat kullanıcı hatasını veya kötü platform seçimini otomatik olarak geri almaz. Kavram Aksiyon tanımı İşlem açısından soru Ledger / blockchain İşlemlerin hangi kayıt sistemi üzerinde tutulduğunu doğrulamak.

**Konular:** fundamental_derivatives, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0398`

### PDF s. 399 — 19.3 — Bitcoin, Ethereum, Coin, Token ve

Kategori Temel görev / anlatı Araştırma sorusu Bitcoin / payment-type coin Transfer, kıtlık ve store-of-value kullanımı. Arz kuralı, network güvenliği, likidite ve custody nasıl? Smart-contract platform Uygulama, token, işlem ücreti ve network activity.

**Konular:** fundamental_derivatives, liquidity_imbalance, support_resistance, market_basics, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0399`

### PDF s. 400 — 19.4 — Tokenomics, Supply, Market Cap ve FDV

19.4 Tokenomics, Supply, Market Cap ve FDV Tokenomics (bir coin veya token’ın arz, dağıtım, kullanım ve teşvik kurallarını inceleme), “birim fiyat ucuz mu?” sorusundan önce gelir. Market cap yaklaşık olarak price × circulating supply; FDV ise fiyatın belirtilen maksimum veya fully diluted supply ile çarpımını kullanır.

**Konular:** support_resistance, fundamental_derivatives, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0400`

### PDF s. 401 — 19.5 — Trading Pair: Base, Quote ve Fiyat

Ana risk Circulating supply Piyasada dolaşımda olduğu bildirilen miktar. Veri tanımı ve kilitli/bridge varlık farkı. Max / total supply Protokol veya kaynakta belirtilen toplam sınır.

**Konular:** support_resistance, fundamental_derivatives, liquidity_imbalance, market_basics, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0401`

### PDF s. 402 — 19.6 — CEX, DEX, Broker ve Analiz Platformu

• Spot/futures etiketi ve sözleşme tipi. • Tick size, quantity step ve minimum notional. • Pair’in 24 saatlik hacmi, spread’i ve order-book depth’i.

**Konular:** market_basics, fundamental_derivatives

**Kart:** `ATK-TR-D1.0-2026-08.p0402`

### PDF s. 403 — 19.6 — CEX, DEX, Broker ve Analiz Platformu

Araç Ana görev Başlıca kontrol Wallet Private key/seed veya platform yetkisiyle varlık erişimini yönetmek. Custody modeli, backup ve doğru network. TradingView / chart platform Feed, chart, indicator, alert ve analysis.

**Konular:** fundamental_derivatives, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0403`

### PDF s. 404 — 19.7 — Hesap, KYC, Yetki ve Borsa Seçimi

19.7 Hesap, KYC, Yetki ve Borsa Seçimi KYC / Know Your Customer (platformun kimlik ve uygunluk doğrulaması yapması), borsanın ürün ve çekim yetkileriyle bağlantılı olabilir. Doğrulama süresi, belge türü ve erişilebilir ürünler ülke ve platforma göre değişebileceği için tek bir platform ekranı evrensel kural olarak kabul edilmemelidir.

**Konular:** market_basics, fundamental_derivatives

**Kart:** `ATK-TR-D1.0-2026-08.p0404`

### PDF s. 405 — 19.8 — Fonlama, Deposit–Withdrawal ve Network

Borsa seçim alanı Soracağım soru Kırmızı bayrak Yetki / jurisdiction Platform benim ülkemde hangi hizmetleri sunuyor? Ürün erişimi ve çekim koşulları belirsiz. KYC ve privacy Hangi veri isteniyor, kim saklıyor, erişim nasıl korunuyor?

**Konular:** market_basics, volume_flow, fundamental_derivatives, patterns, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0405`

### PDF s. 406 — 19.8 — Fonlama, Deposit–Withdrawal ve Network

Adım Kontrol Neden Memo / tag Platform istiyorsa doğru ek alan. Bazı ortak adres sistemlerinde hesaba yönlendirme için gerekir. Fee / minimum Network fee, platform fee ve minimum withdrawal.

**Konular:** fundamental_derivatives, market_basics, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0406`

### PDF s. 407 — 19.9 — Wallet, Custody, Private Key ve Seed

19.9 Wallet, Custody, Private Key ve Seed Phrase Wallet (blockchain üzerindeki adres ve anahtarlarla etkileşimi yöneten araç), coin’leri fiziksel dosya gibi içine koymaz; erişim ve işlem imzalama yetkisini yönetir. Custody sorusu “Bakiyeyi nerede görüyorum?” değil, “İşlem yetkisini sağlayan anahtar veya hesap kontrolü kimde?” sorusudur.

**Konular:** fundamental_derivatives, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0407`

### PDF s. 408 — 19.10 — Hesap ve Cüzdan Güvenlik Protokolü

Avantaj / sorumluluk Exchange custody Platform account ve iç kontrol sistemi. Kolay execution; counterparty, withdrawal ve account riskini kabul etmek. Hot self-custody wallet Private key/seed kullanıcıda, internet bağlı cihazda.

**Konular:** fundamental_derivatives, market_basics, risk_management, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0408`

### PDF s. 409 — 19.11 — Spot Trading: Varlık, Bakiye ve Emir

Gerçeklik: 2FA önemli bir katmandır; phishing, email compromise, kötü API key, SIM saldırısı veya yanlış wallet imzası gibi diğer riskleri tek başına kapatmaz. VAKA ANALİZİ — “DESTEK GÖREVLİSİ” SEED İSTİYOR Bir mesaj, hesabımdaki sorunu çözmek için seed phrase veya screen-share istiyor. İşlemi durdurur, mesajdaki linki kullanmadan resmi uygulamaya girer ve resmi support kanalını kendim açarım.

**Konular:** market_basics, fundamental_derivatives, relative_cross_market, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0409`

### PDF s. 410 — 19.12 — Futures, Perpetual, Margin ve Funding

VAKA ANALİZİ — MARKET ORDER SLIPPAGE Temsili altcoin’de ekranda son fiyat 1,00 USDT; fakat ask tarafı ince ve 10.000 USDT’lik market buy farklı kademeleri tüketiyor. Teknik stop mesafem ve R:R emrin ardından bozuluyor. Emirden önce depth ve tahmini slippage kontrolü yaparım.

**Konular:** market_basics, risk_management, fundamental_derivatives

**Kart:** `ATK-TR-D1.0-2026-08.p0410`

### PDF s. 411 — 19.13 — Leverage, Liquidation ve Stop İlişkisi

19.13 Leverage, Liquidation ve Stop İlişkisi Leverage, yön tahminini iyileştirmez; aynı sermaye ile daha büyük notional exposure oluşturur. Pozisyon büyüdükçe aynı fiyat hareketinin para etkisi artar ve borsanın teminatı korumak için hesapladığı liquidation seviyesi yaklaşabilir.

**Konular:** risk_management, fundamental_derivatives, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0411`

### PDF s. 412 — 19.14 — Kriptoda Emir, Likidite, Volatilite ve Feed

Sıra Yapılacak Yanlış sıra 1 Teknik geçersizlik Setup’ın bozulduğu fiyatı grafikten belirlemek. Önce leverage seçip stopu ona uydurmak. 2 Risk bütçesi Bölüm 13’e göre kabul edilen para kaybını belirlemek.

**Konular:** risk_management, strategy_design, market_basics, automation_ai, fundamental_derivatives

**Kart:** `ATK-TR-D1.0-2026-08.p0412`

### PDF s. 413 — 19.15 — Tam Kripto İşlem ve Operasyon İş Akışı

Konu Kriptoya özgü kontrol Eylem Exchange feed Aynı pair farklı venue’de farklı wick/hacim üretebilir. Ana execution venue feed’ini referans al. Spot–futures basis Sözleşme spot fiyattan ayrışabilir.

**Konular:** fundamental_derivatives, strategy_design, market_basics, risk_management, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0413`

### PDF s. 414 — 19.15 — Tam Kripto İşlem ve Operasyon İş Akışı

Fon USDT spot wallet’ta; withdrawal gerekmiyor. Network riski yok, custody riski var. Setup Üst TF trend, orta TF pullback; kapanış trigger bekleniyor.

**Konular:** risk_management, strategy_design, fundamental_derivatives, market_basics, pullback

**Kart:** `ATK-TR-D1.0-2026-08.p0414`

### PDF s. 415 — 19.15 — Tam Kripto İşlem ve Operasyon İş Akışı

Hızlı Başvuru Gördüğüm İlk kontrol Varsayılan eylem BTCUSDT symbol Exchange, spot/futures ve quote asset Kimliği doğrulamadan analiz yok. 0,01 fiyatlı token Supply, market cap, FDV ve liquidity “Ucuz” etiketi kullanma. Stablecoin bakiye Peg, issuer/backing, venue ve withdrawal Risksiz nakit sayma.

**Konular:** fundamental_derivatives, market_basics, risk_management, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0415`

### PDF s. 416 — 19.15 — Tam Kripto İşlem ve Operasyon İş Akışı

Gördüğüm İlk kontrol Varsayılan eylem Deposit adresi Varlık, network, address, memo ve fee Küçük test transferi. Exchange wallet Custody ve withdrawal yetkisi Uzun vadeli ve trading bakiyesini ayır. Futures paneli Contract, margin, funding ve mark price Spot sahipliği gibi davranma.

**Konular:** fundamental_derivatives, market_basics, risk_management, automation_ai, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0416`

### PDF s. 417 — 19.15 — Tam Kripto İşlem ve Operasyon İş Akışı

Terim Aksiyon tanımı Market cap Price × circulating supply ile yaklaşık mevcut piyasa değerini görmek. FDV Price × fully diluted supply ile gelecekteki arz varsayımını görmek. Trading pair Base asset’in quote asset cinsinden fiyatını okumak.

**Konular:** support_resistance, market_basics, fundamental_derivatives, relative_cross_market, risk_management

**Kart:** `ATK-TR-D1.0-2026-08.p0417`

### PDF s. 418 — 19.15 — Tam Kripto İşlem ve Operasyon İş Akışı

Düşük birim fiyat neden ucuzluk kanıtı değildir? BTC/USDT pair’inde base ve quote hangileridir? ETH/BTC yükselirken hangi relatif güç değişimi gerçekleşir?

**Konular:** fundamental_derivatives, risk_management, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0418`
