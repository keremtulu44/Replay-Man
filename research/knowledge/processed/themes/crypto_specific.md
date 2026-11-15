# crypto_specific

**Kapsam:** 62 sayfa eşleşmesi

## Proje yorumu (`inference`)

Kripto piyasasının kesintisiz seans, funding, saklama ve likidasyon özellikleri ayrı bağlam gerektirir.

## Nasıl kullanılabilir?

Kriptoya özgü veri, saklama ve piyasa yapısı farkları

## Kaynak şeritleri

### 1. ATK-TR-D1.0-2026-08 — PDF s. 398

> ANA TRADING KİTABI | BÖLÜM 19 Kripto Piyasaları, Borsalar, Cüzdanlar ve Kaldıraç • 383 19.2 Blockchain, Ağ ve Merkeziyetsizlik Derecesi Blockchain (işlemleri sıralı kayıt yapısında tutan ve network katılımcıları tarafından doğrulanan dijital ledger), kripto varlığın hangi kayıt ve transfer ortamında yaşadığını açıklar. Cryptography (bilgiyi ve yetkiyi matematiksel anahtarlarla doğrulama) kayıt güvenliğinin parçalarından biridir; fakat kullanıcı hatasını veya kötü platform seçimini otomatik olarak geri almaz. Kavram Aksiyon tanımı İşlem açısından soru Ledger / blockchain İşlemlerin hangi kayıt sistemi üzerinde tutulduğunu doğrulamak. Transfer on-chain mi, yalnız borsa içi bakiye hareketi mi? Node / validator Network kurallarını doğrulayan katılımcı yapısını anlamak. Kontrol az sayıda katılımcıda yoğunlaşıyor mu? Decentralization Kontrol, doğrulama ve yönetim gücünün ne kadar dağıldığını incelemek. “Merkeziyetsiz” etiketi hangi ölçüte dayanıyor? Confirmation / finality Transferin kabul edilmesi için gereken ağ onaylarını izlemek. Borsa kaç confirmation sonrası bakiyeyi açıyor? Network fee On-chain işlemi gerçekleştirme maliyetini kontrol etmek. Tutar için fee orantısız mı; ağ yoğun mu? Tablo 19.2 – Ağ katmanı kontrolü EKRANDA NE ARIYORUM? • Deposit veya withdrawal ekranında seçilen network adı. • Minimum çekim, network fee ve beklenen confirmation bilgisi. • Token’ın farklı ağlarda aynı ticker ile sunulup sunulmadığı. • Transfer geçmişinde transaction ID / hash ve durum. • Borsa içi transfer ile on-chain transferin ayrı seçenek olup olmadığı. …

**Bölüm/alt başlık:** 19 / 19.3 — Bitcoin, Ethereum, Coin, Token ve

**Kaynak özeti (`source`):** 19.2 Blockchain, Ağ ve Merkeziyetsizlik Derecesi Blockchain (işlemleri sıralı kayıt yapısında tutan ve network katılımcıları tarafından doğrulanan dijital ledger), kripto varlığın hangi kayıt ve transfer ortamında yaşadığını açıklar. Cryptography (bilgiyi ve yetkiyi matematiksel anahtarlarla doğrulama) kayıt güvenliğinin parçalarından biridir; fakat kullanıcı hatasını veya kötü platform seçimini otomatik olarak geri almaz. Kavram Aksiyon tanımı İşlem açısından soru Ledger / blockchain İşlemlerin hangi kayıt sistemi üzerinde tutulduğunu doğrulamak.

### 2. ATK-TR-D1.0-2026-08 — PDF s. 396

> ANA TRADING KİTABI | BÖLÜM 19 Kripto Piyasaları, Borsalar, Cüzdanlar ve Kaldıraç • 381 Bu Bölümün Amacı Kripto grafiği diğer finansal grafikler gibi fiyat, hacim ve yapı üretir; fakat işlemin operasyon katmanı belirgin biçimde farklıdır. Aynı BTC etiketi bir borsada spot varlık, başka bir panelde perpetual futures sözleşmesi, bir wallet’ta on-chain bakiye veya bir ETF içinde dolaylı maruz kalma anlamına gelebilir. Bu bölümün amacı blockchain mühendisliği öğretmek veya coin tavsiyesi vermek değildir. Hangi varlığı, hangi pair ile, hangi venue ve ürün üzerinde işlem yaptığınızı doğrulayacak; fonlama, custody, emir, kaldıraç ve güvenlik adımlarını tek çalışma akışına bağlayacaksınız. BÖLÜM SONUNDA • Ağ, varlık, pair, venue ve ürün katmanlarını birbirinden ayırabileceksiniz. • Bitcoin, Ethereum, coin, token, altcoin ve stablecoin rollerini karşılaştırabileceksiniz. • Supply, market cap ve FDV verilerini birim fiyat yanılgısına düşmeden okuyabileceksiniz. • BTC/USDT gibi pair’lerde base ve quote görevini açıklayabileceksiniz. • CEX, DEX, TradingView ve wallet görevlerini ayırabileceksiniz. • KYC, deposit, withdrawal, network ve custody kontrollerini uygulayabileceksiniz. • Spot ile futures/perpetual ürünleri ve liquidation riskini ayırabileceksiniz. • Market, limit ve stop emirlerinde spread, depth ve slippage etkisini kontrol edebileceksiniz. • Kripto işlemini teknik analiz kadar operasyon güvenliğiyle de kaydedebileceksiniz. 19.1 Kripto İşlemini Katmanlarına Ayırmak Crypto trade’i tek bir “coin alım satımı” olarak görmem. …

**Bölüm/alt başlık:** 19 / 19.1 — Kripto İşlemini Katmanlarına Ayırmak

**Kaynak özeti (`source`):** Bu Bölümün Amacı Kripto grafiği diğer finansal grafikler gibi fiyat, hacim ve yapı üretir; fakat işlemin operasyon katmanı belirgin biçimde farklıdır. Aynı BTC etiketi bir borsada spot varlık, başka bir panelde perpetual futures sözleşmesi, bir wallet’ta on-chain bakiye veya bir ETF içinde dolaylı maruz kalma anlamına gelebilir. Bu bölümün amacı blockchain mühendisliği öğretmek veya coin tavsiyesi vermek değildir.

### 3. ATK-TR-D1.0-2026-08 — PDF s. 413

> ANA TRADING KİTABI | BÖLÜM 19 Kripto Piyasaları, Borsalar, Cüzdanlar ve Kaldıraç • 398 Konu Kriptoya özgü kontrol Eylem Exchange feed Aynı pair farklı venue’de farklı wick/hacim üretebilir. Ana execution venue feed’ini referans al. Spot–futures basis Sözleşme spot fiyattan ayrışabilir. Basis/funding ve mark price kontrolü yap. News / listing Ani volatility ve trading halt/delisting riski. Event takvimi ve borsa duyurularını izle. Price difference Venue, fee, inventory ve latency farkı. Arbitraj sanmadan net maliyet ve execution kontrol et. Tablo 19.14 – Kripto emir ve piyasa davranışı DOĞRU BİLİNEN YANLIŞ Mit: Kripto 24/7 açık olduğu için işlem fırsatı ve liquidity her zaman aynıdır. Gerçeklik: Katılım, spread, depth, haber etkisi ve borsa operasyonu günün ve haftanın farklı bölümlerinde değişebilir. BORSALAR ARASI FİYAT FARKI Aynı varlık farklı venue’lerde kısa süre farklı fiyatlanabilir. Bu fark; transfer süresi, fee, gas, spread, slippage, order-book depth, veri hatası ve karşı taraf riskinden arındırılmadan kâr değildir. Stratejinin ayrıntısı Bölüm 24’te ele alınacaktır. 19.15 Tam Kripto İşlem ve Operasyon İş Akışı Kripto işlem planını teknik analiz ve operasyon güvenliği olarak iki ayrı kontrol listesine bölmem; ikisini tek zincirde uygularım. Çünkü doğru setup yanlış pair’de, yanlış network’te veya kontrolsüz futures margin’iyle sermayeyi koruyamaz. Aşama Yazılacak kontrol Çıktı 1 Varlık Network, coin/token türü, supply ve temel görev. Varlık kimliği. 2 Pair Base, quote ve relatif fiyat tezi. Doğru symbol/pair. 3 Venue Exchange/DEX, feed, liquidity, fee ve access. …

**Bölüm/alt başlık:** 19 / 19.15 — Tam Kripto İşlem ve Operasyon İş Akışı

**Kaynak özeti (`source`):** Konu Kriptoya özgü kontrol Eylem Exchange feed Aynı pair farklı venue’de farklı wick/hacim üretebilir. Ana execution venue feed’ini referans al. Spot–futures basis Sözleşme spot fiyattan ayrışabilir.

### 4. ATK-TR-D1.0-2026-08 — PDF s. 416

> ANA TRADING KİTABI | BÖLÜM 19 Kripto Piyasaları, Borsalar, Cüzdanlar ve Kaldıraç • 401 Gördüğüm İlk kontrol Varsayılan eylem Deposit adresi Varlık, network, address, memo ve fee Küçük test transferi. Exchange wallet Custody ve withdrawal yetkisi Uzun vadeli ve trading bakiyesini ayır. Futures paneli Contract, margin, funding ve mark price Spot sahipliği gibi davranma. Yüksek leverage Stop, quantity, margin modu ve liquidation Leverage’ı son ayar yap. Market order Spread, depth ve slippage Average fill’i önceden tahmin et. Farklı borsa fiyatı Fee, transfer, latency, liquidity ve veri Net maliyet olmadan arbitraj deme. 24/7 işlem İzleme, alarm, liquidity ve event Her saat işlem zorunlu değil. Tablo 19.18 – Hızlı başvuru Kripto İşlem Kontrol Listesi  Varlık, network ve token contract/kimlik bilgisi doğrulandı.  Pair’in base ve quote asset’i yazıldı.  Exchange/feed ile spot, futures veya perpetual etiketi doğrulandı.  Borsa yetkisi, KYC status, fee ve withdrawal koşulları kontrol edildi.  Account, email, 2FA, session, API ve withdrawal güvenliği gözden geçirildi.  Deposit/withdrawal gerekiyorsa network, address, memo ve test transferi uygulandı.  Custody modeli ve bakiyenin borsada kalma süresi planlandı.  Spot/futures product terms, mark/index/funding alanları okundu.  Teknik stop önce, quantity ve leverage sonra belirlendi.  Liquidation teknik stopun ötesinde ve margin modu bilinçli seçildi.  Order type, trigger source, partial/no-fill ve slippage senaryosu yazıldı.  24/7 izleme sorumluluğu alarm ve stop ile planlandı. …

**Bölüm/alt başlık:** 19 / 19.15 — Tam Kripto İşlem ve Operasyon İş Akışı

**Kaynak özeti (`source`):** Gördüğüm İlk kontrol Varsayılan eylem Deposit adresi Varlık, network, address, memo ve fee Küçük test transferi. Exchange wallet Custody ve withdrawal yetkisi Uzun vadeli ve trading bakiyesini ayır. Futures paneli Contract, margin, funding ve mark price Spot sahipliği gibi davranma.

## Test fikri (`hypothesis`)

Bu konuya ait kaynak varyantları korunur. İlk aşamada sabit eşik seçilmez; geniş sembol evreninde aynı tanımların amaçladığı davranışa katkısı karşılaştırılır.
