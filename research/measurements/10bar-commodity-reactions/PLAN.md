# 10 mumda emtia hareketi ve BIST tepkisi — ölçüm planı

Bu yeni plan kullanıcı örneği (Brent +%4, TUPRS -%3) üzerine sonuçlar hesaplanmadan yazılmıştır. Arşiv/önceki analizler önceden incelendiğinden bağımsız kör ön kayıt değildir. Arşivde 2025-11–2026-11 veri vardır. Önceki turda üretilmiş bazı dosyalar çalışma alanında görünmemektedir; bu araştırma bağımsızdır.

## Çerçeve ve yön

Tüm 100 BIST hissesi ve 10 BIST endeksi hedef; Brent, WTI, altın, gümüş, bakır, platin, paladyum ayrı kaynak. Birim USD ve ayrıca yalnızca eşzamanlı taze USD/TRY ile hesaplanan yaklaşık TRY. BIST için `1h` ve `4h` ayrı çalışılır, her pencerede **10 kullanılabilir BIST barı**: olay barı dahil son 10 tamamlanmış barın ilki açılışından sonuncusu kapanışına. 4h barlar parça sayısına göre tamamlanmış filtreli; 1h/4h barlar gerçek seans takvimi garantisi değildir, 10×4 saat takvim süresi demek değildir ve seans dışı hareketleri de içerebilir.

XU100 referansının 10 barlık dizisindeki **her barın damgası** hedefte aynı sırada ve araya ilave/eksik bar girmeden mevcut olmalı; tüm OHLC gözlemleri pozitif/geçerli. Böylece Brent ve hissenin baktığı zaman aralığı aynı BIST başlangıç ve bitiş barlarıdır. Emtia/kur saatlik serileri, BIST pencere başlangıcında ve nominal son kapanışında yalnız bitmiş son 1h kapanışla ölçülür (bar başlangıcı +1h). Her uç en fazla 90 dakika eski, TRY için emtia/kur uçları birbirinden en fazla 60 dakika ayrı olabilir. Daha eski veya eksik uç `unknown`, ileri veri kullanılmaz. Emtia aralıkları 1h as-of nedeniyle 30 dakika kadar kayabilir; vadeli kontrat USD fiyatı/TRY çarpımı gerçek alım/satım ürün fiyatı değildir.

## Eşzamanlı ve sonrasındaki 10 mum

- `same`: ilk BIST barı açılışı → onuncu bar kapanışı. Örnek: Brent aynı aralıkta ≥+%4, TUPRS ≤−%3. **Sonradan gözlenebilir ilişki**; emtia hareketinin sonucunu başlangıçta bilip işlem yapmak değildir.
- `after`: kaynak 10 barlık hareketi bitip bilindikten sonra, sinyal barı kapanışından takip eden 10 BIST barının son kapanışına hedef değişimi. Önceki pencere seçimi kullanılır. Bu kapanıştan işlem yapılabileceği varsayılmadığından yalnız betimleyici ileri etikettir; spread, gecikme, maliyet ve yeni haberler yoktur. İlk gecelik fiyat boşluğu dahildir. Takip eden 10 hedef barı da XU100 referans barlarıyla tam eşleşmelidir.

XU100 farkı, hedef ve XU100'ün aynı pencere başlangıç/bitiş fiyat oranı farkıdır; portföy hedge getirisi değildir. Sinyal başlangıcı ile sonucun son nominal kapanışı aynı takvim bölümünde kalır (2026-07-01 ve 2026-09-01 UTC), diğer sonuçlar NaN. Kaynak etiketinin başlangıç ve bitişi mutlaka aynı dönem; ufuk sonu diğer döneme geçemez. Her split veri sınırlarından sonraki barlar biliniyor olmalı. Bu bölümler önceden görülmüştür.

## Eşikler, tekrarlar ve karşılaştırma

Önceden sabit: kaynak ≥+%4 (`up4`), ≤−%4 (`down4`), ≥+%2 (`up2`), ≤−%2 (`down2`), |değişim|<%1 (`flat1`), `all` bilinen kaynak. Hedef ≤−%3 ve ≥+%3 olayları, ham ve XU100 farkının medyanı, pozitiflik oranı ve geçerli n; ayrıca sürekli büyüklük bantları tüm gruplar için yayımlanır. Kaynak ≥+%4 ile hedef ≤−%3 doğrudan kullanıcı örneği olduğu için **a priori tanımlıdır**.

Üç örnekleme ayrı raporlanır:
- `all_bars`: her bitiş barı; bitişikler aynı 10-barı büyük ölçüde tekrarlar, bağımsız örnek değildir.
- `fixed_nonoverlap`: tüm kaynak ve hedef verilerinden bağımsız, kronolojik XU100 10-bar pencereleri çakışmayacak şekilde split başına ilk uygun bitişler. Sonradan verim veya hedef sonucuna göre seçilmez. Bazı şok günleri sabit ızgarada yakalanmayabilir.
- `shock_episode`: her kaynak×birim×eşik×split için eşik ilk geçilen bilinen pencereleri seç; sonraki pencere başlangıcı, son tutulan sinyal bitiş barından kesinlikle sonra olmalı. Hedef performansı kullanılmaz. Yükseliş/düşüş ve %2/%4 ayrı olay havuzlarıdır; diğer eşiğin seçimi diğerini engellemez. Bu seçim, `all` sabit ızgara ile birebir eşleştirilmiş bir kontrol değildir.

Tüm sonuçlar her bölümde tüm geçerli kaynak günlerinin `all` taban oranıyla karşılaştırılır; örnekleme rejiminin kendisine uygun ayrı taban kullanılır, `shock_episode` sonuçları için `all_bars` tabanı sadece bağlam olarak ve bu kısıtla verilir. En az 10 geçerli sonuç **betimleyici kapsam etiketi**, istatistiksel güven veya nedensellik değildir. ≤−%3 sayısı/valid n ve aynı koşullu baz oranı gösterilir; olaylar zaman, hisse ve emtia arasında bağımlı, çoklu test yüksektir. Örtüşmeme seri bağımsızlığı garanti etmez.

## Çıktılar

Kaynak, pencere ve hedef tabloları tekrar üretilebilir; 10-barda Brent ≥4% + TUPRS ≤−3% somut tarih örnekleri, tüm hisse/endeks koşullu özetleri ve sayılar, girdi SHA-256 manifesti ayrı kaydedilir. Pozisyon/short, ücret, FX/emtia hedge uygulanabilirliği ve fiyat ayarlama sorunları kapsanmaz; sonuçların tamamı veri örneğine özgü keşifseldir.

## Sonradan eklenen sıçrama duyarlılığı

İlk örneklerde kaynak saatlik kapanışları arasında %10'u aşan gözlemler görüldükten sonra, sonucu değiştirebilecek veri/kontrat/gece sıçraması duyarlılığı olarak eklenmiştir; önceden belirlenmiş ana filtre değildir. Her kaynak penceresinde ardışık **mevcut** saatlik kapanışlar arasındaki azami mutlak değişim hesaplanır. `no_jump10` yalnız bu azami değer ≤%10 olan bilinen pencerelerle ayrı raporlanır; büyük sıçrama mutlaka hata/roll demek değildir ve arşivde hiç sıçrama görülmemesi doğruluk garantisi değildir. Şok pencereleri bu kapıdan sonra kaynak sinyaliyle yeniden seçilir, hedef sonuçlarına bakılmaz. Ana `all` sonuçları korunur.
