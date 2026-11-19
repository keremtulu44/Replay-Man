# Dip adayı araştırması — sabit deney sözleşmesi

**Durum:** 19 Kasım 2026'da, mevcut Replay-Man veri ve önceki araştırmaları görülmüşken hazırlanmış keşif planı. Bu, önceki veriden bağımsız ön kayıt değildir. İç dönemlerdeki eğitim/doğrulama/test etiketleri temiz ileri test anlamına gelmez. Bu plan hisse al/sat tavsiyesi, portföy performansı veya gerçek gerçekleşme iddiası değildir.

## Soru ve üç aday

Amaç mutlak dibi önceden bildiğini iddia etmek değil, sinyal üretildiğinde bilinen bir dip-adayı bilgisinin basit fiyata ek katkısını ölçmektir. Yalnız OHLC kullanılır; **hacim yoktur**. `4h` ve `1d` ayrı sonuçlardır; kaynak `complete=false` satırlar çıkartılır ve sayılır. Sinyal barı tamamlanmadan sinyal bilinmez. Birden fazla deneme aynı olayı temsil edebilir.

- **A — failed_low5:** Önceki beş kullanılabilir barın en düşük seviyesi `L5`; `low[t] < L5`, `close[t] > L5` ve `close[t] > open[t]`. Bu, mevcut sanal işlem çalışmasındaki basit vekildir, kitapta anlatılan yapının tamamı değildir. Başlangıç ATR14 mevcut ve pozitif olmalıdır.
- Aynı hisse/periyotta ilk A adayından sonra **10 kullanılabilir bardan az** sürede gelen yeni A adayı seçilmez. Seçim yalnız geçmişte seçilmiş adaylara bakar; bütün A adaylarına ve ardından alt kümelere aynı kural uygulanır.
- **B — A + eski destek adayı:** A barından önce bilinen 2+2 teyitli yatay swing bölgesi, ATR14 × 0,25 yarı genişlikle oluşmuş ve o anda `support_candidate` olmalıdır. A barının high–low aralığı bölgeyle kesişir, A kapanışı bölge alt sınırı altında değildir ve önceki kapanış da bu alt sınırın altında değildir. Bölge yaratma/güncelleme barındaki bilgi aynı barda geçmişe taşınmaz. Birden fazla bölge için en küçük merkeze-normalize mesafe, eşitlikte bölge yaratılış sırası kullanılır. A'nın bölgesiz alt kümesi de korunur.
- **C — B + karşı teyit:** B sonrasındaki 1–5 kullanılabilir bar içinde ilk `close > B.high` kapanışında C yayınlanır. B zamanına geri taşınmaz. Aynı hisse/periyotta birden fazla B aynı barda teyitlenirse ilk B temsilcidir. Teyit gerçekleşmeyen ve sonu gözlenemeyen B'ler ayrı sayılır. C, C anındaki ATR ile değerlendirilir.

B ve C'nin ek bilgi sağladığı **varsayılmaz**; A ve B aynı bar/aynı aday havuzunda karşılaştırılır. C'nin giriş ve takip zamanı değiştiğinden A/B ile ham sonuç farkı eşleştirilmiş nedensel etki değildir.

## Dip tanımı ve sayımlar

Geçmiş sonuç etiketi olarak, iki tarafında beşer bar bulunan **5+5 yerel dip** kullanılır; eşit uçlarda en sağdaki pivot seçilir. Bu etiket yalnız beş sağ bar tamamlanınca bilinebilir ve hiçbir sinyal özelliğine girmez. Bir sinyal, pivotun 2 bar öncesi ile 3 bar sonrası arasında ve sinyal kapanışı pivot dip fiyatından en fazla sinyal anındaki 1 ATR yukarıdaysa bu dip ile eşleşebilir. En yakın pivot seçilir; eşitlikte erken pivot seçilir. Sinyal başına eşleşme ve kapsanan benzersiz pivotlar ayrı raporlanır. Bu, aralık/ölçek seçimine bağlı bir **yerel dip vekilidir**; gerçek veya büyük dip garantisi değildir.

Veri/bölüm sınırına yakın, etiketi tam bilinmeyen sinyal `unknown`; eksik sonuç zarar veya yanlış alarm sayılmaz. Pivot kapsaması için sinyal penceresi ve pivotun beş sağ barı aynı değerlendirme bölümünde tamamlanmış olmalıdır. Dönem, hisse, aday sayısı, bölge kapsamı, C teyitlenmeyenler ve sansürlüler saklanır.

## Giriş, takip ve kıyas

- Nominal **bir sonraki kullanılabilir barın açılışı** (`next_open`) ve daha geç, bir bar daha beklenen açılış (`delayed_open`) ayrı hesaplanır. Birincisi ana fiyat vekili; ikincisi gecikme duyarlılığıdır. Gerçek seans kapanışı ve emir gerçekleşmesi doğrulanmadığı için ikisi de gerçek işlem garantisi değildir. Kullanılabilir 4s barlar arada atlanan kısmi seans barlarını içermez.
- Girişten sonraki **10 ve 20 kullanılabilir bar** ayrı ufuklardır. Sabit ufuk açılış→son kapanış getirisi, MFE/MAE, aynı giriş/bitiş etiketinde XU100 açılış→kapanış farkı ayrı raporlanır; benchmark eksikse `unknown`, sıfır değildir.
- Ayrı varsayımsal işlem: sinyal barında bilinen ATR14 ile girişten **1 ATR stop / 2 ATR hedef**, en fazla 10 veya 20 bar. Gap seviyenin ötesinde açılırsa açılış kullanılır. Aynı barda hedef ve stop görülürse iki sıra için alt/üst sonuç ayrı; sırası uydurulmaz. Tam ufuk bölüm/veri sınırına sığmıyorsa sonuç `censored`. Gidiş-dönüş %0 / %0,10 / %0,25 / %0,50 varsayımsal maliyet duyarlılığıdır; ölçülmüş piyasa maliyeti değildir.
- Yalnız bir varlıkta az sayıda veya çok örtüşen olaydan evrensel oran çıkarılmaz. Aday ortalaması portföy getirisi değildir. Hisse ve hafta bazında sayılar ayrıca gösterilir.

## Dönemler ve bağımsızlık

Mevcut arşiv: 1 Temmuz 2026'dan önce `train`, 1 Temmuz–31 Ağustos `validation`, 1 Eylül ve sonrası `historical_test`; tümü **önceden incelenmiş keşif verisi**. İleri sonuç/etiket kendi bölüm sınırını geçerse dışlanır. Ortak takvim sınırı kullanılacaktır; bunlar model eğitimi veya bağımsız ileri doğrulama değildir.

Ek tarihsel dayanıklılık: daha önce bu depoda bulunmayan `megecr/bist-pairs-trading` deposunun **f4a353bf9cf1ac3621c294fb397b812c5691e099** commitindeki günlük hisse CSV'leri incelenebilir; yalnız Replay-Man havuzuyla kesişen semboller, sinyal tarihi **2022-01-01–2025-10-31** ve bunlardan önceki ısınma kullanılır. Bu kaynak yfinance ile indirilmiştir; `auto_adjust` politikası indirme kodunda sabitlenmemiştir. Dönem ve dosyalar bağımsız bir piyasa sağlayıcısı değildir; geçmişe yönelik ek kontrol, ileri test değildir. Bu arşivde güvenilir XU100 bulunmazsa `unknown` bırakılır; başka bir kaynağın eşleştiği varsayılmaz. Kaynak dosyalar Git'e eklenmez; sabit commit, lisans, kapsam, hash ve komut raporlanır. Kaynak kalite ön incelemesinde IEEE yuvarlaması kaynaklı çok küçük OHLC uç hataları görüldüğünden, yalnız fiyatın `1e-9` katından küçük geometri farkları uygun sınıra düzeltilip sayılır; daha büyük hata veya yinelenen tarih içeren seri reddedilir. Bu tolerans ön incelemeden sonra tanımlanmış keşif amaçlı bir veri temizleme kuralıdır.

Gerçek ileri gözlem için plan ve kod dondurulduktan sonra **20 Kasım 2026 veya sonraki** yeni, daha önce incelenmemiş kapanmış veriler gerekir. Ayrı replay çıktısında veri/kod/plan hash'leri, kayıt tarihi, ısınma aralığı ve kesilmiş ufuklar tutulacaktır. Henüz veri yoksa sonuç `blocked_data`, başarı oranı sıfır veya başarılı değildir. Daha önce incelenmiş döneme yeniden `test` adı verilmez.

## Karar kuralı

Yalnızca mevcut tarihsel dönemler veya dış geçmiş dönem olumlu çıkarsa `exploratory`; işlem kuralı onaylanmaz. İleri bir çalışmada adayın tartışmaya değer sayılması için asgari olarak ≥100 sonucu bilinen aday, ≥20 hisse, ≥20 farklı hafta, gerçekçi giriş/maliyet duyarlılığı, dip kapsaması/yanlış alarm ve aynı anda seçilen bölgesiz A kontrolüne karşı güven aralığı raporlanmalıdır. Bu sayılar yeterlilik garantisi değildir; seçilmiş tek başarılı hücreye göre karar verilmez. Net getiri veya anlamlı ek katkı gösterilemezse olumsuz sonuç da kaydedilir.

## P6 karşı genişleme düzeltmesi

Eski `cilt2-lifecycle` sonucu failure barından başlayarak sonradan öğrenilen `counter_expansion` etiketine göre ayrılmıştı. Yeni motor failure olayını değiştirmez; karşı genişleme gerçekleşirse ayrı bir olayı **genişlemenin bilindiği barda** üretir. Aynı hisse/dönem/tam örnek için eski failure başlangıçlı görünüm yalnız geçmiş seçim yanlılığını göstermek amacıyla ve yeni teyit başlangıçlı görünüm ayrı raporlanır. Endeks her ufukta hisse başlangıç **ve** bitiş zamanında eşlenir. Eski arşiv korunur ve uyarıyla işaretlenir.
