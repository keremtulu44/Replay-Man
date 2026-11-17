# Pozisyon öncesi makro risk tablosu — çalışma sözleşmesi

Amaç kullanıcının uzun yönlü işlem fikrinde “altın/petrol/bakır gibi bir kaynak düştüğünde bu hisse geçmişte ne sıklıkla düşmüş?” sorusunu **risk bağlamı** olarak sistematik göstermek. Bu bir otomatik alım/satım emri veya yatırım tavsiyesi değildir. Kaynak/hisse örnekleri ve önceki sonuçlar daha önce görüldü; çalışma tamamen yeni kör test değil.

## Evren, sinyal ve yön

Bütün 100 BIST hissesi ve 10 endeks; 7 emtia vadeli proxy'si: Brent, WTI, altın, gümüş, bakır, platin, paladyum. Her biri USD ve emtia × USDTRY yaklaşık TRY vekilinde ayrı. Ortak BIST referansında 10 `1h` veya 10 `4h` tamamlanmış bar, kaynak ve hedef zamanlarının as-of sözleşmesi `../10bar-commodity-reactions/PLAN.md` ile aynı. Bar bitişi nominal süre; eksik/bar as-of/kur uyumu belirsizse sinyal veya sonuç bilinmiyor. İşaret sıfırdan küçük `down0`, büyük `up0`; ayrıca kaynak ≥+%2, ≤−%2, ≥+%4, ≤−%4 ayrı. Çok küçük oynama `down0` sayılır; kaynak büyüklüğü sabit %2/%4 kontrolleriyle de gösterilir. Aynı dört koşul dahil her kaynak ve hedef kaydedilir, sonuca göre seçilip kötü örnekler atılmaz.

## Kullanıcı örneğindeki oran ve zaman

Her koşulda **hisse hedef getirisi <0** düşüş, >0 yükseliş, tam 0 yataydır; kaynak ve hedef bilinen n içinde `düşen/n`, `yükselen/n`, `yatay/n` ayrı gösterilir. −%3 veya daha kötü ayrıca, daha derin risk olarak sayılır. `same` kaynak ve hissenin aynı on barda birlikte hareketidir; kaynak yönü pencere sonunda bilinir, geçmişte hissedilen eşzamanlı baskı olarak yorumlanabilir ama sonraki mumlar için tahmin ya da sinyal başında kullanılabilir bilgi değildir.

Pozisyon sonrası öncelikli görünüm `post_open`: kaynak 10-bar sinyali kapanınca bilinir, **nominal sinyal kapanışından kesinlikle daha sonra başlayan ilk ortak hedef/XU100 barının açılışından başlayarak 10 ortak BIST barının son kapanışına** hisse getirisi. Sinyal kapanışına denk gelen barın açılışı atlanır; zamanlar birebir eşleşmeli, eksik/uygunsuz değer `NaN`, kaynak pencere başlangıcı ve son ufuk nominal bitişi aynı UTC split olmalı. Bu bir gecikmeli açılış vekilidir, emir gerçekleşmesi/likidite/maliyet/stop garantisi değildir. `after` eski kapanıştan sonraki 10 bara etiket ayrı durur; bu giriş gerçekte yakalanabilir varsayılmaz. `post_open` sinyale kadar yaşanmış zararı tekrar saymaz, işlem öncesi mevcut pozisyonun geçmiş zararı başka bir şeydir.

## Tekrar, payda, karşılaştırma

Ana görünüm her kaynak × yön/eşik × hisse × para birimi × periyot için **kaynak şokları bilindiğinde seçilen ve kaynak 10-bar pencereleri çakışmayan** `shock_episode`, herhangi bir hedef sonucu dikkate alınmadan seçilir. Hedef barı/sonuç eksikse n dışındadır, daha sonra sonuca bakılarak başka şok seçilmez. Seçim aynı kaynak eşik ve takvim split'inde ayrı; farklı kaynaklar ve eşikler aynı olayları paylaşabilir. Örtüşmeyen giriş pencereleri bağımsız olay, varlıklar arası bağımsızlık, sonraki portföy çakışmasının giderilmesi demek değildir. `all_bars` ve `fixed_nonoverlap` ayrıca korunur.

Tüm eşik × hedef × yön için eğitim, doğrulama, test **ve** bu bölümler içi geçerli olayların toplamı verilir (her bölümden başka bölüme taşan ufuklar yok); toplam için olay sayıları toplanır ve oran paydan hesaplanır, ortalama oran alınmaz. Baz: aynı kaynak/birim/periyot/hissede bütün bilinen kaynak pencerelerinin bağımsızca sabit 10-bar ızgarasındaki hedef düşme oranı. Sabit ızgara şok havuzuyla aynı tarihlerden oluşmaz; fark yalnız betimleyici kıyas, eşleştirilmiş kontrol veya nedensel risk primi değildir. Toplam ve bölüm sayıları/hesaplanamayan örnekler gösterilir; yarın için güvenilir olasılık iddiası yoktur.

## Bayrak ve eksik örnek

Uzun işlem için n≥10 ve en az %70 tarihsel düşüş `tarihsel_uyari`; n≥10 ve <%70 `esik_altinda`; n<10 `ornek_yetersiz`. %70 ve 10, kullanıcı örneğinin anlaşılır bir tarama kuralına çevrilmiş **keyfi, betimleyici eşikleridir**, doğrulanmış risk limiti değildir. Bayrağı `post_open` toplam örneğine uygula; `same` bayrağı geçmiş eşzamanlı gözlem olarak ayrı tutulur. Tüm sonuçlar, baz sayı ve baz farkıyla yayımlanır; düşük/yetersiz kayıtlar saklanır. `no_jump10` duyarlılığı bağımsız olarak ayrıca gösterilir ve sıçramaların hata olduğu iddia edilmez. Önceki test periyodu görüldü, çok sayıda kombinasyon var; yüksek oranlar sahte keşif olabilir. Tek başına pozisyon veto etmez.

`down3_count`/n ve baz da saklanır; n dışındaki ham kaynak şok sayısı gösterilir. `sample_status` yalnızca örnek büyüklüğü. Çıktı tüm kombinasyonların CSV'si, insan tarafından okunur açıklama, örnek hisseler ve istenen hisse/kaynak için bir sorgu CLI'dir; canlı kur/fiyat sağlayıcısı veya gerçek-zamanlı bildirim bu görevde yoktur. Aynı anda birden fazla eşik/emtia gerçekleşirse oranları çarpmak veya toplamamak gerekir; ortak şoklar aynı günlere denk gelebilir.
