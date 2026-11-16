# ATK-TR-D1.0-2026-08 — Bölüm 21

**PDF sayfaları:** 439–456
**Sayfa kartları:** 18

## Alt başlıklar

- 21.1 — Opsiyon ve Hedge’i Aynı Şey Sanmamak
- 21.3 — Long Call: Yükseliş Hakkı ve Sınırları
- 21.4 — Long Put: Düşüş Hakkı ve Sınırları
- 21.5 — ITM, ATM, OTM ve Değer Bileşenleri
- 21.6 — Premium, Expiration ve Theta
- 21.7 — Vade Sonu Başabaş ve Kâr/Zarar Haritası
- 21.8 — Opsiyon İşleminde Risk Bütçesi ve
- 21.10 — Protective Put ile Aşağı Yön Tabanı
- 21.11 — Direct Hedge: Short, Futures ve Ters Ürün
- 21.12 — Hedge Oranı, Basis ve Mismatch Riski
- 21.14 — Hedge Maliyeti, Geçersizlik ve Kapatma
- 21.15 — Tam Portföy Koruma İş Akışı

## Konu dağılımı

- `fundamental_derivatives`: 17 sayfa
- `derivatives_options`: 15 sayfa
- `market_basics`: 15 sayfa
- `hedge_arbitrage`: 14 sayfa
- `portfolio_correlation`: 12 sayfa
- `risk_management`: 6 sayfa
- `execution_microstructure`: 3 sayfa
- `relative_cross_market`: 2 sayfa
- `volatility`: 2 sayfa
- `support_resistance`: 1 sayfa
- `crypto_specific`: 1 sayfa

## Sayfa şeritleri

### PDF s. 439 — Bölüm girişi/devamı

BÖLÜM 21 Opsiyonlar, Hedge ve Portföy Koruma Stratejileri Sözleşme hakkından hedge maliyeti ve çıkış planına

**Konular:** fundamental_derivatives, hedge_arbitrage, portfolio_correlation

**Kart:** `ATK-TR-D1.0-2026-08.p0439`

### PDF s. 440 — Bölüm girişi/devamı

Bu Bölümün Amacı Opsiyonlar, küçük bir premium karşılığında dayanak varlık üzerinde koşullu bir hak satın almaya; hedge ise mevcut bir riskin etkisini başka bir pozisyonla azaltmaya yarar. Bu iki araç aynı değildir: her opsiyon hedge değildir, her hedge de opsiyonla kurulmaz. Bu bölümde önce sözleşmeyi okuyacak, long call ve long put sonuçlarını vade sonu matematiğiyle kuracak, sonra protective put, direct hedge, pozisyon azaltma ve çeşitlendirmeyi aynı risk sorusu üzerinde karşılaştıracağız.

**Konular:** derivatives_options, fundamental_derivatives, hedge_arbitrage, market_basics, portfolio_correlation

**Kart:** `ATK-TR-D1.0-2026-08.p0440`

### PDF s. 441 — 21.1 — Opsiyon ve Hedge’i Aynı Şey Sanmamak

21.1 Opsiyon ve Hedge’i Aynı Şey Sanmamak Option (opsiyon), alıcıya dayanak varlığı belirli strike fiyatından belirli tarihe kadar veya tarihte alma ya da satma hakkı veren; fakat bunu yapma zorunluluğu getirmeyen sözleşmedir. Hedge (ana pozisyona zıt veya dengeleyici maruziyet ekleyerek belirli riski azaltma), bir amaçtır. Long put bir hedge aracı olabilir; aynı put yalnız yön spekülasyonu için de alınabilir.

**Konular:** fundamental_derivatives, derivatives_options, hedge_arbitrage, market_basics, portfolio_correlation

**Kart:** `ATK-TR-D1.0-2026-08.p0441`

### PDF s. 442 — 21.3 — Long Call: Yükseliş Hakkı ve Sınırları

21.2 Opsiyon Sözleşmesinin Anatomisi Bir option işlemi yön seçmeden önce sözleşme okuma işidir. Underlying (option değerinin bağlı olduğu dayanak), contract multiplier (bir kontratın kaç birim dayanağa karşılık geldiği), strike (hakkın kullanılacağı fiyat), expiration (sözleşmenin son geçerlilik tarihi), premium (option kontratının birim fiyatı) ve settlement/deliverable birlikte doğrulanır. Alan Aksiyon sorusu Risk Underlying Hangi hisse, ETF, endeks, futures veya başka ürün?

**Konular:** derivatives_options, market_basics, execution_microstructure, fundamental_derivatives, relative_cross_market

**Kart:** `ATK-TR-D1.0-2026-08.p0442`

### PDF s. 443 — 21.4 — Long Put: Düşüş Hakkı ve Sınırları

 Tezin gerçekleşmesi için yalnız yön mü, ayrıca süre ve büyüklük de gerekiyor mu?  Strike ve expiration hedef hareketle uyumlu mu?  Premiumun yüzde kaçı spread nedeniyle anında kaybediliyor?

**Konular:** derivatives_options, market_basics, portfolio_correlation, execution_microstructure, fundamental_derivatives

**Kart:** `ATK-TR-D1.0-2026-08.p0443`

### PDF s. 444 — 21.5 — ITM, ATM, OTM ve Değer Bileşenleri

Call için S > K olduğunda ITM; put için S < K olduğunda ITM’dir. ATM, fiyatın strike’a yakın olduğu bölgedir. OTM option intrinsic value taşımaz; fakat vade ve belirsizlik nedeniyle time value taşıyabilir.

**Konular:** derivatives_options, market_basics, fundamental_derivatives, hedge_arbitrage, portfolio_correlation

**Kart:** `ATK-TR-D1.0-2026-08.p0444`

### PDF s. 445 — 21.6 — Premium, Expiration ve Theta

Dayanak fiyatı, strike, kalan süre, beklenen volatilite, faiz/taşıma, temettü ve arz–talep option fiyatını etkileyebilir. Theta, zaman geçtikçe optionın time value kaybetme eğilimini anlatır; bu kayıp sabit hızda olmak zorunda değildir. Değişken Long option alıcısı açısından Kalan süre azalır Diğer her şey aynıysa time value baskı görebilir.

**Konular:** derivatives_options, execution_microstructure, market_basics, volatility, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0445`

### PDF s. 446 — 21.7 — Vade Sonu Başabaş ve Kâr/Zarar Haritası

DOĞRU BİLİNEN YANLIŞ Mit: Theta her gün aynı miktarda premium siler. Gerçeklik: Zaman değeri doğrusal erimez; moneyness, volatilite ve vade yapısı sonucu değiştirir. Theta anlık duyarlılık ölçüsüdür, kesin günlük zarar takvimi değildir.

**Konular:** derivatives_options, market_basics, volatility, fundamental_derivatives, hedge_arbitrage

**Kart:** `ATK-TR-D1.0-2026-08.p0446`

### PDF s. 447 — 21.8 — Opsiyon İşleminde Risk Bütçesi ve

21.8 Opsiyon İşleminde Risk Bütçesi ve Sözleşme Sayısı Long option işleminde “premium küçük” ifadesi risk hesabı değildir. Toplam debit = premium × multiplier × kontrat sayısı + ücretlerdir. Sözleşmenin değersiz sona erebileceğini varsayarak kontrat sayısını önceden tanımlanan risk bütçesine göre seçerim.

**Konular:** risk_management, market_basics, portfolio_correlation, fundamental_derivatives, derivatives_options

**Kart:** `ATK-TR-D1.0-2026-08.p0447`

### PDF s. 448 — 21.10 — Protective Put ile Aşağı Yön Tabanı

21.9 Stop, Hedge, Pozisyon Azaltma ve Nakit Koruma ihtiyacı oluştuğunda ilk çözüm her zaman yeni bir türev pozisyon değildir. Stop tezi sonlandırır; pozisyon azaltma directional exposure’ı doğrudan düşürür; nakit taşımak riski ve karmaşıklığı azaltır; hedge ise ana pozisyonu korurken karşı maruziyet ve yeni maliyet ekler. Araç Ana görev Maliyet / risk Uygun soru Stop-loss Yanlış tezi kapatmak.

**Konular:** risk_management, derivatives_options, fundamental_derivatives, hedge_arbitrage, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0448`

### PDF s. 449 — 21.11 — Direct Hedge: Short, Futures ve Ters Ürün

Karar alanı Soru Çıkış Olay geçince satılacak mı, vade sonuna mı taşınacak, roll mu edilecek? Önce portföyün hangi kısmını koruyacağımı, dayanakla uyumlu option ürününü, strike ve expirationı seçerim. Premiumu “kaybedilecek sigorta maliyeti” olarak bütçeler; olay sonrası putu kapatma veya roll koşulunu önceden yazarım.

**Konular:** market_basics, derivatives_options, fundamental_derivatives, relative_cross_market, hedge_arbitrage

**Kart:** `ATK-TR-D1.0-2026-08.p0449`

### PDF s. 450 — 21.11 — Direct Hedge: Short, Futures ve Ters Ürün

 Long ve hedge ürününün fiyat sürücüsü gerçekten aynı mı?  Notional değerler aynı para biriminde mi?  Futures mark price, funding, margin ve liquidation ne?

**Konular:** fundamental_derivatives, hedge_arbitrage, crypto_specific, market_basics, portfolio_correlation

**Kart:** `ATK-TR-D1.0-2026-08.p0450`

### PDF s. 451 — 21.12 — Hedge Oranı, Basis ve Mismatch Riski

DOĞRU BİLİNEN YANLIŞ Mit: Long pozisyon kadar short açarsam risk tamamen sıfırlanır. Gerçeklik: Beta/delta, multiplier, basis, currency, timing ve maliyet farkları nedeniyle notional eşitlik ekonomik risk eşitliği olmayabilir. 21.12 Hedge Oranı, Basis ve Mismatch Riski Hedge ratio, hedge maruziyetinin korunan pozisyon maruziyetine oranını ifade eder.

**Konular:** fundamental_derivatives, hedge_arbitrage, risk_management, derivatives_options, market_basics

**Kart:** `ATK-TR-D1.0-2026-08.p0451`

### PDF s. 452 — 21.14 — Hedge Maliyeti, Geçersizlik ve Kapatma

VAKA ANALİZİ — XAGTRYG CROSS-HEDGE XAGTRYG pozisyonunu yalnız XAGUSD short ile korumak gümüş dolar bacağını azaltabilir; USDTRY bacağı açık kalır. XAGTRYG ≈ XAGUSD × USDTRY ilişkisi nedeniyle hedge hedefini önce “metal fiyatı mı, TL kur riski mi, ikisi mi?” diye ayırırım. Tek bacakla tüm TL fiyat riskinin kapandığını varsaymam.

**Konular:** fundamental_derivatives, hedge_arbitrage, risk_management, market_basics, portfolio_correlation

**Kart:** `ATK-TR-D1.0-2026-08.p0452`

### PDF s. 453 — 21.15 — Tam Portföy Koruma İş Akışı

Hedge kapatma tetikleyicisi Eylem Expiration yaklaştı Kapat, exercise, allow expire veya roll seçenekleri ürün kuralıyla incelenir. Basis/korelasyon bozuldu Koruma aracı değiştirilir veya pozisyon azaltılır. Gerçeklik: Ana pozisyon yükselirken hedge maliyet yazabilir; bu, sigortanın çalışmadığı anlamına gelmez.

**Konular:** fundamental_derivatives, hedge_arbitrage, risk_management, portfolio_correlation, derivatives_options

**Kart:** `ATK-TR-D1.0-2026-08.p0453`

### PDF s. 454 — 21.15 — Tam Portföy Koruma İş Akışı

Hızlı Başvuru Gördüğüm durum İlk kontrol Varsayılan eylem Option premium çok düşük Multiplier, OTM mesafe, spread ve expiration Toplam debit ve sıfıra gitme riskini hesapla. Option ITM Ödenen premium ve vade sonu başabaş ITM’yi net kâr sanma. Dayanak beklenen yönde gidiyor ama option düşüyor Time decay ve volatilite Vade öncesi fiyatlama bileşenlerini kontrol et.

**Konular:** fundamental_derivatives, hedge_arbitrage, derivatives_options, risk_management, portfolio_correlation

**Kart:** `ATK-TR-D1.0-2026-08.p0454`

### PDF s. 455 — 21.15 — Tam Portföy Koruma İş Akışı

 Direct hedge’de notional, beta/delta, basis, currency, funding ve margin kontrol edildi.  Korelasyon farklı lookback ve stres dönemlerinde incelendi.  Hedge açılışından önce geçersizlik, kapatma ve roll koşulu belirlendi.

**Konular:** derivatives_options, fundamental_derivatives, hedge_arbitrage, market_basics, portfolio_correlation

**Kart:** `ATK-TR-D1.0-2026-08.p0455`

### PDF s. 456 — 21.15 — Tam Portföy Koruma İş Akışı

Premiumun intrinsic ve time value bileşenleri nasıl ayrılır? Theta neden sabit günlük kayıp takvimi değildir? Dayanak doğru yönde giderken long option neden zarar yazabilir?

**Konular:** fundamental_derivatives, hedge_arbitrage, derivatives_options, market_basics, portfolio_correlation

**Kart:** `ATK-TR-D1.0-2026-08.p0456`
