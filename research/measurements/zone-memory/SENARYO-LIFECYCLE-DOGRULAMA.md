# Bölge lifecycle senaryoları — tarihsel sınama

**Karar:** Bölge geçişi ve karşı taraftan yeniden ziyaret dizileri mevcut kayıtlarda tekrar tekrar oluşuyor. Ancak bu ilk sınamada, yeniden ziyaret senaryosunun benzer ikinci ziyaretlere göre **dört tür, iki yön ve farklı periyotlarda tutarlı bir yön avantajı sağladığı gösterilmedi**. Bu araştırma canlı sinyal, kârlılık testi veya bağımsız ileri doğrulama değildir.

## 1. Tam olarak ne sınandı?

Önceki [yön lifecycle taslağındaki](BOLGE-YON-LIFECYCLE-SISTEMATIGI.md) kapanış temelli olaylar için yeni bir motor yazıldı. Her bölge kendi kimliğinde izlenir; yakın bölgeler birleştirilmez:

1. Bölge yalnız oluşum/teyit barı kapandıktan sonra bilinir. Bu çalışmada **oluşumdan sonra en az bir dış kapanış** gözlenmeden ziyaret başlatılmaz. Oluşum sonrası ilk barda hem temas hem dış kapanış varsa bu bar ziyaret sayılmaz. Bu, önceki pilotlardan farklı, açık bir seçimdir.
2. Yeni temas barından **önceki** kapanışın o andaki banda göre tarafı belirlenir. Eğimli bant her kullanılabilir barda güncellenir.
3. Ziyaret ancak ardışık **aynı tarafta iki dış kapanış** ile biter. Karşı taraf veya bant içi kapanış sayacı yeniden başlatır. Temas mumları ve ziyaretler ayrıdır.
4. Alttan geliş ve üstte bitiş `yukarı aday`; üstten geliş ve altta bitiş `aşağı aday`. Adaydan hemen sonraki **aynı bölgenin** ziyaretinde, fiyat yeni taraftan gelip aynı tarafta iki dış kapanışla bitirirse sırasıyla `yukarı ikinci ziyaret` veya `aşağı ikinci ziyaret`. Sonraki ziyaret ters tarafta biterse `karışık`.
5. Bu etiketler yalnız gerekli ikinci kapanış **sonunda** bilinir. Ziyaret açık kaldıysa sansürlü; geliş tarafı belirsizse yön belirsiz. Aynı barda iki sınırın aşılması ayrıca kaydedilir ve bar içi sıra bilinmez. Eğimli bandın fiyat değişmeden fiyata yaklaşması veya fiyatı geçmesi mümkündür.

`İkinci ziyaret` sonraki hemen gelen tamamlanmış ziyaret üzerinden, arada sabit bir üst süre sınırı olmadan araştırıldı. Bu, öngörülebilir bir zaman aralığı veya başarı olasılığı demek değildir. Senaryo oluşması, senaryo yönünde sonraki hareketin gerçekleşmesiyle **aynı şey değildir**.

### Karşılaştırma grubu

İkinci ziyaret senaryosunu, aynı tür/periyot/bölüm/son kapanış tarafında iki ardışık ziyaretin de **geldiği tarafta** bittiği durumlarla karşılaştırdık (`aynı taraf → aynı taraf`). Her iki grubun sonraki sonucu, son ziyaretin iki kapanışla tamamlandığı andan itibaren ölçüldü. Böylece ikinci ziyaretin sonucunu bilmeden onu başlangıca taşımadık.

Bu gruplar **aynı hisse ve tarih üzerinde eşleştirilmiş değildir**. Yaş, bölge genişliği, oynaklık, geçmiş ve piyasa rejimleri farklı olabilir. Karşılaştırma bu nedenle nedensel hafıza etkisi veya strateji ablation'ı değildir.

## 2. Kapsam ve senaryoların gözlenmesi

- BIST mevcut listesindeki 100 hisse; yatay, oyalanma, hızlı uzaklaşma ve eğimli bölgeler.
- **4s ve günlük:** dört türün her biri 100 hissede.
- **1s ve 2s:** yatay, oyalanma ve hızlı uzaklaşma 100 hissede; **eğimli yalnız alfabetik ilk 15 hissede pilot**. Saatlik eğimli 100-hisse koşusu bu çalışmada tamamlanmadı; 15 hisse rastgele örnek değildir.
- Yaklaşık bir yıllık mevcut arşiv; daha önce incelenmiş dönemler. %60/%20/%20 kronolojik eğitim/doğrulama/tarihsel test sınırları önceki evren çalışmasıyla aynı kullanıldı.
- Her türde hisse/periyot/**ziyaretin tamamlandığı bar** başına bölge kimliğine göre sonuçtan bağımsız bir temsilci seçildi. Sonuç ve senaryo seçimden sonra raporlandı; önceki ziyaretin kendisi temsilci olmayabilir ama bölgenin tüm geçmişinden türetilir. Farklı türler yine aynı hisse ve barı paylaşabilir.

Aşağıdaki sayılar seçilmiş tamamlanmış temsilcilerde **olayın ortaya çıktığını** gösterir; bağımsız tekrar sayısı, olasılık veya senaryo başarı oranı değildir. Aynı hisse, bölge, fiyat barı ve gelecek pencereleri örtüşebilir.

| Tür | 1s yukarı / aşağı ikinci ziyaret | 2s yukarı / aşağı | 4s yukarı / aşağı | Günlük yukarı / aşağı |
|---|---:|---:|---:|---:|
| Yatay | 15.143 / 15.152 | 6.117 / 6.341 | 2.630 / 2.878 | 1.072 / 1.344 |
| Oyalanma | 5.641 / 6.085 | 1.973 / 2.322 | 619 / 911 | 181 / 334 |
| Hızlı uzaklaşma | 9.124 / 9.504 | 3.367 / 3.861 | 1.236 / 1.579 | 355 / 626 |
| Eğimli | 3.631 / 3.638 **(15 hisse)** | 1.497 / 1.568 **(15 hisse)** | 4.388 / 4.853 | 1.855 / 2.133 |

Toplam **614.630 tamamlanmış tür-içi temsilci** raporlandı; türler arası aynı barlar tekrar sayılır. Seçim öncesi tüm ziyaret sayıları ve açık ziyaretler her `lifecycle-*/inventory.csv` içinde. Yalnız tamamlanan olaylara ve temsilcilere bakmak, özellikle uzun/sansürlü ziyaretlerin dağılımını değiştirir; bu tablo evrendeki bütün bölgelerin hangi olasılıkla yeniden ziyaret edildiğini ölçmez.

## 3. İkinci ziyaretten sonra yön devam etti mi?

Son ziyaret tamamlandıktan sonraki **5 ve 10 kullanılabilir bar** ayrı ölçüldü. Beş barlık yönlü XU100-aşırı getiri = `(hisse getirisi − XU100 getirisi) × çıkış yönü` (`üst=+1`, `alt=−1`). Yalnız başlangıç ve bitiş etiketleri endeksle bire bir eşleşen ve sonucu kendi kronolojik bölüm sınırını aşmayanlar kullanıldı. Bu **kâr veya fiyat yönü olasılığı değildir**.

### Günlük: aşağı ikinci ziyaret ve karşılaştırma

| Bölge | Bölüm | Geçiş → aynı taraf n / medyan | Aynı → aynı n / medyan | Fark, yüzde puanı |
|---|---|---:|---:|---:|
| Yatay | Doğrulama | 355 / +%0,45 | 543 / +%0,93 | −0,48 |
| Yatay | Tarihsel test | 355 / −%0,50 | 437 / −%0,25 | −0,26 |
| Oyalanma | Doğrulama | 88 / +%0,49 | 483 / +%0,62 | −0,13 |
| Oyalanma | Tarihsel test | 109 / −%0,04 | 485 / −%0,78 | +0,74 |
| Hızlı uzaklaşma | Doğrulama | 163 / +%0,16 | 424 / +%0,89 | −0,74 |
| Hızlı uzaklaşma | Tarihsel test | 197 / −%0,28 | 377 / −%0,67 | +0,39 |
| Eğimli | Doğrulama | 519 / +%0,54 | 864 / +%0,83 | −0,29 |
| Eğimli | Tarihsel test | 570 / −%0,67 | 678 / +%0,01 | −0,68 |

Fark, iki farklı olay grubunun medyanları farkıdır; olaylar bire bir eşleşmiş değildir. Oyalanma ve hızlı çıkışta işaret iki bölüm arasında değişiyor. Yatay ve eğimlide fark iki bölümde negatif, ama bu **mutlaka aşağı fiyat hareketi** demek değildir; sonucun işareti endekse göre ve yönle çarpılarak hesaplanmıştır. Çoklu denemeler ve seçilmiş bölüm sonucu özellikle önemlidir.

### Yukarı ve 4s farklı bir resim gösteriyor

Günlük yatay **yukarı** ikinci ziyaretin medyan yönlü XU100 farkı doğrulamada −%1,22 (n=228), tarihsel testte +%0,26 (n=187). Aynı grupta tarihsel testin **ham yönlü hisse medyanı −%2,45**: hisse genel olarak düşerken endekse göre fark pozitif olabildi. Dolayısıyla “endekse göre pozitif” → “fiyat yükseldi” değildir.

4s yatay aşağı ikinci ziyarette test medyanı −%0,34 (n=748), aynı→aynı grupta −%0,34 (n=950); fark yalnız yaklaşık **+0,007 yüzde puanı**. Günlük ve 4s beş-bar süreleri farklıdır; bunları doğrudan performans yarışı gibi yorumlamamalı. Tüm tür, yön, periyot ve bölümlerin n, medyan ve 10 bar çıktıları kaynak `groups.csv` dosyalarında; beş bar karşılaştırmaları [comparisons.csv](lifecycle-analysis/comparisons.csv).

### Belirsizlik

Aynı haftadaki tüm hisseleri birlikte örnekleyen 500 tekrarlı blok bootstrap uygulandı. Örneğin günlük yatay aşağı testte iki medyan farkı **−0,26 puan**, aralık yaklaşık **[−1,07; +0,83] puan**. Günlük oyalanma aşağı testte fark **+0,74 puan**, aralık **[−0,70; +1,79] puan**. Test yaklaşık 10 haftadır.

Aralıklar bu sonuçlar görülmüşken yapılan keşif karşılaştırmalarıdır; beş bar sonuçları haftalar arasında örtüşebilir, aynı hisse ve tarih bağımlıdır ve çok sayıda hücre incelenmiştir. Aralıklar bağımsız ileri doğrulama veya genel bir etkinin ispatı değildir. Hisse karşılaştırmasında her iki gruptan da en az üç olay olan hisselerin sayısı ve işaretleri aynı CSV'dedir; az gözlem güvence değildir.

## 4. İnsan tarafından izlenebilir örnek

ASELS 4s yatay `z1` bölgesi, yeni lifecycle kurallarıyla:

- `v2` 1 Aralık 2025 06:30 UTC etiketli barda **alttan** başlıyor; 1 Aralık 10:30 etiketinde iki üst dış kapanış tamamlandığında **yukarı aday** biliniyor.
- `v3` 2 Aralık 06:30 etiketinde **üstten** başlıyor; 2 Aralık 10:30 etiketindeki ikinci üst kapanış tamamlandığında **yukarı ikinci ziyaret** etiketi oluşuyor.
- Bundan sonraki beş barda yönlü XU100 farkı yaklaşık **−%0,14**. Bu tek örnek ve seçilmiş örnekler yön veya getiri genellemesi kanıtı değildir.

Etiketler gerçek seans kapanışı değil kaynak bar zaman etiketidir. `v3` temsilci olay kaydında bulunur; `v2` başka bir bölge aynı bitiş barında önce seçilmişse temsilci dosyasından çıkarılmış olabilir. Bölgenin tam ziyaret zinciri girdi fiyatı ve lifecycle motoruyla yeniden üretilir; önceki ziyaretin pozisyonu ve sınıfı `v3` kaydında da korunur.

## 5. Ne sonuç çıkar, ne açık?

**Desteklenen:** Dört türde karşı tarafa geçiş, ikinci ziyaret ve ters sonuçlu `karışık` dizileri bu tanımlarla gözleniyor. Bu, lifecycle dilinin somut fiyat kayıtlarına uygulanabildiğini gösteriyor.

**Desteklenmeyen:** İkinci ziyaretin tek başına sonraki yönü öngördüğü, türün başka türden üstün olduğu, her zaman kalıcı rol değişimi olduğu veya bu etiketlerle kârlı işlem yapılabileceği. Türler aynı fiyat olayına denk gelebilir; 1s/2s eğimli tarama 15 hisselik seçilmiş pilottur.

**Henüz yapılmadı:** Her geçiş adayından itibaren, gerçekleşmeyen/bitmeyen yeniden ziyaretler dâhil uygun sansürlemeyle senaryonun gerçekleşme olasılığı; olayların hisse/tarih ve volatiliteye göre eşleştirilmesi; farklı ATR/yüzde ve dış kapanış eşikleri; bölgeden bölgeye yol ve gerçek geometri; ilk dış kapanıştan içeri dönüş/fitil senaryolarının tüm evrende yeni motorla ölçümü; maliyet ve uygulanabilirlik; gerçek seans kapanışları ve uzun, daha önce görülmemiş bağımsız veri. Bu eksikler nedeniyle “doğrulandı” sözcüğü burada yalnız **olayın mekanik olarak gözlenmesi ve tarihsel sınama** anlamındadır.

## 6. Çıktılar ve tekrar üretim

- [Senaryo sayıları](lifecycle-analysis/scenario-counts.csv), [karşılaştırmalar ve bootstrap](lifecycle-analysis/comparisons.csv), [analiz girdilerinin hash'leri](lifecycle-analysis/summary.json).
- `lifecycle-{horizontal,dwell,impulse,sloped}`: günlük/4s; `lifecycle-*-hourly`: 1s/2s. `events.csv.xz` temsilci ziyaretlerin kimliği, bölge sınırı, önceki ve son olay, senaryo ve ileri sonuçları içerir; `groups.csv`, `inventory.csv`, girdi/benchmark hash'leri ve `summary.json` ayrı kaydedilir.
- Yer tasarrufu için `compact_lifecycle` yalnız türetilebilir/sabit kolonları çıkarıp CSV'yi XZ ile saklar. Ham çalıştırıcı gzip çıktısını yeniden üretir; önceki bitiş konumu ve bölge kimliği korunur. Kompaktlaştırma yuvarlak yol kontrolünü 1e−12 toleransla yapar.
- Koşuların kullandığı lifecycle motoru hash ile [kaynak arşivinde](sources/zone_lifecycle-recorded.py) korunmuştur. Koşulardan sonra yalnız geliş tarafı `unknown` olan tamamlanmış ziyaretin etiketini `none` yerine `unknown` yazan savunmacı düzeltme yapıldı; sekiz çıktıdaki 614.630 temsilcinin hiçbirinde bu durum yoktur. Her koşunun kendi `summary.json` dosyası gerçek çalıştırılan motorun hash'ini saklar; güncel motor yeniden çalıştırılabilir.

```bash
# Dört türün her biri için günlük ve 4s; --kind dwell, impulse, sloped ile tekrarla.
.venv/bin/python -m tools.measure_zone_lifecycle --kind horizontal --intervals 4h,1d \
  --output research/measurements/zone-memory/lifecycle-horizontal
# 1s/2s: yatay, oyalanma, hızlı uzaklaşmada 100 hisse; eğimli yalnız limit 15.
.venv/bin/python -m tools.measure_zone_lifecycle --kind horizontal --intervals 1h,2h \
  --output research/measurements/zone-memory/lifecycle-horizontal-hourly
.venv/bin/python -m tools.measure_zone_lifecycle --kind sloped --intervals 1h,2h --limit 15 \
  --output research/measurements/zone-memory/lifecycle-sloped-hourly
# Bütün sekiz koşu tamamlandıktan sonra:
.venv/bin/python -m tools.compact_lifecycle
.venv/bin/python -m tools.summarize_lifecycle \
  --output research/measurements/zone-memory/lifecycle-analysis --draws 500
.venv/bin/python -m pytest -q
```
