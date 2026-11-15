# PTA-C1-2026 — Bölüm 4

**PDF sayfaları:** 22–27
**Sayfa kartları:** 6

## Alt başlıklar

- 4.1 — Stochastic sayısı nereden gelir?
- 4.4 — 80 neden otomatik SAT, 20 neden otomatik AL değildir?
- 4.5 — Trend içi geri çekilme kullanımının mantığı
- 4.6 — Stochastic RSI neden daha hassastır?
- 4.9 — 50 orta çizgisi ne anlatır?
- 4.10 — Üç osilatörü üst üste koymak neden sorun?

## Konu dağılımı

- `momentum`: 6 sayfa
- `trend_regime`: 5 sayfa
- `risk_management`: 3 sayfa
- `pullback`: 3 sayfa
- `strategy_design`: 1 sayfa
- `volatility`: 1 sayfa

## Sayfa şeritleri

### PDF s. 22 — 4.1 — Stochastic sayısı nereden gelir?

BÖLÜM 4 Stochastic ve Stochastic RSI Bu iki gösterge 0–100 arasında gidip geldiği için “osilatör” olarak adlandırılır. Önce neyi ölçtüklerini ayırın; 80 ve 20 seviyelerini otomatik al-sat düğmesine çevirmeyin. HIZLI ROL — Ana görev: Stochastic ile fiyatın son aralığın neresinde kapandığını, Stoch RSI ile RSI’nın kendi aralığındaki yerini görmek.

**Konular:** momentum, trend_regime, risk_management

**Kart:** `PTA-C1-2026.p0022`

### PDF s. 23 — 4.4 — 80 neden otomatik SAT, 20 neden otomatik AL değildir?

4.2 — %K ve %D çizgileri aynı şeyi göstermez Stochastic çoğu platformda iki çizgiyle gösterilir. %D ise %K’nın yumuşatılmış biçimidir; klasik kullanımda %K’nın hareketli ortalaması olarak hesaplanır. Bu nedenle %K–%D kesişimi iki bağımsız gösterge kesişimi değildir.

**Konular:** momentum, trend_regime, pullback

**Kart:** `PTA-C1-2026.p0023`

### PDF s. 24 — 4.5 — Trend içi geri çekilme kullanımının mantığı

İlk 80 teması otomatik satış işareti değildir. TEKNİK SORUN — “AŞIRI ALIM” KELİMESİ “Aşırı alım” ifadesi psikolojik olarak “artık düşmeli” çağrışımı yapar. Stochastic’in matematiği ise yalnız kapanışın yakın dönem aralığında yüksek bir konumda olduğunu söyler.

**Konular:** momentum, trend_regime, pullback

**Kart:** `PTA-C1-2026.p0024`

### PDF s. 25 — 4.6 — Stochastic RSI neden daha hassastır?

AYAR UYARISI K=20, D=1 gibi ayarlar yalnız bir kullanım tercihi olabilir. Bu değerler “Stochastic’in doğru ayarı” değildir. Ayar, strateji ve zaman dilimiyle birlikte değerlendirilmelidir.

**Konular:** momentum, strategy_design

**Kart:** `PTA-C1-2026.p0025`

### PDF s. 26 — 4.9 — 50 orta çizgisi ne anlatır?

4.7 — Daha hassas = daha iyi değildir Stoch RSI’nın yüksek hassasiyeti daha erken tepki sağlayabilir; aynı özellik yatay veya gürültülü piyasada daha fazla yanlış sinyal üretir. Daha hızlı tepki, daha yüksek doğruluk değildir. Araç Neyi 0–100 aralığına dönüştürür?

**Konular:** momentum, pullback, risk_management, trend_regime

**Kart:** `PTA-C1-2026.p0026`

### PDF s. 27 — 4.10 — Üç osilatörü üst üste koymak neden sorun?

4.10 — Üç osilatörü üst üste koymak neden sorun? Üç araç aynı formülü kullanmaz; ancak aynı karar katmanında yoğunlaşır ve Stoch RSI doğrudan RSI’dan türetilir. Bu nedenle eşzamanlı sinyalleri üç bağımsız teyit değildir.

**Konular:** momentum, volatility, risk_management, trend_regime

**Kart:** `PTA-C1-2026.p0027`
