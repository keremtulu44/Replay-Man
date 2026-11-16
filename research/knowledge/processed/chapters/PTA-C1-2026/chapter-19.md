# PTA-C1-2026 — Bölüm 19

**PDF sayfaları:** 116–120
**Sayfa kartları:** 5

## Alt başlıklar

- 19.1 — Classic Pitchfork’un üç pivot mantığı
- 19.4 — Dönüş noktalarını geçmişe uydurma hatası nasıl test edilir?
- 19.5 — Küçük pivot hatası ileri bölgelerde büyüyebilir
- 19.8 — Pitchfork kombinasyonları

## Konu dağılımı

- `geometry_tools`: 5 sayfa
- `risk_management`: 3 sayfa
- `volatility`: 2 sayfa
- `trend_regime`: 2 sayfa
- `validation_replay`: 1 sayfa
- `breakout_failure`: 1 sayfa
- `volume_flow`: 1 sayfa

## Sayfa şeritleri

### PDF s. 116 — 19.1 — Classic Pitchfork’un üç pivot mantığı

BÖLÜM 19 Andrews Pitchfork ve Varyantları: Orta Çizgi Geometrisi Pitchfork üç önemli dönüş noktası seçerek bir orta çizgi ve ona paralel sınırlar oluşturur. Önemli olan çok çizgi çizmek değil, seçilen üç noktanın neden anlamlı olduğunu ve bu geometrinin ne zaman artık işe yaramadığını bilmektir. HIZLI ROL — Ana görev: üç önemli dönüş noktasından orta çizgi ve paralel sınırlar oluşturmak.

**Konular:** geometry_tools, risk_management, volatility

**Kart:** `PTA-C1-2026.p0116`

### PDF s. 117 — 19.4 — Dönüş noktalarını geçmişe uydurma hatası nasıl test edilir?

19.2 — Schiff, Modified Schiff ve Inside neden var? Schiff, Modified Schiff ve Inside varyantları aynı pivotlardan farklı başlangıç geometrileri üretir. Bu esneklik bazı yapılara daha iyi uyum sağlayabilir; fakat kural önceden belirlenmemişse geriye dönük uydurmayı da kolaylaştırır.

**Konular:** geometry_tools

**Kart:** `PTA-C1-2026.p0117`

### PDF s. 118 — 19.5 — Küçük pivot hatası ileri bölgelerde büyüyebilir

Kontrol Geçerli yaklaşım Geçmişe aşırı uyum işareti A–B–C Önceden tanımlı büyük belirgin dönüş noktaları Fiyat ilerledikçe pivot kaydırmak Varyant Kullanım kuralı analizden önce belli Geçmişe en iyi oturan türü seçmek İhlal İhlali kaydet, yapı teyidini ayrı değerlendir Kırılan Pitchfork’u silip yenisini çizmek 19.5 — Küçük pivot hatası ileri bölgelerde büyüyebilir Pitchfork’un eğimi seçilen A–B–C pivotlarından türetilir. Başlangıç pivotlarından biri küçük miktarda kaydırıldığında ilk bölümde fark az görünebilir; çizgi ileri uzadıkça orta çizgi ve paralel sınırlar arasındaki konum farkı büyür. Bu nedenle pivotu birkaç bar ileri veya geri taşımak yalnız başlangıç noktasını değil, ilerideki bütün geometrik alanı değiştirir.

**Konular:** geometry_tools, validation_replay

**Kart:** `PTA-C1-2026.p0118`

### PDF s. 119 — 19.8 — Pitchfork kombinasyonları

19.6 — Orta çizgi ve kanal dışı kırılım nasıl okunur? Orta çizgi fiyatın kesin hedefi değildir; yalnız geometrik merkez referansıdır. Kanal dışı kapanış da otomatik trend dönüşü değildir.

**Konular:** geometry_tools, trend_regime, breakout_failure, risk_management

**Kart:** `PTA-C1-2026.p0119`

### PDF s. 120 — 19.8 — Pitchfork kombinasyonları

Pitchfork + Fibonacci Orta çizgi + oran ve hedef bölgeleri Benzer geometrik bilgi; iki ayrı teyit sayma Pitchfork + AVWAP Geometri + hacim ağırlıklı maliyet/konum Farklı veri mantığı Pitchfork + ATR Geometri + fiyat hareketliliği/risk Stopta ek pay için faydalı BÖLÜM SONUCU Önce üç anlamlı pivot, sonra Classic Pitchfork; alternatif varyant yalnız önceden tanımlı gerekçeyle. Orta çizgi ve kanal sınırları konum gösterir, tek başına giriş işareti değildir.

**Konular:** geometry_tools, volatility, risk_management, trend_regime, volume_flow

**Kart:** `PTA-C1-2026.p0120`
