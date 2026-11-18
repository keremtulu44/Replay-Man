# Bölge Hafızası ve Hareket Karakteri — Replay Araştırma Planı

**Durum:** 100 hisselik mevcut veride keşif taraması ve ilk duyarlılık ölçümü tamamlandı; bütün plan ve bağımsız doğrulama tamamlanmadı. Bulgular ve açık maddeler: [sonuç raporu](../measurements/zone-memory/SONUC-RAPORU.md).
**Tarih:** 17 Kasım 2026
**Tür:** Keşif amaçlı, hacimsiz tarihsel fiyat davranışı araştırması

## 1. Amaç ve beklenen sonuç

BIST hisselerinde fiyatın tekrar tekrar tepki verdiği, içinde kaldığı, hızla uzaklaştığı, geçtiği veya sonradan farklı yönden kullandığı yatay ve eğimli bölgeleri; bu bölgelere gelen ve bu bölgelerden ayrılan hareketlerin karakteriyle birlikte incelemek.

Amaç mevcut destek/direnç fikrini yeni bir isimle sunmak değil; **bölgenin geçmişi ve hareketin yapısı birlikte gerçekten ek bilgi sağlıyor mu** sorusunu cevaplamak. Araştırma, geleceğe erişmeyen replay üzerinde yeni davranış adayları keşfedecek; değerli bulunanlar daha sonra özel indikatör, uyarı veya strateji araştırmasına dönüştürülebilecek. Tek bir puan, otomatik işlem veya başarı garantisi başlangıç hedefi değildir.

Araştırma çıktıları şunları ayrı sunar:

1. Bulgu özeti: tanım, veri dönemi, örnek ve hisse sayısı, baz karşılaştırması, dönemler, sınırlama ve karar.
2. İncelenebilir gerçek geçmiş örnekler: hisse, periyot, tarihler, olay dizisi ve olay anında bilinen değerler.
3. Ham olay ve sonuç kayıtları: yeniden hesaplama, inceleme ve sonraki indikatör geliştirme için makine-okunur dosyalar.

## 2. Kullanıcıyla netleşen tercihler

- Öncelik **keşif**; indikatör biçimine ancak sonuçları gördükten sonra karar verilecek.
- BIST hisseleri; `1h`, `2h`, `4h`, `1d` önce ayrı, uygunluk sağlanırsa daha sonra birlikte incelenecek.
- Yatay destek/direnç, eğimli hizalar ve sadece bunlarla sınırlı olmayan bölge türleri araştırılacak.
- Örnek: birbirine yakın yerden iki aşağı dönüş, doğrulandığı andan sonra direnç **adayı** olabilir; kesin direnç değildir. Benzer şekilde destek, karma ve rol değiştiren bölgeler de araştırılır.
- İlk tepkiden sonra görülenler ile en az iki tepkiyle oluşmuş adayların **sonraki** ziyaretleri ayrı incelenir.
- Farklı bölge tanımları, tepki tanımları, ATR/yüzde toleransları ve tüm/sınırlı geçmiş ayrı karşılaştırılacak. Eğimli çizgiler için birden fazla yöntem denenebilir.
- Seviye geçilse bile geçmişi silinmez; eski tepkiler eşit ağırlıklı tutulur. Sınırlı geçmiş ayrı bir varyanttır; varsayılan ağırlıklı unutma yoktur.
- Ayrı ziyaret ile bir ziyaret içindeki temas eden mum sayısı ayrı tutulur.
- Yakın bölgelerin kimlikleri birleştirilmez; ilişkileri ve örtüşmeleri ayrıca kaydedilir.
- Yaklaşma, temas, ayrılma; yakındaki bölgeler ve önceki bölgeden gelen yol incelenir. Farklı sabit ufuklar ile sonraki olay ayrı ölçülür.
- Tekrarlanabilirlik, karar desteği ve beklenmedik keşiflerin üçü de değerlidir. Hacim kullanılmayacak; grafik arayüzü yapılmayacak.

## 3. Kapsam ve mevcut altyapı

### 3.1 Veri

- Girdi: `data/ohlcv/bist_equities/*/*/bars/{1h,2h,4h,1d}.csv`; her seri `asset_id`, `series_id`, periyot ve dosya hash'iyle kaydedilir. Aynı varlık için birden fazla seri varsa seçim ve dışlananlar manifestte açıkça gösterilir; otomatik karıştırılmaz.
- XU100 yalnız benchmark olarak, aynı periyot ve uyumlu zaman için kullanılır; eksik eşleşme `unknown` olur, ileriye doldurulmaz.
- Mevcut arşiv yaklaşık bir yıllık, mevcut hisse havuzu tarihsel endeks üyeliği değildir. İlk tur bu veriyle keşiftir; daha uzun tarihçe ve yeni gelen veri **ayrı bir sonraki doğrulama** aşamasıdır. Daha uzun verinin mevcut veya indirilebilir olduğu varsayılmaz.
- `1h` ve `1d` native; `2h` ve `4h` saatlikten türetilmiş serilerdir. `complete=false` barlar varsayılan analizden çıkarılır ve kapsamda sayılır. Bu etiketin seans takvimiyle doğrulanmış kapanış garantisi olmadığı raporlanır. Veri başlangıcı, bitişi, eksikler, kurumsal işlemler ve ham fiyat politikası gözlemlerle birlikte belirtilir; kullanıcı kapsamı daha önce onayladığı için bunlar tüm araştırmayı otomatik durdurmaz.
- Hacim, hacim türevleri, emir defteri, gerçek alıcı/satıcı niyeti ve OB/FVG tanımları kapsam dışıdır. OHLC'den çıkarılan davranış, gerçek emir akışı gibi adlandırılmaz.

### 3.2 Yeniden kullanım ve fark

- `replayman/replay.py`: bar yükleme, nedensel özellikler ve replay; forward sonuçları ayrı tutulur.
- `replayman/swings.py`: `pivot_position` ile `confirmed_position` ayrımına sahip teyitli swingler.
- `replayman/structure.py` ve `replayman/lifecycle.py`: mevcut yapı/olay tanımları ve karşılaştırma için referans. Mevcut `structure_events` ilk yaşam döngüsüne ve yaş sınırına odaklıdır; sürekli hafızalı yeni seviyelerin tamamı olarak kabul edilmez.
- `research/measurements/cilt1-level-tools/`, `cilt2-lifecycle/`, `cilt2-pressure-quality/`, `cilt2-compression/`, `attempts/`: daha önce ne ölçüldüğünün ve tekrarlanan bilginin kontrolü. Örneğin çıplak baskı kaybı → dönüş daha önce olumsuz/kararsız bulundu; yeni çalışma bunu doğrulanmış sinyal saymaz.

## 4. Değişmez replay ve zaman sözleşmesi

1. Her karar anında yalnızca o ana kadar **kapanmış ve bilinebilir** veri kullanılır. `ts_utc` dosyada bar başlangıcı/etiketi olabileceğinden otomatik kapanış sayılmaz.
2. Pivotun geometrik zamanı ayrı, teyit zamanı ayrıdır. Aday bölge ilk tepki teyit edilmeden bilinmez; ikinci tepkiyle güçlenen aday da ancak ikinci tepki teyit edildiğinde bilinir. Sonraki ziyaret ölçümünde bu tepkiler hedef ziyaret gibi sayılmaz.
3. Her durum ve özellik için `event_time`, `known_at`, kaynak kimlikleri ve hesaplama sürümü saklanır. Bölge yaratma/güncelleme aynı barda olursa yeni durum o bar kapanışından sonra bilinir; aynı barın geçmiş iç sırası geriye dönük uydurulmaz. Olay değerlendirmesiyle aynı bar içi sıra belirlenemiyorsa `ambiguous` olur.
4. Özellikler/olaylar ve ileriye dönük sonuçlar ayrı tablolarda saklanır. Geleceğe bakarak yeniden hesaplanmış kümeler, çizgiler, geçmiş başarı oranları veya tamamlanmamış olaylar geçmiş karar anına taşınmaz.
5. Üst zaman verisi yalnız **fiili tamamlanma zamanı biliniyorsa** alt zaman kararında kullanılabilir. Native günlük ve türetilmiş barların zaman etiketi kapanış kanıtı değildir. Uygun kapanış eşlemesi doğrulanamayan kombinasyon `unknown`/kapsam dışı raporlanır; zorla eşleştirilmez. Önce periyotlar ayrı çalışır.
6. Eksik bar, sıfır/eksik ATR, bölünme ve veri sonu gibi durumlar düşürülmek yerine uygun `unknown`, `insufficient_history`, `censored` veya kalite bayraklarıyla sayılır. Eşikler ve sayısal varyantlar sonuçlara bakılmadan bir deney manifestine yazılır.

## 5. Bölge motoru tasarımı

### 5.1 Ortak nesne ve sürümleme

Her aday için `zone_id`, `asset_id`, `series_id`, `interval`, `zone_type`, `method`, `parameter_set`, kaynak olay kimlikleri, `created_known_at`, mevcut alt/üst sınır ve merkez, yön/rol, sürüm ve durum tutulur. Yatay bölge fiyat aralığıdır; eğimli bölgede merkez zamana göre değişir, sınırlar o anda hesaplanır.

Bölge sınırları ve çizgi geometri sürümü yalnız yeni bilgi öğrenildiği anda değişebilir. Önceki karar anının sınırları **immutable snapshot** olarak saklanır. Geçilen bölgenin hafızası silinmez; her temas/ziyaret ve rol olayı önceki bilinen geometriyle bağlanır. Yakın adaylar ayrı tutulur; `overlaps` ilişkisi ayrı kaydedilir, otomatik birleştirme yoktur.

İlk sürümde deterministik aday eşleştirme: önceden tanımlanmış tolerans içinde uygun aday varsa en küçük normalize uzaklık; eşitlikte en eski `zone_id`. Değilse yeni aday. Bir kaynak tepki tek bir adaya yazılır; alternatif gruplama ayrı parametre sürümüdür. Herhangi bir olayın birden fazla farklı bölgeye ziyareti mümkün olduğundan bağımlılık ve örtüşme ayrıca raporlanır.

### 5.2 Tepki kaynakları ve adaylar

Aşağıdaki türler birbirine karıştırılmadan ayrı kimlikle üretilir:

1. **Teyitli uç tepkisi:** `2+2` teyitli tepe/dip ilk temel varyant. Mevcut swing motorunun `known_at` bilgisini kullan. Tepe/dip etiketleri gelecekteki teyit zamanından önce görünmez. `5+5` duyarlılık varyantı ayrı.
2. **Belirgin uzaklaşma:** Önceden belirlenmiş uzaklık eşiğiyle bölgeden çıkış; kararın bilindiği bar kapanışında olay olur. ATR ve yüzdesel yöntemler ayrı. Belirgin uzaklaşma, gerçekleşmeden önce tepki sayılmaz.
3. **Oyalanma:** Geçmişe dönük sabit pencere içinde kapanışların bir fiyat bandında geçirdiği süre ve bant genişliği; pencere kapanmadan aday yayımlanmaz. Bölge hacim profili veya gerçek emir birikimi olarak yorumlanmaz.
4. **Hızlı çıkış noktası:** Önceden tanımlanmış süre içinde ATR/yüzde ile normalize fiyat uzaklaşması ve başlangıç aralığı; yalnız hareket eşiği aşıldığında bilinir. Geriye bakıp hareketin başlangıcında biliniyormuş gibi gösterilmez.

İlk teyitli tepki tek-tepkili aday oluşturabilir. İkinci **ayrı** ve uyumlu tepki, o anda iki-tepkili adayı/ilgili bölge geçmişini oluşturur. İlk-tepki sonrası ve iki-tepki sonrası çalışmalar ayrı tutulur. İki tepki aynı yöndeyse başlangıç rolü aday destek/direnç; ters yönlü veya karışık ise `mixed`. Farklı kaynakların birleşiminden yeni birleşik bölge üretilmez; örtüşme ilişkisi ayrı saklanır.

### 5.3 Tolerans ve çizgiler

- İlk araştırma parametreleri, performans sonuçları görülmeden manifestte dondurulur. Başlangıç için **öneri**: ATR14 × `{0.10, 0.25, 0.50}` ve fiyatın `{0.25%, 0.50%, 1.00%}` genişliği; bunlar doğrulanmış eşikler değildir. ATR yok/sıfırsa ATR varyantı `unknown`, yüzde varyantı bağımsız hesaplanır. İşlem maliyeti ve fiyat adımı bilgisi yoksa toleranslar gerçek emir sınırı gibi sunulmaz.
- Yatay adayın temel merkezi ilk bilinen kaynak fiyatıdır; temel sürümde sabitlenir. İkinci kaynak toleransla eşleştirilir; ileride adaptif merkez denenirse yeni sürüm ve önceki durumu koruyan ayrı varyant olarak yapılır. Aralık genişliği yaratılış anındaki ilgili ATR veya yüzdeye göre dondurulur; dinamik genişlik ayrıca test edilir, geçmiş değiştirilmez.
- Eğimli temel varyantlar: teyitli iki tepeyi veya iki dibi birleştiren çizgi; ayrıca tepe ve dipleri karma kullanan çizgiler ve paralel kanal adayları **ayrı yöntemler** olarak. Çizgi iki teyit sonrası kullanılabilir, üçüncü ve sonraki bağımsız ziyaretler ölçülür. Eğim hesaplaması bar indeksine göre; aynı pozisyonlu uçlar ve tanımsız değerler reddedilir. Zaman eksenli çizgiler ayrı varyanttır.
- Çizginin eğimi, iki kaynak arasındaki min/max mesafe ve olası aday sayısına ilişkin sınırlar, pilot öncesi veri kapsamına uygun seçilip manifestte kaydedilir. İki noktanın zorunlu olarak çizgi oluşturması nedeniyle gerçek üçüncü temas, tesadüfi/eşleştirilmiş çizgi bazları ve aday sayılarıyla kıyaslanır. Sonraki pivotları kullanarak geçmiş çizgi ayarlanmaz.
- Hafızanın tamamı saklanır. Analizde **tüm bilinen geçmiş** ve sabit son pencere (`100`/`250` bar başlangıç adayları; periyoda göre gün karşılığı raporlanır) ayrı görünüm. Pencere sınırı eski kayıtları silmez; tüm tepkiler eşit ağırlıklıdır.

## 6. Ziyaret, tepki ve seviye yaşam döngüsü

### 6.1 Ziyaret tanımı

Başlangıç varyantında bir barın `[low, high]` aralığı bölgeyle kesişirse temas barıdır. İlk temas ziyareti açar. Bölge dışı **iki ardışık kapanış** ziyareti bitirir; bu iki barın kapanışı bilinene kadar ziyaret açık kalır. Bölgeye daha erken dönüş aynı ziyaret olarak sayılır. Yeni ziyaret kapanmış bir önceki ziyaret sonrası başlar. `exit_confirmation_bars=1,2,3` ayrı ön-kayıtlı duyarlılık varyantlarıdır.

Her ziyarette ilk temas ve bilinebilir zamanı, temas eden mum sayısı, toplam süre, kapanışların iç/dış konumu, öncesinde gelinen taraf ve ilgili geometri sürümü kaydedilir. Bir mum aynı anda birçok bölgeyle kesişebilir; her ilişki ayrı kaydedilir. OHLC, bu bölgelerin mum içindeki gerçek temas sırasını göstermez.

### 6.2 Ayrı olay türleri

- İlk temas, bölge içinde kalma, üst/alt sınırın fitille aşılması, kapanışla aşılması.
- Bölge dışında ardışık kapanışlar ile tanımlanan kabul **vekili**, bölgeye geri giriş, ardından dönüş ve karşı tarafta yeniden temas.
- Destek/direnç rolü başlangıçta veya daha sonra **gözlenen davranış etiketi** olarak tutulur. Geçiş tek başına başarılı rol değişimi değildir: geçiş sonrası karşı taraftan gerçekleşen ziyaret ve tanımlı uzaklaşma ayrıca gerekir.
- Fiyat bölgenin her iki sınırını aynı mumda aşarsa gerçek sıralama bilinmez; yalnız barın gösterdiği gerçekler kaydedilir, sıralı senaryo uydurulmaz.
- Oluşmuş her olayın tespit anındaki snapshot'ı, olay sayıları, eski olaylar, en son ziyaretten geçen süre ve kırılım/rol tarihi ayrı tutulur. Olaydan sonra bilinen sonuçları olay anı özelliği yapma.

## 7. Hareket karakteri

Her ölçü yaklaşma, temas/ziyaret ve ayrılış olarak ayrı fazlarda hesaplanır; tamamlanmamış faz sonuçları faz bitmiş gibi sunulmaz.

### 7.1 Yaklaşma

- Başlangıç varyantı: önceki `5` ve `10` tamamlanmış bar veya o anda bilinen önceki bölgeden ayrılma; kaynak tanımı ayrı tutulur. Hedefe uzaklığın ATR ve yüzde olarak değişimi.
- Net ilerleme / geçen bar, toplam kapanış yolu, yol verimi = `abs(net değişim) / sum(abs(kapanış değişimleri))`; sıfır payda `unknown`.
- Son ve önceki eşit pencerenin hızları, geri çekilme derinliği/süresi, yön değiştirme sayısı, yeni uçları koruma süresi. Fiyatın tek bir muma sıkıştığı durumlar ve negatif/eksik paydalar açıkça işaretlenir.
- Aynı hareketin önceki bölümüyle; aynı hissede yalnız daha önce tamamlanmış benzer hareketlerle; diğer hisselerde yalnız o anda mevcut eşzamanlı/tarihsel verilerle ayrı karşılaştır. Geçmiş benzerliğinin özelliği için yalnız **o tarihte sonucu tamamlanmış** olayları kullan; örnek azsa `unknown`.

### 7.2 Temas ve ayrılış

- Temasta durma süresi, bölge içindeki kapanış konumu, fitil/kapanış ayrımı ve karşı sınır davranışı.
- Ayrılışta mesafe/hız, geri çekilme ve kaynak bölgeye geri ziyaret; yalnız yaşanmış barlarla güncellenen mevcut durum.
- Önceki/sonraki bölge ilişkisi: karar anında zaten bilinen komşu bölgelere uzaklık, aradaki alan ve örtüşme. Yeni bölgenin ileride oluşacağı bilgisi hedef diye kullanılamaz.

## 8. Araştırma soruları ve sonuçlar

Hipotezler keşif amaçlıdır; önceden başarılı kabul edilmez. Her biri bölge türü, yön, periyot ve hisse bazında incelenir:

- **H1 — Hafıza:** İlk tepki sonrası ile iki veya daha fazla ayrı tepki sonrası, sonraki ziyaretin dönüş/geçiş/kalış dağılımı değişiyor mu? Ziyaret sayısını mum sayısıyla karıştırma.
- **H2 — Rol ve geçmiş geçiş:** Çok geçilmiş veya iki taraftan kullanılmış alanlarda sonraki davranış, aynı tür daha az geçmişi olan alanlardan farklı mı?
- **H3 — Yaklaşma karakteri:** Aynı bölge tipine yavaşlayarak, hızlanarak veya farklı yol verimiyle yaklaşımın sonraki olaylarla betimleyici ilişkisi var mı?
- **H4 — Ayrılma ve yol:** Bölgeden uzaklaşma, geri dönüş ve bilinen komşu bölgeye varış süresi/yolu nasıl değişiyor?
- **H5 — Etkileşim:** Bölge hafızası + hareket karakteri, aynı olay kümesinde bölgeyi veya hareketi tek başına kullanmaktan ölçülebilir ek ayrım sağlıyor mu?
- **H6 — Geometri ve zaman:** Yatay/eğimli/karma, ATR/yüzde toleransı, tüm/sınırlı geçmiş ve periyotlar arasında hangi farklar dayanıklı? Üçüncü eğimli temas uygun kontrol çizgilerinden ayrışıyor mu?

### 8.1 Sabit ufuk sonuçları

Olayın bilinebildiği bar kapanışından **sonraki** `1, 3, 5, 10, 20` tamamlanmış bar için ham getiri, gerektiğinde açıkça tanımlanan yaklaşım yönüne göre getiri, MFE/MAE, bölge dışında kalma ve geri dönüş. Olayın oluştuğu barın high/low değeri ileri MFE/MAE'ye dahil edilmez. Ufuk veri sonunu veya deney dönemi sınırını aşıyorsa `censored`, başarı/başarısızlık değil. Sabit ufuklar aynı takvim süresini temsil etmez; periyotlar birleştirilmez.

### 8.2 Olay bazlı sonuçlar

Bilinen komşu bölgeye varış, kaynağa dönüş, bölgeyi kapanışla geçiş, geri giriş ve teyitli yeni uç: olay zamanı, bilinebilir zamanı ve geçen bar sayısı kaydedilir. Başlangıçta `20` bar gözlem sınırı önerilir; gerçekleşmeyenler `censored`, eksik veriler `unknown`. Aynı mumda iki hedefe dokunma sırası bilinmiyorsa `ambiguous`; teyit gerektiren pivot geometrik zamanda değil teyit anında bilinir. Bir hedefe varamama, otomatik biçimde tersine dönme değildir.

## 9. Karşılaştırma ve keşif disiplini

### 9.1 Bazlar ve ek bilgi

- Aynı hisse/periyot/yön/benzer dönem içindeki tüm uygun ziyaretler ve mümkün olduğunda geçmiş volatilite/mesafe bakımından eşleştirilmiş örneklerle karşılaştır. Eşleşme yetersizse bunu yaz; rastgele eşleşmenin nedensellik kanıtı olduğu iddia edilmez.
- Basit mevcut teyitli swing/tek temas, mevcut yapı olayı ve yalnız hareket özellikleri karşılaştırması. Aynı bilgi olup olmadığını olay örtüşmesi ve aynı örnek kümesinde performans farkıyla incele.
- H5 için aynı kapsamdaki dört varyant: baz; baz + hafıza; baz + hareket; baz + ikisi. Farkı dağılım, örnek sayısı ve dönemler üzerinde raporla; daha çok filtreyi otomatik üstün sayma. Eksik özellikli olaylar ayrıca gösterilir; eşit karşılaştırma kümesi açıkça tanımlanır.
- Uygunsa ham getirinin yanında eşzamanlı XU100 aşırı getiri; benchmark barı eksik/eşleşmiyorsa ayrı eksik olarak say. Olay bazlı sonuçlar ve ileri getiriler farklı ölçülerdir, tek başarı oranına toplanmaz.

### 9.2 Dönem ve güven

- Ortak takvim sınırlarıyla kronolojik `%60 / %20 / %20` keşif/doğrulama/tarihsel test; sınırlar veri kapsamından **önceden** dondurulur. Isınma geçmişi her dönemin öncesinden kullanılabilir ama eğitim/özellik eşikleri geleceğe bakmaz; sonuç penceresi sınırı aşan olaylar ilgili bölüm için sansürlenir.
- Bu dönemler projede daha önce incelenmiş olabileceğinden “el değmemiş test” denmez. Değerli aday için yeni ve daha uzun tarihli veri üzerinde ayrı, önceden sabitlenmiş ileri doğrulama planlanır.
- Olay sayısı, bilinen sonuç sayısı, benzersiz hisse, bölge ve ziyaret sayısı; hisse ve takvim kırılımı, medyan ve dağılımlar verilir. Başlangıç karar eşiği önerisi: ilgili bölümde `n >= 30` tamamlanmış **ziyaret** ve `>= 10` hisse; bu eşik kanıt garantisi değil, daha azı `ornek_yetersiz`. Sayılar etkileşimli ve örtüşen olayları bağımsız yapmaz.
- Çoklu koşul/parametre ve aynı olayın farklı bölgelerde tekrar görülmesi açıkça sayılır. Basit güven aralıkları kullanılacaksa bağımlı mumları bağımsız varsaymak yerine tarih ve/veya hisse bloklarına dayalı yöntem kullanılır; uygun blok sayısı yoksa belirsizlik raporlanır. Keşfedilen tüm tarama ailesi ve seçilen/elenen sonuçlar saklanır. En iyi görünen satır seçilip genellenmez.
- Sonuç durumları: `aday`, `baglam_gerekli`, `olumsuz`, `kararsiz`, `ornek_yetersiz`, `bilgi_tekrari`, `veri_uygun_degil`. Ayrı bir ileri doğrulama olmadan `kanitlandi` veya canlı kullanım onayı verilmez.

## 10. Uygulama paketleri ve tamamlanma ölçütleri

### P0 — Envanter ve ön kayıt

- Kaynak/dosya kapsamı, periyot, zaman ve hash manifesti; seçilen seri politikası; ön kayıtlı parametre ve hipotez manifesti.
- Karşılaştırılacak mevcut araştırmaları ve farklılıklarını kaydet; çalışmayı yeni bulunmuş sonuç gibi sunma.
- **Tamam:** her seri için satır/tarih/eksik/partial sayısı ve deney sözleşmesi erişilebilir.

### P1 — Bölge ve tepki kayıtları

- Yatay tek/iki tepki, destek/direnç/karma, tepki tanımı varyantları, oyalanma ve hızlı çıkış adayları; deterministik kimlik ve snapshot.
- ATR/yüzde, tüm/sınırlı geçmiş ve ayrı ziyaret/temas mumları.
- **Tamam:** sentetik olaylar beklenen anda oluşur, önceki olaylar sonraki verilerle değişmez.

### P2 — Eğimli hiza ve örtüşme

- İki teyitli uçla aday eğim; tepe/dip ve karma yöntemler; kanallar ayrı. Üçüncü temas ve eşleştirilmiş kontrol. Yakın bölge kimlikleri korunur.
- **Tamam:** kaynak noktaları, çizgi sürümü, bağımsız sonraki ziyaret ve muğlak sıralamalar kaydedilir; aday patlaması ölçülür.

### P3 — Hareket ve bölgeler arası yol

- Yaklaşma, temas, ayrılış ölçüleri; aynı hareket, hisse geçmişi ve diğer hisselerle karşılaştırma; önceden bilinen komşu bölge ilişkileri.
- **Tamam:** mevcut durum ile sonradan gerçekleşen sonuçlar ayrı; bölgeye yaklaşan ve ondan ayrılan hareket geçmiş veriden yeniden üretilebilir.

### P4 — Sabit ufuk, olay sonucu ve karşılaştırma

- H1–H6, bazlar, ablation/örtüşme, XU100 uygunluk ve sansürleme; dönem/hisse kırılımları.
- Önce birkaç sembol/periyotta pilot; sonra hesaplama süresi ve veri kapsamı raporlanarak tüm BIST/periyotlar. Pilot örneklerinin en iyi sonuçları seçmek için yeni parametre üretilirse ayrı `post_hoc` kaydı oluşturulur.
- **Tamam:** ham ve özet tablolar, negatif/yetersiz bulgular ve tüm denenen varyantlar mevcut.

### P5 — Çoklu zaman ve aday kararı

- Gerçek kapanış anı doğrulanabilen alt/üst zaman eşleşmelerini ayrı hesapla; diğerlerini `unknown` raporla.
- Bulguları dönem, örnek, tekrarlanabilirlik, bilgi tekrarı ve sınırlamalarla sınıflandır. Ancak sonrasında özel indikatör/uyarı taslağı öner.
- **Tamam:** bulgu özeti, insanın inceleyebileceği örnekler, ham olaylar ve sonraki doğrulama önerisi sunulmuş olur.

### P6 — Daha uzun geçmiş ve bağımsız ileri gözlem

- Veri bulunabilirliği, maliyet ve kullanım koşulları ayrıca araştırılır; daha uzun veri varsa girdi politikasıyla birlikte ayrı sürüm olarak kaydedilir.
- Keşif sonrasında aday ve parametreler dondurularak daha önce incelenmemiş veri/gelecek dönem üzerinde yeniden ölçülür. Tarihsel evren üyeliği ve veri kapsamı açıkça belirtilir.
- **Tamam:** önceki keşif ile yeni dönem ayrı raporlanır; veri bulunamazsa aşama `blocked_data` ve gerekçesiyle açık kalır.

## 11. Dosyalar ve teslim sözleşmesi

Uygulama başladığında önerilen konumlar; henüz oluşturulmuş çalışma/sonuç değillerdir:

- `replayman/zone_memory.py`, `replayman/movement_character.py`: nedensel durum ve özellik hesapları.
- `tools/measure_zone_memory.py`: manifestte dondurulan parametrelerle pilot/tam evren çalıştırıcısı; CLI tasarımı uygulamada belgelenir.
- `tests/test_zone_memory.py`, `tests/test_movement_character.py`, `tests/test_zone_research.py`: sentetik ve uçtan uca regresyonlar.
- `research/measurements/zone-memory/README.md`: yöntem, bulgular, komutlar ve sınırlamalar.
- Aynı klasörde `input-manifest.csv`, `experiment-config.json`, `zone-events.csv.gz`, `visits.csv.gz`, `movement-events.csv.gz`, `outcomes.csv.gz`, `overlaps.csv.gz`, `summary.json`, `findings.csv`, `examples.csv` ve dönem/hisse karşılaştırmaları. Dosyalar girdi hash'i, kod/parametre sürümü ve üretim zamanıyla ilişkilendirilir. Büyük üretilmiş dosyalar mevcut saklama kuralları ve kullanıcıyla kararlaştırılacak boyut sınırlarıyla yönetilir.

Her `zone_id` olayına hisse, seri, periyot, tür, yöntem, geometri sürümü ve kaynak bağlanır; her ziyarete `visit_id`; her harekete `movement_id`; sonuçlara olay kimliği, ufuk, bilinebilirlik, durum (`observed/censored/unknown/ambiguous`) bağlanır. Bir olayın birden fazla bölgeyle ilişkisi tekilleştirilmeden korunur.

## 12. Test ve kabul listesi

- [ ] Tek tepki yalnız teyitten sonra aday; ikinci bağımsız tepki yalnız kendi teyidinden sonra sayılır.
- [ ] Gelecek barlar değiştirildiğinde önceki anların özellikleri, bölge kimlikleri/snapshot'ları ve olayları değişmez; yalnız ileri sonuçlar değişebilir.
- [ ] Destek, direnç, karma, çoklu geçiş ve rol değişimi geçmişi korunur; yakın bölgeler birleşmez.
- [ ] Aynı ziyaretin temas mumları ile ayrı ziyaretlerin sayısı farklıdır; sınır/eşitlik/çıkış davranışı deterministiktir.
- [ ] ATR yok/sıfır, eşit fiyat, eksik veri, kısmi bar, sıfır yol ve veri sonu sessizce başarıya dönüşmez.
- [ ] Eğimli aday sadece iki teyitten sonra görünür; üçüncü temas bağımsız kaydedilir; çizgi geçmişi sonradan düzeltilmez.
- [ ] Oyalanma ve hızlı çıkış sadece koşulun ilk bilindiği anda yayımlanır.
- [ ] İki sınır/iki hedef aynı barda görüldüğünde bilinmeyen iç sıra `ambiguous` kalır.
- [ ] İleri ufuklar, deney dönemi sınırı, teyit gecikmesi ve sansürleme doğru işlenir; XU100 eksikliği açıkça sayılır.
- [ ] Çoklu zaman eşleşmesi yalnız doğrulanmış üst zaman kapanışından sonra yapılır; doğrulanamayanlar dışlanıp sayılır.
- [ ] Tek başına/birlikte karşılaştırmalar aynı olay kümesinde yapılır; her varyant, örnek sayısı ve olumsuz sonuç saklanır.
- [ ] Küçük sentetik örnekten pilot ve tam evrene deterministik yeniden üretim; girdi hash ve parametre manifesti.

## 13. Çalışma sınırı

Bu belge uygulama ve ölçüm planıdır; herhangi bir yeni indikatörün başarılı olduğunu iddia etmez. Gerçek emir/portföy yönetimi, canlı alım-satım, grafik arayüzü, hacim ve kullanıcının ayrı OB/FVG sistemi bu planın dışındadır. Bir bulgunun istatistiksel olarak umut verici görünmesi, tek başına işlem tavsiyesi veya gelecekte kârlılık güvencesi değildir.
