# PTA-C1-2026 — Bölüm 1

**PDF sayfaları:** 6–9
**Sayfa kartları:** 4

## Alt başlıklar

- 1.1 — İndikatörün adı değil, görevi önemlidir
- 1.3 — Üç indikatör aynı şeyi söylüyorsa üç teyit yoktur
- 1.5 — Ayarları geçmişe uydurma riski (geçmişe aşırı uyum)
- 1.6 — Minimal sistem testi

## Konu dağılımı

- `momentum`: 3 sayfa
- `volatility`: 3 sayfa
- `risk_management`: 3 sayfa
- `trend_regime`: 3 sayfa
- `volume_flow`: 1 sayfa
- `breakout_failure`: 1 sayfa
- `validation_replay`: 1 sayfa

## Sayfa şeritleri

### PDF s. 6 — 1.1 — İndikatörün adı değil, görevi önemlidir

BÖLÜM 1 İndikatörleri Doğru Kullanma Mantığı Bir indikatörü öğrenmeden önce, ondan hangi bilgiyi istemeniz gerektiğini öğrenin. Grafiğe indikatör eklemek kolaydır. Zor olan, her aracın hangi soruya cevap verdiğini ve hangi soruya cevap veremediğini bilmektir.

**Konular:** volume_flow, momentum, volatility, risk_management, trend_regime

**Kart:** `PTA-C1-2026.p0006`

### PDF s. 7 — 1.3 — Üç indikatör aynı şeyi söylüyorsa üç teyit yoktur

Bilgi sınıfı Sorduğu soru Örnek araç Tek başına söylemez Katılım / hacim Harekete aktivite eşlik ediyor mu? Volume Devam garantisini Yapı Belirgin dönüş ve kırılım davranışı ne? Fiyat yapısı, S/R Hareketin ne kadar güçlendiğini/zayıfladığını 1.2 — Bağlam, konum, giriş işareti ve risk aynı şey değildir Bir sistemde “işleme uygun ortam” ile “şimdi giriş yap” kararı ayrılmalıdır.

**Konular:** risk_management, momentum, trend_regime, volatility, breakout_failure

**Kart:** `PTA-C1-2026.p0007`

### PDF s. 8 — 1.5 — Ayarları geçmişe uydurma riski (geçmişe aşırı uyum)

Kombinasyon Rol dağılımı Değerlendirme RSI + Stoch + Stoch RSI Hareket gücü + hareket gücü + hareket gücü Yüksek tekrar riski MA + MACD kesişim Trend bilgisi + MA farkından gelen benzer trend/hareket gücü bilgisi Kısmi tekrar MA + RSI + ATR Yön + hareket gücü + fiyat hareketliliği/risk Daha tamamlayıcı Fiyat yapısı + AVWAP + RSI Yapı + konum + hareket gücü Daha bağımsız bilgi 1.4 — “Klasik kural” neden bazen bozulur? Teknik analiz eğitimlerinde kısa kurallar işe yarar: “RSI 70 üstü aşırı alım”, “ADX 25 üstü güçlü trend”, “fiyat 200 MA üstünde yükseliş yönlü”. Sorun, bu cümleleri her piyasada geçerli yasa gibi kullanmaktır.

**Konular:** momentum, volatility, trend_regime, validation_replay, risk_management

**Kart:** `PTA-C1-2026.p0008`

### PDF s. 9 — 1.6 — Minimal sistem testi

1.6 — Minimal sistem testi Yeni bir indikatör eklemeden önce şu testi uygulayın:  Bu araç hangi soruyu cevaplıyor?  Aynı bilgiyi başka bir araç zaten veriyor mu?  Bu aracı kaldırırsam karar mantığım gerçekten zayıflıyor mu?

**Konular:** referans

**Kart:** `PTA-C1-2026.p0009`
