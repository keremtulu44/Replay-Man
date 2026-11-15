# PTA-C1-2026 — Bölüm 3

**PDF sayfaları:** 15–21
**Sayfa kartları:** 7

## Alt başlıklar

- 3.2 — RSI sayısı matematiksel olarak nereden gelir?
- 3.3 — 70 neden otomatik SAT değildir?
- 3.6 — Uyumsuzluk (divergence): uyarı var, kesin zaman yok
- 3.7 — RSI çalışma aralığının kayması (Range Shift)
- 3.9 — Gizli yükseliş uyumsuzluğu: fiyat yapısı zayıflığa rağmen korunuyor
- 3.11 — RSI + Stochastic + Stoch RSI: üç teyit mi?

## Konu dağılımı

- `momentum`: 7 sayfa
- `risk_management`: 3 sayfa
- `volume_flow`: 3 sayfa
- `trend_regime`: 3 sayfa
- `volatility`: 2 sayfa
- `support_resistance`: 1 sayfa
- `breakout_failure`: 1 sayfa
- `fundamental_derivatives`: 1 sayfa
- `strategy_design`: 1 sayfa

## Sayfa şeritleri

### PDF s. 15 — 3.2 — RSI sayısı matematiksel olarak nereden gelir?

BÖLÜM 3 RSI: Aşırı Alım / Aşırı Satımın Ötesi 70 ve 30 seviyelerini otomatik satış ve alış düğmesi gibi kullanmayın. Önce RSI’nın fiyat hareketinin gücü hakkında ne söylediğini anlayın. HIZLI ROL — Ana görev: fiyat hareketinin ne kadar güçlü olduğunu görmek.

**Konular:** momentum, volatility, risk_management, volume_flow

**Kart:** `PTA-C1-2026.p0015`

### PDF s. 16 — 3.3 — 70 neden otomatik SAT değildir?

Bu hesap önemli bir ayrımı gösterir: RSI fiyatın ekonomik olarak ucuz veya pahalı olduğunu hesaplamaz. Son dönemdeki yukarı ve aşağı hareketlerin birbirine göre ne kadar güçlü olduğunu sayısallaştırır. TEKNİK AYRINTI — FORMÜLÜ NEDEN BİLİYORUZ?

**Konular:** momentum, trend_regime, volume_flow

**Kart:** `PTA-C1-2026.p0016`

### PDF s. 17 — 3.6 — Uyumsuzluk (divergence): uyarı var, kesin zaman yok

3.4 — 30 neden otomatik AL değildir? Güçlü düşüş trendinde RSI uzun süre düşük bölgede kalabilir. “RSI 30 altı = fiyat ucuz” ifadesi iki ayrı kavramı karıştırır: hareket gücü zayıflığı ile değerleme.

**Konular:** momentum, trend_regime, risk_management, support_resistance, volume_flow

**Kart:** `PTA-C1-2026.p0017`

### PDF s. 18 — 3.7 — RSI çalışma aralığının kayması (Range Shift)

Bu bir uyarıdır; kendi başına giriş zamanlaması değildir. Uyumsuzluk “fiyat ve hareket gücü aynı hızda ilerlemiyor” bilgisidir. Buradan “fiyat şimdi dönecek” sonucu çıkarmak ikinci ve kanıtlanmamış bir varsayım ekler.

**Konular:** momentum, trend_regime

**Kart:** `PTA-C1-2026.p0018`

### PDF s. 19 — 3.9 — Gizli yükseliş uyumsuzluğu: fiyat yapısı zayıflığa rağmen korunuyor

ÖNEMLİ AYRIM Çalışma aralığı kayması bir giriş işareti değildir. Piyasa ortamındaki hareket gücü davranışını sınıflandırmaya yardım eder; işlem kararı için fiyat yapısı ve fiyat davranışı ayrıca değerlendirilmelidir. 3.8 — Başarısız salınım (Failure Swing): RSI’nın kendi tepe ve dip yapısını okumak Uyumsuzlukta fiyat ile RSI karşılaştırılır.

**Konular:** momentum, breakout_failure

**Kart:** `PTA-C1-2026.p0019`

### PDF s. 20 — 3.11 — RSI + Stochastic + Stoch RSI: üç teyit mi?

Bu yapı grafiğin herhangi bir yerinde aynı anlama gelmez. Öncesinde yükseliş yönlü fiyat yapısının bulunması gerekir. Asıl bilgi “RSI düştü” değil, RSI’daki zayıflığa rağmen fiyatın daha yüksek dip yapısını korumasıdır.

**Konular:** momentum, risk_management, volatility, fundamental_derivatives, strategy_design

**Kart:** `PTA-C1-2026.p0020`

### PDF s. 21 — 3.11 — RSI + Stochastic + Stoch RSI: üç teyit mi?

BÖLÜM SONUCU RSI’yı “70/30 sinyal makinesi” olarak kullanmak yerine, önceden tanımlanmış yapı ve konum içinde hareket gücü katmanı olarak kullanın. Uyumsuzluk uyarıdır; aşırı alım/aşırı satım ise dönüş garantisi değildir.

**Konular:** momentum

**Kart:** `PTA-C1-2026.p0021`
