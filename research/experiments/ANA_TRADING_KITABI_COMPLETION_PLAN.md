# Ana Trading Kitabı Eksiksiz Tamamlama Planı

## Kaynak

- **Kimlik:** `ATK-TR-D1.0-2026-08`
- **Eser:** Ana Trading Kitabı — Dijital Sürüm 1.0
- **Sayfa:** 530
- **Bölüm:** 24
- **Mevcut bilgi tabanı:** 530/530 sayfa kartı, 24/24 bölüm sentezi

## Amaç

Kitabın her atomik iddiasını kaynak sayfası, kullanım amacı ve uygun olduğu yerde matematiksel/nedensel deney tanımıyla kapatmak. Kitap yalnız OHLCV teknik analizden oluşmadığı için bütün iddialar zorla fiyat testi hâline getirilmeyecek. Her claim aşağıdaki nihai sınıflardan birine girecek:

1. `tested`
2. `tested_as_variant`
3. `context_only`
4. `duplicate_information`
5. `chance_like`
6. `negative`
7. `insufficient_sample`
8. `data_unsuitable`
9. `external_data_required`
10. `not_ohlcv_testable`
11. `process_rule`
12. `reference_only`
13. `deferred_ob_fvg`
14. `deferred_execution_portfolio`

Olumsuz, veri-uygunsuz ve ölçülemeyen sonuçlar silinmeyecek.

---

# Değişmez çalışma ilkeleri

- 530/530 sayfa nihai disposition alacak.
- Her test edilebilir atomik claim `BR-ATK-xxx` kimliği alacak.
- Kaynak, asistan çıkarımı ve test hipotezi ayrı tutulacak.
- Cilt 1 ve Cilt 2’de zaten ölçülen bilgi yeniden “yeni keşif” sayılmayacak; mevcut BR kurallarıyla çapraz bağlantı kurulacak.
- OHLCV ölçümlerinde yalnız kapanmış barlar ve teyit anında bilinen yapı kullanılacak.
- 125 varlık ve uygun 1h/2h/4h/1d evreni korunacak.
- BIST için XU100-aşırı sonuç; kronolojik ve ortak takvim ayrımı; sembol tutarlılığı; MFE/MAE bulunacak.
- Hacim yalnız veri-uygun gruplarda kullanılacak.
- Parametre komşuluğu ve bilgi tekrarı kontrol edilecek.
- İşlem/portföy simülasyonunun ayrıntıları mevcut kullanıcı talebine uygun biçimde ertelenecek; araştırma ve ürün amacı öncelikli kalacak.
- OB/FVG için yeni ana sistem kurulmayacak; ilgili claim’ler `deferred_ob_fvg` olarak kullanıcının sistemiyle bağlantı kurulmasını bekleyecek.
- Temel, tahvil, opsiyon, zincir üstü ve arbitraj iddialarında veri yoksa sonuç uydurulmayacak; `external_data_required` kaydı tutulacak.

---

# Çalışma paketleri

## ATK-P1 — 530 sayfa kapsamı ve atomik claim registry

### Yapılacaklar

- 530 sayfanın kaynak özetlerini atomik iddialara ayır.
- 24 bölümün bütün alt başlıklarını claim’lere bağla.
- Her claim için kaynak sayfası, konu, veri gereksinimi, test edilebilirlik ve hedef paket kaydet.
- Mevcut BR-001–BR-034 ve BR-C1-001–BR-C1-022 bağlantılarını çıkar.
- Tekrar eden iddiaları silmeden `duplicate_information` veya mevcut kural bağlantısıyla koru.
- Formül sözlüğü ve unresolved dosyası oluştur.

### Çıktılar

```text
atk-page-coverage.csv
atk-claim-registry.json
atk-formula-registry.json
atk-unresolved-claims.csv
cross-book-rule-map.csv
```

## ATK-P2 — Price action, swing ve piyasa yapısı

### Bölümler

2–3.

### Ölçülecekler

- Mumun gövde, fitil, kapanış ve bağlam boyutları.
- Swing high/low ve teyit gecikmesi.
- HH/HL/LH/LL dizileri.
- Trend, range ve geçiş durumu.
- Yapı kırılımı, acceptance ve failure.
- Hareket kalitesi, yol verimliliği ve baskı kaybı.

### Mevcut bilgi bağlantısı

Cilt 2 BR-024–BR-030 sonuçlarıyla çapraz bağlanacak; yalnız yeni tanım veya yeni bağlam varsa yeni deney açılacak.

## ATK-P3 — Bölge, destek/direnç ve likidite dili

### Bölümler

4–5.

### Ölçülecekler

- Çizgi yerine ATR-normalize bölge genişliği.
- Teyitli destek/direnç yaşı ve temas sayısı.
- Eşit tepe/dip kümeleri.
- Önceki gün/hafta uçları.
- Fitille taşma, kapanış kırılımı, failure ve karşı genişleme.
- Likidite havuzu için yalnız OHLCV’den gözlenebilir vekiller.

### Sınır

Gerçek bekleyen emir ve stop konumu OHLCV’den bilinemez. OB/FVG claim’leri kullanıcının sistemi gelene kadar `deferred_ob_fvg`; emir akışı iddiaları `not_ohlcv_testable` veya `external_data_required` olur.

## ATK-P4 — Formasyon ve mum aileleri

### Bölüm

6.

### Ölçülecekler

- Tek, iki ve üç mumlu formasyon aileleri.
- Dönüş/devam formasyonları.
- Omuz-baş-omuz, ikili tepe/dip, üçgen, takoz ve bayrak geometrileri.
- Formasyon tamamlanma zamanı ile görsel başlangıç zamanı ayrımı.
- Formasyon adı ile temel geometri arasındaki bilgi tekrarı.

### Mevcut bağlantı

Cilt 2 mum/dizi sonuçları ve Cilt 1 seviye araçlarıyla karşılaştırılacak.

## ATK-P5 — Hacim, indikatör ve teyit mimarisi

### Bölümler

7–8.

### Ölçülecekler

- Hacim–fiyat ilişkisi ve RVOL.
- OBV/CMF benzeri hacim türevleri için veri uygunluğu.
- MA, RSI, Stochastic, MACD, ATR, Bollinger, ADX, Supertrend ve Ichimoku.
- Aynı bilgi ailesindeki indikatör örtüşmesi.
- Fiyat davranışına marjinal katkı.

### Mevcut bağlantı

Cilt 1’in 106 parametre varyantı, MFE/MAE, ortak takvim ve ablation sonuçları temel alınacak. Kitap varyantı yeni değilse tekrar ölçüm yerine doğrudan kaynak bağlantısı kurulacak.

## ATK-P6 — Ölçüm araçları ve geometrik seviyeler

### Bölüm

9.

### Ölçülecekler

- Fibonacci retracement/extension.
- Risk/reward geometrisi; işlem simülasyonu olmadan olay sonrası MFE/MAE bağlamı.
- ATR-normalize mesafe ve uzamışlık.
- Regresyon kanalı ve standart sapma bantları.
- Anchor hassasiyeti ve teyitli swing zorunluluğu.
- Ekran ölçeğine bağlı açıların reddi.

## ATK-P7 — Çoklu zaman dilimi ve fractal yapı

### Bölüm

10.

### Ölçülecekler

- 1h olay + tamamlanmış 2h/4h bağlamı.
- 4h olay + tamamlanmış 1g bağlamı.
- Üst zaman trend/rejim/seviye konumu.
- Alt ve üst zaman uyumu/uyumsuzluğu.
- Aynı bilginin türetilmiş zaman dilimlerinde tekrar sayılması.
- As-of birleşim ve tamamlanmamış bar sızıntısı testi.

## ATK-P8 — İşlem stili, setup ve strateji kartı

### Bölümler

11–12.

### Yapılacaklar

- Strateji, setup, tetik ve işlem kavramlarını ayrı şemalara dönüştür.
- Setup’ın bağlam, konum, tetik, geçersizlik ve veri gereksinimini tanımla.
- Kullanıcının kendi indikatör ve stratejisini ekleyebileceği genel kural şeması oluştur.
- Tek sembole özel olmayan yaklaşık 70–80+ sembollük doğrulama kapısı tanımla.
- Strateji kartı JSON şeması ve replay protokolü oluştur.

### Sonuç türü

Bu paketin önemli bölümü `process_rule` ve yazılım gereksinimidir; her madde finansal sinyal gibi test edilmeyecek.

## ATK-P9 — Risk, hedef/stop ve pozisyon yönetimi sınırı

### Bölümler

13 ve 23.

### Ölçülecekler

- R birimi ve ATR-normalize geçersizlik mesafesi.
- MFE/MAE dağılımı.
- Hedef ve stopun aynı barda görülmesi durumunda `ambiguous`.
- Sabit hedef yerine yapı/volatiliteye göre olay sonrası yol.
- Maliyet ve kayma stresleri.

### Erteleme sınırı

Portföy büyüklüğü, çoklu pozisyon tahsisi ve ayrıntılı execution simülasyonu `deferred_execution_portfolio` olarak tutulacak.

## ATK-P10 — Psikoloji, günlük ve süreç kalitesi

### Bölüm

14.

### Yapılacaklar

- Psikoloji iddialarını finansal sinyal değil süreç kuralı olarak ayır.
- Önceden kayıt, günlük, hata sınıfı ve karar sonrası inceleme şeması oluştur.
- Sonucu bilmeden karar kalitesi puanlaması.
- Kural ihlali, plansız işlem ve sonuç yanlılığı alanları.

### Sonuç

Büyük bölümü `not_ohlcv_testable` veya `process_rule`; sahte fiyat avantajı üretmeye zorlanmayacak.

## ATK-P11 — Platform, veri, replay ve araştırma altyapısı

### Bölüm

15.

### Yapılacaklar

- Watchlist, sembol kimliği ve veri kaynağı gereksinimleri.
- Veri audit kapıları: OHLC geometrisi, boşluk, tekrar, zaman dilimi ve kurumsal sıçrama.
- Geleceği göstermeyen replay sözleşmesi.
- Önbellek, yeniden üretilebilirlik ve deney sürümleme.
- Kullanıcı tanımlı indikatör/strateji eklenti arayüzü.

## ATK-P12 — AI destek sınırı ve insan–AI yetki modeli

### Bölüm

16.

### Yapılacaklar

- AI’nın araştırma, açıklama, kodlama ve tarama görevlerini ayır.
- AI’nın oracle veya garanti kaynağı olmadığı süreç kuralları.
- Veri sızıntısı, sonuç uydurma ve sonuca göre kural değiştirme denetimi.
- Her AI önerisi için kaynak, varsayım ve doğrulama durumu.
- Kullanıcı onayı gerektiren ürün kararları ile otomatik araştırma işlerini ayır.

## ATK-P13 — Döngü, çapraz piyasa, tahvil ve zaman bağlamı

### Bölümler

17, 20 ve 22.

### Ölçülecekler

- Trend/range/volatilite rejim döngüsü.
- XU100, GSPC, USDTRY, altın ve Brent bağlamı.
- Gün içi seans, haftanın günü ve resmi takvim.
- UTC/yerel saat/DST güvenliği.
- Mevcut tahvil verisi yeterli değilse faiz/tahvil claim’leri `external_data_required`.
- Tek çapraz piyasa değişkeninin bütün olaylarda evrensel kabul edilmemesi.

## ATK-P14 — Temel analiz ve değerleme

### Bölüm

18.

### Yapılacaklar

- Finansal tablo, oran, büyüme, borç ve nakit akışı claim’lerini veri gereksinimiyle kaydet.
- OHLCV’den ölçülemeyen iddiaları açıkça ayır.
- Gerekli fundamental veri şemasını tanımla.
- Veri sağlanmadan uydurma backtest yapılmayacak.
- Teknik olay + temel bağlam birleşimi sonraki veri aşamasına bırakılacak.

## ATK-P15 — Kripto, opsiyon ve hedge

### Bölümler

19 ve 21.

### Yapılacaklar

- Kripto spot/perpetual, funding, open interest ve zincir üstü veri ayrımı.
- Merkezi hacim ile borsa-parçalı hacim farkı.
- Opsiyon payoff matematiği, fakat veri olmadan performans iddiası yok.
- Greeks/IV/skew için gerekli veri sözleşmesi.
- Hedge ile yönlü işlem ayrımı.
- Uygun olmayan mevcut veri için `external_data_required`.

## ATK-P16 — Arbitraj, bütünleşik karar mimarisi ve nihai sağlamlık

### Bölüm

24 ve kitap genel sentezi.

### Yapılacaklar

- Aynı varlık/ürün/pair/ağ kimliği doğrulama kuralları.
- Fiyat farkında ücret, transfer süresi, likidite ve yürütme riski.
- Mevcut veri gerçek arbitraj testi için yeterli değilse açık disposition.
- Kitabın tam karar zinciri: veri → bağlam → yapı → olay → teyit → risk → inceleme.
- Her aşamanın marjinal katkısı ve bilgi tekrarı.
- Parametre komşuluğu, ortak takvim, sembol tutarlılığı, maliyet ve yanlış keşif kontrolü.
- 530/530 sayfa ve unresolved sıfır kapanışı.

---

# Deney grupları

## Doğrudan mevcut OHLCV ile ölçülebilir

- Price action ve yapı
- Mum/formasyon
- Hacim uygun grupları
- İndikatörler
- Çoklu zaman
- Seans/zaman
- Çapraz piyasa
- MFE/MAE ve maliyet stresleri

## Mevcut kurallarla bağlantılanacak

- Cilt 2 fiyat davranışı ve kırılım yaşam döngüsü
- Cilt 1 indikatör, seviye, çizim ve bilgi ailesi sonuçları

## Ek veri gerektiren

- Finansal tablolar
- Tahvil/faiz eğrisi
- Opsiyon zinciri, IV ve Greeks
- Funding/open interest/on-chain
- Gerçek emir defteri ve mikro yapı
- Gerçek çapraz borsa arbitraj yürütmesi

## Bilimsel olarak OHLCV testi yapılmayacak

- Psikoloji tavsiyeleri
- Etik ve sorumluluk
- Platform kullanım tercihleri
- AI yetki ilkeleri
- Yasal/eğitim amaçlı açıklamalar

Bunlar süreç veya referans kuralı olarak korunacak.

---

# Tamamlanma kriterleri

Ana Trading Kitabı yalnız şu koşulların tamamında tamamlanmış sayılacak:

1. 530/530 sayfada disposition.
2. Bütün atomik claim’lerde benzersiz kimlik.
3. Test edilebilir claim’lerde `BR-ATK` veya doğrulanmış mevcut BR bağlantısı.
4. Her ölçümde açık formül, parametre ve bilinebilir olay zamanı.
5. Uygun tam evren ölçümü.
6. Ham, yönlü ve BIST için XU100-aşırı sonuç.
7. Eğitim/doğrulama/test ve ortak takvim.
8. Sembol tutarlılığı.
9. MFE/MAE ve maliyet stresi.
10. Parametre komşuluğu.
11. Çapraz kitap bilgi tekrarı ve olay örtüşmesi.
12. Harici veri gereken claim’lerin açık veri sözleşmesi.
13. OB/FVG’nin `deferred_ob_fvg` kalması.
14. Execution/portföy ayrıntılarının `deferred_execution_portfolio` kalması.
15. Olumsuz, yazı-tura, yetersiz örnek ve veri-uygunsuz sonuçların korunması.
16. `atk-unresolved-claims.csv` dosyasının yalnız başlık satırı içermesi.
17. Yazılım, bilgi tabanı ve OHLCV denetimlerinin geçmesi.

---

# Hedef çıktı düzeni

```text
research/experiments/atk-completion/
├── README.md
├── atk-page-coverage.csv
├── atk-claim-registry.json
├── atk-formula-registry.json
├── atk-unresolved-claims.csv
├── cross-book-rule-map.csv
├── rule-overlap-matrix.csv
├── external-data-contracts.json
├── final-results.md
└── final-summary.json

research/experiments/atk-rule-results/
└── BR-ATK-xxx-<rule>/
    ├── source-links.json
    ├── definition.json
    ├── event-study.csv
    ├── symbol-results.csv
    ├── parameter-results.csv
    └── decision.md
```

## Uygulama sırası

```text
P1 kapsam
→ P2–P7 OHLCV ve çapraz-kitap ölçümleri
→ P8–P12 süreç/ürün/replay mimarisi
→ P13 çapraz piyasa ve zaman
→ P14–P15 harici veri sözleşmeleri
→ P16 nihai karar zinciri ve sağlamlık
```

Her paket sonuçları kaydedilip test edilecek; sonuca bakarak önceki tanım sessizce değiştirilmeyecek.
