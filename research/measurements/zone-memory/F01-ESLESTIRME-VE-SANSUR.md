# F01 — eşleştirilmiş karşılaştırma ve geri gelmeyenler

**Sonuç:** F01'in önceki toplu farkı, aynı hisse ve benzer önceden bilinen özelliklere göre yapılan bu eşleştirmede daha belirsiz hale geldi. Beş bar yönlü XU100 farkının eşler arası medyanı doğrulamada **+0,41**, tarihsel testte **+1,15 yüzde puanı**; her iki dönem için haftalık ve hisse bloklarıyla keşif aralıkları sıfırı kapsıyor. Adayı doğrulanmış yön/işlem sinyali saymak için yeterli kanıt yok.

Ayrıca yalnız geri gelmiş bölgeleri değil tüm uygun aşağı geçiş adaylarını izlediğimizde, test döneminde tam 20 bar gözlemi bulunan 819 adayın **266'sında** bu süre içinde aynı bölgeye yeni ziyaret başlamadı; **61 aday** dönem/veri sınırında 20 bar için sansürlüydü. Oranlar aynı-bar temsilci seçimi ve tam pencere koşuluna bağlı betimlemelerdir, bütün bölgelerin evrensel olasılığı değildir.

## 1. Soru ve kapsam

F01: **4s yatay bölgede üstten gelip iki alt kapanışla geçen ziyaret → aynı bölgeye alttan 11 veya daha fazla kullanılabilir bar sonra geliş → ziyaretin iki alt kapanışla tamamlanması.** Karar/sonuç başlangıcı ancak ikinci ziyaretin son iki kapanışından sonradır.

Bu çalışma iki şeyi araştırır:

1. F01 tamamlanmış olaylarının, karşılaştırılabilir `aynı taraf → aynı taraf` ziyaretlerine göre sonuçları, **aynı hisse ve yakın zamanda** nasıl görünüyor?
2. İlk aşağı geçiş adayından sonra, **hiç geri gelmeyenler veya veri sonunda tam gözlenemeyenler** dahil sonraki ziyaretler nasıl dağılıyor?

Veri: 100 mevcut BIST hissesi; 4s, ATR × 0,25 yatay bölgeler; yaklaşık bir yıllık **önceden incelenmiş** arşiv. XU100 yalnız aynı başlangıç/bitiş bar etiketlerinde karşılaştırma. 4s kısmi mumlar çıkarıldığı için bar sayısı doğrulanmış 4 saatlik seans süresi değildir; `bar_ts` gerçek kapanış saati kanıtı değildir.

## 2. Eşleştirme: nasıl yapıldı?

Kaynak aynı tür/hisse/bitiş barı için seçilmiş tek temsilci tamamlanmış olaylardır. İki taraf da aşağı taraf ve 11+ bar gecikme koşulunu sağlar:

- **Vaka:** karşı tarafa geçiş → alttan yeniden ziyaret ve altta bitiş.
- **Kontrol:** önceki ve sonraki ziyaretin her ikisi geldiği tarafta bitmiş, sonraki ziyaret önceki bitiş tarafıyla aynı taraftan gelmiş.

Eşleştirme kuralları hesaplamadan önce bu çalışma için sabitlendi; ancak veri ve F01 adayı önceki çalışmalarda görüldü, **bağımsız veya ön-kayıtlı sınama değil**:

- Aynı hisse, 4s, aynı kronolojik bölüm ve aşağı bitiş tarafı.
- İkinci ziyaretlerin bitişleri arasında **en az 6, en fazla 40 kullanılabilir bar**. En az 6, bir çiftin beş barlık sonuç pencerelerinin doğrudan örtüşmesini önlemeyi amaçlar; farklı çiftler yine örtüşebilir. 10 barlık pencereler bir çiftte dahi örtüşebilir.
- Temas öncesinde bilinen `ATR14 / önceki kapanış` oranının kontrol/vaka oranı **0,75–1,33**. Bant genişliği / temas öncesi ATR oranının kontrol/vaka oranı **0,5–2,0**.
- Uygun kontroller arasından bar uzaklığı, volatilite ve bant genişliğinin normalize uzaklıkları toplamı en küçük olan seçilir; sıralama ve eşitlikler deterministiktir. Vakalar kronolojik işlenir, kontrol tekrar kullanılmaz. Eşleştirme global optimum garantisi vermez.
- Eşleşmede **gelecek getiri, XU100 sonucu veya sonucun mevcut olup olmadığı kullanılmaz**. Önce eşleştirilir; sonra her iki olayın ufku ve benchmark'ı bulunuyorsa sonuç ölçülür. Kontrol geçmişte ya da vakadan sonra olabilir: bu tarihsel analizdir, canlı karar sırasında gelecekteki kontrolü kullanma kuralı değildir.

İlk ve sonraki ziyaretlerin sadece tamamlandığı barlar kullanılır; aynı hisse ve yakın tarih tek başına tüm piyasa rejimini, bölge yaşını, geçmişi veya hareket yolunu eşitlemez. Bu çalışma nedensel etki ispatı değildir.

### Eşleşme kapsamı

| Bölüm | F01 vaka | Eşleşen çift | Eşleşmeyen vaka | 5 bar iki tarafı da ölçülebilen çift | Hisse |
|---|---:|---:|---:|---:|---:|
| Eğitim | 241 | 103 | 138 | 94 | 58 |
| Doğrulama | 136 | 49 | 87 | 45 | 34 |
| Tarihsel test | 160 | 46 | 114 | 37 | 29 |

Son sütun, **sonucu ölçülebilen çiftlerdeki** hisse sayısıdır. Eşleştirilemeyen vakalar ve eşleştirilmiş ama sonuçları eksik çiftler sonucun dışında bırakılmıştır; bu seçim nedeniyle sonuç tüm F01 vakalarına genellenemez. Testte eşleşen iki olay arasındaki medyan uzaklık **12,5 kullanılabilir bar**; kontrolün 23'ü vakadan önce, 23'ü sonradır.

## 3. Eşleşmiş sonuçlar

**Eş içi fark** = vaka yönlü sonucu − aynı hissenin eşleşmiş kontrol yönlü sonucu. Negatif/pozitif `aşağı yönlü ham getiri`, hisse getirisinin işareti ters çevrilerek oluşturulur. Endeks farkında `(hisse − XU100) × −1` kullanılır. Eş içi farkların medyanı, iki grubun medyanlarının farkıyla aynı şey değildir.

### Beş bar, yönlü XU100 farkı

| Bölüm | Tam çift / hisse | Eş içi fark medyanı | Vakası daha yüksek / kontrolü daha yüksek | Haftalık blok aralığı |
|---|---:|---:|---:|---:|
| Eğitim | 94 / 58 | **+1,00 puan** | 53 / 41 | [−0,39; +1,34] |
| Doğrulama | 45 / 34 | **+0,41 puan** | 27 / 18 | [−1,54; +1,09] |
| Tarihsel test | 37 / 29 | **+1,15 puan** | 21 / 16 | [−2,51; +2,32] |

Testte hisse bloklu keşif aralığı **[−1,79; +2,11] puan**. Her iki aralık sıfırı kapsıyor ve testte yalnız **11 hafta** var. Aralıklar 1.000 tekrarlı örneklemelerdir; hafta bloğu vakanın haftasına göre, hisse bloğu hisseye göre kuruldu. İki ayrı yeniden örnekleme, zaman/hisse/kontrol penceresi bağımlılığının tamamını çözmez. Eşleştirme sırasında daha sonra gelecek kontroller olabildiği ve aynı veride çok sayıda hipotez denendiği için bunlar bağımsız istatistiksel doğrulama değildir.

### Beş bar, ham hisse yönü

Endeksten bağımsız **aşağı yönlü ham hisse** eş içi medyan farkı: doğrulama **+0,25 puan** (45 çift), tarihsel test **−0,43 puan** (37 çift). Testte vaka 18 çiftte, kontrol 19 çiftte daha yüksek aşağı yönlü ham getiri gösterdi. Testte haftalık keşif aralığı **[−4,10; +4,16] puan**. Yönlü endeks farkının pozitif olması, eşleşmiş örnekte ham hisse hareketinin de tutarlı biçimde daha aşağı olduğu anlamına gelmiyor.

On bar sonuçları ayrı tutuldu; eşlenen iki olayın ufukları örtüşebilir ve sonuç sınırları nedeniyle çift sayısı azalır. Testte 10 bar için yönlü XU100 eş içi medyan farkı **−0,39 puan** (28 çift; haftalık aralık [−3,12; +0,95]); ham aşağı yönlü eş içi medyan farkı **−1,80 puan**. On bar ham farkın keşif blok aralığı sıfır dışına çıkmış olsa da yalnız 28 çift/9 hafta, örtüşen pencereler ve çoklu denemelerle bağımsız doğrulama sayılmaz. Tüm sonuçlar [results.csv](f01-matched/results.csv).

### Bir eşin somut kaydı

**AGHOL 4s**, vaka bitiş etiketi 8 Eylül 2026 06:30 UTC ve kontrol bitiş etiketi 18 Eylül 10:30 UTC; aralarında 17 kullanılabilir bar var. Vaka ve kontrolün temas öncesi ATR/fiyat oranları yaklaşık %2,36 ve %2,83; bant/ATR oranları 0,72 ve 0,39. Beş bar aşağı yönlü XU100 farkları sırasıyla yaklaşık **+%1,00** ve **+%2,69**; bu eşte vaka−kontrol **−1,68 yüzde puanı**. Kontrolün daha sonraki tarihli olması, bu eşin gerçek zamanlı kullanıldığı anlamına gelmez. Kimlikler ve bütün eşler [pairs.csv](f01-matched/pairs.csv), eşleşmeyenler [unmatched.csv](f01-matched/unmatched.csv).

## 4. Geri gelmeyenler ve sansür

Yeni tarama, her 4s yatay bölgenin tüm ziyaret dizisini tekrar oluşturdu. Tüm tamamlanmış ziyaretlerde hisse/bitiş barı başına temsilci seçimi **önce** yapıldı; sonra yukarı veya aşağı ilk geçiş adayı seçildi. Her aday için aynı bölgenin **ilk sonraki ziyaretinin** başlaması ve ziyaretin bitmesi 10/20/40 kullanılabilir bar içinde ayrı incelendi. Yeniden üretilen **5.765** yukarı/aşağı geçiş temsilcisi önceki kayıtla anahtar bazında bire bir eşleşti.

Aşağı adaylara ait 20 bar görünümü:

| Bölüm | Aday | 20 bar tam gözlenebilir | Dönem/veri sınırında sansürlü | Tam pencerede geri temas başlamadı | Temas başladı | Aynı tarafta tamamlandı |
|---|---:|---:|---:|---:|---:|---:|
| Eğitim | 1.542 | 1.431 | 111 | 262 | 1.169 | 700 |
| Doğrulama | 783 | 687 | 96 | 141 | 546 | 378 |
| Tarihsel test | 880 | 819 | 61 | 266 | 553 | 345 |

Testte tam penceredeki 553 geri gelişten **63'ü** 11–20 bar arasında başladı; 20 bar bitmeden hem geç başlayıp aynı tarafta tamamlanan ziyaret sayısı **33**. 202 tanesi karşı tarafta tamamlandı; 4 ziyaret pencere sonunda hâlâ açıktı, 2'si belirsizdi. Bu durumlar ve hiç dönmeyenler birbirinden ayrıdır.

Süre dolmadan dönem/veri sınırına ulaşan adayların tamamı ana 20 bar oranından `sansürlü` ayrıldı; bu 61 olayın **46'sında** sınırdan önce en az bir geri temas görülmüştü. İstenirse takip bilgilerinde erken gerçekleşen bu temaslar ayrı görülebilir; tam pencere yüzdesinin paydasına sonradan eklenmez. 40 bar için testte **356 sansürlü, 524 tam pencere** olduğundan 10/20/40 bar yüzdelerinin paydaları farklıdır. Tam-pencere analizi erken dönemdeki olayları seçebilir; sansürü düzeltilmiş survival/Kaplan–Meier tahmini yapılmadı.

Bunlar seçilmiş temsilci adaylar ve gözlenen veri için betimleyici sayılardır; bağımsız fiyat olayları veya F01'in gelecek başarı olasılığı değildir. Hacim, işlem maliyeti ve emir yürütme yoktur. [summary.csv](f01-censoring/summary.csv) ve olay bazında [cohort.csv.xz](f01-censoring/cohort.csv.xz), yukarı adayları ve 10/40 barı da içerir. Olay dosyasındaki sonraki ziyaret alanları **sonradan bilinen sonuçtur**, ilk aday anındaki özellik değildir.

## 5. Karar ve açık kalanlar

- **Kaydedilebilir davranış:** Karşıya geçiş, geri geliş, geri gelmeme, tamamlanmış ikinci ziyaret ve açık ziyaret ayrı ayrı ölçülebiliyor.
- **F01 için karar:** Daha adil ama küçük örnekli eşleştirme, önceki toplu farkın kararlı bir yön avantajı olduğunu göstermedi. Eşleşme oranı düşük; bu, güçlü etki yoktur kanıtı da değildir.
- **Açık:** Eşleştirme toleransları ve 11 bar sınırı varyantları; ortak hisse ve zaman bağımlılığını birlikte ele alan yöntemler; gerçek seans saatleri; kurumsal işlem ve endeks üyeliği; daha uzun, önceden incelenmemiş veri. Bağımsız veri bu çalışmada elde edilmedi ve **bağımsız doğrulama yapılmadı**.
- Gerçek bir indikatör/strateji iddiası için hipotez, maliyet ve değerlendirme kuralları önce sabitlenmeli; henüz işlem veya kâr testi yapılmadı.

## 6. Dosyalar ve tekrar üretim

- [Eşler](f01-matched/pairs.csv), [eşleşmeyen vakalar](f01-matched/unmatched.csv), [eşli sonuçlar](f01-matched/results.csv), [eşleme kapsamı](f01-matched/eligible-inputs.csv), [yöntem hash'leri](f01-matched/summary.json).
- [Sansür grupları](f01-censoring/summary.csv), [tüm aday/pencere kayıtları](f01-censoring/cohort.csv.xz), [girdi/yöntem hash'leri](f01-censoring/summary.json).

```bash
.venv/bin/python -m tools.evaluate_f01_matching \
  --output research/measurements/zone-memory/f01-matched --draws 1000
.venv/bin/python -m tools.measure_f01_censoring \
  --output research/measurements/zone-memory/f01-censoring
.venv/bin/python -m pytest -q
.venv/bin/python -m tools.archive_zone_research
```
