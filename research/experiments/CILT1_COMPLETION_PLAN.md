# Cilt 1 Eksiksiz Deneysel Tamamlama Planı

## Amaç

139 sayfalık **Profesyonel Teknik Analiz — Cilt 1: İndikatörler ve Çizim Araçları** kaynağını yalnız okunmuş bir arşiv olarak değil; her test edilebilir atomik iddiası kaynak sayfası, matematiksel tanım, nedensel uygulama ve tam evren sonucuyla kayıtlı bir kural atlası olarak tamamlamak.

Cilt 2'deki sonuçlar Cilt 1 için bağlamdır; indikatör sinyallerinin fiyat davranışından bağımsız bilgi ekleyip eklemediği ayrıca ölçülecektir.

## Değişmez ölçüm ilkeleri

- 139/139 sayfada nihai disposition.
- Her atomik test edilebilir claim için `BR-C1-xxx`, kaynak kartı ve gerçek formül.
- İndikatör yalnız t anına kadar kapanmış barlardan hesaplanır; merkezli pencere ve geleceğe göre swing yoktur.
- 125 varlık ve uygun 1h/2h/4h/1d evreni; hacim araçlarında veri uygunluk kapısı.
- Kronolojik %60/%20/%20; ortak takvim ve sembol sonuçları.
- Ham/yönlü sonuç, BIST'te XU100-aşırı sonuç, MFE/MAE ve maliyet stresi.
- Varsayılan parametre yanında komşuluk; tek en iyi ayar seçilmez.
- Aynı bilgi ailesindeki araçlar için olay örtüşmesi ve marjinal katkı.
- Olumlu, olumsuz, yazı-tura, rejime bağlı, tekrarlı bilgi, yetersiz örnek ve veri-uygunsuz sonuçlar silinmez.
- Çizim araçlarında anchor/pivot ancak nedensel teyit sonrası kullanılabilir.

---

## C1-P1 — Sayfa, claim ve formül registry

**Kapsam:** 139 sayfanın tamamı, 21 bölüm.

- Kaynak özetlerini atomik iddialara ayır.
- Kaynak / asistan çıkarımı / test hipotezini ayrı tut.
- Formül, parametre, veri gereksinimi ve bilinebilir zamanı kaydet.
- Tekrarları bir BR altında birleştir; nüansları varyant olarak koru.
- OHLCV dışı iddiaları gerekçeli sınıflandır.

**Çıktı:** sayfa kapsamı, claim registry, unresolved CSV, formül sözlüğü.

## C1-P2 — Hareketli ortalamalar ve trend tabanı

**Bölümler:** 1–2.

- SMA, EMA ve fiyat/ortalama mesafesi.
- Eğim, ortalama sıralaması, kesişim ve gecikme.
- 20/50/100/200 komşuluğu; EMA/SMA farkı.
- Kesişim ile zaten gerçekleşmiş fiyat hareketinin bilgi tekrarı.
- Trend/range ve Cilt 2 hareket kalitesi bağlamı.

**Ana soru:** Ortalama olayı, yalnız geçmiş getiri/eğim bilgisinin üstüne katkı ekliyor mu?

## C1-P3 — Momentum osilatörleri

**Bölümler:** 3–5.

- RSI formülü, 30/50/70 bölgeleri, eşik geçişi ve failure swing.
- Stochastic %K/%D, kapanışın aralık içindeki yeri.
- MACD çizgisi, sinyal, histogram, sıfır geçişi.
- Aşırı alım/satımın dönüş mü trend devamı mı olduğu.
- RSI/Stochastic/MACD olay örtüşmesi ve marjinal bilgi.
- Divergence yalnız nedensel teyitli pivotlarla.

## C1-P4 — Volatilite ailesi

**Bölümler:** 6–8.

- True Range ve ATR; ATR yüzdesi ve normalleştirme.
- Bollinger orta/üst/alt bant, genişlik ve %B.
- Sıkışma/genişleme, bant dışı kapanış ve geri dönüş.
- Keltner/kanal benzeri volatilite bantları ve squeeze varyantları.
- Cilt 2 sıkışma/kırılım ölçümlerine ek bilgi testi.

## C1-P5 — Hacim, RVOL, VWAP ve AVWAP

**Bölümler:** 9–10.

- Hacim, RVOL ve fiyat ilerleme verimliliği.
- Kırılım/pullback/yeni uçta hacim değişimi.
- VWAP sapması ve çaprazı.
- AVWAP anchor'ı yalnız teyitli swing, kırılım veya takvim olayıyla.
- Endeks/FX temsili hacmi `data_unsuitable`.
- Hacim filtresinin fiyat davranışına marjinal katkısı.

## C1-P6 — Volume Profile ve fiyat-hacim yerleşimi

**Bölüm:** 11.

- POC, value area, HVN/LVN için önceden kayıtlı fiyat-bin tanımları.
- Rolling profil pencereleri ve yalnız geçmiş barlardan profil.
- POC/value-area kabulü, reddi ve geçişi.
- Bin sayısı ve pencere komşuluğu.
- OHLCV bar içinde hacmin fiyata dağılımının bilinmediği açıkça işaretlenir; yaklaşık dağıtım varyantları kesin emir akışı sayılmaz.

## C1-P7 — ADX/DMI, Supertrend ve Ichimoku

**Bölümler:** 12–14.

- +DM, −DM, TR, +DI, −DI ve ADX.
- ADX eşik/yükseliş kombinasyonları.
- Supertrend ATR çarpanı ve yön değişimi.
- Ichimoku Tenkan/Kijun/Senkou/Chikou; ileri çizimin geleceği görme olmadığı fakat olay zamanında yalnız bilinen verinin kullanılacağı açık uygulama.
- Üç trend sisteminin fiyat eğimi ve MA ailesine bilgi tekrarı.

## C1-P8 — Pivotlar, destek/direnç ve Fibonacci

**Bölümler:** 15–17.

- Günlük/haftalık klasik pivot ve CPR; yalnız tamamlanmış önceki dönem.
- Teyitli swinglerden destek/direnç bölgesi.
- Temas, kırılım, acceptance, retest ve failure.
- Fibonacci retracement/extension anchor'ları teyitli swing çiftlerinden.
- Seviye kalabalığı ve aynı fiyat bilgisinin tekrar sayılması.

## C1-P9 — Gann, Pitchfork ve regresyon/kanal araçları

**Bölümler:** 18–20.

- Gann açılarında ekran açısı yerine fiyat/zaman ölçeği.
- Pitchfork üç pivotu ve varyantları; pivotlar teyitten sonra etkin.
- Regresyon/standart sapma kanalları ve eğim.
- Anchor hassasiyeti, komşu pivotlar ve çizim öznel seçiminin sonuç etkisi.
- Yeterli nedensel tanım kurulamayan iddialar `not_ohlcv_testable` veya `insufficient_definition`.

## C1-P10 — Bilgi aileleri ve minimal sistem

**Bölümler:** 1 ve 21.

Araçları rol bazında grupla:

1. Yön/trend
2. Momentum
3. Volatilite
4. Katılım/hacim
5. Yapı/konum
6. Risk

- Aynı aile içi sinyal Jaccard örtüşmesi.
- Getiri korelasyonu ve koşullu karşılıklı bilgi vekilleri.
- Bir aracı çıkarınca karar/avantaj değişimi.
- Aynı bilgiyi üç kez sayan kombinasyonları `duplicate_information` olarak işaretle.

## C1-P11 — Birleşik sistemler ve marjinal karar zinciri

- Fiyat davranışı tabanı → tek indikatör → bağımsız aile → çoklu aile sırası.
- Her aşamada olay kaybı, benchmark-aşırı medyan ve sembol tutarlılığı.
- MA+RSI+ATR, yapı+AVWAP+RSI gibi önceden kayıtlı kombinasyonlar.
- Sonuca göre kombinasyon üretme yok.
- Ek filtre örnek azaltıyor ama avantaj eklemiyorsa `redundant_filter`.

## C1-P12 — Sağlamlık, maliyet ve nihai kapanış

- Parametre komşuluğu ve zaman dilimi kararlılığı.
- Eğitim/doğrulama/test ile ortak takvim kontrolü.
- Sembol medyanı ve pozitif sembol oranı.
- XU100-aşırı sonuçlar.
- %0/%0,10/%0,25/%0,50 maliyet.
- Çoklu hipotez/yanlış keşif kaydı; en iyi varyant yerine aile düzeyi sonuç.
- Olay örtüşme matrisi.
- 139/139 disposition; unresolved sıfır.
- Yazılım, bilgi tabanı ve veri denetimi.

---

## Beklenen çıktı düzeni

```text
research/experiments/cilt1-completion/
├── cilt1-page-coverage.csv
├── cilt1-claim-registry.json
├── cilt1-unresolved-claims.csv
├── formula-registry.json
├── rule-overlap-matrix.csv
├── final-results.md
└── final-summary.json

research/measurements/
├── cilt1-moving-averages/
├── cilt1-momentum/
├── cilt1-volatility/
├── cilt1-volume-vwap/
├── cilt1-volume-profile/
├── cilt1-trend-systems/
├── cilt1-level-tools/
├── cilt1-drawing-tools/
├── cilt1-information-families/
└── cilt1-decision-robustness/
```

## Tamamlanma tanımı

Cilt 1 yalnız 139 sayfanın tamamı kapandığında, bütün test edilebilir atomik claim'ler gerçek BR kimliği ve formülle bağlı olduğunda, uygun evrende nedensel ölçümler çalıştığında, başarısız sonuçlar korunduğunda ve unresolved dosyası boş olduğunda tamamlanmış sayılır.
