# PTA-C1-2026 — Bölüm 12

**PDF sayfaları:** 74–78
**Sayfa kartları:** 5

## Alt başlıklar

- 12.2 — +DM ve −DM nereden gelir?
- 12.3 — ADX yükselirken fiyat neden düşebilir?
- 12.4 — 20 ve 25 eşikleri neden fizik yasası değildir?
- 12.6 — ADX tepesi fiyat tepesi değildir
- 12.7 — +DI / −DI kesişimi neden otomatik giriş değildir?

## Konu dağılımı

- `trend_regime`: 5 sayfa
- `risk_management`: 2 sayfa
- `volatility`: 2 sayfa
- `breakout_failure`: 1 sayfa
- `momentum`: 1 sayfa

## Sayfa şeritleri

### PDF s. 74 — 12.2 — +DM ve −DM nereden gelir?

BÖLÜM 12 ADX ve DMI: Yön ile Gücü Ayırmak ADX tek başına “fiyat yukarı mı gidiyor, aşağı mı?” demez. Asıl görevi hareketin ne kadar güçlü olduğunu ölçmektir. Yönü anlamak için +DI ve −DI çizgilerine, daha önemlisi fiyatın kendi yapısına bakılır.

**Konular:** trend_regime, risk_management

**Kart:** `PTA-C1-2026.p0074`

### PDF s. 75 — 12.3 — ADX yükselirken fiyat neden düşebilir?

Örnek Hesap Sonuç Bar A → Bar B Önceki H=100, L=92; Yeni H=104, L=93. +DM=4, −DM=0 Bar B → Bar C Önceki H=104, L=93; Yeni H=103, L=88. +DM=0, −DM=5 TEKNİK ZİNCİR +DM / −DM → True Range → Wilder tipi yumuşatma → +DI / −DI → DX → ADX.

**Konular:** trend_regime, volatility

**Kart:** `PTA-C1-2026.p0075`

### PDF s. 76 — 12.4 — 20 ve 25 eşikleri neden fizik yasası değildir?

12.4 — 20 ve 25 eşikleri neden fizik yasası değildir? 20 ve 25 yaygın ADX referanslarıdır; kesin sınırlar değildir. Enstrüman, zaman dilimi ve piyasa davranışı değiştikçe aynı eşik farklı anlam taşıyabilir.

**Konular:** trend_regime

**Kart:** `PTA-C1-2026.p0076`

### PDF s. 77 — 12.6 — ADX tepesi fiyat tepesi değildir

12.5 — ADX’i tek eşik yerine dört hareket evresiyle okumak ADX’in yalnız 20 veya 25’in üzerinde olup olmadığına bakmak yerine seviyesi ile eğimi birlikte değerlendirilebilir. Düşük + düşen Yönlü güç zayıf / düzensiz ortam olabilir Yönün ne olduğunu Düşük + yükselen Yönlü güç oluşmaya başlıyor olabilir Yeni trendin kesin başladığını Yüksek + yükselen Mevcut yönlü güç artıyor olabilir Yükseliş mi düşüş mü olduğunu Yüksek + düşen Trend artık önceki hızda güçlenmiyor Trendin bittiğini Bu dört durum, “ADX 25’in üstünde = güçlü trend” cümlesinden daha fazla bağlam taşır. Kesikli 25 çizgisi yalnız referanstır; ADX’in yükselmesi veya düşmesi yönü tek başına söylemez.

**Konular:** trend_regime

**Kart:** `PTA-C1-2026.p0077`

### PDF s. 78 — 12.7 — +DI / −DI kesişimi neden otomatik giriş değildir?

12.7 — +DI / −DI kesişimi neden otomatik giriş değildir? DI kesişimi yukarı ve aşağı hareket arasındaki üstünlüğün değiştiğini gösterir. Fiyatın iyi bir bölgede olduğunu veya stopun nerede olması gerektiğini söylemez.

**Konular:** breakout_failure, trend_regime, volatility, momentum, risk_management

**Kart:** `PTA-C1-2026.p0078`
