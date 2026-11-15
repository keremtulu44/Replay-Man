# execution_microstructure

**Kapsam:** 121 sayfa eşleşmesi

## Proje yorumu (`inference`)

OHLC barı emir sırasını ve gerçek dolumu tam göstermez; maliyet ve fill varsayımları ayrı simülasyon katmanıdır.

## Nasıl kullanılabilir?

Replay sonrası gerçekçi emir ve maliyet simülasyonu

## Kaynak şeritleri

### 1. ATK-TR-D1.0-2026-08 — PDF s. 32

> ANA TRADING KİTABI | BÖLÜM 1 Piyasalar, Trading Mekaniği ve Grafik Temelleri • 17 1.9 Bid, Ask ve Fiyatın Oluşumu Grafikte tek bir fiyat çizgisi görülse de işlem anında piyasada en az iki temel fiyat vardır: alıcıların ödemeye razı olduğu en yüksek fiyat ve satıcıların kabul etmeye razı olduğu en düşük fiyat. Bid ve ask kavramları, emirlerin nasıl eşleştiğini ve neden ekrandaki son fiyatla işlem fiyatının farklılaşabildiğini anlamanın temelidir. Bid ve ask  Bid: Bekleyen alış emirleri içindeki en yüksek fiyatı ifade eder.  Ask: Bekleyen satış emirleri içindeki en düşük fiyatı ifade eder.  Spread: En iyi ask ile en iyi bid arasındaki farktır.  Last price: En son gerçekleşen işlemin fiyatıdır; bid veya ask ile aynı olmak zorunda değildir. Bir alıcı market emri gönderdiğinde ask tarafındaki bekleyen satış emirleriyle eşleşir. Bir satıcı market emri gönderdiğinde ise bid tarafındaki bekleyen alış emirleriyle eşleşir. Bu nedenle market alışın maliyeti çoğu zaman ask, market satışın gerçekleşme noktası ise bid tarafına yakındır. Taraf Fiyat Bekleyen miktar ASK / Satış 101,20 40 birim ASK / Satış 101,10 25 birim EN İYİ ASK 101,00 15 birim SPREAD 0,20 - EN İYİ BID 100,80 30 birim BID / Alış 100,70 50 birim BID / Alış 100,60 80 birim Şekil 1.6 – Sadeleştirilmiş emir defteri ve spread Emir defteri ve bekleyen likidite Merkezi emir defteri kullanan piyasalarda limit emirleri fiyat seviyelerinde bekler ve görünen likiditeyi oluşturur. Market emirleri bu bekleyen likiditeyle eşleşir. …

**Bölüm/alt başlık:** 1 / 1.9 — Bid, Ask ve Fiyatın Oluşumu

**Kaynak özeti (`source`):** 1.9 Bid, Ask ve Fiyatın Oluşumu Grafikte tek bir fiyat çizgisi görülse de işlem anında piyasada en az iki temel fiyat vardır: alıcıların ödemeye razı olduğu en yüksek fiyat ve satıcıların kabul etmeye razı olduğu en düşük fiyat. Bid ve ask kavramları, emirlerin nasıl eşleştiğini ve neden ekrandaki son fiyatla işlem fiyatının farklılaşabildiğini anlamanın temelidir. Bid ve ask  Bid: Bekleyen alış emirleri içindeki en yüksek fiyatı ifade eder.

### 2. ATK-TR-D1.0-2026-08 — PDF s. 33

> ANA TRADING KİTABI | BÖLÜM 1 Piyasalar, Trading Mekaniği ve Grafik Temelleri • 18 gerçekleşebilir. Ortalama gerçekleşme fiyatı ilk görülen ask fiyatından daha yüksek olur. Bu fark slippage veya fiyat kayması olarak adlandırılır. Fiyat kayması yalnızca büyük traderların sorunu değildir. Düşük likidite, haber anı, hızlı hareket, geniş spread veya gecikmeli veri küçük emirlerde de beklenen fiyattan sapma oluşturabilir. Bu nedenle grafik fiyatı, emir ekranındaki bid-ask ve işlem geçmişi birlikte değerlendirilmelidir. Spread işlem maliyetinin bir parçasıdır Bir ürün 100,80 bid ve 101,00 ask ile işlem görüyorsa, market alış yapan kişi yaklaşık ask tarafına, hemen market satış yapan kişi ise bid tarafına yakın işlem görür. Fiyat hiç değişmese bile alış ve anında satış arasında spread kadar fark oluşabilir. Komisyon ayrı bir maliyettir; spread ve komisyon birlikte değerlendirilmelidir. Emir defteri kesin gelecek değildir Order book yalnızca o anda görünen bekleyen emirleri gösterir. Emirler iptal edilebilir, değiştirilebilir veya yeni emirlerle yer değiştirebilir. Spoofing gibi yanıltıcı büyük emir örnekleri de bulunabilir. Bu nedenle emir defteri tek başına “kesin destek” veya “kesin direnç” olarak kullanılmamalı; gerçekleşen işlemler ve fiyat tepkisiyle birlikte okunmalıdır. Grafikteki fiyat ile işlem fiyatını ayırın Grafik çoğu zaman son işlem fiyatını gösterir. Emriniz ise bid veya ask tarafındaki gerçek likiditeyle eşleşir. Özellikle hızlı piyasalarda “grafik seviyeme geldi ama farklı fiyattan işlem oldu” durumu bu ayrımdan kaynaklanabilir. …

**Bölüm/alt başlık:** 1 / 1.10 — Teknik Analiz ve Temel Analiz

**Kaynak özeti (`source`):** Ortalama gerçekleşme fiyatı ilk görülen ask fiyatından daha yüksek olur. Bu fark slippage veya fiyat kayması olarak adlandırılır. Fiyat kayması yalnızca büyük traderların sorunu değildir.

### 3. ATK-TR-D1.0-2026-08 — PDF s. 500

> ANA TRADING KİTABI | BÖLÜM 24 Arbitraj, Piyasa Verimliliği ve Operasyon Riski • 485 Tablo 24.9 – Veri doğruluğu ve stale quote kontrolü EKRANDA NE ARIYORUM?  İki fiyatın exchange timestamp’i ve local receive time’ı.  Last değil bid/ask ve miktar bazlı depth.  Feed bağlantısı, son update süresi ve outlier uyarısı.  Symbol mapping’in spot/futures ve quote doğruluğu.  Fiyat farkı oluştuğunda venue’nin trading/withdrawal health durumu. DOĞRU BİLİNEN YANLIŞ Mit: Aynı grafikte iki fiyat çizgisi gördüğüm için veriler eşzamanlıdır. Gerçeklik: Aggregator, indicator veya chart farklı cache ve update hızları kullanabilir. Görsel eşzamanlılık execution eşzamanlılığı değildir. 24.10 Order Book Depth ve Uygulanabilir Fiyat Executable price (belirli miktarın order book kademeleri tüketildikten sonra oluşan ortalama gerçekleşme fiyatı), top-of-book fiyatından farklı olabilir. Arbitraj hesaplaması her iki bacakta aynı eşleşen miktarın volume-weighted fill fiyatıyla yapılır. Miktar etkisi Ucuz venue Pahalı venue Sonuç Küçük Q İlk ask’ta dolabilir. İlk bid’de dolabilir. Görünen farkın çoğu korunur. Orta Q Birden çok ask kademesi tüketilir. Birden çok bid kademesi tüketilir. Gross spread daralır. Büyük Q Price impact ve partial fill artar. Satış fiyatı aşağı kayar. Net edge negatife dönebilir. Dengesiz depth Buy leg tam, sell leg kısmi. Açık inventory oluşur. Leg risk ve emergency unwind. Tablo 24.10 – Miktar ve uygulanabilir fiyat Volume-weighted executable buy ve sell hesaplandıktan sonra iki bacağın minimum filled quantity’si eşleşen Q kabul edilir. …

**Bölüm/alt başlık:** 24 / 24.11 — Tam Maliyet Yığını ve Güvenlik Tamponu

**Kaynak özeti (`source`):**  İki fiyatın exchange timestamp’i ve local receive time’ı.  Last değil bid/ask ve miktar bazlı depth.  Feed bağlantısı, son update süresi ve outlier uyarısı.

### 4. ATK-TR-D1.0-2026-08 — PDF s. 98

> ANA TRADING KİTABI | BÖLÜM 5 Likidite, FVG ve Fiyat Boşlukları • 83 Tablo 5.1 – Likidite kelimesinin üç farklı kullanım alanı Aynı kelime, farklı soru “Bu piyasa likit mi?” sorusu işlem maliyeti ve order book derinliğiyle ilgilidir. “Bu tepenin üzerinde likidite var mı?” sorusu ise görünür yapının çevresinde tetiklenebilir emir kümelenmesi ihtimaliyle ilgilidir. Likidite görünmez; etkisi gözlenir Stop emirleri tetiklenmeden önce çoğu standart grafikte görünmez. Iceberg veya dark-pool işlemleri de bütünüyle gözlenemeyebilir. Bu nedenle traderın görevi “burada kesin şu kadar emir var” demek değil; belirgin seviyelerin neden emir çekebileceğini anlamak ve fiyat o seviyeye geldiğinde kapanış ile takip davranışını ölçmektir. 5.2 Emirler Likiditeyi Nasıl Oluşturur? Bölüm 1’de emir türlerinin temel görevleri anlatıldı. Likidite açısından üçlü ayrım yeniden kısa biçimde kullanılmalıdır: limit emirler bekleyen pasif likidite sağlar, market emirler mevcut limitleri tüketerek fiyatı hareket ettirir, stop emirleri ise belirli fiyat görüldüğünde market veya limit emrine dönüşerek yeni akış oluşturur. Emir türü Likidite görevi Fiyata etkisi Limit emir Order book’a alış veya satış teklifi koyar; gerçekleşene kadar pasif bekler. Karşı market emir geldiğinde doldurulur; derinlik sağlar. Market emir Mevcut en iyi limit emirleri tüketir; likidite alır. Yeterli derinlik yoksa birden fazla fiyat seviyesini geçerek slippage yaratır. Stop emir Tetik fiyatına kadar latent/gizli bekler; tetiklenince aktif emre dönüşür. …

**Bölüm/alt başlık:** 5 / 5.3 — Buy-Side ve Sell-Side Liquidity

**Kaynak özeti (`source`):** “Bu tepenin üzerinde likidite var mı?” sorusu ise görünür yapının çevresinde tetiklenebilir emir kümelenmesi ihtimaliyle ilgilidir. Likidite görünmez; etkisi gözlenir Stop emirleri tetiklenmeden önce çoğu standart grafikte görünmez. Iceberg veya dark-pool işlemleri de bütünüyle gözlenemeyebilir.

### 5. PTA-C1-2026 — PDF s. 133

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 133 Alan Yazılması gereken kural Bağlam Trend veya yatay piyasa nasıl tanımlanıyor? Yön Alış veya satış yönü hangi açık koşulla belirleniyor? Konum İşlem yalnız nerede aranacak? Giriş işareti Tam olarak hangi kapanış veya olay giriş izni veriyor? Fikrin bozulduğu seviye Hangi fiyat davranışı fikri yanlışlıyor? Risk Stop, pozisyon büyüklüğü ve maksimum hesap riski nasıl hesaplanıyor? Yönetim Takip eden stop, kâr alma veya çıkış kuralı ne? İşlem yok Hangi koşullarda sistem bilinçli olarak işlem üretmiyor? Test Hangi veri aralığı ve ölçülerle test edilecek? SON KONTROL Bir işlem düzenini açıklamak için beş indikatörün adını söylemeniz gerekiyorsa sistemi yeniden sadeleştirin. İyi bir işlem planı birkaç net cümleyle bağlamı, yönü ve piyasa ortamını, konumu, giriş işaretini, fikrin nerede bozulacağını, riski ve yönetimi anlatabilmelidir. 21.9 — Sistemi kurduktan sonra: beklenen değer ve sermaye dalgalanması Sistemin kurallarını yazmak ilk adımdır. İkinci soru, geçmişte iyi görünen sonucun gerçekten dayanıklı bir avantaj mı, yoksa tesadüf ve geçmişe aşırı uyum mu olduğudur. Bu bölümde amaç ileri istatistik yapmak değil; sistemin sonuçlarını birkaç temel ölçüyle daha gerçekçi sınamaktır. Bir sistemin kalitesi yalnız kazanma oranıyla ölçülemez. …

**Bölüm/alt başlık:** 21 / 21.9 — Sistemi kurduktan sonra: beklenen değer ve sermaye

**Kaynak özeti (`source`):** Alan Yazılması gereken kural Bağlam Trend veya yatay piyasa nasıl tanımlanıyor? Yön Alış veya satış yönü hangi açık koşulla belirleniyor? Konum İşlem yalnız nerede aranacak?

### 6. PTA-C1-2026 — PDF s. 95

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 95 BÖLÜM 16 Trend Çizgileri, Yatay Seviyeler ve Kanallar Çizgi çizmek kolaydır. Zor olan, hangi iki noktanın neden seçildiğini ve çizginin neyi kanıtlamadığını bilmektir. HIZLI ROL — Ana görev: fiyat hareketini çizgiler ve bölgelerle daha kolay okumak. Tek başına trend dönüşünü veya giriş zamanını söylemez. Ana risk: çizgileri sonradan fiyata uydurmak, tek bir fiyatı kesin duvar sanmak ve ekrandaki açıyı trend gücü gibi yorumlamak. İyi eşleşme: fiyat yapısı + ATR. Araç Ana soru En büyük yanlış kullanım Yatay seviye / bölge Fiyat geçmişte nerede reaksiyon verdi? Tek bir hassas fiyatı kesin duvar kabul etmek Trend çizgisi Yönlü belirgin dönüş noktaları hangi eğim boyunca gelişiyor? İki uygun noktayı sonradan seçerek geçmişe uydurmak Paralel Kanal Aynı eğim içindeki karşı sınır nerede? İki kenarı ayrı ayrı “güzel oturacak” şekilde eğmek Uzatılmış çizgi / ışın Referansı geleceğe taşımak Uzatılan çizgiyi gelecekte zorunlu reaksiyon seviyesi sanmak 16.1 — Destek ve direnç: çizgiden önce bölge düşünün Birbirine yakın destek/direnç tepkilerini tek bir fiyata zorlamak yerine dar bir bölge olarak okuyun. Mum gövdeleri, fitiller, alış-satış farkı (spread) ve veri farklılıkları reaksiyonları küçük bir fiyat aralığına yayabilir.

**Bölüm/alt başlık:** 16 / 16.1 — Destek ve direnç: çizgiden önce bölge düşünün

**Kaynak özeti (`source`):** BÖLÜM 16 Trend Çizgileri, Yatay Seviyeler ve Kanallar Çizgi çizmek kolaydır. Zor olan, hangi iki noktanın neden seçildiğini ve çizginin neyi kanıtlamadığını bilmektir. HIZLI ROL — Ana görev: fiyat hareketini çizgiler ve bölgelerle daha kolay okumak.

## Test fikri (`hypothesis`)

Bu konuya ait kaynak varyantları korunur. İlk aşamada sabit eşik seçilmez; geniş sembol evreninde aynı tanımların amaçladığı davranışa katkısı karşılaştırılır.
