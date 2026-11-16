# ATK-TR-D1.0-2026-08 — Bölüm 7

**PDF sayfaları:** 128–146
**Sayfa kartları:** 19

## Alt başlıklar

- 7.1 — Hacim Verisi Ne Ölçer?
- 7.2 — Hacim–Fiyat İlişkisi ve Bağıl Hacim
- 7.3 — Trend, Pullback ve Range’de Hacim
- 7.4 — Breakout, Fakeout ve Gap Teyidi
- 7.5 — Volume Spike, Climax ve Exhaustion
- 7.7 — VWAP: Hacim Ağırlıklı Ortalama
- 7.8 — Volume Profile: Hacmi Fiyata Dağıtmak
- 7.10 — Order Book, Market–Limit Emir ve Bid–
- 7.11 — Footprint Chart ve Mum İçi Hacim
- 7.13 — Footprint Imbalance ve Stacked Imbalance
- 7.14 — Absorption, Initiation ve Order-Flow
- 7.15 — Bütünleşik Hacim ve Mikro Yapı İş Akışı

## Konu dağılımı

- `volume_flow`: 19 sayfa
- `execution_microstructure`: 12 sayfa
- `market_basics`: 9 sayfa
- `derivatives_options`: 8 sayfa
- `trend_regime`: 7 sayfa
- `breakout_failure`: 7 sayfa
- `liquidity_imbalance`: 6 sayfa
- `candle_behavior`: 3 sayfa
- `momentum`: 3 sayfa
- `support_resistance`: 3 sayfa
- `follow_through`: 2 sayfa
- `crypto_specific`: 1 sayfa
- `fundamental_derivatives`: 1 sayfa
- `sessions_timing`: 1 sayfa
- `pullback`: 1 sayfa
- `market_structure`: 1 sayfa
- `ohlcv_data`: 1 sayfa

## Sayfa şeritleri

### PDF s. 128 — Bölüm girişi/devamı

BÖLÜM 7 Hacim, Volume Profile, Order Flow ve Mikro Yapı

**Konular:** volume_flow

**Kart:** `ATK-TR-D1.0-2026-08.p0128`

### PDF s. 129 — 7.1 — Hacim Verisi Ne Ölçer?

Fiyatın Arkasındaki Katılımı Okumak Fiyat grafiği bize hareketin sonucunu gösterir. Hacim ve order-flow araçları ise bu sonucun hangi işlem aktivitesiyle oluştuğunu farklı açılardan inceler. Ancak bütün hacim araçları aynı şeyi ölçmez: standart volume zamana, volume profile fiyata, VWAP hacim ağırlıklı ortalamaya, footprint ise gerçekleşen işlemin bid–ask dağılımına odaklanır.

**Konular:** volume_flow, market_basics, execution_microstructure, crypto_specific, fundamental_derivatives

**Kart:** `ATK-TR-D1.0-2026-08.p0129`

### PDF s. 130 — 7.2 — Hacim–Fiyat İlişkisi ve Bağıl Hacim

Tek bir büyük katılımcı çok yüksek hacim üretebilir; çok sayıda küçük katılımcı ise daha düşük toplam hacimde kalabilir. Hacim, işlem aktivitesinin miktarını gösterir; katılımcı kimliğini göstermez. Her gerçekleşen işlemde bir alıcı ve bir satıcı vardır.

**Konular:** volume_flow, sessions_timing

**Kart:** `ATK-TR-D1.0-2026-08.p0130`

### PDF s. 131 — 7.3 — Trend, Pullback ve Range’de Hacim

Fiyat davranışı Hacim davranışı İlk yorum Kontrol edilmesi gereken Yükseliyor Artıyor Yukarı ilerlemeye artan katılım eşlik ediyor. Close kalitesi, direnç, follow-through. Yükseliyor Azalıyor Fiyat ilerliyor fakat katılım daralıyor.

**Konular:** volume_flow, trend_regime, execution_microstructure, market_basics, pullback

**Kart:** `ATK-TR-D1.0-2026-08.p0131`

### PDF s. 132 — 7.4 — Breakout, Fakeout ve Gap Teyidi

Piyasa durumu Sağlıklı işaret Uyarı işareti Yükseliş trendi Yukarı impulse’larda artan; geri çekilmede azalan hacim. Yeni high oluşurken hacim ve fiyat ilerlemesinin sürekli daralması. Düşüş trendi Aşağı impulse’larda artan; tepki rallisinde azalan hacim.

**Konular:** volume_flow, breakout_failure, trend_regime, candle_behavior, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0132`

### PDF s. 133 — 7.5 — Volume Spike, Climax ve Exhaustion

Kırılım işareti Olumlu teyit Fakeout uyarısı Hacim Yakın geçmişe ve aynı saate göre belirgin artış. Takip Sonraki barlarda yeni alanda acceptance. Hemen karşı mum ve eski alanın geri alınması.

**Konular:** volume_flow, breakout_failure, liquidity_imbalance, trend_regime, candle_behavior

**Kart:** `ATK-TR-D1.0-2026-08.p0133`

### PDF s. 134 — 7.7 — VWAP: Hacim Ağırlıklı Ortalama

İki farklı exhaustion davranışı vardır. Birincisinde trend uzarken katılım giderek azalır; hareket yeni ekstrem üretse bile destek daralır. İkincisinde son bir yüksek hacimli climax oluşur fakat fiyat bu çabaya rağmen ilerleyemez.

**Konular:** volume_flow, momentum, market_structure, trend_regime, breakout_failure

**Kart:** `ATK-TR-D1.0-2026-08.p0134`

### PDF s. 135 — 7.7 — VWAP: Hacim Ağırlıklı Ortalama

TEMEL FORMÜL VWAP = Σ(Fiyat × Hacim) / Σ(Hacim). Hesap yalnız seçilen session veya anchor içindeki verileri kapsar; reset noktası değişince çizgi de değişir. Fiyat rising VWAP üzerinde Session içinde hacim ağırlıklı ortalamanın üzerinde kabul.

**Konular:** volume_flow, support_resistance, trend_regime, breakout_failure, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0135`

### PDF s. 136 — 7.8 — Volume Profile: Hacmi Fiyata Dağıtmak

YAYGIN HATA VWAP’ı her zaman “institutional support” diye adlandırmak. VWAP bir benchmark ve ortalama referansıdır; tepki oluşması katılımcıların o seviyede gerçekten işlem üretmesine bağlıdır. 7.8 Volume Profile: Hacmi Fiyata Dağıtmak Standart volume her barın toplam aktivitesini zaman ekseninde gösterir.

**Konular:** volume_flow, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0136`

### PDF s. 137 — 7.10 — Order Book, Market–Limit Emir ve Bid–

Bu nedenle aynı grafikte farklı iki profile farklı POC ve value area üretebilir. Analiz öncesinde “hangi hareketi veya auction dönemini ölçüyorum?” sorusu cevaplanmalıdır. 7.9 POC, Value Area, HVN ve LVN Point of Control (POC), seçilen profilde en yüksek hacme sahip fiyat kutusudur.

**Konular:** volume_flow, execution_microstructure, market_basics, trend_regime, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0137`

### PDF s. 138 — 7.11 — Footprint Chart ve Mum İçi Hacim

Kavram Veri durumu Yorum sınırı Best bid / best ask En yüksek görünen alış ve en düşük görünen satış limiti. Başka venue’ler veya gizli likidite görünmeyebilir. Spread Best ask ile best bid farkı.

**Konular:** execution_microstructure, market_basics, volume_flow, liquidity_imbalance, ohlcv_data

**Kart:** `ATK-TR-D1.0-2026-08.p0138`

### PDF s. 139 — 7.11 — Footprint Chart ve Mum İçi Hacim

Dikkat Bid volume Bid tarafında gerçekleşen, çoğunlukla agresif satış olarak sınıflanan hacim. Sınıflandırma veri sağlayıcının trade-at-bid/ask yöntemine bağlıdır. Ask volume Ask tarafında gerçekleşen, çoğunlukla agresif alış olarak sınıflanan hacim.

**Konular:** volume_flow, execution_microstructure, market_basics, support_resistance, derivatives_options

**Kart:** `ATK-TR-D1.0-2026-08.p0139`

### PDF s. 140 — 7.13 — Footprint Imbalance ve Stacked Imbalance

7.12 Delta ve Cumulative Volume Delta Delta, belirli bar veya fiyat seviyesinde ask tarafında gerçekleşen hacim ile bid tarafında gerçekleşen hacim arasındaki farktır. Yaygın convention Delta = Ask Volume − Bid Volume şeklindedir; bazı platformlarda işaret veya sınıflandırma yöntemi farklı olabilir. DELTA FORMÜLÜ Delta = Agresif alış hacmi − agresif satış hacmi.

**Konular:** volume_flow, derivatives_options, market_basics, execution_microstructure, momentum

**Kart:** `ATK-TR-D1.0-2026-08.p0140`

### PDF s. 141 — 7.14 — Absorption, Initiation ve Order-Flow

Terim Tanım Ana kullanım Sınır Sell imbalance Bid tarafındaki hacmin karşı ask hücresine göre baskın olması. Agresif satış yoğunluğunu işaretlemek. Destekte tek başına bearish değildir.

**Konular:** volume_flow, derivatives_options, execution_microstructure, market_basics, candle_behavior

**Kart:** `ATK-TR-D1.0-2026-08.p0141`

### PDF s. 142 — 7.15 — Bütünleşik Hacim ve Mikro Yapı İş Akışı

Exhaustion’da ise ekstrem fiyatlara saldıran agresif tarafın aktivitesi azalır veya yeni fiyatlarda işlem devam etmez. İkisi birlikte görülebilir; fakat veri hikâyeleri farklıdır. YAYGIN HATA Negatif delta gördüğünüz her low’u bullish absorption saymak.

**Konular:** volume_flow, derivatives_options, breakout_failure, execution_microstructure, follow_through

**Kart:** `ATK-TR-D1.0-2026-08.p0142`

### PDF s. 143 — 7.15 — Bütünleşik Hacim ve Mikro Yapı İş Akışı

Soru Öncelikli araç Yardımcı araç Bekleyen görünür limit emirleri nerede? Order book / depth Heatmap Mum içinde hangi taraf agresifti? Footprint / delta CVD Agresyon sonuç üretti mi?

**Konular:** volume_flow, execution_microstructure, breakout_failure, derivatives_options, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0143`

### PDF s. 144 — 7.15 — Bütünleşik Hacim ve Mikro Yapı İş Akışı

Araç Tek cümlelik görev En büyük hata Absorption Yüksek çaba–düşük sonuç uyumsuzluğunu işaretler. Karşı teyit olmadan dönüş etiketi vermek.  Volume karşılaştırmam aynı zaman dilimi ve benzer seans saatleriyle mi?

**Konular:** volume_flow, market_basics, execution_microstructure, derivatives_options, follow_through

**Kart:** `ATK-TR-D1.0-2026-08.p0144`

### PDF s. 145 — 7.15 — Bütünleşik Hacim ve Mikro Yapı İş Akışı

Terim Kısa tanım Value Area Toplam profile hacminin seçilen yüzdesini kapsayan alan. VAH / VAL Value area üst ve alt sınırı. HVN / LVN Yerel yüksek / düşük hacim düğümü.

**Konular:** volume_flow, market_basics, execution_microstructure, breakout_failure, derivatives_options

**Kart:** `ATK-TR-D1.0-2026-08.p0145`

### PDF s. 146 — 7.15 — Bütünleşik Hacim ve Mikro Yapı İş Akışı

Order book ile footprint arasındaki veri farkı nedir? Delta nasıl hesaplanır ve pozitif delta neden her zaman fiyat yükselişi değildir? CVD divergence neden tek başına dönüş teyidi sayılmaz?

**Konular:** volume_flow, derivatives_options, execution_microstructure, liquidity_imbalance, momentum

**Kart:** `ATK-TR-D1.0-2026-08.p0146`
