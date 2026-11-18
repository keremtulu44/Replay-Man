# Bölge türü mü, geliş karakteri mi? — Aynı olaylarda keşif karşılaştırması

**Durum:** Tamamlanan şey mevcut veri üzerinde sınırlı, tekrar üretilebilir bir karşılaştırmadır; kapsamlı doğrulama veya işlem sistemi değildir. Önceden incelenmiş, yaklaşık bir yıllık BIST verisinde 100 hisse ve 1s/2s/4s/günlük periyotlar ayrı kullanıldı. Hacim kullanılmadı. Eğitim/doğrulama/test ayrımları kronolojiktir, fakat kullanıcıyla daha önce incelenmiş aynı veri kullanıldığından bağımsız ileri doğrulama değildir.

## 1. Kısa cevap

**Bu basit karşılaştırmada ne bölge türü göstergeleri, ne de seçtiğimiz geliş karakteri göstergeleri, tek başına ya da birlikte, bütün periyot ve dönemlerde tutarlı ve anlamlı bir tahmin iyileşmesi göstermedi.** Günlük testte çok küçük iyileşmeler görünse de doğrulama bölümünde aynı iyileşme yok. Sonuçlar, daha gelişmiş hareket temsillerinin veya farklı sonuç ölçülerinin işe yaramayacağını kanıtlamaz; yalnız burada kurulan dar karşılaştırmayı sınırlar.

Bu nedenle şimdi bir **hareket sınıflandırma dili** oluşturabiliriz ama “oynağı şu tür olan bölge şu hareketi üretir” şeklinde genellenmiş kural çıkaramayız. Önceki rapordaki bazı koşullu medyanların negatif olması da otomatik olarak bu dört modelden birinin yeni olaylarda daha başarılı olacağı anlamına gelmiyor.

## 2. Bu kez neyi, hangi ortak örnekte karşılaştırdık?

Önceki dört bölge türü taramalarının **858.671 uygun tür-içi temsilî kaydı**, aynı hisse / periyot / bar konumunda bir araya getirildi. Böylece **348.612 tekil hisse-periyot-bar olayı** oluştu. Bunlar birbirinden bağımsız gözlem değildir: aynı hissedeki veya farklı hisselerdeki yakın tarihler ve beş barlık sonuç pencereleri örtüşebilir.

- Aynı bar için önceden belirlenmiş öncelikle **yatay → oyalanma → hızlı uzaklaşma → eğimli** temsilcilerden biri seçildi. Seçim ileri sonuca bakmaz.
- Olayın yönü ve hareket sınıfı bu temsilciye aittir. Diğer türlerden, **aynı barda temsilcisi olan ve temsilcinin merkezine göre tarafı seçilen tarafla aynı olanlar** birer bayrak olarak kaydedildi. Bölge kimlikleri kaynak dosyalarda ayrı kalır.
- Bu bayraklar **geometrik kesişim değildir**. Aynı barda iki bölgeye temas etmiş olmak, fiyat aralıklarının birbirleriyle kesiştiğini göstermez. Tür içindeki tek temsilci bazı diğer adayları gizleyebilir; dolayısıyla sıfır bayrağı o türden hiçbir bölge yok anlamında da kullanılmamalıdır.
- Farklı çalıştırmalarda dönem etiketi uyuşan olaylar tutuldu; dönem uyuşmazlığı nedeniyle çıkarılan anahtar sayısı **0**. Aynı anahtardaki bar etiketi, hisse sonucu ve aynı taraftaki endeks farkı tutarlılığı kontrol edildi.
- Çıktılar karşılaştırılırken, tarafı ve ilerleme sınıfı bilinen, 5 barlık sonuç dönem sınırını aşmayan ve XU100 başlangıç/bitiş etiketleri bire bir eşleşen olaylar kullanıldı. Yol sınıfı sıfır yol durumunda ayrıca `unknown` olarak korunur. İleri sonucun bulunması bu **tarihsel değerlendirme örneklemi** için bir koşuldur; bu, olay anında geleceğin bilindiği veya canlı uygulanabilir bir filtre olduğu anlamına gelmez.
- Bu karşılaştırmada bölge hafızası özellik olarak kullanılmadı. Bölge türlerinde önceki ziyaret ve teyit sayıları aynı kavram olmadığından tek ortak sayıymış gibi birleştirilmedi.

Fiyat dosyalarının SHA-256 değerleri, dört türün girdi manifestleriyle karşılaştırıldı; hareket yolu için kullanılan fiyat dosyaları manifest hash'leriyle ayrıca doğrulandı. 2s/4s eksik/kısmi mum filtreleri ve bar etiketlerinin gerçek seans kapanışı olmaması önceki rapordaki gibidir.

### Geliş karakteri: iki ayrı ölçü

1. **İlerleme değişimi:** Temastan önceki 10 kapanış değişimini iki beşli bölüme ayır. Bölge yönüne göre son beşin net hareketi ilk beşten büyükse `rising`, küçükse `falling`. Bu, her mumda hızlanma veya emir akışı ölçümü değildir.
2. **Yol verimliliği:** Temas öncesi son 10 kapanış değişiminin mutlak net yer değiştirmesini toplam mutlak kapanış yoluna böl. Bu keşifte eşik **0,60**: `direct` ≥0,60; `choppy` <0,60. Yol sıfırsa `unknown`. Bu ölçü net hareketin bölgeye doğru olduğunu garanti etmez; `direct` burada yalnız daha az dolambaçlı kapanış yolu demektir. Eşik ön-kayıtlı değil, araştırma varyantıdır.

Her ikisi yalnız temas mumundan **önceki** kapanışları kullanır; tür bayraklarının bilinebilmesi içinse temas mumunun high–low bilgisi gerekir. Sonuç, temas mumunun kapanışından sonraki beşinci uygun mum kapanışına kadardır. Dolayısıyla karşılaştırma, temas oluşmadan önce bir alarm ve işlem maliyetleri dahil gerçekleşebilir emir testi değildir.

### Karşılaştırılan modeller

Aynı periyottaki **eğitim** olaylarında her hücrenin beş barlık yönlü XU100-aşırı sonuç medyanı öğrenildi. Doğrulama ve testte hücre tahmini sabit tutuldu:

- `taraf`: yalnız temsilci bölge merkezinin altında/üstünde olma.
- `hareket`: taraf + ilerleme değişimi.
- `bölge`: taraf + dört tür bayrağı.
- `bölge + hareket`: taraf + dört bayrak + ilerleme değişimi.
- `hareket + yol`: taraf + ilerleme değişimi + yol verimliliği sınıfı.
- `bölge + hareket + yol`: bunların tamamı.

Yönlü sonuç = `(hisse 5 bar getirisi − eşleşen XU100 5 bar getirisi) × yaklaşım yönü`. Her periyot ayrı eğitildi; aynı doğrulama/test olayları bütün modellerde kullanıldı. Test hücresinde eğitimden **30'dan az kayıt** varsa taraf modelinin eğitim medyanına dönüldü. Bu eşik, model sınıfı ve hücre tahmin yöntemi keşif seçimi olup, model yeteneklerinin tamamını temsil etmez.

## 3. Ortak örnekte sonuçlar

Ölçü: **ortalama mutlak tahmin hatası** (MAE), yüzde puanı cinsinden; küçük daha iyidir. Bu rakam kazanç, zarar veya strateji getirisi değildir. Her satırda tüm modeller aynı olaylara bakar. Beş bar farklı periyotlarda farklı süreler olduğundan satırlar arasında doğrudan performans yarışı yapılmamalıdır.

| Periyot / bölüm | Olay | Taraf | Hareket | Bölge | Bölge + hareket | Hareket + yol | Bölge + hareket + yol |
|---|---:|---:|---:|---:|---:|---:|---:|
| Günlük doğrulama | 4.219 | 4,00536 | 4,00492 | 4,01259 | 4,01123 | 4,00653 | 4,01569 |
| Günlük tarihsel test | 4.369 | 4,48460 | 4,48180 | 4,48266 | 4,47879 | 4,48648 | 4,48241 |
| 4s doğrulama | 8.854 | 2,75484 | 2,75435 | 2,75842 | 2,75980 | 2,75402 | 2,76122 |
| 4s tarihsel test | 8.991 | 3,10302 | 3,10240 | 3,10274 | 3,10484 | 3,10241 | 3,10739 |
| 2s doğrulama | 18.315 | 1,86549 | 1,86623 | 1,86597 | 1,86709 | 1,86631 | 1,86884 |
| 2s tarihsel test | 18.552 | 2,12897 | 2,12913 | 2,13036 | 2,13089 | 2,12878 | 2,13142 |
| 1s doğrulama | 41.892 | 1,17124 | 1,17125 | 1,17162 | 1,17174 | 1,17125 | 1,17228 |
| 1s tarihsel test | 42.588 | 1,34337 | 1,34321 | 1,34409 | 1,34409 | 1,34331 | 1,34441 |

**Okuma:** Günlük tarihsel testte `bölge + hareket`, `taraf` modelinden yaklaşık **0,0058 yüzde puanı** daha düşük hata verdi; günlük doğrulamada ise yaklaşık **0,0059 puan daha yüksek** hata verdi. Günlük testte mutlak hata yaklaşık 4,48 puan olduğundan fark çok küçük. 4s/2s/1s tarihsel testte aynı birleşim taraf modelinden daha düşük hata göstermedi.

Yol sınıfı eklenince `hareket + yol`, `hareket` modeline karşı günlük testte yaklaşık **0,0047 puan daha yüksek hata** verdi; 2s testte yaklaşık **0,00035 puan daha düşük** hata verdi. Doğrulamada 2s yönü ters. Bu bulgu “yol önemsizdir” değil, **bu tek eşik ve bu sonuç ölçüsünde güvenilir katkı gösterilmedi** demektir.

Günlük testte `bölge + hareket + yol` ile taraf modeli arasındaki hata farkı 100 hissenin **47'sinde** daha düşük, 53'ünde daha yüksekti. Hisse sonuçları birbirinden bağımsız değildir. Günlük testte daha ayrıntılı birleşik modelin olaylarının %7,7'sinde hücre yetersizliğinden taraf modeline dönüldü; doğrulamada bu oran %10,3'tü. Diğer model ve periyotların geri dönüş oranları [scores.csv](type-vs-movement/scores.csv)'de.

### Belirsizlik ve temsilci seçimi

Sabit eğitim tahminleriyle, aynı haftanın tüm hisseleri birlikte yeniden örneklenerek 500 tekrarlı keşif amaçlı haftalık blok aralığı hesaplandı. Günlük testte `bölge + hareket` modelinin tarafa karşı hata iyileşmesi **+0,0058 puan**, yaklaşık aralık **[−0,0107; +0,0269] puan**; testte yalnız **10 haftalık** blok var. Negatif iyileşme daha yüksek hata demektir. Aralık sıfırın iki tarafını da kapsıyor.

Bu aralıklar modeli yeniden eğitmez; haftalar arası örtüşen beş bar sonuçları, çok sayıda deneme ve hisse bağımlılığı nedeniyle bağımsız doğrulama değildir. Bütün çiftler için [weekly-intervals.csv](type-vs-movement/weekly-intervals.csv).

Temsilci sırasını tersine çevirdiğimiz duyarlılıkta günlük testte aynı iyileşme yaklaşık **+0,0062**, doğrulamada **−0,0042 puan** oldu; 4s testte fark **−0,0037 puan** oldu. Temsilci değişince seçilen taraf ve tür bayrakları değişebilir; aynı anahtar sayısının korunması aynı özelliklerin seçildiği anlamına gelmez. Ana sonucun — tutarlı avantaj gösterilememesi — bu kaba duyarlılıkta değişmediği görülüyor. Sonuçlar: [type-vs-movement-reversed](type-vs-movement-reversed/).

## 4. Bölge ve hareket çeşitlerine dair betimleyici bir örnek

Günlük veride aynı barda dört türün de **aynı taraflı temsilci bayrağı** olan ve seçili merkezin altında bulunan kayıtları ayıralım. Bu, dört çizginin geometrik olarak çakıştığı anlamına gelmez:

| Bölüm | İlerleme artan: n / yönlü aşırı medyan | İlerleme azalan: n / yönlü aşırı medyan |
|---|---:|---:|
| Eğitim | 162 / −%1,01 | 141 / −%0,21 |
| Doğrulama | 134 / −%1,40 | 135 / −%0,29 |
| Tarihsel test | 197 / −%0,85 | 156 / +%0,93 |

Bu gruplar eşleştirilmiş değildir, veri görüldükten sonra seçilen örneklerdir ve bir sonuç üretirken aynı dönem ve hisseler tekrarlanır. Yönlü XU100 farkı negatif diye fiyatın mutlaka aşağı döndüğü söylenemez. **Bu tablo araştırılabilecek bir davranış sınıfını tarif eder; bu sınıfın diğer türlere üstün olduğunu veya doğrulanmış indikatör yarattığını göstermez.**

Aynı günlük testte dört bayrak + alttan geliş + artan ilerleme grubunun 197 olayından 181'i `choppy`, yalnız 16'sı `direct` sınıfında. Hücreleri daha fazla bölmek hızla küçük örnekler yaratır. Ayrıntılar [groups.csv](type-vs-movement/groups.csv) ve [groups-path.csv](type-vs-movement/groups-path.csv).

### Gerçek kayıt: ASELS

`BIST_ASELS`, günlük, **2026-10-01 21:00 UTC bar etiketi** (gerçek seans kapanış saati olduğu doğrulanmadı): seçilen yatay temsilci `z27:v3`; diğer aynı-bar/aynı-taraf temsilciler oyalanma `z8:v7`, hızlı uzaklaşma `z11:v8`, eğimli `z222:v4`. Seçilmiş merkeze göre önceki kapanış altta; 10 bar karşılaştırmasında ilerleme artan; yol verimliliği 0,0884 (`choppy`). Beşinci sonraki barın etiketi 2026-10-08 21:00 UTC; hisse kapanıştan kapanışa **−%3,17**, XU100 **−%0,03**, yönlü endeks farkı **−%3,14**.

Bu tek örnek seçilmiş bir tarihsel olaydır, işlem sonucu veya kural doğrulaması değildir. Aynı özelliklere sahip ASELS **2026-10-20 21:00 UTC** etiketli farklı olayda hisse beş bar sonucu **+%3,69**, yönlü endeks farkı **+%7,24** idi. Sonuçlar farklı olabilir. İki olayın özellikleri ve sonuçları [events.csv.gz](type-vs-movement/events.csv.gz) dosyasında; bölge/ziyaret kimlikleri türlerin `universe-*/events.csv.gz` kayıtlarında, hisse/periyot/pozisyon üzerinden görülebilir. Geometrik alan veya bar içi sıra burada ölçülmedi.

## 5. Sonuç olarak önerilen sistematik

Bölge türü ve geliş türünü şimdilik **etiketleme ve karşılaştırma boyutları** olarak tut:

1. **Bölge:** yatay / oyalanma / hızlı uzaklaşma kaynağı / eğimli; özgün kimlikler korunur.
2. **Geliş:** alt/üst; önceki ve yakın net ilerleme; yol verimliliği ve geri çekilme gibi ayrı özellikler. Bilinmeyen bilgileri sıfıra çevirmeme.
3. **Temas:** fitil, kapanış, sınır dışı kalma, tekrar ziyaret. Bar içi sıra bilinmiyorsa belirsiz.
4. **Sonraki hareket:** sadece beşinci kapanış değil; ayrılış, bölgede kalma, geçiş ve dönüş yolunun ayrıca nedensel biçimde ölçülmesi.
5. **Karşılaştırma:** aynı hisse/bar olayını bir kez say, türleri bağımsız oy gibi sayma, gerçek fiyat aralığı kesişimini ve daha iyi eşleşmiş bazları ayrıca ölç.

Burada 3–4 numaralı yaşam döngüsünün tamamı ve gerçek geometrik kesişim **henüz uygulanmadı**. Daha uzun, daha önce incelenmemiş veride önceden belirlenmiş hipotezlerle test edilmeden al/sat sinyali, fiyat hedefi veya kârlılık iddiası üretilmemeli. Sabit ufuk dışında önemli olaylara kadar analiz, kurumsal işlemler ve komisyon/uygulanabilirlik de açık.

## 6. Dosyalar ve yeniden üretim

- [Olay kayıtları](type-vs-movement/events.csv.gz), [tarihsel doğrulama/test tahminleri](type-vs-movement/predictions.csv.gz), [gruplar](type-vs-movement/groups.csv), [yol sınıflı gruplar](type-vs-movement/groups-path.csv).
- [Model hataları](type-vs-movement/scores.csv), [eşlenik hata farkları](type-vs-movement/paired-scores.csv), [haftalık blok aralıkları](type-vs-movement/weekly-intervals.csv), [girdi ve metot hash'leri](type-vs-movement/summary.json).
- 30 kayıt eşiği ve 0,60 yol eşiği keşif amaçlıdır. Duyarlılık koşusu ters öncelikle aynı girdilerden yeniden üretilebilir.

```bash
.venv/bin/python -m tools.compare_zone_movement \
  --output research/measurements/zone-memory/type-vs-movement --min-train 30
.venv/bin/python -m tools.compare_zone_movement \
  --output research/measurements/zone-memory/type-vs-movement-reversed \
  --reverse-anchor --summary-only --min-train 30
.venv/bin/python -m pytest -q
```
