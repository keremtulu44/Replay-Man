# On filtre ve yön testi — geçmiş veride keşif

**Sonuç:** On filtreyi ayrı ayrı kurup dört bölge türünde, iki yönde ve iki periyotta sınadık. Çoğu filtre için doğrulama ve tarihsel testte tutarlı bir yönsel ayrım gösterilemedi. Daha önce bulduğumuz **geç yeniden ziyaret** adayı yeniden görüldü; ancak bu aynı verinin yeniden analizi olduğu için yeni/bağımsız doğrulama değildir.

Tüm sonuçlar araştırma amaçlıdır. Filtreler bu çalışmadan önce kodda sabitlendi, ancak veri ve önceki bulgular zaten incelenmişti; ön-kayıtlı veya bağımsız hipotez testi değildir. 10 filtre, dört tür, iki periyot, iki yön ve çeşitli dönemlerde çok sayıda karşılaştırma yapılmıştır.

## 1. Hangi ortak senaryo test edildi?

Ana örnek: Bir bölgenin **karşı tarafında iki kapanışla biten ziyaret**, ardından aynı bölgeye yeni taraftan gelen ve **aynı tarafta iki kapanışla biten sonraki ziyaret** (`geçiş → aynı taraf`). Yön, ikinci ziyaretin son kapanış tarafına göre yukarı/ aşağı ayrı tutulur. Sonuç, ikinci kapanışın tamamlandığı andan sonraki **beş kullanılabilir bar** üzerinden ölçülür.

İki ayrı soru soruldu:

1. **Filtre var mı/yok mu?** Aynı geçiş→yeniden ziyaret örneklerinde filtreyi sağlayan ve sağlamayan olayların sonuçları karşılaştırıldı.
2. **Filtreli senaryo ve kontrol:** Filtreyi sağlayan geçiş→yeniden ziyaret olayları, aynı tür/periyot/yön/dönemde filtreyi sağlayan **aynı taraf → aynı taraf** ziyaretleriyle karşılaştırıldı.

İki soru da farklı olay kümeleridir; aynı hisse ve tarihte eşleştirilmiş deney veya nedensel etki ölçümü değildir. Aynı hisse, zaman ve bölgedeki sonuç ufukları örtüşebilir. Hisse/periyot/tür/bitiş barında tek temsilci seçimi önceki çalışmadan korunur; farklı türlerde aynı mum tekrar sayılabilir.

Kapsam: **100 mevcut BIST hissesi, günlük ve 4s**, yatay, oyalanma, hızlı uzaklaşma ve eğimli bölgeler. 80.252 senaryo veya kontrol olayı için filtre özellikleri çıkarıldı; beş bar XU100 eşleşmesi ve dönem sınırı koşulları sağlananlar sonuç karşılaştırmasına girdi. 1s/2s bu onlu taramaya dahil değil.

## 2. On filtre

Tüm özellikler ikinci ziyaretin **son iki kapanışı tamamlandığında** bilinir. Yaklaşım ölçüleri temas barından önceki kapanışlardan, ziyaret ölçüleri ise bitişe kadar olan barlardan hesaplanır. ATR, ziyaret başlangıcından önce bilinen 14 barlık basit ATR'dir. Eksik veya hesaplanamayan özellik `unknown`; sahte `hayır` değildir. Hacim kullanılmaz.

| No | Filtre | Test edilen başlangıç kuralı |
|---|---|---|
| **F01** | Geç yeniden ziyaret | Önceki ziyaretin bitişi ile yeni temasın başlangıcı arasında **11+ kullanılabilir bar**. |
| **F02** | Çok temaslı ziyaret | Yeni ziyaret içinde **3+ temas mumu**. Ayrı ziyaret sayısı değildir. |
| **F03** | Uzun ziyaret | Yeni ziyaret başlangıcından ikinci dış kapanışa kadar **5+ kullanılabilir bar**; her barın temas etmesi gerekmez. |
| **F04** | Güçlü bölge yönlü yaklaşım | Temas öncesi son beş kapanış değişiminin bölge yönündeki net ilerlemesi **en az 1 ATR**. |
| **F05** | Artan net ilerleme | Temas öncesi son beş barın bölge yönlü net ilerlemesi, ondan önceki beşten yüksek. Her mumda hızlanma veya emir akışı anlamına gelmez. |
| **F06** | Daha doğrudan yol | Temas öncesi 10 değişimde mutlak net hareket / toplam mutlak yol **≥0,60**. Net hareket bölgeye doğru olmak zorunda değildir. |
| **F07** | Dar bant | Ziyaret başlangıcındaki tam bant genişliği **≤1 temas-öncesi ATR**. Türler arasında bant kuralları farklıdır. |
| **F08** | Çıkış yönünde net ilerleme | Bitiş kapanışı ile iki bar önceki kapanış arasındaki, son dış tarafa göre yönlü fark **≥0,5 ATR**. Bu ancak bitişte bilinir. |
| **F09** | Çift sınır belirsizliği | Ziyaret içinde en az bir mumun high–low aralığı **iki sınırı da aşmış**. Bu bir üstünlük değil, iç sırası bilinmeyen durum filtresidir. |
| **F10** | Daha fazla geçmiş ziyaret | İkinci ziyaret başlangıcından önce aynı bölgede **en az 3 tamamlanmış ziyaret**. Teyitli swing sayısıyla aynı şey değildir. |

Eşikler keşif içindir; en uygun değerler değildir. F02 ve F03 birbiriyle ilişkili olabilir. F07 bölge türünün oluşturma biçimiyle bağlantılıdır. F09'da bar içi sıranın bilinmediği özellikle korunmalıdır.

## 3. On filtrenin genel sonucu

Aşağıdaki tablo, **filtre var/yok karşılaştırmasında** yeterli veri olan hücrelerin doğrulama ve tarihsel testte medyan farkı işaretinin aynı kalıp kalmadığını özetler. Hücre = bölge türü × periyot × son taraf; en fazla 16 hücre. Her iki dönemde iki grubun her birinde en az 30 endeks eşleşmeli olay ve 20 hisse bulunan hücreler sayıldı. Bu, hisse bağımsızlığı veya güçlü istatistiksel yeterlilik garantisi değildir.

| Filtre | Uygun hücre | İki dönemde fark işareti aynı | İki dönemde de aynı tarafta sıfır dışı blok aralığı |
|---|---:|---:|---:|
| F01 Geç ziyaret | 11 | 7 | 0 |
| F02 Çok temas | 15 | 6 | 0 |
| F03 Uzun ziyaret | 14 | 4 | 0 |
| F04 Güçlü yaklaşım | 11 | 8 | 0 |
| F05 Artan ilerleme | 15 | 4 | 0 |
| F06 Doğrudan yol | 11 | 6 | 0 |
| F07 Dar bant | 4 | 1 | 0 |
| F08 Çıkışta ilerleme | 15 | 5 | 0 |
| F09 Çift sınır | 9 | 3 | 0 |
| F10 Geçmiş ziyaret | 11 | 3 | 0 |

İşaretin aynı olması, büyüklüğün kararlı olduğunu, etki bulunduğunu veya sonraki fiyatın o yöne gittiğini göstermiyor. Haftalık blok aralıkları 500 yeniden örneklemedir; haftalar arası beş bar örtüşmesi, hisseler arası bağımlılık ve çoklu deneme sürer. Bu tablo özellikle **aynı iki dönemde tekrar eden güçlü bir filtre etkisi gösteremediğimizi** anlatır; filtrelerin hiçbir koşulda değerli olamayacağını kanıtlamaz.

`F07` için yalnız dört uygun hücre vardı; çoğu özellikle yatay bölgede neredeyse bütün olaylar dar bant koşuluna girdiğinden karşılaştırma grubu küçüldü. Bu, 1 ATR eşiğinin her tür için iyi bir ayrıştırıcı olmadığını gösterir; “bant genişliği önemsizdir” sonucunu değil.

### Filtreli senaryo ile kontrol

İkinci soruda, filtreyi sağlayan geçiş→yeniden ziyaret olayları, filtreyi sağlayan aynı→aynı olaylarıyla karşılaştırıldı. Aynı minimum örnek kuralıyla yalnız **F01 / yatay / 4s / aşağı** hücresinde doğrulama ve tarihsel testin iki haftalık aralığı da aynı tarafta sıfırın dışındaydı. Bu, [önceki küçük filtre araştırmasındaki](KUCUK-FILTRELER-KESIF.md) **aynı adayın aynı veride yeniden üretilmesidir**; yeni doğrulama değildir. 925 karşılaştırma üretildiğinden ve çoklu deneme düzeltmesi yapılmadığından başka bir veri üzerinde sabitleyip sınamak gerekir.

## 4. İncelenmeye değer somut aday: F01

**Yatay / 4s / aşağı yönlü ikinci ziyaret** için önceki ziyaretten sonra yeni temasın `11+` bar gecikmesi:

| Bölüm | Geç gelen senaryo: yönlü XU100 medyanı | Aynı filtreli kontrol | Fark |
|---|---:|---:|---:|
| Eğitim | +%1,10 · n=235 | +%0,84 · n=329 | +0,27 puan |
| Doğrulama | +%1,12 · n=128 | +%0,03 · n=216 | +1,09 puan |
| Tarihsel test | +%0,53 · n=143 | −%0,26 · n=199 | +0,78 puan |

Aşağı yönlü XU100 farkı `(hisse getirisi − XU100 getirisi) × −1` olarak hesaplanır. İki medyanın farkı, **eşleştirilmiş hisse getirisi** değildir.

Aynı senaryonun **kendi içinde** geç gelen `11+` grup ile erken `1–10` grup karşılaştırıldığında testte fark +1,12 puan, fakat doğrulamada +0,67 puan ve blok aralığı **[−0,24; +1,23] puan**. Dolayısıyla kontrol karşılaştırması dikkat çekse de “geç geliş erken gelişten kesin daha iyidir” sonucu çıkmaz. F01 tarihsel testte aynı iki grupta üçer olay bulunan yalnız **5 ortak hisse** vardır; bunlardan 2'sinde geç grubun hisse medyanı daha yüksek, 3'ünde daha düşüktür.

Ham fiyat yönünü endeks farkından ayrı tutmak için: Bu geç senaryo grubunun tarihsel testte beş barlık **aşağı yönlü ham hisse medyanı +%1,46**, yani ham hisse getirisi medyanı −%1,46'dır. Bu tek grup ve görüldükten sonra seçilmiş tarihsel sonuçtur; işlem, maliyet veya garanti değildir.

## 5. Yön açısından değerlendirme ve sonraki adım

- **Bugünkü karar:** Bir yön tahmin kuralı onaylanmadı. F01 yalnızca daha dikkatli incelenmeye değer bir aday; F04 ve diğerleri ilginç görünebilir ama bu kesitte kararlı ek etki göstermedi.
- **Senaryo bilgisi korunmalı:** Yukarı/aşağı, bölgenin türü ve periyot ayrı tutulmalı; dört türün aynı mumdaki olayları bağımsız kanıt sayılmamalı.
- **İyi test:** Önce hipotezi ve gecikme tanımını sabitle; aynı hisse, yakın tarih, aynı periyot/son taraf ve benzer oynaklık/bölge özellikleriyle eşleştirilmiş kontrol kur. Eşleşmeyen olayları ve farklı hisse dağılımını raporla.
- **Yaygınlık ve zaman:** Hiç geri gelmeyen veya veri sonunda hâlâ açık adayları sansürlü olarak ayrıca ölç. 11 kullanılabilir 4s bar resmî 44 saat veya seans kapanışı değildir. Eşik komşulukları, yüzde/ATR bant varyantları ve 10 bar ufuk için ayrı önceden tanımlanmış sınama yap.
- **Bağımsızlık:** Daha uzun ve daha önce incelenmemiş tarihçe ile doğrulama, kurumsal işlem ve endeks üyeliği etkisi, maliyet ve uygulanabilirlik henüz yok. Bu eksikler kapanmadan al/sat veya indikatör performansı iddia edilmez.

## 6. Veri, yöntem ve tekrar üretim

- [Filtre bazında gruplar ve ham/yönlü medyanlar](ten-filters/groups.csv), [tüm karşılaştırmalar, hisse sayıları ve haftalık aralıklar](ten-filters/comparisons.csv), [olay anahtarlı 10 özellik](ten-filters/features.csv.xz), [kaynak ve kod hash'leri](ten-filters/summary.json).
- Kaynaklar önceki [lifecycle sınaması](SENARYO-LIFECYCLE-DOGRULAMA.md) ve dört `lifecycle-*/events.csv.xz` dosyasıdır. Ham OHLC dosyaları kaynak manifest hash'ine karşı yeniden doğrulandı.
- `comparisons.csv` dosyasında `filter_yes_vs_no_in_retest`, ilk soru; `retest_vs_control_filter_yes`, ikinci sorudur. `median_difference`, dosyadaki ondalık getiri cinsindedir; yüzde puanı için 100 ile çarpılır.

```bash
.venv/bin/python -m tools.analyze_lifecycle_ten_filters \
  --output research/measurements/zone-memory/ten-filters --draws 500
.venv/bin/python -m pytest -q
```
