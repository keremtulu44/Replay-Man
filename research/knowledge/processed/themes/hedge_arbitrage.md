# hedge_arbitrage

**Kapsam:** 49 sayfa eşleşmesi

## Proje yorumu (`inference`)

Korunma ve arbitraj fikirleri yön tahmininden farklı amaç, maliyet ve yürütme semantiğine sahiptir.

## Nasıl kullanılabilir?

Korunma ve göreceli değer stratejilerinin gelecekteki modülü

## Kaynak şeritleri

### 1. ATK-TR-D1.0-2026-08 — PDF s. 452

> ANA TRADING KİTABI | BÖLÜM 21 Opsiyonlar, Hedge ve Portföy Koruma Stratejileri • 437 VAKA ANALİZİ — XAGTRYG CROSS-HEDGE XAGTRYG pozisyonunu yalnız XAGUSD short ile korumak gümüş dolar bacağını azaltabilir; USDTRY bacağı açık kalır. XAGTRYG ≈ XAGUSD × USDTRY ilişkisi nedeniyle hedge hedefini önce “metal fiyatı mı, TL kur riski mi, ikisi mi?” diye ayırırım. Tek bacakla tüm TL fiyat riskinin kapandığını varsaymam. 21.13 Çeşitlendirme ve Korelasyonun Sınırları Diversification, doğrudan karşı pozisyon açmak yerine portföyü farklı risk sürücülerine dağıtır. Correlation coefficient iki getiri serisinin seçilen lookback içindeki birlikte hareketini özetler; nedensellik, gelecekteki ilişki veya kriz koruması garantisi vermez. Korelasyon gözlemi Doğru yorum Yanlış sonuç +1’e yakın Seçilen dönemde benzer yönde hareket eğilimi. Her zaman aynı gider. 0’a yakın Doğrusal birlikte hareket zayıf. Bağımsız veya risksizdir. −1’e yakın Seçilen dönemde zıt yönde hareket eğilimi. Kesin hedge olur. Rejim değişimi İlişki enflasyon, likidite, kriz ve politika ile değişebilir. Geçmiş katsayı sabit kalır. Tablo 21.13 – Korelasyonun doğru kullanımı EKRANDA NE ARIYORUM?  Korelasyon price değil return serisi üzerinden mi hesaplanıyor?  Lookback ve timeframe yatırım ufkumla uyumlu mu?  Normal dönem ve stres döneminde sonuç farklı mı?  İki ürün aynı currency, sektör veya liquidity faktörüne mi bağlı?  Çeşitlendirme görünen sembol sayısını mı, gerçek risk sürücülerini mi artırıyor? DOĞRU BİLİNEN YANLIŞ Mit: Negatif korelasyonlu varlık bulursam portföyüm korunur. …

**Bölüm/alt başlık:** 21 / 21.14 — Hedge Maliyeti, Geçersizlik ve Kapatma

**Kaynak özeti (`source`):** VAKA ANALİZİ — XAGTRYG CROSS-HEDGE XAGTRYG pozisyonunu yalnız XAGUSD short ile korumak gümüş dolar bacağını azaltabilir; USDTRY bacağı açık kalır. XAGTRYG ≈ XAGUSD × USDTRY ilişkisi nedeniyle hedge hedefini önce “metal fiyatı mı, TL kur riski mi, ikisi mi?” diye ayırırım. Tek bacakla tüm TL fiyat riskinin kapandığını varsaymam.

### 2. ATK-TR-D1.0-2026-08 — PDF s. 486

> ANA TRADING KİTABI | BÖLÜM 23 Pozisyon Yönetimi, Kâr Alma ve Çıkış Stratejileri • 471 23.13 PSAR ve Heikin Ashi ile Yardımcı Çıkış Teyidi Parabolic SAR, trend boyunca fiyatın arkasında noktalar üretip flip olduğunda olası dönüş/exit uyarısı verebilir. Heikin Ashi ise OHLC’nin ortalanmış dönüşümünü kullanarak trendi daha pürüzsüz gösterir. Her ikisi de yardımcı filtre olabilir; gerçek işlem fiyatı ve ana yapı yerine geçmez. Araç Çıkış fikri Sınır / güvenlik PSAR Dot flip veya trail seviyesi. Range’de sık flip/false signal; yapı ve rejim teyidi. Heikin Ashi Wick yapısının bozulması veya karşı renkli mum. Gecikmeli ve sentetik OHLC; emir, standart mum ve gerçek fiyat üzerinden uygulanır. ATR/Chandelier Volatilite ayarlı dinamik stop. Multiplier ve anchor test edilmeli. Moving average Close/cross veya slope kaybı. Lag ve whipsaw; tek başına tam çıkış değil. Tablo 23.13 – Gösterge destekli çıkışlar EKRANDA NE ARIYORUM?  Heikin Ashi sinyali oluştuğunda standart mumun gerçek close’u nerede?  PSAR flip range gürültüsü mü, aynı zamanda yapı kaybı mı?  Gösterge exit’i başlangıç planında test edilmiş mi?  Alarm ile gerçek emir aynı fiyat kaynağını mı kullanıyor?  Gösterge gecikmesi verilen kârı ve hit rate’i nasıl değiştiriyor? DOĞRU BİLİNEN YANLIŞ Mit: Heikin Ashi karşı renk verdiğinde veya PSAR flip olduğunda en doğru çıkış oluşur. Gerçeklik: İki araç da gecikmeli/bağlama duyarlıdır. Standart mum, structure ve ürün fiyatı ile teyit edilir. 23.14 Hedge Kapatma, Roll ve Tam Pozisyon Çözümü Hedge açmak kadar kapatma kuralı da girişte yazılmalıdır. …

**Bölüm/alt başlık:** 23 / 23.14 — Hedge Kapatma, Roll ve Tam Pozisyon

**Kaynak özeti (`source`):** 23.13 PSAR ve Heikin Ashi ile Yardımcı Çıkış Teyidi Parabolic SAR, trend boyunca fiyatın arkasında noktalar üretip flip olduğunda olası dönüş/exit uyarısı verebilir. Heikin Ashi ise OHLC’nin ortalanmış dönüşümünü kullanarak trendi daha pürüzsüz gösterir. Her ikisi de yardımcı filtre olabilir; gerçek işlem fiyatı ve ana yapı yerine geçmez.

### 3. ATK-TR-D1.0-2026-08 — PDF s. 453

> ANA TRADING KİTABI | BÖLÜM 21 Opsiyonlar, Hedge ve Portföy Koruma Stratejileri • 438 Hedge kapatma tetikleyicisi Eylem Expiration yaklaştı Kapat, exercise, allow expire veya roll seçenekleri ürün kuralıyla incelenir. Basis/korelasyon bozuldu Koruma aracı değiştirilir veya pozisyon azaltılır. Tablo 21.15 – Hedge geçersizlik ve çıkış kartı DOĞRU BİLİNEN YANLIŞ Mit: Hedge para kaybediyorsa başarısızdır. Gerçeklik: Ana pozisyon yükselirken hedge maliyet yazabilir; bu, sigortanın çalışmadığı anlamına gelmez. Değerlendirme toplam portföy sonucu ve önceden tanımlı risk azaltımıyla yapılır. 21.15 Tam Portföy Koruma İş Akışı Koruma kararı aşağıdaki sırayla uygulanır. Araç seçimi ilk değil dördüncü adımdır; önce risk ve ana tez tanımlanır. Aşama Eylem Çıktı 1 Ana pozisyon Dayanak, miktar, maliyet, zaman ufku ve tez. Korunan varlık kartı. 2 Risk Fiyat düşüşü, gap, olay, volatilite, currency veya likidite riski. Tek cümlelik risk tanımı. 3 Tez kapısı Risk geçici mi, ana tez bozuldu mu? Kapat / azalt / hedge kararı. 4 Araç Stop, cash reduction, put, short futures veya çeşitlendirme. En sade uygun araç. 5 Boyut Notional, multiplier, beta/delta, currency ve maximum loss. Hedge oranı. 6 Süre Olay tarihi, expiration, vade ve roll ihtiyacı. Zaman uyumu. 7 Maliyet Premium, spread, commission, funding, tax ve fırsat maliyeti. Toplam koruma bütçesi. 8 Geçersizlik Hedge ne zaman gereksiz veya yanlış? Kapatma koşulu. 9 Uygulama Paper/limit order, fill ve margin kontrolü. Açık hedge kaydı. 10 İzleme Toplam portföy delta/notional, basis ve korelasyon. Under/over-hedge alarmı. …

**Bölüm/alt başlık:** 21 / 21.15 — Tam Portföy Koruma İş Akışı

**Kaynak özeti (`source`):** Hedge kapatma tetikleyicisi Eylem Expiration yaklaştı Kapat, exercise, allow expire veya roll seçenekleri ürün kuralıyla incelenir. Basis/korelasyon bozuldu Koruma aracı değiştirilir veya pozisyon azaltılır. Gerçeklik: Ana pozisyon yükselirken hedge maliyet yazabilir; bu, sigortanın çalışmadığı anlamına gelmez.

### 4. ATK-TR-D1.0-2026-08 — PDF s. 451

> ANA TRADING KİTABI | BÖLÜM 21 Opsiyonlar, Hedge ve Portföy Koruma Stratejileri • 436 DOĞRU BİLİNEN YANLIŞ Mit: Long pozisyon kadar short açarsam risk tamamen sıfırlanır. Gerçeklik: Beta/delta, multiplier, basis, currency, timing ve maliyet farkları nedeniyle notional eşitlik ekonomik risk eşitliği olmayabilir. 21.12 Hedge Oranı, Basis ve Mismatch Riski Hedge ratio, hedge maruziyetinin korunan pozisyon maruziyetine oranını ifade eder. Basit notional oran başlangıç kontrolüdür: hedge notional ÷ korunan notional. Fakat farklı dayanaklarda beta, delta veya tarihsel ilişki nedeniyle ekonomik oran değişebilir. Durum Sonuç Kontrol Under-hedge Düşüşte koruma yetersiz kalır. Korunan notional ve sensitivity yeniden hesaplanır. Full notional hedge Yönsel risk büyük ölçüde azalabilir. Basis ve ürün farkı hâlâ vardır. Over-hedge Portföy net short hâle gelebilir. Hedge kâr aracı olmaya başladı mı? Cross-hedge Benzer fakat aynı olmayan dayanak kullanılır. Rolling correlation, beta, currency ve stress dönemleri. Option hedge Delta zamanla ve fiyatla değişebilir. Statik kontrat sayısı koruma oranını sabit tutmaz. Tablo 21.12 – Hedge oranı ve mismatch BASIS RİSKİ Hedge ürünü ile korunan pozisyon arasındaki fiyat farkının beklenmedik değişmesine basis risk denir. Aynı ekonomik hikâyeye bağlı iki ürün, tam aynı zamanda ve aynı oranda hareket etmek zorunda değildir.

**Bölüm/alt başlık:** 21 / 21.12 — Hedge Oranı, Basis ve Mismatch Riski

**Kaynak özeti (`source`):** DOĞRU BİLİNEN YANLIŞ Mit: Long pozisyon kadar short açarsam risk tamamen sıfırlanır. Gerçeklik: Beta/delta, multiplier, basis, currency, timing ve maliyet farkları nedeniyle notional eşitlik ekonomik risk eşitliği olmayabilir. 21.12 Hedge Oranı, Basis ve Mismatch Riski Hedge ratio, hedge maruziyetinin korunan pozisyon maruziyetine oranını ifade eder.

## Test fikri (`hypothesis`)

Bu konuya ait kaynak varyantları korunur. İlk aşamada sabit eşik seçilmez; geniş sembol evreninde aynı tanımların amaçladığı davranışa katkısı karşılaştırılır.
