# Bölge hafızası — ilk yatay swing pilotu

**Durum:** 100 hisselik mevcut veri keşfi ve ilk duyarlılık ölçümü yapıldı. Ana bulgular ve eksikler [sonuç raporunda](SONUC-RAPORU.md). Bu sayfadaki eski pilotlar korunmuştur; çalışma doğrulanmış indikatör veya işlem sinyali değildir. [Ana plan](../../plans/bolge-hafizasi-hareket-karakteri.md) ve açık kalan aşamalar geçerlidir.

## Ne yapıldı?

- Teyitli 2+2 swing tepe ve dipleriyle, teyit barı kapandıktan sonra **sabit merkezli yatay aday bölge** açılıyor. Yalnız en az 14 barla hesaplanmış ATR mevcutsa ATR varyantında bölge açılır.
- Daha sonra fiyat bölgeyi ziyaret ettiğinde oluşan bir swing, ayrı bir ziyarete aitse ve teyit edilirse, en yakın uygun bölgenin tepki sayısı artıyor. Bir pivot yalnız bir bölgeye atanır; aynı ziyarette birden fazla pivot aynı bölgeye ikinci tepki olarak sayılmaz. Eşit uzaklıkta önce oluşturulmuş bölge seçilir. Uygun bölge yoksa yeni aday açılır; yakın bölgeler birleştirilmez.
- Her bölge, ziyaretin başlangıcında **o anda bilinen** tepki sayısını ve kendi geçmiş ziyaret sayısını saklar. Bir ziyaretin yarattığı tepki yalnız teyidinden sonra sonraki karar anlarında bilinir. Destek/direnç/karma etiketleri kesin sonuç değil, teyitli tepe/dip bileşimine dayanan aday rolüdür.
- Bar aralığının bölgeyle kesişmesi temas; fiyatın iki ardışık kapanış boyunca bölge dışında kalması ziyaret bitişidir. Ziyaret içindeki temas mumları ayrıca tutulur. İki sınırın aynı bar içinde aşılma sırası bilinmez.
- Temas öncesi beş barın net getirisi, ATR ile normalize hızı ve kapanış yolu verimliliği kaydedilir. Gelecek 1/3/5/10/20 barın getirisi, yüksek ve düşük erişimi **ayrı sonuç dosyasındadır**; veri sonunda ufuk tamamlanamazsa `censored`.
- Kullanıcı tercihiyle hacim hesaplamada kullanılmaz. Veri dosyası projenin ortak yükleyicisi nedeniyle hacim kolonuna sahip olmalıdır; kolondaki değer bölge veya hareket hesaplarına girmez.

## Pilot kapsamı

ASELS, THYAO ve TUPRS, yalnız 4 saatlik veri, iki ayrı tolerans denemesi: `0.25 × ATR14` ve fiyatın `%0,50`si. Sınırlar bölge oluşurken sabitlenir. Sonuçlarda `4h` kaynak dosyadaki `complete=false` parçalar çıkarılmıştır; bu nedenle bir ufuktaki bar sayısı duvar saati veya kesintisiz seans süresi değildir. `complete` alanı resmî seans takviminin doğrulandığı anlamına gelmez.

| Varyant | Bölge oluşumu | Teyitli sonraki tepki | Bölge ziyareti | 5 bar sonucu bilinen ziyaret |
|---|---:|---:|---:|---:|
| ATR × 0,25 | 143 | 232 | 1.210 | 1.198 |
| Fiyat × %0,50 | 164 | 218 | 1.452 | 1.438 |

Sayılar üç hisse ve bu veri dönemiyle sınırlıdır. Aynı fiyat hareketi birden fazla bölgenin ziyaretine katkıda bulunabilir; ziyaretler bağımsız gözlem değildir. İki yöntemdeki bölgeler/ziyaretler bire bir eşleşmez. Dar toleransla her ikisi de aşılan barlar çok olduğu için bar içi sıranın belirsiz kalması özellikle önemlidir. Bu sayıların hiçbiri bir yöntemin diğerinden iyi olduğunu göstermez.

`descriptive-5bar.csv` ilk tepki sonrası ve iki veya daha fazla teyitli tepki sonrası ziyaretlerin beş barlık **ham, yönsüz** kapanış getirilerini özetler. Bunlar farklı olay kümeleri, piyasa dönemleri ve yönler içerebilir; eşleşmiş kontrol, XU100 kıyası, dönem ayrımı ve bağımlılık düzeltmesi yapılmadı. Bu tablodan al/sat avantajı veya özel indikatör çıkarımı yapılmaz.

## Eğimli bölge ve hareket karakteri — ikinci pilot

Aynı üç hisse ve 4 saatlik serilerde, iki ayrı teyitli uçla eğimli adaylar oluşturuldu. Yöntemler: iki tepe (`high_high`), iki dip (`low_low`) ve bir tepe ile bir dip (`mixed`). Her yeni uç için, her türden geçmişte teyitli en son üç uygun uç seçilir; geometrik uçlar 8–80 kullanılabilir bar uzaklıkta olmalıdır. Bunlar araştırma öncesi sabit pilot sınırlarıdır; tüm olası çizgiler taranmış değildir. İkinci ucun teyidi tamamlanınca çizgi bilinir, takip bir sonraki bardan başlar. Çizgi sonraki fiyatlara uydurulmaz. Merkez, **kullanılabilir bar sırasına** göre değişir; gerçek geçen zaman eksenindeki çizgiyle aynı değildir.

Aynı geometri için `0,25 × ATR14` ve `%0,50` sabit genişlikler ayrı çalıştırıldı. Her iki yöntemde de 2.200 aday çizgi oluştu: 556 tepe-tepe, 544 dip-dip, 1.100 karma. ATR varyantında 8.334, yüzde varyantında 8.329 ziyaret kaydedildi. Aday ve ziyaret sayısı üstünlük değildir: aynı mum ve aynı pivot birçok farklı çizgiye dahil olabilir. Özellikle karma çizgiler sırf iki uçtan geçirildiği için doğrulanmış destek/direnç ya da kanal değildir. ATR varyantında çizgi oluşumundan sonraki ayrı ziyaretlerde 1.455 teyitli uç tepkisi kaydedildi; bu sayı da bağımsız üçüncü temasların sayısı değildir.

Hareket çalışması, her ziyaret öncesindeki son 10 kullanılabilir barın ilk ve son beşindeki net değişimi karşılaştırır. Yön, **temas öncesi kapanışın o anda bilinen bölge merkezine göre hangi tarafta olduğuna** dayanır; geçmişteki hareketin gerçekten sürekli bölgeye ilerlediği varsayılmaz. `progress_change_atr`: son beş barın bölge yönündeki net değişimi eksi önceki beş barın değişimi, temas öncesinde bilinen ATR'ye bölünmüş. Ayrıca iki parçanın yol verimliliği, yön değişimi sayısı ve on barlık en büyük ters yönlü geri alma kaydedilir. Gelecek sonuçlar özellik tablosuna girmez.

**Yalnız keşif örneği:** Yatay ATR pilotunda, bu ölçünün azaldığı 597 ziyarette sonraki 5 barın bölge yönüne göre medyan getirisi yaklaşık **−%0,42**; arttığı 599 ziyarette medyan **%0,00**. Yüzde toleransı pilotunda medyanlar sırasıyla yaklaşık **−%0,22** ve **+%0,11**. Bunlar farklı/örtüşen ziyaret kümeleri ve yalnız üç hissedir; dönem, yön, aynı barın birden fazla bölgede sayılması ve piyasa koşulları kontrol edilmedi. Bir sinyal veya dayanıklı etki iddiası değildir; aynı-küme karşılaştırması ve daha geniş veriyle incelenmesi gereken ham bir adaydır. Başlangıçta bölgeye dönük hız azalması mutlaka yavaşlayan bir hareket anlamına gelmez; iki bölümde ters yönde hareket de bulunabilir.

`movement-pilot-*` dizinlerindeki `movement-features.csv.gz` ziyaret kimliğine bağlı nedensel özellikleri; `descriptive-5bar.csv` yalnız betimleyici gruplamayı; `summary.json` kaynak ve kod hash'lerini içerir. Yönlü getiri pozitifse sonraki kapanış, olay öncesindeki fiyatın bölgeye yönüyle aynı yöndedir; giriş, işlem maliyeti veya gerçekleşme varsayımı içermez.

## Oyalanma ve hızlı uzaklaşma — altı hisse, dört periyot

ASELS, THYAO, TUPRS, AKBNK, BIMAS ve AEFES için `1h`, `2h`, `4h`, `1d` ayrı çalıştırıldı. Başlangıç eşikleri iki çalışmadan önce kod/deney sözleşmesinde sabitlendi; başarı için sonradan ayarlanmış eşikler değildir:

- **Oyalanma (`dwell`):** Son 10 kullanılabilir kapanışın en yüksek/en düşük farkı, mevcut ATR14'ün en fazla iki katı olduğunda koşul başlar. O pencerenin en düşük/en yüksek fiyatlarına iki tarafta `0,25 × ATR14` eklenerek sabit aday bölge tanımlanır. Koşul kesintisiz sürerken tek aday; koşul sona erip yeniden başlarsa başka aday üretilir. Bu, gerçekleşen emir veya hacim dağılımı değildir.
- **Hızlı uzaklaşma (`impulse`):** Son beş kullanılabilir barda net kapanış hareketinin mutlak büyüklüğü, başlangıç barında bilinen ATR14'ün en az iki katına ulaştığında koşul başlar; ilk eşik barı kapanınca kaynak barın high–low aralığına, eşik barındaki `0,25 × ATR14` eklenerek bölge kaydedilir. Koşul aynı yönde kesintisiz sürerken tek aday açılır. Yön değişimi yeni bir koşuldur. Bu sınır hareketin başlangıcında biliniyormuş gibi gösterilmez.
- Her bölgede kaynak olayından sonra önce bölge dışı bir kapanış beklenir. Bundan sonraki temaslar ziyaret olur; kaynak oluşumundaki mumlar kendi bölgesine ziyaret sayılmaz. İki ardışık bölge dışı kapanış bir ziyareti bitirir. Giriş tarafı biliniyorsa ve bu iki kapanış aynı taraftaysa, geldiği tarafa veya karşı tarafa çıkış **kapanış vekili** olarak ayrı kaydedilir. Diğer durumlar `unknown`; bu, gerçek bar içi yolun bilindiği veya kesin dönüş/kırılım gerçekleştiği anlamına gelmez. Bu sayımlar ancak ziyaretin kapanışında geçmiş hafızaya eklenir.

| Bölge türü | Aday bölge | Bölge ziyareti | Hisse/periyot bazında tek ziyaret/bar |
|---|---:|---:|---:|
| Oyalanma | 1.562 | 19.826 | 8.725 |
| Hızlı uzaklaşma | 1.837 | 23.634 | 9.683 |

Ziyaret sayısı bağımsız olay sayısı değildir. Aynı hisse ve barda birden fazla bölgeye temasları göstermek için **tüm ziyaretler** ve ayrıca her hisse/periyot/bar için sonuç ve hareket grubuna bakmadan bölge kimliği sırasıyla seçilmiş **tek ziyaret/bar** ayrı raporlandı. Bu seçim diğer bölgeleri silmez; görünümü değiştirir, örtüşen sonuç pencerelerini veya hisseler arası bağımlılığı çözmez.

`summary-multiframe-*/splits.csv` ve `per-asset.csv`: bar etiketlerine göre ortak kronolojik %60/%20/%20 bölümleri, iki ziyaret görünümü, olay ve kullanılabilir sonuç sayısı, hisse kırılımı, beş barlık bölgeye yaklaşım yönündeki getirinin medyanı ve pozitif oranını içerir. Ufkun son bar etiketi dönem sınırına ulaşır veya aşarsa sonuç o bölümden dışlanır; tam giriş/çıkış zamanı ve seans kapanışı doğrulanmış değildir. Verinin tamamı daha önce incelenmiş olabileceğinden bölümler bağımsız ileri test değildir.

**İlk kontrol örneği:** Oyalanma bölgelerinde, 4 saatlik tek ziyaret/bar görünümünde bölge yönündeki net ilerlemesi azalan grubun beş barlık yönlü medyanı eğitimde yaklaşık **−%0,49** (155), doğrulamada **−%0,14** (105), tarihsel testte **+%0,10** (116). Bu işaret değişimi, pilotta tek bir döneme bakarak genel kural çıkarmamak gerektiğini gösterir. Seçilmiş altı hisse, tek parametre kümesi, örtüşen ufuklar ve gerçek kapanış belirsizliği nedeniyle rakamlar yatırım veya strateji kanıtı değildir.

## Dosyalar

Her pilot dizininde:

- `experiment-config.json`: yöntem, eşikler, periyotlar, Python/pandas ve ilgili kod dosyalarının SHA-256'ları.
- `input-manifest.csv`: kaynak dosya, SHA-256, toplam/kullanılan/dışlanan satır ve bar etiketleri.
- `zone-events.csv.gz`: bölge oluşumu ve teyitli yeni tepkiler; pivot zamanı ve bilinebilirlik için teyit barının konumu.
- `visits.csv.gz`: yalnız ziyaret başlangıcında bilinen bölge ve yaklaşma özellikleri.
- `visit-events.csv.gz`: temas, kapanış, fitil, çift sınır belirsizliği ve ziyaret bitişi olayları.
- `outcomes.csv.gz`: ileri ufuk sonuçları; özelliklerden ayrı.
- `examples.csv`: ilk ziyaret kayıtlarından incelenebilir örnekler; başarıya göre seçilmemiştir.
- `descriptive-5bar.csv`, `summary.json`: sınırlı betimleyici özet.

`bar_ts` verideki bar **etiketidir**; doğrulanmış gerçek kapanış saati değildir. `position`, eksik/kısmi barlar çıkarıldıktan sonraki kullanılabilir bar sırasıdır. Aynı bara ait high/low değerleri izlenecek fiyat sırasını göstermez.

## Tekrar çalıştırma

```bash
.venv/bin/python -m tools.measure_zone_memory \
  --symbols BIST_ASELS,BIST_THYAO,BIST_TUPRS --intervals 4h \
  --method atr --tolerance 0.25 \
  --output research/measurements/zone-memory/pilot-4h-atr025

.venv/bin/python -m tools.measure_zone_memory \
  --symbols BIST_ASELS,BIST_THYAO,BIST_TUPRS --intervals 4h \
  --method percent --tolerance 0.005 \
  --output research/measurements/zone-memory/pilot-4h-pct050

# Eğimli pilot ve ona bağlı hareket özellikleri
.venv/bin/python -m tools.measure_zone_memory \
  --symbols BIST_ASELS,BIST_THYAO,BIST_TUPRS --intervals 4h \
  --geometry sloped --method atr --tolerance 0.25 \
  --output research/measurements/zone-memory/pilot-4h-sloped-atr025
.venv/bin/python -m tools.measure_movement_character \
  --pilot research/measurements/zone-memory/pilot-4h-sloped-atr025 \
  --output research/measurements/zone-memory/movement-pilot-4h-sloped-atr025

# Oyalanma örneği; --geometry impulse ile hızlı uzaklaşma ayrı çalışır.
.venv/bin/python -m tools.measure_zone_memory \
  --symbols BIST_ASELS,BIST_THYAO,BIST_TUPRS,BIST_AKBNK,BIST_BIMAS,BIST_AEFES \
  --intervals 1h,2h,4h,1d --geometry dwell --method atr --tolerance 0.25 \
  --output research/measurements/zone-memory/pilot-multiframe-dwell-atr025
.venv/bin/python -m tools.measure_movement_character \
  --pilot research/measurements/zone-memory/pilot-multiframe-dwell-atr025 \
  --output research/measurements/zone-memory/movement-multiframe-dwell-atr025
.venv/bin/python -m tools.summarize_behavior_pilot \
  --pilot research/measurements/zone-memory/pilot-multiframe-dwell-atr025 \
  --movement research/measurements/zone-memory/movement-multiframe-dwell-atr025 \
  --output research/measurements/zone-memory/summary-multiframe-dwell-atr025

.venv/bin/python -m pytest -q
```

Bu komutlar belirtilen çıktı dizinlerindeki aynı adlı dosyaları yeniden yazar. Birden fazla seri olan hisse/periyot için otomatik seçim yapılmaz; çalıştırıcı hata verir. Eski yatay/eğimli pilotlar çalıştırıcının önceki sürümleriyle üretildiğinden deney dosyalarındaki çalıştırıcı hash'i mevcut sürümden farklıdır; kayıtlar orijinal pilotu korur. Yatay ve eğimli çekirdekler değiştirilmemiştir. Hareket ve dönem analizleri kaynak girdilerinin hash'ini doğrular.

## Henüz yapılmadı

- Oyalanma ve hızlı çıkış bölgelerinin farklı eşik/tolerans varyantları; paralel kanallar ve eğimli çizgiler için uygun kontrol çizgileri.
- Birbirine yakın bölgelerin örtüşme ilişkisi, kalıcı rol değişimi ve tam bölge yaşam döngüsü.
- Uzaklaşma temelli ikinci tepki tanımı; tüm/sınırlı hafıza, diğer eşik/pencere varyantları.
- Hareketin geçmiş benzer hareketler ve diğer hisselerle karşılaştırılması; ayrılış ve komşu bölgelerle ilişkisi. İlk/son beş mum karşılaştırması dışında daha kapsamlı hareket analizi henüz yapılmadı.
- Tüm olay türleri için kapsamlı olay bazlı sonuçlar, eşleştirilmiş baz/ablation, XU100 ve bağımlılık analizi. Dönem sınırında sansürleme ve zaman kırılımı yalnız yukarıda açıklanan davranış pilotunun beş bar görünümünde uygulandı.
- Tam evrende beş bar dışındaki ufuklar, çoklu zaman eşleşmesi ve daha uzun bağımsız doğrulama. Dört bölge türünün tüm hisselerdeki beş bar taraması [sonuç raporunda](SONUC-RAPORU.md) sunulmuştur.

Özellikle veri etiketlerinin gerçek bar kapanışına eşlenmesi henüz uygulanmadı; bu pilot çoklu zaman uyumu veya gerçek zamanlı sinyal üretmez. `complete=false` satırların çıkarılması yaklaşım ve ufukları eksik aralıkların üzerinden atlatabilir. Bu sınırlama dikkate alınarak sonuçların genellenmesi sonraki çalışmaya bırakılmıştır.
