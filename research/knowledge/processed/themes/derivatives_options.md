# derivatives_options

**Kapsam:** 38 sayfa eşleşmesi

## Proje yorumu (`inference`)

Türevlerin doğrusal olmayan risk ve sözleşme yapısı spot OHLC stratejilerinden ayrı değerlendirilmelidir.

## Nasıl kullanılabilir?

Opsiyon ve türev ürünlerin ayrı fiyat/risk semantiği

## Kaynak şeritleri

### 1. ATK-TR-D1.0-2026-08 — PDF s. 443

> ANA TRADING KİTABI | BÖLÜM 21 Opsiyonlar, Hedge ve Portföy Koruma Stratejileri • 428 EKRANDA NE ARIYORUM?  Tezin gerçekleşmesi için yalnız yön mü, ayrıca süre ve büyüklük de gerekiyor mu?  Strike ve expiration hedef hareketle uyumlu mu?  Premiumun yüzde kaçı spread nedeniyle anında kaybediliyor?  Başabaş fiyatı yakın teknik hedefin ötesinde mi?  Kontrat sayısı sıfıra gidebilecek toplam premiuma göre mi seçildi? DOĞRU BİLİNEN YANLIŞ Mit: Call alırsam fiyat biraz yükseldiğinde mutlaka kâr ederim. Gerçeklik: Dayanak yükselse bile hareket yetersiz, geç veya volatilite düşüşüyle birlikteyse option fiyatı zarar yazabilir. Vade sonu başabaş yalnız strike + premiumdır. 21.4 Long Put: Düşüş Hakkı ve Sınırları Long put (premium ödeyerek dayanağı strike’dan satma hakkı satın alma), bearish yön görüşü veya long varlığın aşağı yönünü sınırlama amacıyla kullanılabilir. Protective put kullanımında amaç putun tek başına kârı değil, dayanakla birlikte toplam portföy tabanıdır. Long put alanı Vade sonu mantığı Intrinsic value max(Strike − Dayanak fiyatı, 0) Net sonuç / pay max(K − S, 0) − ödenen premium Başabaş Strike − pay başına premium Maksimum sözleşme kaybı Ödenen premium × multiplier; ücretler ayrıca Aşağı potansiyel Dayanak sıfıra kadar düşebildiği için intrinsic kazanç strike ile sınırlıdır Tablo 21.4 – Long put vade sonu haritası VAKA ANALİZİ — PUT BAŞABAŞI Strike 100, pay başına premium 3 olan long put için vade sonu başabaş 97’dir. Dayanak 98’de kapanırsa put ITM olabilir; fakat intrinsic value 2 olduğu için ödenen 3 premiumu karşılamaz ve net sonuç hâlâ −1/pay olur. …

**Bölüm/alt başlık:** 21 / 21.4 — Long Put: Düşüş Hakkı ve Sınırları

**Kaynak özeti (`source`):**  Tezin gerçekleşmesi için yalnız yön mü, ayrıca süre ve büyüklük de gerekiyor mu?  Strike ve expiration hedef hareketle uyumlu mu?  Premiumun yüzde kaçı spread nedeniyle anında kaybediliyor?

### 2. ATK-TR-D1.0-2026-08 — PDF s. 23

> ANA TRADING KİTABI | BÖLÜM 1 Piyasalar, Trading Mekaniği ve Grafik Temelleri • 8 Spot işlemin “kaldıraçsız ve risksiz” olduğu düşünülmemelidir. Varlığın fiyatı düşebilir, piyasa likiditesi azalabilir veya saklama ve platform sorunları oluşabilir. Spot işlemin temel farkı, pozisyonun doğrudan varlık sahipliğine dayanmasıdır. Vadeli işlem sözleşmesi (futures) Vadeli işlemde trader, dayanak varlığın kendisinden çok onun fiyatına bağlı bir sözleşmede pozisyon alır. Sözleşme, belirli koşulları ve vade yapısını içerir. Kullanılan piyasaya göre nakdi uzlaşma, teslimat veya farklı sözleşme mekanizmaları bulunabilir. Futures piyasası, spot piyasaya göre daha yüksek kaldıraç kullanımına imkân verebilir. Kaldıraç hem kazancı hem kaybı büyütür. Bu nedenle futures işlemi, yalnızca “daha fazla kazanma” aracı değil; teminat, tasfiye ve sözleşme risklerinin birlikte yönetilmesi gereken ayrı bir üründür. Opsiyon sözleşmesi (options) Opsiyon, belirli bir dayanak varlığı önceden belirlenmiş bir kullanım fiyatından, belirli bir süre içinde alma veya satma hakkı sağlayan sözleşmedir. Alım opsiyonu (call) yükseliş yönlü, satım opsiyonu (put) düşüş yönlü beklentilerle ilişkilendirilebilir; ancak gerçek kâr ve zarar yapısı yalnızca yön tahminine bağlı değildir.  Kullanım fiyatı (strike): Opsiyon hakkının hangi fiyattan kullanılabileceğini belirler.  Prim (premium): Opsiyon sözleşmesi için ödenen bedeldir.  Vade sonu (expiration): Opsiyon hakkının geçerli olduğu sürenin sonudur.  Call / Put: Sırasıyla alma ve satma hakkını ifade eden temel opsiyon türleridir. …

**Bölüm/alt başlık:** 1 / 1.4 — Sahip Olunan Varlık ile Sözleşme

**Kaynak özeti (`source`):** Spot işlemin “kaldıraçsız ve risksiz” olduğu düşünülmemelidir. Varlığın fiyatı düşebilir, piyasa likiditesi azalabilir veya saklama ve platform sorunları oluşabilir. Spot işlemin temel farkı, pozisyonun doğrudan varlık sahipliğine dayanmasıdır.

### 3. ATK-TR-D1.0-2026-08 — PDF s. 455

> ANA TRADING KİTABI | BÖLÜM 21 Opsiyonlar, Hedge ve Portföy Koruma Stratejileri • 440  Direct hedge’de notional, beta/delta, basis, currency, funding ve margin kontrol edildi.  Korelasyon farklı lookback ve stres dönemlerinde incelendi.  Hedge açılışından önce geçersizlik, kapatma ve roll koşulu belirlendi.  Başarı tek hedge bacağıyla değil toplam portföy kaybıyla ölçülecek. Temel Sözlük Terim Aksiyon tanımı Option Belirli strike ve tarihte dayanağı alma/satma hakkının sözleşmesini okumak. Underlying Option değerinin bağlı olduğu varlık veya sözleşmeyi doğrulamak. Call Dayanağı strike’dan alma hakkı satın almak. Put Dayanağı strike’dan satma hakkı satın almak. Strike Hakkın kullanılabileceği fiyatı belirlemek. Premium Option için pay başına fiyatı multiplier ile çarpıp toplam debit hesaplamak. Expiration Sözleşmenin sona ereceği tarihi tez süresiyle eşleştirmek. Multiplier Bir kontratın kaç dayanak birimini temsil ettiğini doğrulamak. ITM / ATM / OTM Dayanak ile strike konumunu intrinsic value açısından sınıflandırmak. Intrinsic value Bugün kullanımın ekonomik değerini max(S−K,0) veya max(K−S,0) ile görmek. Time value Premiumun intrinsic dışındaki, kalan süre ve belirsizlikle ilişkili kısmını izlemek. Theta Diğer koşullar aynıyken zaman geçişine option değerinin duyarlılığını izlemek. Break-even Vade sonunda call için K+premium, put için K−premium seviyesini hesaplamak. Protective put Long dayanağa long put ekleyerek belirli süre ve strike için aşağı yön tabanı kurmak. Direct hedge Ana pozisyona karşı short veya dengeleyici maruziyet açmak. …

**Bölüm/alt başlık:** 21 / 21.15 — Tam Portföy Koruma İş Akışı

**Kaynak özeti (`source`):**  Direct hedge’de notional, beta/delta, basis, currency, funding ve margin kontrol edildi.  Korelasyon farklı lookback ve stres dönemlerinde incelendi.  Hedge açılışından önce geçersizlik, kapatma ve roll koşulu belirlendi.

### 4. ATK-TR-D1.0-2026-08 — PDF s. 440

> ANA TRADING KİTABI | BÖLÜM 21 Opsiyonlar, Hedge ve Portföy Koruma Stratejileri • 425 Bu Bölümün Amacı Opsiyonlar, küçük bir premium karşılığında dayanak varlık üzerinde koşullu bir hak satın almaya; hedge ise mevcut bir riskin etkisini başka bir pozisyonla azaltmaya yarar. Bu iki araç aynı değildir: her opsiyon hedge değildir, her hedge de opsiyonla kurulmaz. Bu bölümde önce sözleşmeyi okuyacak, long call ve long put sonuçlarını vade sonu matematiğiyle kuracak, sonra protective put, direct hedge, pozisyon azaltma ve çeşitlendirmeyi aynı risk sorusu üzerinde karşılaştıracağız. Amaç kazancı büyütmekten önce, hangi kaybın hangi maliyetle sınırlandığını görünür kılmaktır. BÖLÜM SONUNDA  Option sözleşmesindeki underlying, multiplier, strike, premium ve expiration alanlarını okuyabileceksiniz.  Long call ve long put için maksimum kayıp ve vade sonu başabaş hesabı yapabileceksiniz.  ITM/ATM/OTM ile intrinsic/time value ayrımını kurabileceksiniz.  Theta’nın option alıcısına karşı çalışan zaman maliyetini yorumlayabileceksiniz.  Stop, hedge, pozisyon azaltma ve çeşitlendirmeyi görevlerine göre ayırabileceksiniz.  Protective put ve direct hedge’in toplam portföy sonucunu nasıl değiştirdiğini okuyabileceksiniz.  Hedge oranı, basis, funding, korelasyon ve maliyet risklerini kontrol edebileceksiniz.  Hedge’i açma, sürdürme, kapatma ve kaydetme planı oluşturabileceksiniz. KAPSAM NOTU Bu bölümün ana opsiyon kaynağı option alıcısının long call ve long put işlemleridir. …

**Bölüm/alt başlık:** 21 / belirlenmedi

**Kaynak özeti (`source`):** Bu Bölümün Amacı Opsiyonlar, küçük bir premium karşılığında dayanak varlık üzerinde koşullu bir hak satın almaya; hedge ise mevcut bir riskin etkisini başka bir pozisyonla azaltmaya yarar. Bu iki araç aynı değildir: her opsiyon hedge değildir, her hedge de opsiyonla kurulmaz. Bu bölümde önce sözleşmeyi okuyacak, long call ve long put sonuçlarını vade sonu matematiğiyle kuracak, sonra protective put, direct hedge, pozisyon azaltma ve çeşitlendirmeyi aynı risk sorusu üzerinde karşılaştıracağız.

### 5. PTA-C2-2026 — PDF s. 107

> PROFESYONEL TEKNİK ANALİZ — CİLT 2 107 EK 3 · DEVAM Kaynakça 15. End-of-Day Bull and Bear Traps - Al Brooks [j3FYCyWBTqc] 16. Trader Training Call With Price Action Trader Al Brooks [91h0Dw9jwQ0] 17. How To Identify Swing Highs & Lows [AHvDE9TxFLU] 18. 15 Best Price Action Strategies After 15 Years of Trading (The Holy Grail) [FBdN2L8SSyY] 19. Trading When a Market Is in a Bull Channel | Al Brooks [RDJWHNwwI-M] 20. Tutorial for Traders： How to Read a Price Chart [ebULiDW6O70] 21. Live Price Action Trade Example 9-16-13 [31GUm-52k9o] 22. Al Brooks on Probabilities, Timing, Scaling [J6lL2pdvV7w] 23. Best Pullback Trading Strategy That Will Change The Way You Trade [cKKLujAdvzk] 24. Trading Price Action Using PIN BARS (Best Forex Candlestick Reversal Pattern) [FQdOyANXSAM] 25. The GOAT Teaches You How To Master Price Action (Ep 5: Al Brooks) [N-kr7PTO_wU] 26. Volume Doesn't Work (Unless You Do This) [aVt0WUJuV6E] 27. 3 Step Process To Finding The Best Trades - Keeping Trading Simple [bGKFvrjsnZA] KAYNAK KULLANIMI Kaynak videolardaki reklam, kişisel performans anlatısı ve doğrulanmamış kesinlik iddiaları kitap metnine taşınmamıştır. Kitapta kaynak fikirler Türkçe anlatımla yeniden kurulmuş; görseller öğretim amacıyla özgün hazırlanmıştır.

**Bölüm/alt başlık:** 13 / 13.10 — Son kontrol: karar vermeden önce 10 soru

**Kaynak özeti (`source`):** End-of-Day Bull and Bear Traps - Al Brooks [j3FYCyWBTqc] 16. Trader Training Call With Price Action Trader Al Brooks [91h0Dw9jwQ0] 17. How To Identify Swing Highs & Lows [AHvDE9TxFLU] 18.

## Test fikri (`hypothesis`)

Bu konuya ait kaynak varyantları korunur. İlk aşamada sabit eşik seçilmez; geniş sembol evreninde aynı tanımların amaçladığı davranışa katkısı karşılaştırılır.
