# PTA-C1-2026 — Bölüm 13

**PDF sayfaları:** 79–83
**Sayfa kartları:** 5

## Alt başlıklar

- 13.1 — Supertrend’in temel hesabı: ATR bantları
- 13.3 — Supertrend yön değişimi nasıl oluşur?
- 13.5 — Supertrend neden doğal olarak gecikir?
- 13.6 — Supertrend çizgisini stop olarak kullanmak
- 13.7 — Hangi kombinasyonlar anlamlı?

## Konu dağılımı

- `volatility`: 5 sayfa
- `indicator_systems`: 5 sayfa
- `trend_regime`: 5 sayfa
- `position_management`: 3 sayfa
- `risk_management`: 2 sayfa
- `candle_behavior`: 1 sayfa
- `volume_flow`: 1 sayfa
- `momentum`: 1 sayfa

## Sayfa şeritleri

### PDF s. 79 — 13.1 — Supertrend’in temel hesabı: ATR bantları

BÖLÜM 13 Supertrend: ATR Tabanlı Trend Takibi Supertrend tek çizgiyle sade görünür. Ancak çizginin yeri ATR’ye, yani fiyatın ne kadar geniş hareket ettiğine göre değişir. Bu yüzden “renk değişti = yeni trend kesin başladı” şeklinde okunmamalıdır.

**Konular:** volatility, indicator_systems, risk_management, trend_regime, position_management

**Kart:** `PTA-C1-2026.p0079`

### PDF s. 80 — 13.3 — Supertrend yön değişimi nasıl oluşur?

Görülen nihai Supertrend çizgisi bu bantların durum kurallarıyla filtrelenmiş halidir. 13.2 — “Çizgi fiyatı takip ediyor” anlatısının eksik tarafı Supertrend yalnız “fiyat ± ATR” değildir. Nihai üst/alt bantlar önceki bant değerlerini koşullu biçimde koruduğu için çizgi geçmiş durumdan da etkilenir.

**Konular:** indicator_systems, volatility, trend_regime, candle_behavior, position_management

**Kart:** `PTA-C1-2026.p0080`

### PDF s. 81 — 13.5 — Supertrend neden doğal olarak gecikir?

13.4 — Çarpan ve ATR dönemi neyi değiştirir? Ayar değişimi Tipik etki Bedel Çarpan azalır Çizgi fiyata yaklaşır Daha sık yanlış sinyal / erken yön değişimi Çarpan artar Çizgi uzaklaşır Daha geç yön değişimi / daha geniş tolerans ATR dönemi kısalır Fiyat hareketliliği değişimine daha hızlı tepki Daha oynak çizgi ATR dönemi uzar Daha yumuşak fiyat hareketliliği ölçümü Piyasa ortamı değişimine daha geç tepki GEÇMİŞE AŞIRI UYUM UYARISI Geçmiş grafikte “tam dönüş noktalarını yakalayan” çarpan/ATR dönemi kombinasyonunu aramak parametre uydurmasıdır. Ayar, işlem ufku ve kabul edilen gürültüyle gerekçelendirilmelidir.

**Konular:** volatility, indicator_systems, trend_regime

**Kart:** `PTA-C1-2026.p0081`

### PDF s. 82 — 13.6 — Supertrend çizgisini stop olarak kullanmak

Piyasa Supertrend davranışı Daha doğru okuma Düzenli trend Pozisyonu uzun süre takip edebilir Takip eden stop / piyasa ortamı filtresi için uygun Yatay piyasa Sık yön değişimi üretebilir Tek başına giriş sistemi yapma Ani fiyat hareketliliği şoku ATR genişler, bant mesafesi değişir Stop/risk mantığını ayrıca kontrol et 13.6 — Supertrend çizgisini stop olarak kullanmak Supertrend takip eden stop referansı olabilir; ancak teknik stop mesafesi ile hesap başına para riski ayrı konulardır. Stop uzaksa pozisyon büyüklüğü buna göre ayarlanmalıdır. MİNİ ÖRNEK Giriş 100 TL, Supertrend 92 TL ise teknik mesafe %8’dir.

**Konular:** risk_management, indicator_systems, position_management, trend_regime, volatility

**Kart:** `PTA-C1-2026.p0082`

### PDF s. 83 — 13.7 — Hangi kombinasyonlar anlamlı?

13.7 — Hangi kombinasyonlar anlamlı? Kombinasyon Rol ayrımı Değerlendirme Supertrend + Fiyat yapısı Otomatik trend çizgisi + gerçek fiyat yapısı Güçlü tamamlayıcı Supertrend + RSI/Stoch Trend filtresi + hareket gücü zamanlama Kullanılabilir Supertrend + Hacim/Volume Profile Trend + katılım/konum Kullanılabilir Supertrend + ATR İkisi bağımsız teyit değildir Supertrend zaten ATR içerir Supertrend + 200 MA + MACD Aynı trend bilgisinin tekrarı Çoğu sistemde gereksiz BÖLÜM SONUCU Supertrend ATR tabanlı ve gecikmeli bir trend takip aracıdır. En doğal rolleri piyasa ortamı filtresi ve takip eden stop referansıdır; renk değişimi trend başlangıcı garantisi değildir.

**Konular:** indicator_systems, trend_regime, volatility, volume_flow, momentum

**Kart:** `PTA-C1-2026.p0083`
