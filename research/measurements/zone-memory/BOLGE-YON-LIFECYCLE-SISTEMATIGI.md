# Bölge ve Yön Lifecycle Sistemi — çalışma taslağı

**Amaç:** Fiyatın önceden bilinen bir bölgeyle ilişkisini, geçmişi silmeden aynı dille izlemek; gözlenen konum ve kapanışlardan *yön senaryosu* üretmek. **Durum:** Tasarım önerisi. Kuralların işlem avantajı, gerçekleşme olasılığı veya indikatör performansı doğrulanmadı; uçtan uca yeni lifecycle motoru henüz uygulanmadı.

Önceki çalışmalar: [hareket atlası](BOLGE-TURUNE-GORE-HAREKET-ATLASI.md), [çizim felsefesi](FELSEFE-CIZIM-SISTEMATIGI.md), [tür ve hareket karşılaştırması](BOLGE-TURU-HAREKET-KARSILASTIRMASI.md).

## 1. Ana düşünce

> **Bölge yeri gösterir; hareket geliş biçimini gösterir; kapanış ve sonraki ziyaret, hangi yön senaryosunun şu anda gözlenebilir olduğunu gösterir.**

Sistem tek bir tahmin puanı yerine iki bağımsız şey üretir:

1. **Durum:** Bölge oluştu mu, temas var mı, ziyaret bitti mi, yeniden ziyaret başladı mı?
2. **Yön etiketi:** Şu anda yukarı yönlü senaryo adayı, aşağı yönlü senaryo adayı, karışık veya bilinmiyor mu?

Yön etiketi, kapanışların bölgeye göre yerini ve olay sırasını özetler; sonraki fiyat yönünü veya kazancı garanti etmez. Önce aşağıdaki mekanik dil tanımlanır, sonra bu dilin yararlı olup olmadığı test edilir.

## 2. Bölge kartı

Her ayrı bölge kimliğinde:

- Hisse, periyot, tür: yatay, oyalanma, hızlı uzaklaşma kaynağı veya eğimli.
- Oluşum kaynağı, oluşumun **ilk bilindiği bar**, merkez ve sınırlar. Eğimli bölgede merkez ve sınırlar her kullanılabilir barda eğime göre güncellenir; bar sırası duvar zamanı değildir.
- İlk rol yalnız adaydır: tepe kaynaklı direnç, dip kaynaklı destek veya karma/belirsiz. Oyalanma ve hızlı çıkış alanlarının rolü peşinen destek/direnç ilan edilmez.
- Kaynak olaylar, geçmişteki tüm ziyaretler, geliş tarafları, temas mumları ve sonlar. Geçilen bölgeler silinmez. Yakın bölgeler birleştirilmez ve kimlikleri ayrı tutulur.
- Kullanılan tolerans ve yöntem. ATR × 0,25 mevcut araştırma varyantıdır; tek doğru bant genişliği olarak kabul edilmez. Sınırlı ve tüm geçmiş versiyonları ayrı karşılaştırılır; geçmiş eşit ağırlıklı ham olaylar olarak korunur.

Fiyatın kaynak olayı geçmişte yaşanmış olsa bile alan ancak teyit ve/veya oluşum barı **kapandıktan sonra** kullanılabilir. Yeni bölge geriye dönük olarak geçmiş bir karara eklenmez.

## 3. Kavramlar ve ölçüm kuralları

1. **Temas:** Bir kullanılabilir mumun `[low, high]` aralığı o mumdaki bölge bandıyla kesişir. Temasın görüldüğü mumun tamamlanması gerekir.
2. **Geliş tarafı:** Temastan önceki kapanış ilgili önceki barın bandının açıkça altında veya üstündeyse `alt` veya `üst`; bandın içindeyse ya da veri yetersizse `belirsiz`. Bu öneri, mevcut pilotlarda saklanan `approach_side` ile her olayda bire bir aynı olmak zorunda değildir; uygularken fark test edilmeli.
3. **Dış kapanış:** Kapanış ilgili bardaki üst sınırın üstünde veya alt sınırın altındadır. Fitilin dışarı çıkması, dış kapanış değildir.
4. **İki kapanışlı dış durum:** Ardışık iki kullanılabilir bar **aynı dış tarafta** kapanır. İçeride veya karşı tarafta kapanış sayacı sıfırlar/ilgili tarafa yeniden başlatır. Bu, önerilen çalışma eşiğidir, evrensel kırılım tanımı değildir.
5. **Ayrı ziyaret:** Önceki ziyaretin iki tutarlı dış kapanışla tamamlanmasından sonra yeni bir temas. Ziyaretin içindeki temas mumları ayrı ziyaret sayılmaz.
6. **Belirsizlik:** İki sınır aynı mumda aşıldığında mum içi sıra bilinmez. Bar kapanışının yeri bilinebilse bile iç yol bilinmeyen olarak tutulur. Eksik veri ve henüz kapanmamış ziyaretler sonuç diye etiketlenmez.

Şimdilik 2s/4s kısmi barların çıkarılması sebebiyle “ardışık” kullanılabilir bar sırasıdır; kesintisiz seans veya iki eşit duvar saati aralığı garantisi değildir. Gerçek seans kapanışı ayrıca doğrulanmalıdır.

## 4. Lifecycle: bölge kimliği kalıcı, ziyaretler tekrarlı

Durumlar *tek bir bölge kimliği* içindir. Geçmiş durumlar silinmez; bir ziyaret bitince yeni ziyaret aynı bölgede başlayabilir.

| Durum | Giriş koşulu ve o anda bilinen bilgi | Olası sonraki durum |
|---|---|---|
| `BÖLGE_BİLİNDİ` | Türün kaynağı ve gerekiyorsa teyidi kapandı. | Fiyat alanın dışında; izleniyor. |
| `DIŞARIDA_İZLENİYOR` | Bölgenin oluşumu sonrası fiyat bant dışında gözlenir. | Bölgeye temas; oluştuğu bardaki kaynak hareketi otomatik ziyaret değildir. |
| `ZİYARET_AKTİF` | Bölgeyle yeni mum temas etti. Önceki taraf, yaklaşım ve geçmişin o ana kadarki görüntüsü kaydedilir. | Aynı ziyaret içinde yeni temas, fitil, içeride veya dışarıda kapanış. |
| `DIŞ_KAPANIŞ_ADAYI` | Aktif ziyarette bir dış kapanış var. | İkinci aynı taraf kapanış veya geri giriş; tek kapanışla sonuçlanmaz. |
| `ZİYARET_TAMAMLANDI` | İki ardışık aynı taraf dış kapanışla ziyaret tamamlandı. Girişe göre `aynı taraf` / `karşı taraf` / `belirsiz` kaydedilir. | Alan dışında izleme, daha sonra yeni temas. |
| `YENİDEN_ZİYARET` | Tamamlanmış ziyaretten sonra aynı bölgeye yeni temas. Geçmiş ziyaretle ilişki kurulur. | Yeni ziyaretin sonucunu bekle; önceki kayıtlar değişmez. |
| `AÇIK_VEYA_BELİRSİZ` | Veri bitmiş, taraf tespit edilemiyor veya yeterli bar yok. | Veri geldikçe güncelle; sonuç zorla atanmaz. |

Not: Mevcut bazı yatay/eğimli pilot motorları iki ardışık dış kapanışta bitiş kaydederken kapanışların aynı tarafta olmasını zorunlu kılmaz. Bu taslakta **yön sınıflaması için** aynı tarafta iki kapanış şarttır; mevcut pilotların bitiş etiketi bu yeni lifecycle ile bire bir eşdeğer sayılmamalı. Eğimli bandın fiyat hareketi olmadan fiyatın üzerine gelebilmesi de izlenmeli.

## 5. Yön nasıl çıkar?

**Temel kural:** Sadece son mumun rengine bakma; bölgeye göre konumu, ziyaret sırasını ve kapanışları birlikte oku. Aşağıdaki etiketler son duruma aittir ve *gözlenebilir senaryo* anlamındadır.

| Etiket | Mekanik koşul / ne söyler? | Ne söylemez? |
|---|---|---|
| `YÖN_YOK` | Bölge yeni oluştu veya aktif ziyaret henüz iki tutarlı dış kapanışla bitmedi. | “Piyasa yatay gidecek” demek değildir. |
| `YUKARI_ADAY` | Alttan gelinen ziyaret, iki üst dış kapanışla tamamlandı. | Yukarı hareketin devam edeceği veya işlemin kârlı olacağı değildir. |
| `AŞAĞI_ADAY` | Üstten gelinen ziyaret, iki alt dış kapanışla tamamlandı. | Düşüşün devam edeceği veya destek kırılımının kalıcı olduğu değildir. |
| `YUKARI_İKİNCİ_ZİYARET` | `YUKARI_ADAY` sonrasında aynı bölgeye üstten ayrı ziyaret gelir ve o ziyaret iki üst dış kapanışla biter. | Evrensel “destek kesinleşti” anlamına gelmez. |
| `AŞAĞI_İKİNCİ_ZİYARET` | `AŞAĞI_ADAY` sonrasında aynı bölgeye alttan ayrı ziyaret gelir ve o ziyaret iki alt dış kapanışla biter. | Evrensel “direnç kesinleşti” anlamına gelmez. |
| `KARIŞIK` | Yön adayını izleyen ayrı ziyaret, adayın öngördüğü aynı tarafta bitmek yerine iki kapanışla karşı tarafta tamamlandı. | Hangi yönün kazanacağını söylemez; sırf iki taraflı geçmiş bulunması tek başına bu etiketi gerektirmez. |
| `BİLİNMİYOR` | Geliş tarafı, veri veya gerekli kapanış bilgisi yetersiz. | Elde kayıt olmayan şey sıfır sayılmaz. |

İşletim sırası: taraf veya veri belirlenemiyorsa `BİLİNMİYOR`; yeni ziyaret sonuçlanmadıysa güncel etiket `YÖN_YOK` ve önceki tamamlanmış senaryo ayrı geçmiş alanında korunur. Tamamlanan son ziyaret ve hemen önceki tamamlanmış ziyaret birlikte değerlendirilir. Koşullar karşılanırsa ikinci ziyaret etiketi, önceki adaya ters sonuç varsa `KARIŞIK`, yalnız karşı tarafa geçiş varsa yön adayı, aksi halde `YÖN_YOK` yazılır. Bir olayın etiketine kendi sonuçları bilindikten sonra erişilir.

`İKİNCİ_ZİYARET` ilk kez ancak yeni ziyaretin ikinci tutarlı dış kapanışı **tamamlandığında** bilinir; o kapanıştan önce sistem “yeniden ziyaret aktif” durumundadır. Yeni ziyaret için zaman sınırı henüz tercih edilmedi: önce tüm geçmiş kayıt, ayrıca önceden tanımlı 10 bar gibi sınırlı pencere varyantı araştırılır. 10 bar evrensel geçerlilik süresi değildir.

Bir **aynı tarafta tamamlanan ilk ziyaret** ayrı kaydedilir; tek başına yukarı/aşağı geçiş adayı sayılmaz. Örneğin üstten gelip üstte biten ziyaret gözlenen üst-taraf sonucudur; otomatik yükseliş tahmini değildir.

### Ters geliş veya geri dönüş

- İlk karşı tarafa geçişten sonra fiyat tekrar bandın içine gelirse olay `geri temas/ziyaret` olarak yazılır; bir mumdaki fitil tek başına önceki adayı geçersiz kılmaz.
- Yeni ziyaret iki kapanışla önceki adayın karşı tarafında biterse önceki olay silinmez; **yeni karşı olay** yazılır ve bölge `KARIŞIK` olur. İstenirse sonraki ayrı çalışmada ters yönlü yeni senaryonun kuralları ayrıca tanımlanır.
- Veri biterse gerçekleşmeyen olay uydurulmaz. Bölge kimliği ve hafızası korunur.

## 6. Dört bölge türünde aynı iskelet, farklı sorular

| Tür | Aynı lifecycle içinde özellikle izlenecek soru | Henüz doğrulanmamış araştırma hipotezi |
|---|---|---|
| Yatay | Teyitli tepe/dip alanına geliş, geçiş, iki taraftan tekrar kullanım. | Ek teyitli tepki sayısı veya geliş karakteri, sonraki davranış çeşitlerini ayırıyor mu? |
| Oyalanma | Alana geri giriş, içeride geçen temas mumları, hangi tarafta çıkış. | Eski oyalanma alanına dönüldüğünde yeniden oyalanma görülüyor mu? |
| Hızlı uzaklaşma | Kaynağa dönüş ve sonraki tarafın, kaynak hareketinin yönüyle ilişkisi. | Kaynağa farklı dönüş biçimlerinin sonraki ayrılışla ilişkisi var mı? |
| Eğimli | Her barda değişen banda göre temas/kapanış, eğim ve yeni ziyaret. | Çizgi yönü ve fiyat yolu birlikte farklı davranışlar gösteriyor mu? |

Bu sorular olası senaryolardır; veriden çıkarılmış kesin piyasa yasaları değildir. Aynı hisse/mumun birden fazla türde kaydı bağımsız teyit sayılmaz; aynı-barlılık geometrik kesişim kanıtı da değildir.

## 7. Somut senaryo: THYAO 4 saatlik oyalanma alanı

`BIST_THYAO`, `dwell:atr:0.25:z6`, yaklaşık **288,78–305,47** bandı. Bölge geçmişi zaten vardı; aşağıdaki kayıtlar yeni bir bölgenin ilk oluşumunu değil, yaşam döngüsünün belirli bölümünü gösterir. UTC değerleri **bar etiketidir**, gerçek seans kapanış saati doğrulanmadı.

1. `v3` ziyareti **27 Şubat 2026 10:30** etiketiyle üstten başlar. Bu sırada yalnız geçmiş ve temas bilinir; sonuç bilinmez.
2. Dört temas mumu gözlenir. **2 Mart 10:30** ve **3 Mart 06:30** etiketli ardışık kullanılabilir mumlar bandın altında kapanır. Böylece, bu taslağın eşiğine göre, ziyaret karşı tarafta tamamlanmış ve **aşağı senaryo adayı** oluşmuş olur.
3. Aynı bölgenin `v4` ziyareti **3 Mart 10:30** etiketinde alttan başlar. Bu anda durum **yeniden ziyaret aktif**, henüz ikinci ziyaret sonucu değildir.
4. `v4`, **5 Mart 10:30** ve **6 Mart 06:30** etiketli iki ardışık alt dış kapanışla aynı tarafta tamamlanır. Bu taslağa göre **aşağı ikinci ziyaret senaryosu** kaydedilebilir.

Bu yalnız *bir olay dizisi*dir. Sonraki fiyatın düşeceği, kalıcı direnç veya kârlı işlem kanıtı değildir. Aynı yaşam döngüsünde daha önce ve sonra başka ziyaretler de vardır. Kaynak: [ziyaretler](pilot-multiframe-dwell-atr025/visits.csv.gz) ve [ziyaret içi olaylar](pilot-multiframe-dwell-atr025/visit-events.csv.gz).

## 8. Yaklaşım ve ayrılış karakterini yönle nasıl bağlarız?

Yön etiketinin yanına **ayrı** özellikler eklenir, etiketin içine gizlenmez:

- Geliş: önceki ve yakın net ilerleme, yol verimliliği, yön değişimleri, geri çekilme. Bunlar temas öncesi veriden hesaplanır.
- Ziyaret içi: temas mumları, iç/dış kapanışlar, fitiller, iki sınırın aynı mumda aşılması ve açık kalan olaylar.
- Ayrılış: ziyaret bitişinden sonraki mesafe/yol ve önemli olaya kadar geçen süre, ayrı sonuç olarak. Bitmeden geriye taşınmaz.
- Kaynak ve komşu bölgeler: hangisinin ne zaman bilindiği ve gerçek fiyat aralıklarının kesişimi; bu motor henüz yapılmadı.

Örnek ifade: “Aşağı ikinci ziyaret senaryosu; ilk geliş üsttendi, ziyaret dört temas mumu içerdi, ikinci geliş alttandı.” Bu ifade bir gözlem kaydıdır; emir, hedef ve stop içeren bir strateji değildir.

## 9. Zaman dilimi ve test planı

Her periyot ayrı lifecycle tutar. Günlük bir bölgeyi saatlik bağlama taşımak için ilgili günlük barın **gerçek kapanış zamanı** doğrulanmalıdır; şimdi bu eşleştirme yok. Bu yüzden ayrı zaman dilimlerinde ters etiketler çelişki değil, farklı bağlamlar olabilir; tek skorda birleştirilmez.

Uygulama ve doğrulama sırası:

1. Yukarıdaki olayları nedensel olarak üret; aynı mumda iki sınır, eksik veri, farklı dış taraflarda kapanış, ziyaret çakışması ve veri sonu için test yaz.
2. Her tür ve periyotta oluşum → ziyaret → ayrılış → yeniden ziyaret senaryolarının **sayısını ve insan tarafından izlenebilir örneklerini** çıkar. Hisseler ve aynı mumu paylaşan bölgeler bağımsız kabul edilmez.
3. Geliş ve ayrılış karakterini ayrı değişkenlerle ekle. Bölgenin türü, geçmişi ve yolunun katkısını eşleştirilmiş bazlarla kıyasla; bölge genişliği, eşik ve zaman penceresi duyarlılığını göster.
4. İlk bulguları önceden sabitleyip daha uzun ve daha önce incelenmemiş veride doğrula. Kurumsal işlem, endeks üyeliği, gerçek kapanış, maliyet ve uygulanabilir emirler ayrı ele alınır.

Bu plan tamamlanmadan yön etiketi **araştırma ve karar desteği dili** olarak kalır; sinyal veya strateji diye sunulmaz.
