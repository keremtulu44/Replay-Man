# PTA-C1-2026 — Bölüm 8

**PDF sayfaları:** 50–55
**Sayfa kartları:** 6

## Alt başlıklar

- 8.1 — Üç çizgi nasıl oluşur?
- 8.3 — Donchian kırılımı neden stratejinin tamamı değildir?
- 8.5 — Orta bant takip eden stop için nasıl kullanılabilir?
- 8.7 — Bollinger mi Donchian mı?
- 8.8 — Kırılım sistemi için pratik akış

## Konu dağılımı

- `indicator_systems`: 6 sayfa
- `volatility`: 6 sayfa
- `risk_management`: 5 sayfa
- `breakout_failure`: 4 sayfa
- `trend_regime`: 4 sayfa
- `ohlcv_data`: 2 sayfa
- `position_management`: 1 sayfa
- `volume_flow`: 1 sayfa

## Sayfa şeritleri

### PDF s. 50 — 8.1 — Üç çizgi nasıl oluşur?

BÖLÜM 8 Donchian Kanalı: Kırılımı Sadeleştirmek Donchian Kanalı son N mumun en yüksek ve en düşük fiyatlarını iki sınır olarak gösterir. Fiyat bu sınırın dışına çıktığında yeni bir kırılım oluşmuş olabilir. Bu, işleme giriş için bir işaret olabilir; ancak tek başına yön, stop ve pozisyon büyüklüğü belirlemez.

**Konular:** risk_management, breakout_failure, indicator_systems, volatility, ohlcv_data

**Kart:** `PTA-C1-2026.p0050`

### PDF s. 51 — 8.3 — Donchian kırılımı neden stratejinin tamamı değildir?

SAYISAL ÖRNEK 20 periyotluk üst bant 120, alt bant 100 ise orta bant = (120+100)/2 = 110. Yeni fiyat 121’e çıkar ve yöntem güncel barı kırılım için hesaba katıyorsa yeni 20-periyot zirvesi oluşur. Bu olay bir giriş işareti olabilir; kârlı işlem garantisi değildir.

**Konular:** breakout_failure, indicator_systems, trend_regime, volatility, risk_management

**Kart:** `PTA-C1-2026.p0051`

### PDF s. 52 — 8.5 — Orta bant takip eden stop için nasıl kullanılabilir?

Eksik parça Sadece Donchian varsa sorun Tamamlayıcı Risk Stop/pozisyon büyüklüğü yok Yapı + ATR / risk planı 8.4 — Donchian + ATR neden güçlü bir rol kombinasyonudur? ATR “piyasa ne kadar hareket ediyor?”, Donchian “son N periyot sınırı hangi yönde kırıldı?” sorusuna cevap verir. Böylece fiyat hareketliliği koşulu ile yönlü giriş işareti birbirinden ayrılır.

**Konular:** risk_management, indicator_systems, volatility, position_management, trend_regime

**Kart:** `PTA-C1-2026.p0052`

### PDF s. 53 — 8.7 — Bollinger mi Donchian mı?

8.6 — Giriş, çıkış ve yeniden giriş kanallarını ayrı tanımlayın Donchian sisteminde giriş için kullanılan kanal ile çıkış için kullanılan kanal farklı geriye bakış pencerelerine sahip olabilir. Böylece giriş kuralı yeni N-periyot kırılımını izlerken çıkış kuralı daha kısa veya daha uzun bir kanal üzerinden yönetilebilir. Daha kısa çıkış penceresi sınırı fiyata yaklaştırır.

**Konular:** trend_regime, indicator_systems, volatility, breakout_failure, ohlcv_data

**Kart:** `PTA-C1-2026.p0053`

### PDF s. 54 — 8.8 — Kırılım sistemi için pratik akış

Özellik Bollinger Bands Donchian Kanalı En iyi tamamlayıcı Fiyat yapısı / Hacim ATR / Fiyat yapısı / Hacim TEKRAR RİSKİ Bollinger + Donchian ancak görevleri ayrılırsa anlamlıdır: Bollinger bant yapısını, Donchian ise kırılım sınırını gösterir. Aksi halde iki kanal yalnız grafiği kalabalıklaştırır. 8.8 — Kırılım sistemi için pratik akış Adım Soru Araç örneği 1.

**Konular:** volatility, indicator_systems, breakout_failure, trend_regime, risk_management

**Kart:** `PTA-C1-2026.p0054`

### PDF s. 55 — 8.8 — Kırılım sistemi için pratik akış

Araç Ana soru Matematik sınıfı Yanlış eşitleme Donchian N-periyot sınırı nerede kırıldı? Doğrudan en yüksek/en düşük “Üst bant = aşırı alım.” PROFESYONEL KOMBİNASYON ÖRNEĞİ ATR düşük → piyasa sakin. Donchian üst sınırı kırılıyor → yönlü giriş işareti.

**Konular:** indicator_systems, risk_management, volatility, volume_flow

**Kart:** `PTA-C1-2026.p0055`
