# PTA-C1-2026 — Bölüm 16

**PDF sayfaları:** 95–103
**Sayfa kartları:** 9

## Alt başlıklar

- 16.1 — Destek ve direnç: çizgiden önce bölge düşünün
- 16.2 — Seviyeyi temas sayısıyla değil, fiyatın verdiği tepkiyle değerlendirin
- 16.3 — Trend çizgisinin asıl problemi: iki nokta her zaman bir doğru
- 16.6 — Trend çizgisinde temas sıklığı ve yeniden test davranışı
- 16.7 — Ekrandaki açı bir piyasa sabiti değildir
- 16.8 — Paralel Kanal: ikinci çizgiyi bağımsız uydurmayın
- 16.10 — Çoklu zaman diliminde çizim sırası
- 16.11 — TradingView çizim araçları: analiz değişmesin
- 16.12 — Çizim yaparken 8 soruluk kontrol

## Konu dağılımı

- `trend_regime`: 8 sayfa
- `support_resistance`: 4 sayfa
- `risk_management`: 2 sayfa
- `psychology_process`: 2 sayfa
- `breakout_failure`: 2 sayfa
- `volatility`: 1 sayfa
- `volume_flow`: 1 sayfa
- `candle_behavior`: 1 sayfa
- `fundamental_derivatives`: 1 sayfa
- `geometry_tools`: 1 sayfa
- `market_structure`: 1 sayfa
- `multi_timeframe`: 1 sayfa
- `automation_ai`: 1 sayfa
- `ohlcv_data`: 1 sayfa

## Sayfa şeritleri

### PDF s. 95 — 16.1 — Destek ve direnç: çizgiden önce bölge düşünün

BÖLÜM 16 Trend Çizgileri, Yatay Seviyeler ve Kanallar Çizgi çizmek kolaydır. Zor olan, hangi iki noktanın neden seçildiğini ve çizginin neyi kanıtlamadığını bilmektir. HIZLI ROL — Ana görev: fiyat hareketini çizgiler ve bölgelerle daha kolay okumak.

**Konular:** support_resistance, trend_regime, risk_management, volatility

**Kart:** `PTA-C1-2026.p0095`

### PDF s. 96 — 16.2 — Seviyeyi temas sayısıyla değil, fiyatın verdiği tepkiyle değerlendirin

SAYISAL ÖRNEK Dört belirgin reaksiyon 99,80 / 100,20 / 100,40 / 100,00 seviyelerinde oluşsun. “Doğru destek 100,00’dır” demek gereksiz hassasiyettir. 99,60–100,50 gibi önceden tanımlanmış bir reaksiyon bölgesi dağılımı daha dürüst temsil eder.

**Konular:** support_resistance

**Kart:** `PTA-C1-2026.p0096`

### PDF s. 97 — 16.3 — Trend çizgisinin asıl problemi: iki nokta her zaman bir doğru

Bu nedenle: bölgenin dışına çıkış ≠ bölgenin dışında kabul. Kısa ihlal ve hızlı geri dönüş, ilk kırılımın devam edemediğini gösteren ayrı bir fiyat davranışıdır. Yine de otomatik dönüş sinyali değildir; fiyat yapısı ayrıca değerlendirilmelidir.

**Konular:** trend_regime, volume_flow, psychology_process

**Kart:** `PTA-C1-2026.p0097`

### PDF s. 98 — 16.6 — Trend çizgisinde temas sıklığı ve yeniden test davranışı

16.4 — Trend çizgisi aslında çoğu zaman bir “trend alanı”dır Trend çizgisini tek ve kesin bir sınır yerine dar bir referans alanı olarak düşünmek çoğu durumda daha sağlıklıdır. Özellikle fitil çizgiyi aşıp kapanış yeniden alan içinde kaldığında, yalnız temasa değil kapanışa ve sonraki fiyat davranışına bakın. YANLIŞ / DOĞRU YANLIŞ: “Fitil çizginin altına indi → yükseliş trendi bitti.” DOĞRU: “Trend referans alanı ihlal edildi.

**Konular:** trend_regime, candle_behavior, breakout_failure

**Kart:** `PTA-C1-2026.p0098`

### PDF s. 99 — 16.7 — Ekrandaki açı bir piyasa sabiti değildir

Ardışık temaslar arasındaki süre kısalıyor, fiyat çizgiden eskisi kadar uzaklaşamıyor ve çizginin çevresinde daha fazla zaman geçiriyorsa fiyatın çizgiden önceki kadar güçlü uzaklaşmadığı görülür. Bu yapı kırılım garantisi değildir. Daha doğru okuma, mevcut trend çizgisi geometrisinin reaksiyon gücünün zayıfladığıdır.

**Konular:** trend_regime, breakout_failure, fundamental_derivatives, geometry_tools, market_structure

**Kart:** `PTA-C1-2026.p0099`

### PDF s. 100 — 16.8 — Paralel Kanal: ikinci çizgiyi bağımsız uydurmayın

16.8 — Paralel Kanal: ikinci çizgiyi bağımsız uydurmayın Paralel Kanal iki bağımsız trend çizgisinden oluşmaz. İlk sınır eğimi tanımlar; karşı sınır aynı eğim korunarak paralel taşınır. Böylece iki kenarı da geçmiş fiyata ayrı ayrı uydurma riski azaltılır.

**Konular:** trend_regime

**Kart:** `PTA-C1-2026.p0100`

### PDF s. 101 — 16.10 — Çoklu zaman diliminde çizim sırası

16.9 — Yatay seviye, trend çizgisi ve yapı birlikte nasıl kullanılır? Önce belirgin tepe/diplerle fiyat yapısını okuyun; ardından destek/direnç bölgelerini ve gerekiyorsa trend kanalını ekleyin. Çizim konumu gösterir, giriş ise fiyatın o bölgede verdiği davranışla doğrulanmalıdır.

**Konular:** trend_regime, support_resistance, multi_timeframe, psychology_process, risk_management

**Kart:** `PTA-C1-2026.p0101`

### PDF s. 102 — 16.11 — TradingView çizim araçları: analiz değişmesin

16.11 — TradingView çizim araçları: analiz değişmesin TradingView araçları analiz yönteminin yerine geçmez; yalnız çizimin yanlışlıkla kaymasını azaltır. Mıknatıs (Magnet), çizimleri kilitleme, kopyalama ve bar-kapanış alarmını bu amaçla kullanın. Araç Faydalı kullanım Dikkat Magnet (Mıknatıs) Başlangıç noktasını gerçek OHLC değerine daha hassas bağlamak Güçlü mıknatıs yanlış noktaya yapışırsa kontrol et Lock Drawings (Çizimleri Kilitle) Analiz bittikten sonra başlangıç noktalarının kazara kaymasını önlemek Yanlış çizimi kilitlemek onu doğru yapmaz Clone (Kopyala) Aynı eğim ile paralel kanal oluşturmak Kopyayı bağımsız eğmek kanal mantığını bozar Bar-kapanış alarmı Çizgi/bölge ihlalini ekran başında beklemeden izlemek Alarm = işlem emri değildir

**Konular:** trend_regime, automation_ai, ohlcv_data

**Kart:** `PTA-C1-2026.p0102`

### PDF s. 103 — 16.12 — Çizim yaparken 8 soruluk kontrol

16.12 — Çizim yaparken 8 soruluk kontrol  Bu çizimin görevi ne: yön, konum, sınır mı; yoksa yalnız görsel açıklama mı?  Başlangıç noktaları anlamlı dip/tepelerden mi seçildi, yoksa çizgiyi güzel göstermek için mi?  Grafiğin sağ tarafını kapatsaydım aynı başlangıç noktalarını seçer miydim?

**Konular:** trend_regime, support_resistance

**Kart:** `PTA-C1-2026.p0103`
