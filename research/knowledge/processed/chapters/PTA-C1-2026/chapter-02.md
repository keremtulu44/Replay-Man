# PTA-C1-2026 — Bölüm 2

**PDF sayfaları:** 10–14
**Sayfa kartları:** 5

## Alt başlıklar

- 2.1 — SMA ile EMA arasındaki fark
- 2.2 — 20, 50 ve 200 periyot: gelenek, doğa yasası değil
- 2.5 — 50/200 (Golden Cross) kesişimi neden gecikir?
- 2.6 — Yatay piyasada neden sık yanlış sinyal oluşur?
- 2.7 — Hangi kombinasyonlar faydalı, hangileri gereksiz tekrar?

## Konu dağılımı

- `trend_regime`: 4 sayfa
- `risk_management`: 3 sayfa
- `indicator_systems`: 2 sayfa
- `momentum`: 2 sayfa
- `volatility`: 2 sayfa
- `psychology_process`: 1 sayfa
- `support_resistance`: 1 sayfa
- `position_management`: 1 sayfa
- `pullback`: 1 sayfa

## Sayfa şeritleri

### PDF s. 10 — 2.1 — SMA ile EMA arasındaki fark

BÖLÜM 2 Hareketli Ortalamalar: SMA, EMA ve Kesişim Aynı fiyatı farklı hızlarda yumuşatan bu çizgileri “geleceği bilen araçlar” gibi değil, fiyat değiştikten sonra tepki veren yön göstergeleri olarak okuyun. HIZLI ROL — Ana görev: trendin genel yönünü görmek ve geri çekilmelerde ortalamayı takip etmek. Ana risk: geç tepki vermesi ve yatay piyasada sık yanlış kesişim üretmesi.

**Konular:** indicator_systems, momentum, risk_management, volatility

**Kart:** `PTA-C1-2026.p0010`

### PDF s. 11 — 2.2 — 20, 50 ve 200 periyot: gelenek, doğa yasası değil

Hız, tek başına daha yüksek doğruluk değildir. 2.2 — 20, 50 ve 200 periyot: gelenek, doğa yasası değil 20, 50 ve 200 gibi periyotlar yaygın referanslardır; ancak “200 MA üstü = her zaman yükseliş trendi” kuralı fiyat yapısını tek çizgiye indirger. MA, trend yapısının yerine değil, trend filtresi olarak kullanılmalıdır.

**Konular:** trend_regime, psychology_process

**Kart:** `PTA-C1-2026.p0011`

### PDF s. 12 — 2.5 — 50/200 (Golden Cross) kesişimi neden gecikir?

2.3 — Hareketli ortalamaya tek bir görev verin Görev Ne için kullanılır? Trend filtresi İşlemleri ana yönle aynı tarafta aramaya yardım eder. Hayır Geri çekilme bölgesi Fiyat ortalamaya yaklaştığında izlenecek bölgeyi gösterir.

**Konular:** trend_regime, risk_management, support_resistance, position_management, pullback

**Kart:** `PTA-C1-2026.p0012`

### PDF s. 13 — 2.6 — Yatay piyasada neden sık yanlış sinyal oluşur?

50/200 kesişiminde de aynı gecikme sorunu görülür. TEKNİK AYRINTI — 50/200 (GOLDEN CROSS) 50/200 kesişimi “trend birazdan başlayacak” demek değildir. İki ortalamanın kesişebilmesi için fiyatın yeterli süre ve mesafe boyunca hareket etmiş olması gerekir.

**Konular:** trend_regime

**Kart:** `PTA-C1-2026.p0013`

### PDF s. 14 — 2.7 — Hangi kombinasyonlar faydalı, hangileri gereksiz tekrar?

TEKNİK SORUN — PİYASA ORTAMINI GÖRMEZDEN GELMEK Kesişim sistemi trend takip etmek için tasarlanmışsa, yatay piyasada da aynı başarıyı beklemek tasarım hatasıdır. Çözüm “daha iyi kesişim periyodu” aramak değil, sistemin hangi piyasa ortamında çalıştığını tanımlamaktır. 2.7 — Hangi kombinasyonlar faydalı, hangileri gereksiz tekrar?

**Konular:** indicator_systems, momentum, risk_management, volatility, trend_regime

**Kart:** `PTA-C1-2026.p0014`
