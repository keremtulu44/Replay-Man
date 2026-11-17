# Genel piyasa ve hisse bağlam sistemi — taslak plan

**Durum: Hacim hariç plan kullanıcı tarafından uygun bulundu; endeks ve kur ilk ölçümü tamamlandı, diğer aşamalar sürüyor.** Bu belge henüz yapılmamış ölçümlerin veya ekranın tamamlandığını iddia etmez.

## 1. Amaç

Kullanıcı bir hisseyi incelerken piyasa, endeks, döviz, emtia ve hisse içi verilerinin o anda ne söylediğini; geçmişte benzer koşullarda hissenin nasıl davrandığını birlikte, fakat birbirine karıştırmadan görebilsin. Özellikle uzun pozisyon öncesi riskli tarihsel bağlamlar gösterilsin. Sistem **işlem açmaz, emir göndermez, işlemi engellemez, al/sat tavsiyesi üretmez**; destekleyici bilgi sağlar. Kısa/yukarı-aşağı yön araştırması daha sonra eklenebilir, ancak yükseliş ve düşüş olayları baştan ayrı kaydedilir.

## 2. Mevcut durum

- 100 BIST hissesi, 10 BIST endeksi, 6 küresel endeks/gösterge, 2 döviz serisi ve 7 emtia proxy'si katalogda mevcut; her seri ve periyodun fiili kapsaması ayrıca gösterilecek. Tarihsel evren üyeliği doğrulanmış değildir.
- [Emtia risk arşivi](../measurements/macro-risk-screen/README.md): 7 emtia × hisse/endeks; 1h/4h; 10 mum; USD ve yaklaşık TL vekili; eşzamanlı ve sinyal sonrası sonuçlar zaten ölçüldü.
- [Altın/gümüş denemesi](../measurements/metal-filter-backtest/README.md): seçili sanal işlem kurallarıyla katı eleme senaryoları; genel bir indikatörün değerini kanıtlamaz.
- [Endeks ve kur ilk ölçümü](../measurements/market-context/README.md) tamamlandı. Hisselerle sektör endeksi üyeliği, ortak koşul çalışmaları ve bütün katmanları birleştiren ekran bu kapsamda henüz tamamlanmış değildir. Hisse trend/yapı araştırmaları vardır; bu plan bunları otomatik doğrulanmış sinyal saymaz.

## 3. Gösterilecek bağlam katmanları

### A. BIST ve sektör

- XU100 ve mevcut diğer BIST endekslerinin yönü, büyüklüğü ve güncelliği.
- Her hisse için XU100 karşısında aynı penceredeki göreli hareket ve geçmiş tepki. Endeks düştüğünde/yükseldiğinde hisse kaç olayın kaçında düşmüş/yükselmiş?
- Sektör endeksi mevcut ve üyelik güvenilir biçimde biliniyorsa ayrıca sektör. Üyelik bulunamaz veya zamana göre doğrulanamazsa “sektör bilinmiyor”; otomatik yanlış eşleştirme yapılmaz. İlgili endeksin tarihsel üyelik etkisi açıklanır.

### B. Emtia ve döviz

- Brent, WTI, altın, gümüş, bakır, platin ve paladyum: hem yükseliş hem düşüş; mümkün olduğunda USD ve önceki çalışmadaki yaklaşık TL vekili ayrı. Vadeli seri spot fiyatın aynısı değildir.
- USD/TRY ve mevcut diğer uygun döviz; kur hareketi ile hisse tepkileri ayrı ölçülür. Veride bulunan uygun küresel göstergeler, kapsama kontrolünden sonra ayrı kaynaklar olarak eklenir.
- Her hisse her kaynakla aynı şekilde ilişkilidir veya emtia hareketi sonucun nedenidir varsayılmaz. İlişkiler sonuçlardan bağımsız tüm kombinasyonlar için kaydedilir.

### C. Hissenin kendi durumu

- Fiyat yapısı: son hareket yönü, yakın tepe/dip ve teyitli seviye bağlamı.
- Trend/oynaklık: örneğin ortalamalara göre konum ve ATR gibi, hesaplama yöntemi açık gösterilen ölçüler.
- Kullanıcı tercihi: hacim hiçbir bağlam katmanında, koşulda veya değerlendirmede kullanılmaz.
- Bu bilgiler makro oranlarla otomatik toplanmaz ve bir stratejinin başarılı olduğu iddia edilmez. Teknik göstergelerin geçmiş davranışına yönelik yeni ölçümler ayrı etiketlenir; önceki araştırmalardaki kararsız ve olumsuz bulgular da korunur.

## 4. Tek ve tutarlı ölçüm sözleşmesi

- Başlangıçta 1 saat ve 4 saat periyotları **ayrı**, kaynak ve hedefler için ortak XU100 barları ve 10 mumluk olay pencereleri kullanılır. Mevcut emtia çıktıları aynı tanımlara uyduğu ölçüde yeniden kullanılır; başka ufuklar eklenirse ayrı raporlanır.
- Her kaynak için yükseliş, düşüş ve büyüklük bantları açıkça tanımlanır. Başlangıçta yön ve ±%2/±%4 gibi eşikler incelenebilir; kur/endekste büyük eşikler az olay üretebileceğinden ham olay sayılarıyla gösterilir. Eşikler testten önce dondurulur, en iyi sonuç için sonradan seçilmez.
- Kaynak sinyalinden önce/aynı anda gerçekleşen hisse değişimi (`same`) ve sinyalden kesinlikle sonra başlayan gecikmeli açılıştan sonraki hisse değişimi (`post_open`) ayrı tutulur. Eşzamanlı oran gelecek tahmini gibi gösterilmez. Giriş proxy'si gerçek gerçekleşme garantisi değildir.
- Örn. kaynak düşüş olaylarında hisse `<0`, `=0`, `>0`, ayrıca `≤−%3` adetleri ve `düşen / bilinen sonuç` oranı. Kaynak olayları hedef sonucundan bağımsız ve çakışmasız seçilir; eksik hedef sonucu n dışıdır. Farklı kaynaklara ait olaylar ve sonraki pencereler örtüşebilir.
- Her sonuçla birlikte dönem, sinyal sayısı, geçerli n, düşen/yükselen/yatay sayıları, hareket eşiği, fiyat birimi ve koşulsuz sabit-ızgara baz gösterilir. Baz şoklarla aynı tarihte eşleştirilmiş kontrol değildir; aradaki fark yalnız betimleyici karşılaştırmadır. Uygun olduğunda endeks getirisine göre hisse farkı ayrıca gösterilir.
- Altın ve endeks aynı anda hareket ettiğinde, **ortak koşulun kendi geçmiş olayları** ayrıca hesaplanır ve n yetersizse açıkça belirtilir. Tekil oranlar toplanmaz/çarpılmaz; çelişen bilgiler saklanır. Çoklu koşul ölçümleri örneği hızla küçültür ve çoklu tarama riski doğurur.

## 5. Tek hisse için önerilen ekran

Aşağıdaki yalnızca **tasarım örneğidir**, güncel durum veya yeni hesaplanmış sonuç değildir:

```text
Hisse: [seçilen hisse]    Periyot: 4h    Veri zamanı: [son kapanış]

Piyasa        XU100: yön / büyüklük    Hisseye göre: güçlü / zayıf / belirsiz
Sektör        İlgili endeks ve üyelik doğrulandıysa göster; değilse bilinmiyor
Döviz         USD/TRY: yön / büyüklük  Geçmiş hisse tepkisi: düşen / n
Emtia         Altın, gümüş, Brent ...   Her biri: hareket, düşen / n, baz oran
Hisse         Yapı / trend / oynaklık bilgisi; her biri kendi kaynağıyla
Güven         Dönem, n, eksik/stale veri, dönem tutarlılığı ve açıklama
```

Bir satırda örnek: “Altın −%2 veya daha fazla; geçmişte sonraki 10 mumda hisse 15/20 olayda düşmüş; genel baz 23/40.” Bu, önceki arşivde TUPRS için toplam dönem örneğidir, **anlık güncel sinyal değildir**. Ölçüm periyodu ve karşılaştırmanın niteliği satırda görülecek. `n<10` gibi bir örnek eşiği yalnız kullanıcıya açık keyfi bir ilk filtre olabilir; daha yüksek örnek de kesinlik sağlamaz. Gerekirse “veri yetersiz / koşul yok / hesaplanamadı” ayrı gösterilir. Sonuçlar tek bir 0–100 güven puanına veya otomatik al/sat kararına indirgenmez.

## 6. Doğrulama ve dürüst kullanım

1. Kaynak sinyalleri sadece tamamlanmış ve o anda bilinen verilere dayanır. Kaynak barı en fazla tanımlı süre kadar eski olabilir; kapanış ve zaman eşleşmesi kaydedilir. İleri veri hiçbir geçmiş sinyale girdi yapılmaz.
2. Tarihsel oranlar geçmişe dönük testte yalnız o ana kadar sonucu tamamlanmış olaylardan hesaplanır; günümüzde bilinen toplam oran geçmişe taşınmaz. Dönem sınırlarını aşan ufuklar tasfiye edilir.
3. Hisse/koşul ve dönem kırılımları ile küçük/eksik örnekler korunur; fazla kombinasyon ve geçmişte incelenmiş dönemler nedeniyle sonuçlar keşifseldir. Mümkün olduğunda gelecekte yeni gelen verilerle ayrı ileri gözlem yapılır.
4. Bölünme, fiyat serisi, nominal mum kapanışı, seans, eksik bar, vadeli seri geçişi ve fiyat vekili uyarıları sayısal kapsamla raporlanır; küçük veri oynamaları projeyi durduran önkoşul yapılmaz.
5. Ölçüm kalitesini değerlendirmek için geçmiş bağlamların sonraki hareketleri ve genel bazları karşılaştırılır; seçilen modelin dönem/hisse tutarlılığı incelenir. İndikatörün değerini yalnız kârlı veya zararlı işlem elemesiyle değerlendirmek gerekmez.

## 7. Aşamalar ve teslimler

1. **Ölçüm sözleşmesi ve envanter:** Mevcut dosya/dönem/periyot, endeks ve kur kapsamı, sembol ve güvenilir sektör eşleşmesi tespit edilir. Eksik kapsam açıkça listelenir.
2. **Genel ilişki tabloları:** Mevcut emtia sonuçları korunarak BIST/küresel endeks ve kur × tüm hisseler için aynı yön, büyüklük, 10 mum, eşzamanlı/sonrası, n ve baz tabloları çıkarılır. İstatistikler kaynak bazında ve birleşik indekste filtrelenebilir dosyalara kaydedilir.
3. **Hisse bağlamı:** Önce mevcut nedensel yapı/trend/oynaklık özellikleri tanımlarıyla sunulur; yeni kurallar ve geçmiş tepkileri ayrı araştırılır. Yeni hesaplanmamış bilgiler hesaplanmış gibi sunulmaz.
4. **Ortak durum ve doğrulama:** Önceden belirlenen birkaç anlamlı ortak koşul, dönem/hisse bazlı denetim, örnek azlığı ve zaman sızıntısı testleri. Negatif sonuçlar da yayımlanır.
5. **İndikatör/ekran taslağı:** Sembol ve periyot seçimi, her kaynağın son veri zamanı/hareketi, geçmiş pay/payda ve baz, hisse bağlamı, bilinmezlikler ve ayrıntı bağlantıları. Önce mevcut veriyle çalışan prototip; otomatik sürekli veri akışı veya gerçek zaman iddiası ancak ayrıca yapılırsa eklenir.

Her aşamada yöntem, veri kapsamı ve kısıtları içeren Türkçe rapor; ham ve özet dosyalar; yeniden çalıştırma komutu ve birim testleri tutulur. Veri erişimi veya yetersiz örnek varsa ilgili sonuçlar “bilinmiyor” gösterilir, genel çalışma durdurulmaz.

## 8. Kararlar ve uygulama sırası

- Yukarıdaki kapsam ve sıralamaya göre önce **endeks + döviz ilişkileri**, sonra hisse bağlamı ve ekran çalışılması önerilir.
- Yalnız uzun işlem değerlendirme amacına hizmet eden bir **bağlam/uyarı sistemi** yapılacaktır; emir, otomatik veto veya kârlılık vaadi yoktur.
- Hacim kullanıcı isteğiyle kapsam dışıdır. Eşikler, kaynak kapsamı ve görünüm ölçüm sözleşmesinde açıkça kaydedilecektir.
