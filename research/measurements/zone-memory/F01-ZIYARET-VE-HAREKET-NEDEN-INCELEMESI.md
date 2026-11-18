# F01: Ziyaret neden başladı veya başlamadı? — yol incelemesi

**Kısa cevap:** Mevcut kayıtlarda, 20 bar içinde geri ziyaret başlamayan aşağı geçiş adayları, geçişten sonraki ilk beş barda bölgenin altına doğru daha fazla uzaklaşmış görünüyordu. Beşinci barda bölge sınırına yakın kalanlarda, sonraki 15 bar içinde aynı bölgeye temas daha sık gözlendi. Bu, **geometrik ve tarihsel bir ilişki**; fiyatın neden hareket ettiğine, alıcı/satıcı niyetine veya sonrasında hangi yönde gideceğine dair nedensel kanıt değil.

Bu rapor [F01 eşleştirme ve sansür çalışmasının](F01-ESLESTIRME-VE-SANSUR.md) aynı verileri üzerinde ek keşiftir; yeni veya bağımsız bir test değildir. Hacim, emir defteri ve haber kullanmıyoruz; o yüzden ekonomik nedeni belirlemiyoruz.

## 1. Soru ve yöntem: başlangıç anı ile sonradan olanı ayır

100 hisse, **4s yatay bölge**, ATR × 0,25. Başlangıç olayı, üstten gelinen ziyaretin iki ardışık alt dış kapanışla tamamlanmasıdır: `aşağı geçiş adayı`. Bu noktada sonraki ziyaretin olup olmayacağı henüz bilinmez.

- **0. bar:** Adayın ikinci alt dış kapanışının tamamlandığı bar.
- **1–5. barlar:** Fiyatın bölgeden uzaklaşması ve beşinci kapanışın sınıra uzaklığı ölçülür.
- **6–20. barlar:** Aynı bölgeye ilk yeni ziyaret başlıyor mu diye bakılır.

Beş barlık yol bilgisi ancak **beşinci bar kapandıktan sonra** bilinir; 0. bara geri taşınamaz. 1–5 arasında zaten ziyaret başlayanlar bu iki grup karşılaştırmasından çıkarılır; yoksa geri ziyaretin kendi fiyat hareketini, yeniden ziyaret öncesi özellik diye kullanmış olurduk. Daha önceki örneklemin dışındaki ya da 20 bar boyunca kendi tarihsel bölümünde tam gözlemi olmayan adaylar ayrıca sansürlüdür.

`Uzaklık / ATR`: beşinci bar kapanışının bandın **alt sınırından aşağıya doğru mesafesi**, aday kapanışında bilinen 14 bar ATR'ye bölünür. Pozitif değer bölgenin altında, negatif değer karşı taraftadır. Eğimli bant burada incelenmedi; bandın bu çalışmada yatay ve sabit olduğu unutulmamalı.

Fiyatın aynı bölgeye 6–20 barda **temas etmesi**, F01'in ikinci ziyaretinin o sürede tamamlandığı veya sonrasında düşüş yaşandığı demek değildir. Bu bölüm yalnız *ziyaret başlangıcını* inceler.

## 2. Önce kimler geri geldi, kimler gelmedi?

Tarihsel testteki 880 aşağı aday:

| Durum | Olay |
|---|---:|
| 20 bar boyunca tam gözlemlenemeyen | 61 |
| Tam gözlemde ilk 1–5 barda ziyaret başlayan | 414 |
| Tam gözlemde ilk 5 barda başlamayıp 6–10'da başlayan | 76 |
| Tam gözlemde ilk 5 barda başlamayıp 11–20'de başlayan | 63 |
| Tam gözlemde 20 bar içinde başlamayan | 266 |

Böylece beşinci barda henüz geri gelmemiş ve 20 barı tam gözlenen **405** adayda `sonraki 15 barda başlama` ile `20. bara kadar başlamama` karşılaştırılabilir: 139'a karşı 266. Bu, hisseler/alanlar bağımsızmış gibi kabul edilen bir deney değildir; tam pencere seçimi dönem sonuna yakın olayları dışlar. 61 sansürlü olayın içinde daha kısa aralıkta temas bilgisi bulunabilir ama tam 20-bar oranlarına zorla dahil edilmez.

## 3. Geri gelmemeyle ilişkili görülen yol

İlk beş bar sonunda fiyatın banda uzaklığı:

| Bölüm | 6–20 barda geri gelen: n / medyan uzaklık | 20 bara kadar gelmeyen: n / medyan uzaklık |
|---|---:|---:|
| Eğitim | 241 / **1,38 ATR** | 262 / **2,16 ATR** |
| Doğrulama | 130 / **1,59 ATR** | 141 / **2,26 ATR** |
| Tarihsel test | 139 / **1,42 ATR** | 266 / **2,72 ATR** |

Testte ilk beş kapanışın aşağı yöndeki net ilerlemesi, geri gelen grupta medyan **0,16 ATR**, gelmeyen grupta **1,65 ATR** idi. Bu, birçok gelmeyen örnekte fiyatın ilk beş barda banttan daha fazla uzaklaştığını tarif ediyor. **Ancak** olayların yaşandığı tarihler, hisseler, fiyat rejimleri ve bantlar farklı; uzaklaşmanın gerçek nedenini veya bu özelliğin tek başına nedensel etkisini göstermiyor.

İlk beş bardaki fitil uçları da aynı dönemde farklıydı: aday kapanışından aşağı en uzak fitilin medyanı dönmeyenlerde **2,54 ATR**, dönenlerde **1,60 ATR**; banda doğru en yakın fitilin medyanı sırasıyla **0,17** ve **0,59 ATR**. Bunlar bar içi olay sırasını göstermez. Aday kapanışında ATR/fiyat medyanı %2,84 ve %2,76; bant genişliği medyanı 0,489 ve 0,473 ATR idi. Aday ziyarette temas mumu medyanı 3 ve 2, önceki tamamlanmış ziyaret sayısı medyanı iki grupta da 6 idi. Bu tek değişkenli özetler birbirinden bağımsız etki ölçmez.

İlk **aday kapanışındaki** uzaklık tek başına aynı ayrımı vermedi: testte geri gelenlerin medyanı **1,15 ATR**, gelmeyenlerin **0,95 ATR** idi; eğitim ve doğrulamada sıralama ters yöndeydi. Dolayısıyla “başlangıçta yakınsa kesin döner” kuralı çıkarılamıyor. Fark daha çok *sonraki ilk beş barın gözlenen yolunda* belirginleşiyor.

### Beşinci bardaki mesafeye göre sonraki ziyaret

Aşağı tablo, **yalnız** ilk 5 barda geri gelmemiş ve 20 barı tam gözlenen adayların kendi içindedir. Yüzdeler aynı bölgeye 6–20. barlarda ziyaret **başlamasını** gösterir; ikinci ziyaretin bitişini veya fiyat yönünü değil.

| Bölüm | 0–1 ATR altında, ziyaret başlayan / toplam | 1–2 ATR altında | 2 ATR'den fazla altında |
|---|---:|---:|---:|
| Eğitim | 73 / 90 (**%81,1**) | 107 / 196 (**%54,6**) | 50 / 196 (**%25,5**) |
| Doğrulama | 23 / 30 (**%76,7**) | 73 / 115 (**%63,5**) | 34 / 124 (**%27,4**) |
| Tarihsel test | 44 / 57 (**%77,2**) | 47 / 117 (**%40,2**) | 44 / 226 (**%19,5**) |

Testte 5 adayın beşinci kapanışı sınırın karşı tarafındaydı; bunlar `0–1 ATR altında` grubuna katılmadı ve ayrı kayıtlandı. Temas kaydı olmayan barlar arasında bu tür konumlar görülebilir; OHLC ile barlar arası veya bar içi geçiş sırası kesin bilinmez.

Testte yakın–uzak grup oran farkı **+57,7 yüzde puanı**, 500 tekrarlı haftalık keşif aralığı yaklaşık **[+41,1; +67,7]**; yalnız **9 hafta**. Hisse bloklu ayrı aralık yaklaşık **[+44,3; +71,8]**. Bunlar bu veride sonradan incelenen, farklı olay gruplarının betimlemesidir. Haftalık ve hisselik bağımlılık birlikte çözülmez, sansür ve tam-pencere seçimi sürer. Özellikle **uzak bir bölgeye temas etmek için daha fazla yol kat edilmesi gerekir**: bu yüzden farkın önemli kısmı mesafe ve sabit pencere geometrisiyle uyumlu olabilir. Tek başına piyasa baskısı, bir sonraki yön veya işlem avantajı göstermez.

Aynı gözlem yukarı adaylarda da ayrı hesaplandı; tarihsel testte 20 bar boyunca dönmeyen yalnız **10** yukarı aday vardı. Bu küçük sayı nedeniyle yönler için tek kural üretilemez. Tüm sonuçlar [landmark-groups.csv](f01-reasons/landmark-groups.csv), [landmark-distance.csv](f01-reasons/landmark-distance.csv) ve [landmark-bin-contrast.csv](f01-reasons/landmark-bin-contrast.csv) içindedir.

## 4. Aynı hisseden iki örnek

**AEFES 4s, 16 Eylül 2026 06:30 UTC bar etiketi, yatay `z24:v18`:** Aşağı geçiş adayı kapanışı 18,46; bölgenin alt sınırı yaklaşık 19,24. Aday sonundaki ATR yaklaşık 0,424. Beşinci sonraki bar etiketi 18 Eylül 10:30, kapanış 18,75: alt sınıra uzaklık **1,14 ATR**. İlk yeni ziyaret **8. kullanılabilir barda**, 22 Eylül 06:30 etiketinde başladı.

**AEFES 4s, 15 Ekim 2026 06:30 UTC bar etiketi, yatay `z26:v12`:** Aday kapanışı 18,17; alt sınır yaklaşık 18,26; aday sonu ATR 0,308. Beşinci sonraki bar etiketi 19 Ekim 10:30, kapanış 17,36: alt sınıra uzaklık **2,91 ATR**. Bu bölgeye sonraki 20 kullanılabilir barda ziyaret başlamadı.

Bu iki farklı bölge ve farklı tarih, inceleme sonrası seçilmiş örneklerdir; karşılaştırılmış deney veya evrensel örüntü kanıtı değildir. Bar etiketleri gerçek seans kapanış saatleri olarak doğrulanmadı. Kaynak: [olay bazlı aday kayıtları](f01-reasons/candidates.csv.xz), fiyat ve bölge manifestleri.

## 5. Diğer soru: Eşleştirilmiş F01 yön sonucu neden farklı göründü?

Önceki eşleştirilmiş F01 testinde beş bar sonucu bulunabilen **37 çift / 29 hisse** vardı. Vakalar ve kontroller aynı hisse olsa da farklı tarihlerdeydi. Aşağıdaki yalnız **ortalama** ayrışım cebirsel bir kimliktir; her eş için endeks farkı = ham yönlü hisse farkı − yönlü XU100 farkı:

| Tarihsel testte eşlerin ortalaması | Vaka − kontrol |
|---|---:|
| Aşağı yönlü ham hisse getirisi | **+0,58 puan** |
| Aşağı yönlü XU100 getirisi | **−0,61 puan** |
| Aşağı yönlü endekse göre hisse farkı | **+1,19 puan** |

Yani bu eşlemdeki ortalama endekse göre farkın bir kısmı, vaka ve kontrol tarihlerindeki **endeks hareketlerinin de farklı** olmasından kaynaklanıyor. Bu, hissedeki farkın nedeni veya manipülasyon/satış baskısı olduğuna dair kanıt değil. 37 kullanılabilir çiftin 19'unda kontrol tarihi vakadan sonraydı; eşleştirme geçmiş araştırma içindir, canlı karar anında gelecekteki kontrolü kullanmaz.

Önceki rapordaki **+1,15 puan**, eş içi endeks-farklarının **medyanı**; yukarıdaki **+1,19** ise **ortalamasıdır**. Medyanlar genel olarak aynı şekilde cebirsel parçalanamaz. Testte eş içi ham yön medyanı **−0,43 puan** ve aralığı genişti; bu nedenle endekse göre pozitif medyanı doğrudan güçlü düşüş diye yorumlamamalıyız.

### Ziyaretin kendi karakteri ayrıştırınca

F01 vakalarını ziyaret bitişinde bilinen filtrelere göre ayırdık. Örneğin testte ikinci ziyarette **3+ temas mumu** olan 18 eşte vaka−kontrol endeks-farkı medyanı **+1,57 puan**; 1–2 temaslı 19 eşte **−1,68 puan**. Ancak doğrulamada çok temaslı yalnız 11, eğitimde 18 eş var; birçok filtre ve küçük alt grup incelendi. Bu **keşif hipotezi**, “üç temas avantaj sağlar” kuralı değildir. Aynı alanda çok temas bir süre ölçüsüyle de ilişkili olabilir. Diğer küçük kesitler [pair-filters.csv](f01-reasons/pair-filters.csv); ham/endeks ayrımı [pair-decomposition.csv](f01-reasons/pair-decomposition.csv).

## 6. Genel değerlendirme

**Gözlenen:** Aşağı geçişten sonra ilk 5 barda banttan ne kadar uzaklaşıldığı, sonraki 15 barda ziyaret başlayıp başlamamasıyla bu geçmiş örnekte güçlü biçimde ilişkili. İlk kapanıştaki mesafe ve bant genişliği aynı net ayrımı göstermiyor.

**Bilinmeyen:** Hareketin gerçek nedeni; ilişkinin uzaklık/zaman geometrisi, hisse/piyasa rejimi, oynaklık, belirli dönemler veya başka bölgelerden hangileriyle açıklandığı; sonraki temasın fiyatı hangi yöne götüreceği; çok temaslı F01 kesitinin yeni veride tekrarlanıp tekrarlanmadığı.

**Önerilen sonraki sınama:** Beşinci bardaki mesafeyi baz alan basit bir mekanik karşılaştırma kurup, aynı hisse/yakın dönem/benzer mesafedeki olaylarda başka özelliklerin (ayrılış karakteri, geçmiş temas, diğer bölgeler) **mesafeye ek bilgi** sağlayıp sağlamadığını incelemek. 20 barı tamamlamamış adaylar için süreye bağlı sansür modeli gerekir. Uzun ve incelenmemiş veri yokken yön veya indikatör doğrulaması iddia edilmez.

## 7. Ham veriler ve tekrar üretim

- [Aday ve ölçülmüş yol kayıtları](f01-reasons/candidates.csv.xz), [aday sonuç sınıfları](f01-reasons/candidate-outcomes.csv), [landmark grupları](f01-reasons/landmark-groups.csv), [mesafe sınıfları](f01-reasons/landmark-distance.csv), [blok aralıkları](f01-reasons/landmark-bin-contrast.csv), [diğer dağılım farkları](f01-reasons/landmark-differences.csv).
- [Eşli endeks ayrışımı](f01-reasons/pair-decomposition.csv), [küçük filtre kesitleri](f01-reasons/pair-filters.csv), [girdi/kod hash'leri](f01-reasons/summary.json).
- Adaylar daha önceki sansür taramasının seçilmiş temsilcileriyle bire bir doğrulandı; referans verileri ve kaynak metot hash'leri kaydedildi.

```bash
.venv/bin/python -m tools.investigate_f01_reasons \
  --output research/measurements/zone-memory/f01-reasons
.venv/bin/python -m pytest -q
.venv/bin/python -m tools.archive_zone_research
```
