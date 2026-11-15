# PTA-C1-2026 — Bölüm 7

**PDF sayfaları:** 43–49
**Sayfa kartları:** 7

## Alt başlıklar

- 7.1 — Üç bant neyi temsil eder?
- 7.3 — Üst banda temas neden otomatik SAT değildir?
- 7.4 — Bant sıkışması neyi söyler?
- 7.5 — Bant Genişliği (BandWidth): sıkışmadan genişlemeye hareketlilik
- 7.9 — Bollinger + ATR birlikte kullanılabilir mi?
- 7.10 — Bollinger için pratik karar akışı

## Konu dağılımı

- `volatility`: 7 sayfa
- `risk_management`: 4 sayfa
- `trend_regime`: 3 sayfa
- `volume_flow`: 2 sayfa
- `strategy_design`: 2 sayfa
- `breakout_failure`: 2 sayfa
- `support_resistance`: 1 sayfa
- `momentum`: 1 sayfa

## Sayfa şeritleri

### PDF s. 43 — 7.1 — Üç bant neyi temsil eder?

BÖLÜM 7 Bollinger Bands: Ortalama ve Fiyat Hareketliliği Bollinger bantlarına “fiyat banda değdi, şimdi dönmeli” diye bakmayın. Bantlar, fiyatın kendi ortalaması çevresinde ne kadar dar veya geniş hareket ettiğini görmeye yarayan bir çerçevedir. HIZLI ROL — Ana görev: fiyatın ortalama çevresinde ne kadar dar veya geniş hareket ettiğini görmek.

**Konular:** volatility, risk_management, volume_flow

**Kart:** `PTA-C1-2026.p0043`

### PDF s. 44 — 7.3 — Üst banda temas neden otomatik SAT değildir?

Gerçek Bollinger ayarı çoğunlukla daha uzun bir pencere kullanır; burada amaç yalnız standart sapmanın ne yaptığını görünür kılmaktır. Küçük örnek hesap kolaylığı içindir, strateji parametresi değildir. 7.2 — %B: bant içindeki konumu tek sayıya dönüştürmek %B, fiyatın Bollinger bantlarına göre nerede bulunduğunu sayısallaştırır.

**Konular:** volatility, strategy_design

**Kart:** `PTA-C1-2026.p0044`

### PDF s. 45 — 7.4 — Bant sıkışması neyi söyler?

TEKNİK SORUN — “2 STANDART SAPMA = AŞIRI DEĞER” İki standart sapma, fiyatın “adil değerden aşırı uzak ve dönmek zorunda” olduğu anlamına gelmez. Bollinger bir değerleme modeli değil, ortalama çevresindeki dağılımı gösteren bir bant sistemidir. Bantların daralması, fiyatın son dönemde daha dar dağıldığını gösterir; buna bant sıkışması denir.

**Konular:** volatility

**Kart:** `PTA-C1-2026.p0045`

### PDF s. 46 — 7.5 — Bant Genişliği (BandWidth): sıkışmadan genişlemeye hareketlilik

Gözlem Doğru yorum Yanlış yorum Bantlar daralıyor Fiyat hareketliliği/dağılım daralıyor “Yukarı kırılım geliyor.” Bantlar genişliyor Hareket genişliği artıyor “Trend kesin güçlü.” Fiyat üst bantta Üst bant bölgesinde “Aşırı alım → satış yönlü işlem.” Fiyat alt bantta Alt bant bölgesinde “Ucuz → hemen al.” 7.5 — Bant Genişliği (BandWidth): sıkışmadan genişlemeye hareketlilik döngüsü Bant Genişliği (BandWidth), üst ve alt Bollinger bantları arasındaki genişliği ayrı bir seri halinde izlemeye yarar. Bant Genişliği düşerken bantlar daralır; yükselirken genişler. Sıkışmayı yalnız “bantlar dar görünüyor” diye değerlendirmek yerine, Bant Genişliği’nin enstrümanın kendi geçmişindeki konumuna bakılabilir.

**Konular:** volatility, breakout_failure, strategy_design, trend_regime

**Kart:** `PTA-C1-2026.p0046`

### PDF s. 47 — 7.9 — Bollinger + ATR birlikte kullanılabilir mi?

7.6 — İlk bant kırılımı gerçek yön olmak zorunda değildir: sahte ilk kırılım Sıkışma sonrasında fiyat önce bantlardan birinin dışına çıkabilir fakat orada kalıcı olamayarak yeniden bantların içine dönebilir. Daha sonraki belirgin hareket ilk kırılımın ters yönünde gelişebilir. Bu davranış Bollinger literatüründe “Head Fake” olarak da adlandırılır; burada sahte ilk kırılım ifadesini kullanacağız.

**Konular:** volatility, breakout_failure, support_resistance, risk_management, trend_regime

**Kart:** `PTA-C1-2026.p0047`

### PDF s. 48 — 7.9 — Bollinger + ATR birlikte kullanılabilir mi?

Kombinasyon Mantıklı görev ayrımı Tekrar riski BB + RSI/Stoch Bant konumu + hareket gücü Orta; dönüş otomatiğine dikkat BB + ATR Bant sıkışması koşulu + risk/stop Orta; ikisi de fiyat hareketliliği BB + Bollinger bant genişliği + ATR Üç fiyat hareketliliği görünümü Yüksek

**Konular:** volatility, risk_management, momentum

**Kart:** `PTA-C1-2026.p0048`

### PDF s. 49 — 7.10 — Bollinger için pratik karar akışı

7.10 — Bollinger için pratik karar akışı Adım Soru Bollinger’ın rolü 1. Piyasa ortamı Trend mi, yatay piyasa mı? Bant boyunca ilerleme ve dönüş yorumu değişir 2.

**Konular:** volatility, risk_management, trend_regime, volume_flow

**Kart:** `PTA-C1-2026.p0049`
