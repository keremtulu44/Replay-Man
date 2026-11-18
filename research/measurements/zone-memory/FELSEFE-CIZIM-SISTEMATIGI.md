# Fiyat Bölgesi ve Hareketi — Tarama, Çizim Felsefesi ve Çalışma Sistematiği

**Durum:** Geçmiş veriye dayalı keşif ve tasarım önerisi; tamamlanmış veya performansı doğrulanmış işlem sistemi değil.

**Kapsam:** Mevcut 100 BIST hissesi, yaklaşık bir yıllık arşiv, 1s / 2s / 4s / günlük seriler. Hacim kullanılmaz; görsel arayüz gerekmez.

**Kaynaklar:** [Ana sonuç raporu](SONUC-RAPORU.md), [araştırma yöntemi](README.md), [plan](../../plans/bolge-hafizasi-hareket-karakteri.md).

## 1. Kısa sonuç: çıkarılabilecek felsefe

> **Bir bölge, tek başına al/sat sinyali değil; fiyatın geçmişte temas ettiği ve her gelişinde yeniden sınanması gereken bir davranış alanıdır. Bölgenin kendisi, geçmişi, yaklaşan hareket ve son tepki birbirinden ayrı okunmalıdır.**

Buradan dört çalışma ilkesi öneriyorum:

1. **Çizgiyi değil bölgeyi kaydet.** Bir merkez, iki sınır, kaynak ve oluşumun ilk bilindiği zaman olsun. Kesin nokta ve kesin dönüş varsayma.
2. **Geçmişi silme ama kader olarak da kullanma.** Önceki tepki, geçiş ve farklı taraftan geliş ayrı olaylardır. Çok temasın daima güç veya zayıflık verdiği gösterilmedi.
3. **Bölgeye gelinen taraf ve geliş biçimiyle, bölgeden sonraki davranışı ayrı tut.** Aynı yer farklı yönden ve farklı hareketle aynı anlamı taşımayabilir.
4. **Birden fazla çizimi birden fazla bağımsız kanıt sayma.** Farklı bölge yöntemleri sıklıkla aynı mum/hisse olayını yakalıyor; benzer sonuçlar otomatik olarak birbirini doğrulamaz.

Bunlar veriyle uyumlu, uygulanabilir **araştırma ilkeleri**dir. “Fiyatın niyetini” veya kesin gelecek yönünü bildiren kurallar değildir.

## 2. Bu taramada ne yapıldı?

Mevcut evren çalışmalarındaki olaylar yeniden okundu: yatay teyitli swing, oyalanma, hızlı uzaklaşma ve eğimli hiza. Her yöntemde aynı hisse/periyot/mumda birden çok aday varsa, sonuçlara bakmadan bölge kimliği sırasına göre seçilen **tek temsilî ziyaret** kullanıldı. Beş mum sonucu ve aynı başlangıç/bitiş etiketlerinde XU100 eşleşmesi bulunmayan veya deney dönemi sınırını aşan olaylar bu taramada dışlandı.

- Yatay: 225.899 uygun temsilî ziyaret.
- Oyalanma: 138.874.
- Hızlı uzaklaşma: 151.731.
- Eğimli: 342.167; saatlik ve daha yüksek periyotların iki ayrı çalışması birlikte.
- **Toplam 858.671 tür–ziyaret kaydı**; aynı fiyat mumu birden fazla türde bulunabilir. Bu sayı bağımsız olay sayısı değildir.

Her kayıt bölgeye göre önceki fiyat tarafı, geçmiş durum, 10 mumdaki hareket değişimi, hisse, periyot ve tarihsel dönem bazında ayrıldı. Sonraki beş barın hisse ve XU100 getirileri özellik olarak değil, **ayrı sonuç** olarak ele alındı. Kaynak olay dosyaları ve SHA-256'lar [tarama özeti](philosophy-scan/summary.json) içindedir.

**Bölüm ve saat uyarısı:** Eğitim/doğrulama/test kronolojik etiketlerdir; tümü daha önce incelenmiş yaklaşık bir yıllık veridedir. `ts_utc` bar etiketi gerçek kapanış saati kanıtı değildir; kısmi 2s/4s mumlar dışlandığından ardışık sıra duvar saatini bire bir temsil etmez. Eğimli saatlik ve diğer periyotların dönem sınırları birkaç saat farklı olabilir. Çoklu zaman kapanışı eşleştirilmedi.

## 3. Verinin desteklediği ve desteklemediği noktalar

### 3.1. Önce yön/konum: tek bir toplu sonuç yanıltıyor

Günlük **oyalanma** bölgesi, en az bir geçmiş tamamlanmış ziyaret ve bölge yönünde son beş mumluk net ilerlemenin önceki beşten yüksek olduğu koşul için, sonraki beş mumun yönlü XU100-aşırı medyanı:

| Önceki kapanış | Eğitim | Doğrulama | Tarihsel test |
|---|---:|---:|---:|
| Bölge merkezinin altında | −%1,15 · n=409 | −%1,02 · n=311 | −%0,68 · n=339 |
| Bölge merkezinin üstünde | +%0,44 · n=508 | +%0,99 · n=237 | −%0,83 · n=273 |

Yönlü aşırı getiri `(hisse getirisi − XU100 getirisi) × bölge yönü` olarak ölçülür. Bölgenin altında hisse yükselse bile endeksten az yükselirse değer negatif olabilir. Üstünde yön ters çevrilir. Bunlar getiri, olasılık veya işlem tavsiyesi değildir.

**Çıkarım:** Bölgenin iki tarafını birleştirmek farklı dönem davranışlarını gizliyor. Çizim sistematiğinde **nereden geldiği** etiketini korumak mantıklı; ama yukarıdaki tarihsel farkın gelecekte devam edeceği kanıtlanmadı. Önceki kapanışın konumu, önceki bütün mumların kesintisiz bölgeye geldiği anlamına da gelmez.

Dört türü günlük, bölge altında, artan ilerleme ve kendi tanımlarına göre `1+` geçmiş koşulunda ayrı incelediğimizde yönlü XU100-aşırı medyanlar şöyle:

| Tür | Eğitim | Doğrulama | Tarihsel test |
|---|---:|---:|---:|
| Yatay | −%0,48 | −%0,71 | −%0,54 |
| Oyalanma | −%1,15 | −%1,02 | −%0,68 |
| Hızlı uzaklaşma | −%0,88 | −%1,18 | −%0,35 |
| Eğimli | −%1,07 | −%0,86 | −%0,53 |

İşaretlerin benzer olması ayrı ayrı teyit anlamına gelmez: olaylar türler arasında çakışır ve `1+` tanımı türler arasında aynı değildir. Tablo, sınıfların ortak bağlamda **ayrı raporlanması** gerektiğini gösterir; bir türün diğerine üstünlüğü konusunda eşleştirilmiş karşılaştırma değildir.

### 3.2. Aynı olay farklı yöntemlerde sayılabiliyor

Günlük tarihsel testte oyalanma türünün 1.334 uygun temsilî ziyareti vardı. Bunların 1.171'inde aynı hisse ve aynı mumda bir yatay bölge ziyareti de vardı; **1.070'inde önceki fiyat tarafı da aynıydı** (%80,2). Aynı taraflı 1.070 olayda 10 mum hareket sınıfı da aynıydı ve sonraki hisse/XU100 sonucu hesap gereği aynıydı.

Bu, iki bölgenin **fiyat aralıklarının geometrik olarak üst üste geldiğinin** kanıtı değildir; bu tarama yalnız aynı hisse/mum/taraf örtüşmesini ölçer. Ayrıca sonuçlar her tür için seçilmiş bir temsilciye bağlıdır. Fakat şu açıktır: aynı mumun sonucunu dört farklı etiketle saymak dört bağımsız teyit üretmez.

**Çıkarım:** Çizimleri kaynaklarıyla ayrı sakla, fakat yorumda ortak fiyat olayını bir kez say. Gerçek geometrik kesişim ayrıca hesaplanmadan “çoklu bölge birleşimi üstün” deme. Altı bölge çakışması görünümü, tüm periyot ve dönemler: [same-bar-overlap.csv](philosophy-scan/same-bar-overlap.csv).

### 3.3. Tekrar eden temasın etkisi henüz ayrıştırılmadı

Oyalanmada `0` ilk sonraki ziyaret, `1+` en az bir önceden **tamamlanmış** ziyarettir. Yatayda `1+` ek teyitli swing, eğimlide iki başlangıç ucundan sonra teyitli ek tepkidir: aynı sayılar farklı olayları temsil eder. İlk ziyaret ile 1+ grupları aynı tarih ve aynı fiyat koşullarında eşleştirilmiş değildir.

Günlük, bölgenin altındaki artan ilerleme testinde `1+` ile `0` medyan yönlü aşırı getiri farkı yaklaşık **−0,006 yüzde puanı**dır; gruplar sırasıyla 339 ve 35 olaydır. 500 kez haftalık blok örnekleme fark için yaklaşık **[−1,99; +1,11] yüzde puanı** aralığı üretti. Bu çok geniş aralık, bu veriden bölge hafızasının bağımsız katkısını güvenle ayırt edemediğimizi gösterir.

Bu blok ölçümü keşif **sonrası** seçilen karşılaştırmalardandır; test döneminde yalnız 10 haftalık blok vardır. Beş günlük ufuklar haftalar arasında örtüşebilir, hisselerin sonuçları birbirine bağımlı olabilir ve farklı gruplar aynı olaylar değildir. Bu nedenle aralık bağımsız doğrulama veya tüm yanlılıklardan arınmış istatistiksel kanıt değildir. Ham bilgiler [weekly-bootstrap.csv](philosophy-scan/weekly-bootstrap.csv).

**Çıkarım:** Temas sayısını ve geçmiş tarafları kaydet; fakat “üç dokunuş = güçlü”, “çok dokunuldu = zayıf” veya “rol kesin değişti” kuralını bu sonuçlardan üretme.

### 3.4. Aynı isim farklı periyotta aynı davranış demek değil

Oyalanma, 1+ geçmiş ziyaret, artan ilerleme ve önceki kapanış **bölgenin altında** olan tarihsel testte:

| Ayrı periyot | Olay | Hisse | Beş bar yönlü XU100-aşırı medyan |
|---|---:|---:|---:|
| 1s | 5.458 | 100 | +%0,06 |
| 2s | 2.055 | 99 | +%0,05 |
| 4s | 878 | 95 | +%0,27 |
| Günlük | 339 | 84 | −%0,68 |

Beş günlük bar ile beş saatlik bar eşdeğer zaman ufukları değildir; olay tarihleri ve örnekleri farklıdır. Bu tablo zaman dilimleri arası doğrudan üstünlük karşılaştırması değildir. Ancak **tek bir eşiği veya yorumu her periyoda taşımamamız gerektiğini** gösterir. Tüm yön/hafıza/hareket/dönem tabloları: [condition-surface.csv](philosophy-scan/condition-surface.csv).

## 4. Önerilen çizim sistematiği

Bu bir grafik arayüzü talebi değildir; grafik üstünde elle veya gelecekte programla uygulanabilecek ortak bir tarif ve kayıt sözleşmesidir. Aşağıdaki sınıflar başlangıç için öneridir; kârlılıkları test edilip onaylanmış strateji değildir.

### A. Hangi alanları aday yapacağız?

| Aday türü | Oluşum kuralı | O anda ne biliyoruz? |
|---|---|---|
| **Teyitli tepe/dip bölgesi** | Bir tepe/dip teyit edildikten sonra yatay bir bant açılır. | İlk tepki adayı; ikinci bağımsız teyitten önce “iki kez tepki” denmez. |
| **Tekrarlı yatay bölge** | Daha sonra ayrı bir ziyarette yakın uç teyit edilir. | Kaynak ucu, ek tepkiyi ve önceki ziyaretleri ayrı tutarız. |
| **Oyalanma alanı** | Başlangıç varyantında 10 tamamlanmış mumun kapanış aralığı ≤2 ATR. | Fiyatın tanımlı dönemde dar aralıkta kaldığı; neden kaldığı bilinmez. |
| **Hızlı uzaklaşma kaynağı** | Beş mumluk net hareket ≥2 başlangıç ATR; yalnız eşik bilindiğinde. | Kaynak alan ancak uzaklaşma oluştuktan sonra bilinir; geriye tarih atılmaz. |
| **Eğimli aday** | İki teyitli tepe, iki dip veya karma uç; iki teyit tamamlandıktan sonra. | İki noktadan çizgi üretilebildiği; üçüncü temas tek başına avantaj kanıtı değildir. |

Varsayılan yatay bant genişliğinde `0,25 × ATR` bir **araştırma varyantıdır**, evrensel doğru değildir. Dar/geniş ATR ve yüzde bazlı varyantları ayrı tut. Oyalanma bandı kaynak pencerenin high–low aralığı ve belirlenen toleranstan oluşur. Tepe/dip, oyalanma ve eğimli bölgeler yakınsa **kimliklerini birleştirme**; kaynaklar ve ilişkiler ayrı kalsın.

Eğimli çizginin mevcut kodu eksik/kısmi mumlar çıkarıldıktan sonraki **bar sırasına** göre eğim verir. Bir grafik platformunun duvar saati ekseninde aynı eğimi otomatik varsayma. Eğim/kanalın rastgele çizgilere kıyasla ek değeri henüz ölçülmediğinden eğimli adayları genel kural gibi sıralama.

### B. Bir bölgenin kimlik kartı

Her bölgede şunlar kayıtlı olsun:

- Hisse, kaynak seri, periyot, tür ve hesaplama sürümü.
- Merkez, alt/üst sınır; eğim varsa iki kaynak uç ve eğimin hangi eksende olduğu.
- Kaynak uç/pencerenin zamanı **ve bölgenin ilk bilinebildiği zaman**. Swingin çizildiği geçmiş mum ile teyit mumu aynı şey değildir.
- Önceki ayrı ziyaret sayısı, her ziyarette temas eden mum sayısı, geliş tarafı ve ziyaretin ne zaman tamamlandığı.
- Önceki fitil taşması, kapanışla dışarı çıkma, aynı/karşı tarafta iki dış kapanış, yeniden geliş ve bilinmeyen sıralar.
- Geçmişi tümüyle koru; eski ve yeni olayları eşit ağırlıkla sakla. Sınırlı pencere karşılaştırması ayrı araştırma varyantıdır; geçmiş silinmez.

“Yukarı dönmüş, aşağı dönmüş, geçilmiş” gibi özetler **kaydedilen olaylara bağlansın**. Bir seviyeye sonradan bakıp gelecekte ne olduğunu o tarihte biliniyormuş gibi çizme.

### C. Bölgeye geliş dosyası

Bölgeye temas anından önce bilinenleri ayrı dosyada tut:

1. Önceki kapanış merkezin altında mı üstünde mi? Merkezdeyse `unknown`.
2. İlk beş ve son beş kullanılabilir mumun **bölge yönlü net değişimi**; karşılaştırma ATR ile ölçeklenir. İlerleme artışı her barın hızlandığı anlamına gelmez.
3. Yol verimliliği, yön değiştirme sayısı ve ters yöndeki en büyük geri alma. Hesaplanamayan/sıfır paydalı değerler `unknown`.
4. Önceden bilinen başka bölgeler varsa hangileri? **Mevcut tam evren çalışmasında bölgeler arası yol/gerçek kesişim motoru henüz yapılmadı.** Bu kayıt öneridir, hesaplanmış bulgu değildir.

Her periyodu bağımsız değerlendir. Günlük çizgiyi 1s karara taşımak istenirse önce o günlük barın gerçekten ne zaman kapandığı doğrulanmalı; burada bu eşleştirme yapılmadı.

### D. Temastan sonraki gözlem dili

Bir bölge, kullanıcıya tek bir “güç puanı” yerine aşağıdaki ayrı gözlemlerle anlatılabilir:

- **Aday / izleniyor:** Bölge oluşumu biliniyor, sonraki davranış henüz bilinmiyor.
- **Temas:** Mumun high–low aralığı bantla kesişti. Fitil ve kapanış konumu ayrı kaydedilir.
- **Dış kapanış:** Bant dışında bir kapanış var. Tek başına kalıcılık veya dönüş ispatı değildir.
- **İki dış kapanış:** Mevcut ziyaret varyantında ziyaret kapanır. Çıkışın geldiği tarafla aynı/karşı olması yalnız kapanış tabanlı vekildir.
- **Yeniden ziyaret:** Sonraki ayrı geliş. Önceki olaylar silinmez; farklı taraftan geliş ve sonuçlar ayrıca tutulur.
- **Bilinmiyor / belirsiz:** Bir mumda iki sınır aşılmışsa iç sıra bilinmez; verinin bitmesi, eksik mum veya teyit eksikliği başarı/başarısızlık olarak yazılmaz.

Bu durum adları bir çalışma dilidir. Mevcut swing motoru her adı tam otomatik üretmiyor; özellikle kalıcı rol değişimi ve tüm bölgeler arası yaşam döngüsü sonraki uygulama işleridir.

## 5. Kayıt üzerinden somut örnek — ASELS, 4s

Bu örnek bir işlem önerisi değil, **çizginin geçmişinin nasıl okunacağını** göstermek içindir. Fiyatlar arşivdeki ham TRY seri değerleridir; güncel fiyat değildir. Tarihler kaynak 4s barının UTC etiketidir, doğrulanmış kapanış saati değildir.

- `z16` yatay bölgesinin merkez adayı **339,25**, sınırları yaklaşık **336,41–342,09**. Kaynak tepe bar etiketi 21 Ocak 2026 06:30 UTC; teyit bar etiketi 22 Ocak 06:30 UTC. Bölge ilk pivot anında değil, teyit barı kapandıktan sonra bilinir.
- 12 Mart 06:30 etiketli ziyarette fiyat alttan geldi; ziyaretin kapanışları bandın altında kaydedildi. Bu ziyaretin tepe pivotu ancak **13 Mart teyit barı** sonunda ikinci teyitli tepki olarak biliniyor.
- 19 Mart'ta başlayan başka bir ziyarette kayıtlı geliş tarafı üsttü. 23 Mart'ta iki kapanış bant üstündeydi; 23 Mart etiketli dip ancak **24 Mart teyit barı** sonrasında bölgenin üçüncü teyitli tepkisi sayıldı. Kod bunu `mixed` olarak işaretledi; tek başına kalıcı destek rolü kanıtı değil.
- 25 Mart'taki sonraki ziyarette kayıtlı geliş tarafı yine üsttü; ziyaret sırasında iki sınırın aynı barda aşılma belirsizliği var ve 27 Mart'ta iki kapanış bant altına kaydedildi. Bu olay önceki tarihi silmez ve önceki iki taraflı kullanımı gelecekte garantiye dönüştürmez.

İzlenebilir kaynaklar: [bölge olayları](pilot-4h-atr025/zone-events.csv.gz), [ziyaretler](pilot-4h-atr025/visits.csv.gz), [ziyaret içi olaylar](pilot-4h-atr025/visit-events.csv.gz). Kimlik: `BIST_ASELS:…:4h:atr:0.25:z16`.

## 6. Henüz çıkarılmaması gereken kurallar

- “İki veya üç temas, sonraki sefer kesin dönüş demektir.”
- “Çok kullanılan seviye mutlaka güçlenir” veya “mutlaka tükenir.”
- “Üç farklı tür aynı mumda çalıştı; üç bağımsız teyit var.”
- “Hareketin son beş mumdaki net ilerlemesi arttı; alıcı/satıcı baskısını biliyoruz.”
- “Fitil seviyeyle temas etti; aynı mumda önce hangi sınıra değdiğini biliyoruz.”
- “Bu örnekler kârlı işlem, komisyon sonrası getiri veya portföy sonucu kanıtlıyor.”

## 7. Önerilen sonraki araştırma

1. **Geometrik ilişki:** Aynı anda bilinen bölgelerin gerçekten fiyat aralığı olarak kesişip kesişmediğini kaydet; aynı-bar olay örtüşmesiyle karıştırma. Birden fazla bölgeyi tekleştirmeden ilişkileri göster.
2. **Hafızanın katkısı:** Aynı hisse, yakın tarih, geliş tarafı ve benzer hareket bağlamında geçmiş ziyaret `0` ile `1+` karşılaştır. Yeterli eşleşme yoksa sonucu `unknown` bırak. Hareket tek başına, bölge tek başına ve birleşimi aynı olay kümesinde karşılaştır.
3. **Yol ve yaşam döngüsü:** Önceden bilinen bir bölgeden diğerine gidişi, ayrılış ve yeniden ziyareti nedensel olarak kaydet; fitil/kapanış/bar içi sıra ve olası hedef sansürünü ayır.
4. **Daha uzun ve yeni veri:** Aday ve parametreleri önceden sabitleyip daha önce incelenmemiş dönemde test et. Seans ve kurumsal işlem etkilerini ölç. Üst zaman kapanışı doğrulanmadan çoklu zaman kararı üretme.

Daha uzun veri, eşleştirilmiş kontroller ve gerçek yaşam döngüsü tamamlanmadan bu taslak **araştırma/çalışma felsefesi** olarak kalmalı; otomatik al/sat indikatörü olarak sunulmamalıdır.

## 8. Tekrar üretim ve sınırlamalar

```bash
.venv/bin/python -m tools.analyze_zone_philosophy \
  --root research/measurements/zone-memory \
  --output research/measurements/zone-memory/philosophy-scan --draws 500
.venv/bin/python -m pytest -q
```

Tarama girdileri beş bar ufuklu özet olay dosyalarıdır; bu rapor bütün ufukları, çizgilerin rastgele bazla üstünlüğünü, gerçek bölge örtüşmesini veya doğrulanmış işlem maliyetlerini ölçmüş değildir. Haftalık blok örnekleme yalnız belirtilen günlük oyalanma karşılaştırmalarına uygulanmış, kod ve girdi hash'leri `summary.json` içinde saklanmıştır. `events.csv.gz` dosyalarında veri politikası ham fiyat olduğu için bölünme ve temettü etkileri ayrıca incelenmelidir. Tüm havuz geçmişteki endeks üyeliğini değil mevcut anlık listeyi temsil eder.
