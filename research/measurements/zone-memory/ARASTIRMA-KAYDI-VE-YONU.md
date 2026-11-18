# Bölge ve hareket araştırması — kayıt ve genel yön

Bu dosya, mevcut araştırmanın devam noktası ve çıktı haritasıdır. **Araştırma verileri ve kodu çalışma ağacında kayıtlıdır; bu kayıt kendi başına Git commit'i veya GitHub'a push değildir.** Fiyat arşivi, araştırma dosyaları ve yöntemler [SHA-256 dosya manifesti](KAYIT-DOSYA-MANIFEST.sha256) ile listelenmiştir; kontrollerin kapsamı ve sonucu [kayıt durumu](KAYIT-DURUMU.json) içindedir.

## 1. Mevcut araştırma sorusu

Hacim kullanmadan, nedensel replay üzerinde:

> **Farklı bölge türlerinde, fiyatın geliş, temas, ayrılış ve yeniden ziyaret davranışları arasında tekrarlanan ve karar desteğine dönüşebilecek bir ilişki var mı?**

Amaç bir grafik arayüzü değil; önce fiyat davranışlarını görmek, sonra yeterli kanıt varsa özel indikatör/uyarı tasarlamak. Yakın bölgeler birleştirilmez; her bölgenin tüm geçmişi korunur. Ziyaret sayısı ile temas eden mum sayısı ayrıdır. Bölge geçildi diye geçmiş silinmez.

### Kullanıcının belirlediği çalışma ilkeleri

- Bakım, veri temizliği, CI veya yeni grafikler bu araştırmanın hedefi değil. Mevcut replay ile yeni fiyat davranışları bulunacak; yeterli kanıt ortaya çıkarsa özel indikatör konusu değerlendirilecek. **Hacim kapsam dışı**; mevcut OB/FVG sistemi gelene kadar bunun yerine yeni bir OB/FVG tanımı seçilmeyecek.
- Yalnız direnç değil; destek, direnç, karma/rol değiştiren bölgeler, sık kullanılan ve geçilmiş yatay seviyeler, eğimli hizalar; tekrarlı tepki, oyalanma ve hızlı ayrılış ayrı türler olarak incelenecek. Yakın bölgeler birleştirilmeyecek, ayrı kimlikleri ve geçilmiş olsalar da geçmişleri korunacak.
- Eski ve yeni tepkiler eşit ağırlıklı tutulacak; tüm geçmiş ve sınırlı geçmiş ayrıca karşılaştırılacak. Ayrı ziyaret ile temas eden mum sayısı, fitille geçiş ile kapanışla geçiş, dışarıda kalma ile geri dönüş ayrılacak.
- BIST 1s, 2s, 4s ve 1g önce ayrı ele alınacak; zaman dilimleri arası ilişki, gerçek kapanış zamanları doğrulanmadan kurulmayacak. ATR ve yüzde toleransları ile eğimli hiza yöntemleri ayrı karşılaştırılacak.
- İlk tepkiden sonraki davranış ve iki tepkiyle oluşan adayların sonraki ziyaretleri ayrı araştırılacak. Yaklaşma yolu/hızı, önceki yapı, temastan ayrılış, dönüş, komşu bölgeler ve önceki bölgeden gelen yol; hareketin kendi evreleri, hissenin geçmişi ve diğer hisselerle ayrı ve birlikte ele alınacak.
- Sabit ufukların yanı sıra sonraki önemli olaylar, bölgenin yıpranma/güçlenme/karakter ve rol değişimi de araştırılacak. Tekrarlanabilirlik, karar desteği ve beklenmedik keşiflerin tümü değerlidir; gerçek hisse/tarih örnekleri ve ayrıntılı ham kayıtlar korunacak.
- Mevcut yaklaşık bir yıllık veri **önce keşif** içindir; daha uzun ve incelenmemiş geçmişle doğrulama sonraki aşamadır. Bu listedeki her araştırma sorusu henüz tamamlanmış değildir; kapsam ve açık işler [planda](../../plans/bolge-hafizasi-hareket-karakteri.md) ve aşağıdaki devam notunda yer alır.

## 2. Bugüne kadar ne bulundu?

- Dört bölge türü — yatay teyitli tepe/dip, oyalanma, hızlı uzaklaşma kaynağı ve eğimli hiza — ayrı tanımlandı. Yaklaşık bir yıllık mevcut BIST verisinde dört periyot araştırıldı; kapsam tüm çalışmalar ve alt kümeler için aynı değildir.
- Farklı yöntemler çoğu zaman aynı hisse ve mumdaki fiyat olayını kaydediyor. Bunları bağımsız teyit veya geometri olarak örtüşen alanlar gibi sayamayız.
- Bölgenin hangi tarafından gelindiği, geçmiş ziyaretler ve yaklaşımın ayrı kayıtlar olması anlamlı bir çalışma dili sağlıyor. Buna rağmen **hafızanın bağımsız yön etkisi kanıtlanmadı**.
- `karşı tarafa geçiş → yeni taraftan yeniden ziyaret → aynı tarafta kapanış` dizisi tarihsel kayıtlarda görüldü. Ancak dizinin tek başına güvenilir fiyat yönü veya işlem avantajı sağladığı gösterilmedi.
- On filtre testinde en ilginç aday **F01: yatay 4s, aşağı yönlü senaryoda yeniden ziyaretin önceki ziyaret bitişinden 11+ kullanılabilir bar sonra başlaması**. Doğrulama ve tarihsel testte seçilmiş basit kontrol grubuna karşı pozitif yönlü XU100 medyan farkı çıktı; aynı veri defalarca incelendiğinden bu bağımsız doğrulama değildir.
- İlk F01 testinde her iki grupta en az üç olay bulunan yalnız **5 ortak hisse** vardı; ilk kontroller eşleştirilmedi. Ardından aynı hisse ve yakın tarihte volatilite/bant genişliğiyle eşleştirme yapıldı: tarihsel testte 160 adaydan 46'sı eşleşti, 37 çiftin beş bar sonucu kullanılabildi. Eş içi medyan XU100 farkı +1,15 puan olsa da haftalık aralık [−2,51; +2,32]; ham fiyat yönü karşılaştırması da kararlı avantaj göstermedi. [Yeni rapor](F01-ESLESTIRME-VE-SANSUR.md).
- Aşağı geçiş adaylarından geri gelmeyenler de ayrıca sayıldı: testte tam 20 bar izlenebilen 819 adayın 266'sında aynı bölgeye yeni ziyaret başlamadı; 61 aday 20 bar için sansürlüydü. Bu bir survival analizi veya evrensel oran değildir.
- Geri ziyaret yol incelemesinde testte ilk beş barda dönmeyip 20 barı tam gözlenen 405 aşağı adaydan, beşinci barda 0–1 ATR aşağıda olanların 44/57'si, 2 ATR'den uzak olanların 44/226'sı sonraki 15 barda geri geldi. Bu özellik ancak beşinci barda bilinir; seçim ve mesafe geometrisi önemlidir. Eşli F01'in 37 test çiftinde ortalama endekse göre +1,19 puan fark, +0,58 ham hisse ve −0,61 yönlü endeks farkı bileşenlerine ayrıldı. [Ayrıntılı yol ve bileşen raporu](F01-ZIYARET-VE-HAREKET-NEDEN-INCELEMESI.md), `f01-reasons/`.
- Çoklu denemeler, örtüşen pencereler ve az sayıda hafta nedeniyle aday indikatör veya işlem kuralı değildir.

**Yönlü XU100 farkı, hisse fiyatının yönü veya strateji getirisiyle aynı şey değildir.** Verideki bar etiketleri gerçek seans kapanışını kanıtlamaz. 2s/4s kısmi bar filtreleri, özellikle gecikme ve ufuk süresi yorumunu sınırlar.

### Yapılan işin kapsamı ve okuma sınırları

- Lifecycle kayıtlarında toplam **614.630 tamamlanmış tür-içi temsilci** bulunur. `events.csv.xz`, hisse/tür/periyot/bitiş barı başına tek temsilciyi tutar; tüm ziyaretler değildir. Türler aynı olayı paylaşabilir. Bütün ziyaret ve açıklar ilgili `inventory.csv` dosyalarında ayrıca sayılır.
- Yatay, oyalanma ve hızlı ayrılış türlerinde dört periyot için 100 hisselik koşular vardır. Eğimli bölgede 4s/1g 100 hisse; 1s/2s ise **alfabetik 15 hisselik pilot**tur, rastgele örneklem veya 100 hisselik sonuç değildir. Diğer araştırmaların kendi evren ve periyot kapsamları raporlarında belirtilmiştir.
- Ortak fiyat olaylarında hareket ve bölge türünü birlikte kullanan önceki karşılaştırma, beş barlık yönlü endeks-farklı ters hareket ölçüsünde tutarlı ek avantaj göstermedi. 10 filtre incelemesinde **80.252 olay** ve **925 karşılaştırma** vardı; hiçbir filtre, uygun senaryo içi hücrelerde iki dönemde aynı yönde sıfır dışı haftalık aralık göstermedi.
- F01 eşleştirme sonrasında testte 37 tam 5 bar çifti **29 hisseye** aittir; 160 adayın 114'ü eşleşmedi. Bu nedenle sonuç tüm adayların sonucu değildir. Eşli 10 bar test medyanı −0,39 puan ve 28 çifttir; önceki 5 bar haftalık aralık sıfırı kapsar. Eş kontrolü gelecek tarihli olabildiğinden eşleştirme canlı bir işlem yöntemi değildir.
- 20 bar içindeki ziyaret yokluğu sonsuza kadar dönüş yokluğu değildir; 20 barı gözlenemeyenler sansürlüdür. İlk beş barlık yol analizi erken geri gelenleri dışarıda bırakan bir **beşinci bar landmark** analizidir, tüm geçiş adayları için başlangıç anı tahmini değildir.
- Gözlenen fiyat yolları piyasa katılımcılarının niyetini veya ilişkinin gerçek nedenini belirlemez. Aynı doğrulama/test dönemleri keşiflerde tekrar tekrar görüldü; hiçbir bulgu bağımsız doğrulama, kârlılık veya al/sat sinyali olarak sunulmaz.

## 3. Sonraki araştırma yönü — öneri

### Öncelik A: F01'i daha adil karşılaştır — ilk keşif yapıldı

Aynı 4s hisse ve son taraf için yakın dönemde ve geçmişten bilinen benzer volatilite/bant genişliğiyle kontrol eşleştirildi. Eşleştirme gelecek sonuç kullanmadan ve tekrar kullanımsız yapıldı; eşler, eşleşmeyenler, 5/10 bar sonuçları ve belirsizlik [raporda](F01-ESLESTIRME-VE-SANSUR.md). Testte 160 vakadan yalnız 46'sı eşleşti, 37'sinin iki taraflı 5 bar sonucu vardı. **Bu, önceki veriden çıkarılmış adayı bağımsız doğrulamaz.**

Sonraki olası adım, eşleşme toleranslarını önceden sabit duyarlılık varyantlarıyla ve zaman/hisse bağımlılığını birlikte dikkate alan yöntemle incelemektir; veri azlığını veya eşleşmeyen vakaları gizlememek gerekir.

### Öncelik B: Geri gelmeyen ve açık kalan adayları izle — ilk yol keşfi yapıldı

Yatay 4s temsilci geçiş adaylarında ilk sonraki ziyaret; 10/20/40 bar tam pencere, dönmeyen ve sansürlü durumları ayrı sayıldı. Tam pencere seçimi erken dönem olaylarını kayırabileceğinden, farklı ufuk yüzdeleri aynı payda değildir; sansürü modelleyen survival analizi henüz yapılmadı. [Sansür raporu](F01-ESLESTIRME-VE-SANSUR.md), [ilk beş bar yol ve bileşen incelemesi](F01-ZIYARET-VE-HAREKET-NEDEN-INCELEMESI.md) ve `f01-censoring/`, `f01-reasons/` ham kayıtları.

**Kaldığımız nokta:** Gözlenen mesafe–geri ziyaret ilişkisinin bariz bir mesafe/zaman geometrisinin ötesinde bilgi içerip içermediği bilinmiyor. Önerilen sıradaki keşif, beşinci bardaki mesafeye dayanan basit bir karşılaştırma tabanı kurmak; benzer hisse, dönem ve mesafede yol/önceki ziyaret/komşu bölge özelliklerinin ek katkısını ayrı incelemek. Aday tanımları, hangi anda bilindikleri ve sansür açıkça kaydedilmeli. Bu yeni bir onaylanmış indikatör kuralı değildir.

### Öncelik C: Bağımsız dönemle doğrula

Aday ve değerlendirme planı sonuçlara bakmadan sabitlenip **daha uzun ve daha önce incelenmemiş** veri üzerinde ayrıca sınanmalı. Daha uzun veri bu çalışmada hazır kabul edilmiyor. Gerçek seans kapanışı doğrulanmadan çoklu zaman eşleştirmesi yapılmaz; kurumsal işlem, endeks üyeliği, maliyet ve uygulanabilirlik araştırma/strateji aşamalarında ayrıca ele alınır.

Bu üç aşamanın ardından hangi davranışın tekrarlanabilir, insana faydalı ve beklenmedik keşif değeri taşıdığına bakılarak özel indikatör veya uyarıya karar verilebilir. Şimdi tek başına F01 ya da başka bir filtreyle otomatik al/sat kuralı çıkarılmamalı.

## 4. Dosya haritası

| Dosya veya dizin | İçerik |
|---|---|
| [Araştırma planı](../../plans/bolge-hafizasi-hareket-karakteri.md) | Kapsam, kullanıcı tercihleri ve açık araştırma işleri. |
| [İlk evren sonuç raporu](SONUC-RAPORU.md) | 100 hisselik ilk tarama, duyarlılık, kapsam ve eksikler. |
| [Çizim felsefesi](FELSEFE-CIZIM-SISTEMATIGI.md) | Bölge kimliği, geçmiş, temas ve çoklu zaman ilkeleri. |
| [Bölge ve hareket karşılaştırması](BOLGE-TURU-HAREKET-KARSILASTIRMASI.md) | Ortak olaylarda tür ve geliş özelliklerinin sınırlı karşılaştırması. |
| [Hareket atlası](BOLGE-TURUNE-GORE-HAREKET-ATLASI.md) | Bölgeye göre hareket çeşitleri ve gerçek hisse/bar örnekleri. |
| [Yön lifecycle taslağı](BOLGE-YON-LIFECYCLE-SISTEMATIGI.md) | Durum ve yön senaryosu tanımları. |
| [Lifecycle tarihsel sınaması](SENARYO-LIFECYCLE-DOGRULAMA.md) | Senaryo motoru, 100 hisse/alt kapsam, sonuçlar ve belirsizlik. |
| [Küçük filtre keşfi](KUCUK-FILTRELER-KESIF.md) | Gecikme ve temas sayısı varyantları; F01 adayı. |
| [On filtre ve yön araştırması](ON-FILTRE-YON-ARASTIRMASI.md) | On filtrenin tanımı, karşılaştırmalar ve F01 sınırları. |
| [F01 eşleştirme ve sansür](F01-ESLESTIRME-VE-SANSUR.md) | Aynı hisse eşleri, eşleşmeyenler, geri gelmeyen ve açık adaylar. |
| [F01 ziyaret yolu ve neden incelemesi](F01-ZIYARET-VE-HAREKET-NEDEN-INCELEMESI.md) | İlk beş bar ve geri temas, fiyat/endeks bileşenleri, AEFES örnekleri ve sınırlamalar. |
| [`f01-matched/`](f01-matched/), [`f01-censoring/`](f01-censoring/), [`f01-reasons/`](f01-reasons/) | Eşli/ eşleşmeyen olaylar, sansür kohortu, aday bazında yol, alt grup özetleri ve kaynak hash'leri. |
| [`ten-filters/`](ten-filters/) | 10 filtre özellikleri, gruplar, 925 karşılaştırma ve girdi/kod hash'leri. |
| [`lifecycle-analysis/`](lifecycle-analysis/) ve `lifecycle-*` | Durum/senaryo sonuçları, temsili olaylar, envanter ve kaynak manifestleri. |
| `universe-*`, `sensitivity-*`, `pilot-*`, `movement-*` | Önceki ham olaylar, duyarlılık çalışmaları ve pilot kayıtları. |
| [`sources/`](sources/) | Geçmiş koşularda kullanılan hash'i doğrulanabilir kaynak sürümleri. |

Her rapor kendi kapsamını ve tekrar üretme komutlarını belirtir. `events.csv.xz` / `.csv.gz` sıkıştırılmış olay tablolarıdır. Fiyat girdileri `data/ohlcv/` altında ve ilgili input/benchmark manifestlerinde kayıtlıdır. Manifest, dosyaların doğruluğunu veya gelecekteki piyasa geçerliliğini değil, **kaydedilen içeriklerin değişip değişmediğini** kontrol eder.

## 5. Bütünlük kontrolü ve test

Depo kökünden:

```bash
# Kayıt durumunu ve SHA-256 listesini günceller; önce kaynak veri manifestlerini doğrular.
.venv/bin/python -m tools.archive_zone_research
# Manifestte listelenen dosyaların kaydedilen içerikle eşleşmesini doğrular.
sha256sum -c research/measurements/zone-memory/KAYIT-DOSYA-MANIFEST.sha256
.venv/bin/python -m pytest -q
```

Tekrar üretim komutları belirtilen çıktı dizinlerinde mevcut sonuçları yeniden yazabilir. Bağımsız doğrulama ve canlı işlem testi yapılmadan bulgular araştırma sınıfında kalır.
