# PTA-C2-2026 — Bölüm 12

**PDF sayfaları:** 86–92
**Sayfa kartları:** 7

## Alt başlıklar

- 12.1 — Hacim neyi ekler?
- 12.2 — Mum boyutu ile hacmi birlikte okumak
- 12.3 — Fiyat yeni tepe veya dip yaparken hacim azalırsa ne değişir?
- 12.4 — Davranış zaman dilimi ne işe yarar?
- 12.5 — Üst zaman yükseliş yönlüyken alt zaman hâlâ düşüyorsa ne
- 12.6 — Bir seviyenin gerçekten tutulduğunu nasıl anlarız?

## Konu dağılımı

- `volume_flow`: 5 sayfa
- `multi_timeframe`: 5 sayfa
- `breakout_failure`: 5 sayfa
- `pullback`: 4 sayfa
- `momentum`: 2 sayfa
- `candle_behavior`: 1 sayfa
- `trend_regime`: 1 sayfa
- `volatility`: 1 sayfa
- `support_resistance`: 1 sayfa

## Sayfa şeritleri

### PDF s. 86 — 12.1 — Hacim neyi ekler?

BÖLÜM 12 Hacim ve Çoklu Zaman Dilimi: İkinci Katman Fiyat davranışını önce okuyun. Hacmi ve zaman dilimini, gördüğünüz davranışın gücünü ve bağlamını desteklemek için kullanın. Bu bölüm yeni bir sinyal sistemi kurmuyor.

**Konular:** volume_flow, multi_timeframe, candle_behavior, breakout_failure

**Kart:** `PTA-C2-2026.p0086`

### PDF s. 87 — 12.2 — Mum boyutu ile hacmi birlikte okumak

Hacim yönü tek başına belirlemez; fiyat hareketine eşlik eden aktiviteyi ikinci katman olarak ekler. Mum geniş ve yönlü ilerledi Katılım yüksek Geniş hareket yoğun aktiviteyle oluştu Mum geniş ve yönlü ilerledi Katılım düşük Aynı mesafe daha düşük kayıtlı aktiviteyle alındı Mum küçük kaldı Katılım yüksek Yoğun aktiviteye rağmen fiyat az ilerledi; nedenini bağlamda araştır Mum küçük kaldı Katılım düşük Hem hareket hem aktivite sınırlı; tek başına güçlü sonuç çıkarma 12.2 — Mum boyutu ile hacmi birlikte okumak Kaynak 62, mum boyutu ile hacmi tek bir ölçüye indirgemek yerine farklı kombinasyonlar halinde karşılaştırır. Büyük mum + yüksek hacim, geniş fiyat hareketine yüksek katılım eşlik ettiğini gösterir.

**Konular:** volume_flow

**Kart:** `PTA-C2-2026.p0087`

### PDF s. 88 — 12.3 — Fiyat yeni tepe veya dip yaparken hacim azalırsa ne değişir?

Özellikle küçük mum + yüksek hacim, yüksek aktiviteye rağmen sınırlı fiyat ilerlemesi gösterir; bu durum ancak bağlam ve sonraki davranışla anlam kazanır. Kombinasyon Doğrudan gözlem Yanlış kısa yol Sonraki soru Büyük mum + yüksek hacim Geniş hareket + yüksek katılım “Kesin devam eder” Takip davranışı ve konum hareketi destekliyor mu? Büyük mum + düşük hacim Geniş hareket + düşük aktivite “Hareket sahtedir” Fiyat yapısı ve sonraki mumlar ne yapıyor?

**Konular:** volume_flow, breakout_failure, pullback, trend_regime, volatility

**Kart:** `PTA-C2-2026.p0088`

### PDF s. 89 — 12.4 — Davranış zaman dilimi ne işe yarar?

kanıtlarını ararız: yeni uç üretilememesi, momentum kaybı, karşı yönde büyüyen mumlar, yapı kırılımı veya takip davranışı değişimi. Bu durum otomatik dönüş sinyali değildir; fiyat ilerlerken katılımın aynı ölçüde eşlik etmediğini gösteren bir uyarıdır. TEKNİK AYRIM Fiyat hâlâ yeni tepe/dip üretiyorsa “ilerleme bitti” demeyin.

**Konular:** multi_timeframe, breakout_failure, momentum, pullback, volume_flow

**Kart:** `PTA-C2-2026.p0089`

### PDF s. 90 — 12.5 — Üst zaman yükseliş yönlüyken alt zaman hâlâ düşüyorsa ne

Bölgeye ulaşmak alt zamanı otomatik olarak yükseliş yapmaz; yerel momentum ve yapının gerçekten yön değiştirmesi ayrıca görülmelidir. 12.5 — Üst zaman yükseliş yönlüyken alt zaman hâlâ düşüyorsa ne yaparız? Kaynak 65 bu noktada net bir ayrım yapar.

**Konular:** multi_timeframe, momentum, breakout_failure, pullback, support_resistance

**Kart:** `PTA-C2-2026.p0090`

### PDF s. 91 — 12.6 — Bir seviyenin gerçekten tutulduğunu nasıl anlarız?

12.6 — Bir seviyenin gerçekten tutulduğunu nasıl anlarız? Kaynak 66, bir seviyenin yalnızca temas edildiği için “çalıştığını” kabul etmez. Fiyat desteğe veya dirence değebilir, kısa süre durabilir ve sonra eski yönde ilerlemeye devam edebilir.

**Konular:** pullback, breakout_failure, multi_timeframe

**Kart:** `PTA-C2-2026.p0091`

### PDF s. 92 — 12.6 — Bir seviyenin gerçekten tutulduğunu nasıl anlarız?

Hacim ve MTF, fiyat okumasının yerine geçmez. BÖLÜM SONUCU Hacim ve çoklu zaman dilimi, fiyat davranışına rakip iki ayrı sistem değildir. Hacim katılımı, davranış zaman dilimi ise fiyatın önemli bir bölgede gerçekten değişip değişmediğini gösteren destekleyici katmanlardır.

**Konular:** volume_flow, multi_timeframe

**Kart:** `PTA-C2-2026.p0092`
