# Araştırma sonuçlarının genel denetimi

**19 Kasım 2026 · Karar: keşif sürer; işlem kuralı doğrulanmadı.** Bu rapor mevcut sonuçlar görüldükten sonra yapılmıştır. Aşağıdaki karşılaştırmalar bağımsız ön kayıt, ileri test, yatırım tavsiyesi veya gerçek portföy performansı değildir. Avantajın gösterilememesi, hiçbir koşulda avantaj olamayacağının kanıtı da değildir.

## Yönetici sonucu

1. **Dip adayı, seçilmiş yerel dip tanımına benziyor; bundan işlem avantajı çıkmıyor.** Uzun harici geçmişte A'nın dip vekiliyle eşleşmesi, aynı bar etiketindeki yükselen başka hisselere göre daha sık. Ancak aynı eşlerde sonraki 20 barın getirisi ve stop/hedef modelindeki ortalama sonuç kontrolün üzerinde gösterilemedi. Daha kısa iç dönemlerde işaretler tutarlı değil.
2. **Destek bölgesi ve teyidin ek yararı kanıtlanmadı.** B'nin desteksiz A'ya göre farkları dönem ve periyoda göre değişiyor. P6'da gelecekteki teyidi failure anına taşımak önemli bir iyimserlik yaratıyordu; düzeltilmiş zamanlama sonrasında önceki `continue` kararı geri çekildi.
3. **Yüksek görünen aşağı-yönlü getiri büyük ölçüde piyasa düşüşüyle birlikte oluşmuş.** Eski 4s acceptance adayı daha sıkı ölçülünce testte tamamlanmış 386 olayın ortalama yönlü ham getirisi +%14,02, aynı pencerelerde XU100'ün ortalama getirisi -%13,51; yön düzeltilmiş endeks farkı ortalaması sadece +0,51 yüzde puan. Bu örnek yalnız 5 sinyal haftası ve çok sayıda örtüşen pencere içerir; short kârlılığı kanıtlamaz.
4. **Eski kayıtları hipotez olarak okuyun.** Bazı eski endeks karşılaştırmalarında hisse ve XU100'ün bitiş etiketleri farklılaşabiliyor; bazı tarihsel bölümler sonuç ufkunu bölüm içinde zorunlu tutmuyor. Kitap denetimindeki `PASSED` kapsam/bütünlük sonucudur, finansal başarı notu değildir.

## Kapsam ve okuma biçimi

İç arşiv, güncel evrenden 100 BIST hissesi ve XU100 için yaklaşık bir yıllık 4s/günlük veridir; tarihsel test 1 Eylül 2026'da başlar, en son kullanılabilir hisse barları 13 Kasım civarındadır. Harici arşivde mevcut evrenle kesişen 68 hissenin 2022–31 Ekim 2025 günlük geçmişi vardır. Harici kayıt da yfinance ailesindendir; ayarlama politikası kesin değildir ve doğrulanmış XU100 yoktur. Güncel evren tarihsel üyelikleri temsil etmeyebilir.

Her satır **olay ağırlıklı** bir özettir. Aynı hisse/zaman dilimindeki sinyaller ve 20/60 barlık sonuç pencereleri örtüşebilir; 100 hisse veya yüzlerce olay, yüzlerce bağımsız piyasa dönemi demek değildir. Tam sonuç penceresi gözlenemeyen olaylar sansürlenir. İç 4s hisse verisinde 24.777 kısmi bar ve XU100'de 248 kısmi bar dışlanmıştır; sonraki kullanılabilir bar bu nedenle bazı seans sonlarını atlayabilir. Eşit bar etiketi, gerçek seans/kapanış zamanı veya emir gerçekleşmesinin doğrulanması değildir. “Yüzde puan” iki yüzde arasındaki farktır; XU100 farkı ve yönü terslenmiş getiri nakit kâr değildir.

## 1. Dip adayı ve anlamlı kontrol

**A**: bir bar önceki beş barın dibinin altını görür, o seviyenin üzerinde ve açılışından yüksek kapanır; seçilen A'lar arasında aynı hisse/periyotta en az 10 kullanılabilir bar bulunur. **Dip eşleşmesi**, yalnız sonradan bilinen 5+5 yerel dip etrafında, sinyal kapanışının en fazla 1 ATR uzaklıkta olması gibi seçilmiş koşullarla tanımlanır. Bu etiket gerçek ya da mutlak dibi bilmek değildir; A'nın tanımı ile dip vekili mekanik olarak ilişkilidir.

Karşılaştırmada A'nın **aynı bar etiketindeki başka bir hisseden**, yükseliş mumu ve ham A olmayan kontrol seçildi. Önceki 5 barın ATR'ye bölünmüş hareketi ve önceki ATR/fiyat ölçeği kaliperlerle yaklaştırıldı. Bir kontrol aynı etikette yalnız bir kez kullanıldı; sektör ve likidite eşleşmedi. İşlem sonucuna yalnız iki hissenin **giriş ve 20-bar bitiş etiketi aynı**, iki ufku da gözlenmişse girildi. Kontroller, A sinyallerine uygulanan 10 barlık bekleme kuralına tabi değildir. Seçim ve kaliperler bu genel inceleme sırasında, eski sonuçlar görüldükten sonra belirlendi.

| Kaynak | A / kontrol bulunan | Dip etiketi bilinen çift | A / kontrol dip oranı | Tam ve eş zamanlı 20-bar çift | Ham getiri A−kontrol, ortalama | %0,25 maliyetli model A−kontrol, ortalama |
|---|---:|---:|---:|---:|---:|---:|
| İç, 4s son tarihsel test | 412 / 297 | 270 | %24,1 / %17,8 | 248 | -1,56 puan | +0,04 puan |
| İç, günlük son tarihsel test | 215 / 181 | 170 | %14,7 / %17,1 | 113 | +0,51 puan | -0,43 puan |
| Harici, günlük tarihsel | 2.183 / 1.680 | 1.677 | %36,1 / %21,5 | 1.618 | -0,23 puan `[-1,06; +0,70]` | -0,23 puan `[-0,65; +0,19]` |

Harici dip oranı için eş-içi ortalama fark **+14,55 yüzde puan**, keşif aralığı **[+10,78; +18,69]** puandır. Buna karşılık 20-bar getiri farkı aralıkları sıfırı kapsıyor. Dip etiketinin gelecek bilgisi içeren bir *değerlendirme vekili* olması, seçilen kuralın bu etikete benzerliği, farklı hisselerin özelliklerinin tam eşleştirilmemesi ve birçok araştırmadan sonra bu karşılaştırmanın seçilmesi nedeniyle bu farkı bağımsız öngörü veya nedensel etki saymıyoruz.

Tabloda iç 4s'te 115, günlükte 34; haricide 502 A'ya kontrol bulunamadı, ayrıca haricide birinin geçmiş bağlamı bilinmiyordu. Eşleşenlerden dip etiketi bilinmeyenler sırasıyla 27, 11 ve 3'tür. 20-bar sonraki açılış karşılaştırmasında iç 4s'te 49, günlükte 68 çift sansürlü/bilinmeyen; haricide 41 çift sansürlü/bilinmeyen, 21 çift giriş veya bitiş etiketi farklı olduğu için dışarıda kaldı. Dolayısıyla sonuçlar **eş bulunmuş ve tamamlanmış alt kümeye** aittir; eşleşmeyenleri temsil ettikleri varsayılmamalıdır.

Bu tablodaki ve harici dip farkındaki köşeli aralıklar, yeterli gözlem varsa İstanbul takviminde 5 ardışık haftalık bloklarla, 2.000 çekimli keşif %95 bootstrap aralıklarıdır. Aynı haftadaki hisseler birlikte tutulur; 20 farklı gözlem haftasından azsa bu raporda aralık verilmez. Eşik ilk ara çalışmadan sonra 10'dan 20 haftaya yükseltildi; kısa dönemlerin ilk aralıkları geri çekildi. Harici örnek için bile bu yöntem tüm örtüşme, rejim, örnek seçimi ve çoklu denemeleri düzeltmez. `contemporaneous_matches.csv`, `contemporaneous_pairs.csv` ve `contemporaneous_summary.csv` tüm sayıları içerir.

### Önceki-bar kontrolü neden geri çekildi?

İlk ek kontrolde aynı hissedeki önceki yükseliş mumu, **ileride bir A oluşması şartıyla** seçilmişti. Nitekim sonraki açılış sonucu iki tarafta da gözlenen **1.628/1.628** eşte, kontrolün 20-bar penceresi sonradan gelen A barını içeriyordu. Bu, kontrolü gerçek zamanlı karşı-olgusal yapmaz; gözlenen büyük dip/getiri farkları strateji avantajı diye sunulmamalıdır. Ham tablolar iz bırakmak için `control_*.csv` içinde durur. Üstteki eşzamanlı kontrol bu hatayı azaltır, ancak kendi eşleştirme ve post-hoc sınırlarını kaldırmaz.

## 2. Tek başına getiri, destek ve maliyet

Son iç tarihsel testte A'nın sonraki açılıştan 20 bar ham medyanı 4s'te **-%4,35** (412 sinyalden 360 tam sonuç), günlükte **-%9,23** (215'ten 127 tam sonuç). 1 ATR stop/2 ATR hedef, aynı-barda olumsuz sıra ve varsayımsal toplam %0,25 maliyetle işlem vekilinin medyanı sırasıyla **-%2,69** ve **-%4,45**; net pozitif oranlar %18,6 ve %14,2'dir. Bunlar yalnız tamamı gözlenen ufuklara koşulludur: stop önce gerçekleşse bile tam 20 bar bulunması aranmıştır. Gerçek spread, kayma, sermaye ve gerçekleşme hesaplanmadı.

Destekli A (**B**) ile desteksiz A'nın 20-bar XU100-aşırı medyan farkı iç son dönemde 4s için **-1,39**, günlük için **+1,24** yüzde puandır; ancak yalnız 9 ve 7 farklı sonuç haftası vardır ve gruplar sektör/hisse bazında eşleştirilmiş değildir. Orijinal rapordaki bu kısa haftalık bootstrap aralıkları daha ihtiyatlı genel denetim eşiğini karşılamadığı için teyit edici sayılmamıştır. Harici günlük geçmişte B−desteksiz A ham medyan farkı **-0,15 puan**, orijinal tek-hafta kümeli keşif aralığı `[-1,65; +1,07]` puandır; bu aralık yukarıdaki 5 haftalık blok yöntemiyle hesaplanmamıştır. Bölge filtresinin tutarlı ek yararı gösterilmiş değildir.

Harici geçmişte A'nın 2.137 tamamlanmış olayı için %0,25 maliyetli varsayımsal işlem ortalaması **+%0,35**, medyanı **-%3,27**, pozitif oranı **%39,9**; 5 haftalık keşif aralığı ortalama için **[-%0,21; +%1,14]**. Pozitif ortalama saklanmamalı, fakat negatif medyan ve sıfırı kapsayan belirsizlikle birlikte okunmalıdır. Yıl bazında olay ortalamaları 2022'den 2025'e sırasıyla **+%0,58 / -%0,07 / +%0,93 / -%0,03**; her yıllık keşif aralığı sıfırı kapsar. En iyi %1'lik 22 olay çıkarılınca ortalama **+%0,17** kalır; bu, sonucun yalnız uçlardan oluştuğunu değil, olumlu kuyruğa duyarlılığını gösterir. Hisse ve hafta bazlı ayrıştırmalar `external_*.csv` ve `external_stability.json` içindedir.

## 3. P6: teyidi bekleyince ne değişiyor?

Eski P6, failure barını, sonraki 10 barda karşı genişleme olup olmamasına göre geriye dönük sınıflandırıyordu. Bu bilgi failure anında bilinemez. Düzeltmede teyit ayrı bir olay; giriş için teyit sonrasındaki kullanılabilir açılış esas alınır. [P6 raporu](../p6-causal/README.md) 9.101 failure'ın 7.028 teyitli, 1.792 teyitsiz, 281 sansürlü olduğunu kaydeder.

Yeni aynı-bitiş karşılaştırmasında, her iki görünüm **failure+20 bar kapanışında** sona erer; örnek aynı zamanda eski üç yöntemin de kendi 20-bar sonucunu tamamlayan teyitli olaylarla sınırlıdır. Teyit sonrası açılış eksi gelecekle seçilmiş failure kapanışı için yönlü ham ortalama farkı 4s testte **-1,75 puan** (851 olay, 9 hafta), günlük testte **-3,06 puan** (327 olay, 7 hafta); eş-içi medyan farklar **-1,38 / -2,37** puandır. Teyit sonrası medyan kalan süre her ikisinde 19 bardır. Bu, seçilmiş olaylarda beklenirken gerçekleşmiş fiyat hareketini gösterir; oracle giriş uygulanabilir olmadığından nedensel işlem etkisi değildir. Kısa örnek için bu raporda güven aralığı üretilmedi.

## 4. Eski 4s aşağı acceptance yeniden ölçümü

Eski aday, aynı hisse/bar için birçok seviye olayını tekrarlayabiliyordu. Yeni ölçüm, her hisse/barda ilk pivot temsilcisini tek sayar; aynı takvim bölümünde tamamlanan 60 tam 4s barı, sonraki ve bir bar gecikmeli açılışı ve hisse/XU100 giriş-bitiş etiketlerini kullanır. Aşağıdaki satırlar sağdaki eşit swing ucu ve **her iki girişte de sonuç gözlenen aynı olaylar** içindir; soldaki eşit uç duyarlılığı `acceptance_summary.csv` içindedir.

| Dönem | Aynı iki girişte tam olay | Sinyal haftası | Sonraki açılış yönlü ham medyan | XU100'a göre yönlü medyan fark |
|---|---:|---:|---:|---:|
| Eğitim | 1.111 | 26 | -%5,39 | +3,52 yüzde puan |
| Doğrulama | 161 | 4 | +%3,48 | +4,10 yüzde puan |
| Son tarihsel test | 386 | 5 | +%12,12 | -0,74 yüzde puan |

Yönlü medyan ile ortalama farklı istatistiklerdir.

Son testte 1.101 ham seviye olayı **767 tekil hisse/bar**a iner. Sonraki girişte bunların 394'ü gözlenir, **373'ü sansürlüdür**; gecikmeli girişle ortak tam küme 386'dır. Tamamlanmış kümedeki sinyal tarihleri 1–30 Eylül'dür; sonradan gelen Kasım sinyalleri yeterli ufka sahip değildir. Bu kümede sonraki açılış yönlü ham **ortalama** +%14,02; aynı olayların giriş/bitiş pencerelerinde XU100 **ortalaması -%13,51** ve yönlü fark ortalaması +0,51 puandır. Bu bir piyasa-düşüşü rejimine güçlü maruziyettir, sinyalin piyasadan bağımsız üstünlüğünü kanıtlamaz. Testte yalnız 5 sinyal haftası bulunduğundan güven aralığı verilmedi.

Bu short-benzeri hesap `-(çıkış/giriş − 1)` fiyat vekilidir. Açığa satış yapılabilirliği, ödünç/finansman, işlem kısıtları, gerçekleşme, piyasa etkisi ve portföy riski yoktur. Eğitim, doğrulama ve testteki farklı işaretler ve sansür, eski `%0,6–1,4 beklenen avantaj` yorumunu desteklemez; yeni örnek ve tanımlar eski tablolarla bire bir aynı değildir.

## 5. Eski XU100 hizalaması ve diğer araştırmalar

Eski bazı araçlar hisseye `+h` hisse barı, endekse ise bağımsız `+h` endeks barı kullandı. Aşağıda, mevcut 100 iç hisse ve XU100'de başlangıcı karşılaştırılabilir **tüm olası kapanıştan-kapanışa pencerelerin** bitiş etiketi uyumsuzluğu sayılmıştır; bunlar gerçekleşmiş sinyal/işlem sayısı veya tüm eski araçlar için gerçekleşmiş hata oranı değildir.

| Periyot | 5 bar | 20 bar | 60 bar |
|---|---:|---:|---:|
| Günlük | 500 / 24.495 = %2,04 | 2.000 / 22.995 = %8,70 | 2.895 / 18.995 = %15,24 |
| 4s | 0 / 49.254 | 0 / 47.754 | 0 / 43.754 |

Günlükte ayrıca her ufuk için 100 pencerede endeks başlangıcı yoktur; 5 ve 20 barda başlangıcı bulunan pencerelerin 100'ünde gerçek hisse bitiş etiketi de endekste yoktur. Bu sayımlar evren ve veri sürümüne özgüdür. 4s'te bu örnekte sıfır uyumsuzluk görülmesi, başka periyotlarda veya gelecekte hizalamayı garanti etmez; dönem sızıntısını, kapanıştan gerçekleşme varsayımını veya kârlılığı da doğrulamaz. Yeni ölçümler gerçek iki etiketi eşler. `legacy_alignment_assets.csv` ve `legacy_alignment_summary.csv` ayrıntıyı içerir.

Diğer çalışmalar da aynı sınırlar içinde okunmalı: [swing geometrisi](../cilt2-swing-geometry/README.md) sonuçları parametre/yön/dönemle değişir; [ikinci deneme](../attempts/README.md) eski endeks ve bölümleme sözleşmesiyle tekrar ölçülmeden doğrulanmış aday değildir. [Altın/gümüş filtresinde](../metal-filter-backtest/README.md) örnek 4s başarısız-dip görünümünde 571 karşılaştırılabilir adaydan 45'i elenmiş, ortalama işlem getirisi filtresiz **-%1,424**, filtreli **-%1,427** olmuştur; bu örnekte zararı güvenilir biçimde azalttığı gösterilmemiştir. [Üç kitap denetimi](../../experiments/FINAL_RESEARCH_AUDIT.md) 778 sayfa, 2.228 claim ve 71 kuralın kayıt/kapsam bütünlüğünü ölçer; strateji kârlılığı ölçmez.

## 6. Ne doğrulandı, ne yapılmalı?

`AUDIT.json`: iç dipte 202, harici dipte 68, P6'da 202 girdi dosyasının ve kullanılan plan/kod/çıktıların hash'leri; tüm eşzamanlı çiftlerin zaman/durum kayıtları; örneklenen 200 eşleşmede 400 dip etiketi ve 200 sonuç çiftinde 400 fiyat ile 400 stop/hedef sınırı; P6 ortak-bitişte 200 olay; acceptance'ta 200 olay ve iki eşitlik kuralıyla 10 hissenin yeniden oynatımı; eski hizalamada 20 hisse/ufuk örneği kontrol edildi. Özetler yeniden hesaplandı. Bunlar **artefakt ve örnek aritmetiği** denetimidir; bağımsız fiyat kaynağı veya işlem başarısı doğrulaması değildir. Tam test paketi **187 geçti**; `git diff --check` ve ağsız `run.py --check` başarılıdır.

İleri dip kilidi 19 Kasım 2026 14:55 UTC'de yerel olarak oluşturuldu; ileri başlangıç 20 Kasım İstanbul günüdür. İlk kesit **`blocked_data`, 0 ileri hisse barı**. 202 ısınma serisi ve kesit hash'leri tekrar doğrulandı. Yerel saat/hash üçüncü taraf zaman damgası değildir: özgün kilit, çıktılar ve Git dışındaki `data/ohlcv/` ısınma verisi ayrıca kalıcı ve haricen zaman damgalı saklanmadıkça bağımsız ön kayıt iddiası kurulamaz. Kilidi yeniden oluşturmayın. [İleri protokol](../dip-research/FORWARD.md) zamanında kayıt, maliyet/gecikme ve en az 20 hafta gibi inceleme eşiklerini açıklar; gerçek işlem ve bağımsız sağlayıcı kontrolü yine ayrıca gerekir.

### Yeniden üretim

Aynı Python/pandas/numpy sürümleri ve manifestteki özgün iç fiyat dosyaları gereklidir. Harici dosyalar `.cache` içindedir ve Git'e eklenmez; sabit kaynak arşivini tekrar indirme aracı bunları yeniden kurar. Orijinal çıktıları ezmeden:

```bash
python -m tools.fetch_dip_external --output .cache/external-reference
python -m tools.review_general_results --output .cache/general-review
python -m tools.compare_dip_contemporaneous --output .cache/general-review
python -m tools.review_acceptance_candidate --output .cache/general-review
python -m tools.audit_legacy_alignment --output .cache/general-review
python -m tools.audit_general_review --output .cache/general-review
python -m pytest -q
```

Plan ve ara düzeltmeler [PLAN.md](PLAN.md), üretim hash'leri `run_metadata.json`, `contemporaneous_metadata.json`, `acceptance_metadata.json`, `legacy_alignment_metadata.json`; önceki dip/P6 kontrolleri `integrity.json` içindedir. İleri kilit ve dondurulmuş motor bu genel inceleme sırasında değiştirilmemiştir.
