# Başlangıç Teması — Bilgiyi Sinyal Yığınına Değil Karar ve Araştırma Sistemine Dönüştürmek

> Durum: `preliminary` — Bu dosya kitapların sıralı bölüm incelemesinin yerine geçmez. Tam okumaya başlamadan önce üç eserde tekrar eden yöntem omurgasını, kaynak nüanslarını kaybetmeden görünür kılar.

## 1. Bilgi, kullanım sırasına yerleştirilmelidir

### Kaynak A — Ana Trading Kitabı

> “Trading öğrenirken en büyük sorun bilgi eksikliğinden çok, bilgilerin birbirinden kopuk olmasıdır. Mumlar ayrı, piyasa yapısı ayrı, risk yönetimi ayrı ve psikoloji ayrı öğrenildiğinde grafik karşısında hangi bilginin önce kullanılacağı belirsizleşir.”
>
> “Amaç; ürünü tanımadan grafiğe geçmemek, bağlamı kurmadan tetik aramamak, stop belirlemeden pozisyon büyüklüğü hesaplamamak ve işlem bittikten sonra sonucu süreçten ayırarak değerlendirmektir.”

**Referans:** `ATK-TR-D1.0-2026-08`, PDF s. 4.

### Kaynak B — Profesyonel Teknik Analiz Cilt 1

> “Bir sistemde ‘işleme uygun ortam’ ile ‘şimdi giriş yap’ kararı ayrılmalıdır. Örneğin fiyatın 200 EMA üzerinde olması bir koşul olabilir; AVWAP çevresine geri çekilmesi konumu tanımlayabilir; yapısal kırılım giriş işareti olabilir; ATR ise risk mesafesine yardım edebilir.”

**Referans:** `PTA-C1-2026`, PDF s. 7, Bölüm 1.2.

### Kaynak C — Profesyonel Teknik Analiz Cilt 2

> “Sıra bilinçli olarak fiyatın büyük resminden küçük ayrıntıya doğru gider. Önce nerede olduğumuzu belirleriz. Sonra hangi tarafın daha rahat ilerlediğini ölçeriz. Ardından zayıflama, yapı tipi, kırılım, ikinci deneme ve pullback sonu gibi daha seçici sorulara geçeriz. Hacim ve çoklu zaman dilimi ise en son, fiyatın zaten söylediği hikâyeyi desteklemek veya zayıflatmak için kullanılır.”

**Referans:** `PTA-C2-2026`, PDF s. 93, Bölüm 13.

### Kaynak özeti (`source`)

Üç kaynak aynı ana probleme farklı seviyelerden yaklaşıyor:

- Ana kitap, eğitim ve işlem sürecinin parçalanmasını problem olarak görüyor.
- Cilt 1, karar rollerini ortam–konum–tetik–risk şeklinde ayırıyor.
- Cilt 2, fiyat okumasını büyük bağlamdan küçük davranış ayrıntısına doğru sıralıyor.

Kaynaklar “çok bilgi = iyi karar” demiyor. Bilginin hangi aşamada ve hangi soruya cevap verdiğini açıklaştırıyor.

### Yorum (`inference`)

Replay-Man’de her özellik veya olay yalnız adıyla değil, **karar rolü** ile kaydedilmelidir. Aynı değer farklı rollerde kullanılabilir; ancak bu roller birbirine karıştırılmamalıdır.

Önerilen roller:

1. `context` — Piyasa ortamı ve rejim.
2. `direction` — Operasyonel yön.
3. `location` — Fiyatın anlamlı konumu.
4. `setup` — İzlenmeye değer koşulların birleşimi.
5. `trigger` — Kararın verilebildiği gözlenebilir olay.
6. `invalidation` — Fikri yanlışlayan davranış.
7. `target/space` — Beklenen hareket alanı.
8. `management` — Karar sonrası uygulama.
9. `no_trade` — Bilinçli olarak aday üretmeme koşulu.

### Nasıl kullanılabilir? (`hypothesis/use`)

- Feature registry’de her özellik `family` ve `role` taşıyabilir.
- Deney motoru, yalnız tetik değil bağlam ve konumu ayrı kolonlarda raporlayabilir.
- Replay ekranı “neden aday oldu?” açıklamasını karar zincirine göre gösterebilir.
- Aynı indikatörün hem trend hem tetik hem stop olarak kontrolsüz kullanılmasına uyarı üretilebilir.

---

## 2. Aynı bilgi ailesinin tekrarı bağımsız teyit değildir

### Kaynak — Cilt 1

> “RSI, Stochastic ve Stoch RSI aynı yönde hareket ettiğinde üç ayrı teyit varmış gibi görünebilir; ancak aynı hareket gücü ailesinden bilgi taşırlar ve Stoch RSI doğrudan RSI’dan türetilir. Benzer biçimde çoklu EMA, MACD ve Supertrend de trend bilgisini farklı biçimlerde tekrar edebilir.”
>
> “Bir indikatörü eklemeden önce ‘ne katıyor?’ diye sormak yeterli değildir. Daha güçlü soru şudur: ‘Bu indikatörü çıkarırsam hangi karar aşamasını artık veremiyorum?’ Cevap yoksa araç yalnız görsel güven hissi üretiyor olabilir.”

**Referans:** `PTA-C1-2026`, PDF s. 127, Bölüm 21.1–21.2.

### Kaynak özeti (`source`)

Gösterge sayısı ile bilgi çeşitliliği aynı değildir. Araçlar farklı formüllere sahip olsa da aynı fiyat dönüşümünü veya aynı karar katmanını tekrar edebilir. Kaynak, ekleme testinden daha güçlü olarak çıkarma testini öneriyor.

### Yorum (`inference`)

Her özellik için iki ayrı sınıflama gereklidir:

- **Veri/bilgi ailesi:** trend, momentum, volatilite, hacim, yapı, konum, göreceli güç vb.
- **Karar rolü:** context, location, trigger, risk vb.

İki özellik hem aynı ailede hem aynı roldeyse yüksek tekrar riski taşır. Aynı ailede olup farklı rol oynuyorsa veya farklı aileden aynı olayı destekliyorsa katkısı ayrıca ölçülmelidir.

### Nasıl kullanılabilir? (`hypothesis/use`)

- Kombinasyon deneylerinde her ek bileşen için temel model ile fark raporu üretmek.
- Bileşen çıkarıldığında sembol yaygınlığı, beklenen hareket veya ters hareket değişmiyorsa bileşeni gereksiz aday olarak işaretlemek.
- Korelasyonu yüksek göstergeleri otomatik silmek yerine “tekrar adayı” olarak raporlamak; çünkü benzer girdiler farklı karar zamanlaması üretebilir.

---

## 3. Belirsiz fikir gözlenebilir kurala çevrilmeden test edilmemelidir

### Kaynak — Ana Trading Kitabı

> “‘Destekten al’, ‘güçlü momentumda gir’ veya ‘AI uygun görürse işlem aç’ test edilebilir kurallar değildir. AI’dan kod istemeden önce fikir; veri, durum, olay ve geçersizlik cümlelerine çevrilir. Bu aşamada cevap üretmekten çok belirsizliği bulması istenir.”
>
> “Rules-based strategy, yoruma tamamen kapalı olmak zorunda değildir; fakat karar noktaları gözlenebilir ve kaydedilebilir olmalıdır. ‘Güçlü trend’ dersem güçlü trendin ölçütünü, ‘iyi mum’ dersem mumun kapanış ve gövde koşulunu tanımlarım.”

**Referans:** `ATK-TR-D1.0-2026-08`, PDF s. 257 ve 336–337, Bölüm 12.14 ve 16.6.

### Kaynak özeti (`source`)

Kaynak, tamamen mekanik olmayı zorunlu tutmuyor; fakat karar anlarının gözlenebilir ve kaydedilebilir olmasını istiyor. Doğrudan kod üretmek yerine önce belirsiz kavramların bulunmasını öneriyor.

### Yorum (`inference`)

Bilgi tabanı bir kavramı üç ayrı olgunluk seviyesinde saklayabilir:

1. `narrative` — İnsan tarafından anlaşılabilir fikir.
2. `observable` — Hangi veri ve olaylarla gözleneceği açıklanmış tanım.
3. `operational` — Formül, parametre ve bilinebilme zamanı belirlenmiş uygulama.

İlk kitap okumasında `narrative` ve `observable` seviyeleri hedeflenmeli; kullanıcı talebine uygun olarak kesin eşikler sonraki ayrıntılı çalışmaya bırakılmalıdır.

### Nasıl kullanılabilir? (`hypothesis/use`)

Her kartta şu sorular tutulabilir:

- Hangi veri gerekir?
- Olay en erken ne zaman bilinir?
- Ne gözlenirse fikir desteklenir?
- Ne gözlenirse yanlışlanır?
- Neyi açıklaması veya öngörmesi beklenir?
- Hangi ifadeler hâlâ ölçülemez durumdadır?

---

## 4. Aday, onay ve bozulma aynı zaman değildir

### Kaynak — Ana Trading Kitabı

> “Script indicator mı strategy mi; ikisinin görevi karışmış mı? Sinyal hangi bar ve hangi fiyatla kesinleşiyor? MTF verisi kapanmış üst zaman barından mı geliyor? Aday, onay, bozulma ve reset açıkça tanımlı mı?”
>
> “AI’nın yazdığı script her swing dibine ‘AL’ etiketi yerleştiriyor. Replay’i etiketin öncesinden başlatırım. Etiket pivot için sağ tarafta üç bar bekledikten sonra geçmişteki dibe taşınıyorsa bu olay ‘pivot üç bar sonra onaylandı’ diye kaydedilmelidir; dip anında erken sinyal gibi sunulamaz.”

**Referans:** `ATK-TR-D1.0-2026-08`, PDF s. 338–340, Bölüm 16.7–16.8.

### Kaynak özeti (`source`)

Bir olayın grafikte ait olduğu geçmiş bar ile olayın bilinebildiği bar aynı olmayabilir. Kaynak özellikle pivotların geriye taşınarak erken sinyal gibi sunulmasına karşı uyarıyor.

### Yorum (`inference`)

Her durum tabanlı olayda en az şu zamanlar ayrılmalıdır:

- `observed_at` — Görsel/ekonomik olayın ait olduğu bar.
- `confirmed_at` — Kullanılabilir olduğunun kesinleştiği bar.
- `invalidated_at` — Olayın bozulduğu bar.
- `archived_at` — Yeni adaylara yer açmak üzere yaşam döngüsünün kapandığı bar.

Replay motoru yalnız `confirmed_at` itibarıyla olayı gösterebilir. Araştırma raporu olay sonucunu `observed_at` yerine yanlışlıkla erken başlatmamalıdır.

### Nasıl kullanılabilir? (`hypothesis/use`)

- Swing, divergence, formasyon ve çoklu zaman dilimi sinyallerinde future leak denetimi.
- Replay ekranında aday ile teyit edilmiş olayın farklı görsel durumları.
- Sinyal raporunda “olay geçmişte nerede oluştu?” ve “ne zaman bilinebiliyordu?” alanları.

---

## 5. İlk hareketten çok takip ve kabul davranışı ölçülmelidir

### Kaynak — Cilt 2

> “Daha güçlü kırılım okumasında sınır dışında kapanış, sonraki mumların yeni alanı koruması ve mümkünse geri testte eski bölgenin tamamının geri alınamaması birlikte değerlendirilir.”
>
> “Kırılımın kalitesi ‘geçti mi?’ değil ‘orada kalabildi mi?’ sorusuyla ölçülür.”

**Referans:** `PTA-C2-2026`, PDF s. 96–97, Bölüm 13.5.

### Kaynak özeti (`source`)

Kaynak kırılımı tek bir fiyat geçişi olarak değil, dış kapanış, yeni alanın korunması ve geri test davranışından oluşan süreç olarak ele alıyor. İlk bar bilgi verir fakat kabul sonraki davranışla güçlenir veya zayıflar.

### Yorum (`inference`)

Kırılım tek bir boolean yerine durum makinesi olabilir:

```text
candidate → closed_outside → followed_through → retested → accepted
                                  ↘ reentered → failed
```

Bu durumların her biri farklı zamanda bilinir ve ayrı araştırma sorusu üretir.

### Nasıl kullanılabilir? (`hypothesis/use`)

- İlk kırılımın devam ihtimali.
- Dış kapanışın ek katkısı.
- Takip barı beklemenin doğruluk ve gecikme maliyeti.
- Eski alana dönüş derinliği ile başarısızlık ilişkisi.
- Kabul edilen ve başarısız kırılımların farklı piyasa rejimlerindeki dağılımı.

---

## 6. Beklenen hareketin gerçekleşmemesi de bilgidir

### Kaynak — Cilt 2

> “İlk ve ikinci hareketi karşılaştırıyoruz: hangisi daha fazla mesafe aldı, hangisi daha hızlıydı, yeni uç oluştu mu, karşı tarafın tepkisi büyüdü mü? Beklenen ikinci bacak gelmiyorsa veya başarısız oluyorsa, gerçekleşmeyen hareket de bilgi haline gelir.”
>
> “Her önemli noktada şu soruyu kullanın: ‘Sağlıklı hareket burada ne üretmeliydi?’ Piyasanın gerçekte yaptığı ile bu beklenti arasındaki fark, zayıflamayı erken görünür hale getirir.”

**Referans:** `PTA-C2-2026`, PDF s. 97–98, Bölüm 13.6.

### Kaynak özeti (`source`)

İkinci denemenin yalnız varlığı değil, ilk denemeye göre ürettiği sonuç önemlidir. Beklenen yeni uç veya ilerleme gelmiyorsa yokluk bir davranış bilgisine dönüşür.

### Yorum (`inference`)

Bu yaklaşım “beklenti–gerçekleşme farkı” ailesinin temelini oluşturabilir. Bir piyasa durumu için beklenen davranış önce tanımlanır; gerçekleşen mesafe, süre ve tepki bununla karşılaştırılır.

### Nasıl kullanılabilir? (`hypothesis/use`)

- İlk/ikinci swing mesafe ve süre oranı.
- Yeni uç uzunluğu ve hızlı geri alınma.
- Trend devamının başarısızlık işaretleri.
- Göreceli güçlü hissenin endeks toparlanmasında beklenen tepkiyi verememesi.
- Kırılım sonrası beklenen genişlemenin oluşmaması.

---

## 7. Test türleri farklı sorular cevaplar

### Kaynak — Ana Trading Kitabı

> “Backtest, bar replay, forward test ve paper trading farklı soruları cevaplar.”
>
> “Bar replay: Geleceği görmeden kuralları uygulayabiliyor muyum?”
>
> “Backtest: Kurallar geçmişte hangi sonuç dağılımını üretiyor?”
>
> “Forward / paper: Canlı veri akışında emir ve rutin uygulanabiliyor mu?”

**Referans:** `ATK-TR-D1.0-2026-08`, PDF s. 257–258, Bölüm 12.15.

### Kaynak özeti (`source`)

Kaynak bütün doğrulama biçimlerini tek “backtest” başlığında toplamıyor. Kural denetimi, geçmiş tarama, replay, istatistiksel backtest ve forward/paper test farklı sorunları araştırıyor.

### Yorum (`inference`)

Replay-Man’in adı replay olsa da araştırma motoru ile görsel replay aynı modül değildir:

- Toplu araştırma motoru geniş sembol dağılımını ölçer.
- Replay motoru karar zamanını, future leak’i ve insan tarafından uygulanabilirliği inceler.
- Daha sonraki simülasyon motoru emir/fill ve maliyet davranışını ölçer.

### Nasıl kullanılabilir? (`hypothesis/use`)

Her deney raporunda kanıt türü belirtilmelidir:

```text
rule_review
historical_scan
batch_measurement
bar_replay
forward_observation
execution_simulation
```

Bir türde başarılı olmak diğerlerinin geçtiği anlamına gelmez.

---

## İlk tema sonucu

Üç kaynak birleştirildiğinde başlangıç sistematiği şu hale geliyor:

```text
Kaynak bilgi
→ karar rolü
→ gözlenebilir tanım
→ bilinebilme zamanı
→ aday/onay/bozulma yaşam döngüsü
→ beklenen davranış
→ gerçekleşen davranış
→ geniş sembol ölçümü
→ geleceği göstermeyen replay incelemesi
```

Bu bir işlem stratejisi değildir. Kitaplardan alınacak sonraki kavramları yerleştirmek için başlangıç bilgi mimarisidir. Sıralı okuma sırasında farklı veya çelişkili tanımlar bu çerçeveyi sessizce değiştirmeyecek; varyant olarak eklenecektir.
