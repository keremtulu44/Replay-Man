# PTA-C2-2026 — Bölüm 6

**PDF sayfaları:** 36–44
**Sayfa kartları:** 9

## Alt başlıklar

- 6.1 — Daralma ve genişleme: piyasa neden sürekli aynı tempoda
- 6.2 — Inside bar ve double inside bar: şekilden önce sınırı okuyun
- 6.3 — Örtüşme arttığında fiyat neden daha “sıkışık” görünür?
- 6.4 — Inside barın daha derin anlamı: yeni tepe veya dip üretememek
- 6.6 — Küçük mum kümesinden genişlemeye geçiş
- 6.7 — İlk genişleme başarısız olursa yapı bitmiş sayılır mı?
- 6.8 — Alt sınırı kısa süre aşmak, geri almak ve karşı tarafa genişlemek
- 6.9 — Sıkışmayı okurken hangi sırayı izleyelim?

## Konu dağılımı

- `volatility`: 8 sayfa
- `candle_behavior`: 6 sayfa
- `breakout_failure`: 3 sayfa
- `pullback`: 3 sayfa
- `trend_regime`: 2 sayfa
- `support_resistance`: 1 sayfa
- `momentum`: 1 sayfa
- `psychology_process`: 1 sayfa

## Sayfa şeritleri

### PDF s. 36 — 6.1 — Daralma ve genişleme: piyasa neden sürekli aynı tempoda

BÖLÜM 6 Sıkışmadan Genişlemeye: Inside Bar, Örtüşme ve Fiyat Aralığı Sıkışmayı tek başına yön sinyali saymayın. Önce fiyatın neden ilerleyemediğini, sonra dar alanın nasıl çözüldüğünü okuyun. Bölüm 5’te ana yönün kısa bir kesintiden sonra baskıyı nasıl yeniden kurabildiğini gördük.

**Konular:** volatility, candle_behavior

**Kart:** `PTA-C2-2026.p0036`

### PDF s. 37 — 6.2 — Inside bar ve double inside bar: şekilden önce sınırı okuyun

Genişleme, taraflardan birinin bu alanın dışına doğru yeniden mesafe almaya başlamasıdır. Evrenin durumu Grafikte ne görürüz? Daralma Mumlar daha dar alanda kalır; yeni mesafe üretmek zorlaşır.

**Konular:** candle_behavior, volatility

**Kart:** `PTA-C2-2026.p0037`

### PDF s. 38 — 6.3 — Örtüşme arttığında fiyat neden daha “sıkışık” görünür?

Renkten çok, sınırların genişletilememesi önemlidir. Yapı Asıl bilgi Yanlış kısa yol İç mum Bir mum önceki yüksek-düşük alanının dışına çıkamıyor. “İç mum = yön belli.” Çift iç mum İki mum boyunca daralma sürüyor; alan genişletilemiyor.

**Konular:** candle_behavior, volatility, breakout_failure

**Kart:** `PTA-C2-2026.p0038`

### PDF s. 39 — 6.4 — Inside barın daha derin anlamı: yeni tepe veya dip üretememek

Az örtüşmeli harekette ise her yeni mum önceki alanın ötesinde daha fazla mesafe kazanır. ÖRTÜŞMEYİ DOĞRU OKUYUN Yoğun örtüşme “mutlaka dönüş” demek değildir. Kaynağın desteklediği daha sınırlı sonuç şudur: yönlü momentum hakkında daha az kanıt vardır ve fiyat son aralıkların içinde daha fazla zaman geçirir.

**Konular:** support_resistance, candle_behavior, momentum, pullback

**Kart:** `PTA-C2-2026.p0039`

### PDF s. 40 — 6.6 — Küçük mum kümesinden genişlemeye geçiş

6.5 — Aynı sıkışma neden her yerde aynı anlamı taşımaz? Çift iç mum veya yoğun sıkışma tek başına bağlamdan bağımsız bir mesaj değildir. Kaynağa göre aynı double inside bar önemli bir teknik bölge yakınında duygu değişimine eşlik edebilir; belirgin bir engelden uzakta, mevcut trend içindeki kısa bir duraklama olarak da kalabilir.

**Konular:** volatility, trend_regime, candle_behavior, psychology_process

**Kart:** `PTA-C2-2026.p0040`

### PDF s. 41 — 6.7 — İlk genişleme başarısız olursa yapı bitmiş sayılır mı?

Böylece daralma ve genişleme aynı grafikte art arda okunabilir hale gelir. İlk büyük mum önemli bir değişimdir; fakat onun devam edip etmeyeceği bir sonraki bölümde ele alacağımız kırılım kalitesi ve takip davranışıyla ayrıca değerlendirilecektir. ÜÇ MUM BİR YASA DEĞİLDİR Kaynak küçük mum kümesini en az üç mumla örnekliyor.

**Konular:** volatility, breakout_failure, pullback

**Kart:** `PTA-C2-2026.p0041`

### PDF s. 42 — 6.7 — İlk genişleme başarısız olursa yapı bitmiş sayılır mı?

Özet cümlesi otomatik ayrılamadı; tam kaynak şeridi kart JSONL kaydında korunuyor.

**Konular:** volatility

**Kart:** `PTA-C2-2026.p0042`

### PDF s. 43 — 6.8 — Alt sınırı kısa süre aşmak, geri almak ve karşı tarafa genişlemek

İlk genişleme Dar alanın dışına çıkmayı deniyor. Başarısızlık / geri dönüş İlk hareket sürdürülemiyor. Yeniden sıkışma Fiyat tekrar dar bir alana giriyor.

**Konular:** volatility, breakout_failure

**Kart:** `PTA-C2-2026.p0043`

### PDF s. 44 — 6.9 — Sıkışmayı okurken hangi sırayı izleyelim?

6.9 — Sıkışmayı okurken hangi sırayı izleyelim? Inside bar, double inside bar, yoğun örtüşme, küçük mum kümesi ve dar fiyat aralığı farklı görünümler olabilir; fakat aynı temel soruya bağlanırlar: fiyat son birkaç mumda yeni alan üretmekte zorlanıyor mu? Bu sorunun cevabı evetse ikinci aşama, sıkışmanın nerede oluştuğunu ve hangi tarafın ilk genişlemeyi yaptığını izlemektir.

**Konular:** candle_behavior, volatility, pullback, trend_regime

**Kart:** `PTA-C2-2026.p0044`
