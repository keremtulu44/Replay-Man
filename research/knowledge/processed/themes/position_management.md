# position_management

**Kapsam:** 18 sayfa eşleşmesi

## Proje yorumu (`inference`)

Giriş kalitesi ile çıkış/pozisyon yönetimi aynı iddia değildir ve ayrı deneylerde ölçülmelidir.

## Nasıl kullanılabilir?

Giriş sonrası çıkış, kısmi yönetim ve pozisyon yaşam döngüsü

## Kaynak şeritleri

### 1. ATK-TR-D1.0-2026-08 — PDF s. 489

> ANA TRADING KİTABI | BÖLÜM 23 Pozisyon Yönetimi, Kâr Alma ve Çıkış Stratejileri • 474 Terim Aksiyon tanımı Partial exit Pozisyonun belirli kısmını kapatıp kalanı açık tutmak. Scaling out Birden fazla hedefte miktarı kademeli azaltmak. Break-even stop Stopu entry veya maliyet düzeltilmiş entry seviyesine taşımak. Trade-based break-even Partial kârın kalan stop riskini ve maliyeti karşılaması. Trailing stop Lehe fiyat hareketinde yalnız tek yönde sıkılaşan stop. MFE Maximum Favorable Excursion; trade’in en yüksek lehe ilerlemesi. MAE Maximum Adverse Excursion; trade’in en yüksek aleyhe ilerlemesi. Time stop Beklenen süre içinde ilerleme yoksa pozisyonu azaltma/kapatma. Exit reason Tam/partial çıkışın önceden tanımlı neden sınıfı. Given-back profit MFE ile gerçekleşen çıkış sonucu arasındaki geri verilen kâr. Exit efficiency Çıkış sonucunu stratejinin ulaşılabilir hareketiyle karşılaştıran inceleme ölçüsü. ATR trail Stop mesafesini ATR katıyla volatiliteye uyarlamak. Structure trail Stopu confirmed swing veya protected level arkasına taşımak. Roll Vadesi veya maliyeti yaklaşan hedge/derivative pozisyonunu yeni sözleşmeye taşımak. Tablo 23.17 – Bölüm 23 temel sözlüğü Bölüm Sonu Kontrol Soruları 1. Pozisyon yönetimi neden girişten önce planlanmalıdır? 2. Sabit R hedefi ile teknik hedef hangi farklı soruları cevaplar? 3. Teknik hedefin güçlü bir engelin arkasında kalması ne düşündürür? 4. Hedef hiyerarşisinin temel katmanları nelerdir? 5. Partial exit ile scaling out nasıl ayrılır? 6. Partial sonrası toplam worst-case nasıl hesaplanır? 7. …

**Bölüm/alt başlık:** 23 / 23.15 — Tam Pozisyon Yönetimi İş Akışı

**Kaynak özeti (`source`):** Terim Aksiyon tanımı Partial exit Pozisyonun belirli kısmını kapatıp kalanı açık tutmak. Scaling out Birden fazla hedefte miktarı kademeli azaltmak. Break-even stop Stopu entry veya maliyet düzeltilmiş entry seviyesine taşımak.

### 2. ATK-TR-D1.0-2026-08 — PDF s. 480

> ANA TRADING KİTABI | BÖLÜM 23 Pozisyon Yönetimi, Kâr Alma ve Çıkış Stratejileri • 465 23.6 Normal Stop ile Trailing Stop Görev Ayrımı Regular stop başlangıç tezinin yanlış olduğu seviyeyi korur. Trailing stop (fiyat lehe ilerledikçe belirli kural ile yalnız tek yönde sıkılaşan stop), risk kontrolünden kâr koruma ve trend taşıma görevine geçer. Aktivasyon kuralı olmadan başlangıçtan itibaren kullanılan çok sıkı trail, normal stopun yerine geçemez. Özellik Normal stop Trailing stop Ana görev İlk invalidation ve maksimum risk. Lehe hareket sonrası kâr/risk yönetimi. Seviye Sabit veya yalnız planlı olayla değişir. Yeni high/low, ATR veya yapı ile sıkılaşır. Yön Korkuyla genişletilmez. Longda yalnız yukarı; shortta yalnız aşağı. Uygun ortam Her trade için başlangıç riski. Özellikle trend ve geniş follow-through. Ana hata Stopu uzaklaştırmak veya kaldırmak. Çok sıkı trail ile normal pullback’te çıkmak. Emir riski Trigger sonrası fill seviyesi garanti olmayabilir. Aynı risk + broker/venue takip mantığı. Tablo 23.6 – Normal ve trailing stop EKRANDA NE ARIYORUM?  Trail ne zaman aktive olacak?  Referans son fiyat mı, highest high/lowest low mı, kapanış mı?  Güncelleme tick, bar close veya manuel kontrolle mi?  Stop hesaplandığında geriye doğru gevşiyor mu?  Broker stop-market mi, stop-limit mi; overnight gap ve extended hours politikası ne? DOĞRU BİLİNEN YANLIŞ Mit: Trailing stop tepeye yakın çıkışı garanti eder. Gerçeklik: Trail mesafesi kadar kâr geri verilebilir; gap veya hızlı hareket fill’i daha kötü yapabilir. Çok sıkı mesafe ise trend sürerken erken çıkış üretir.

**Bölüm/alt başlık:** 23 / 23.6 — Normal Stop ile Trailing Stop Görev Ayrımı

**Kaynak özeti (`source`):** 23.6 Normal Stop ile Trailing Stop Görev Ayrımı Regular stop başlangıç tezinin yanlış olduğu seviyeyi korur. Trailing stop (fiyat lehe ilerledikçe belirli kural ile yalnız tek yönde sıkılaşan stop), risk kontrolünden kâr koruma ve trend taşıma görevine geçer. Aktivasyon kuralı olmadan başlangıçtan itibaren kullanılan çok sıkı trail, normal stopun yerine geçemez.

### 3. ATK-TR-D1.0-2026-08 — PDF s. 479

> ANA TRADING KİTABI | BÖLÜM 23 Pozisyon Yönetimi, Kâr Alma ve Çıkış Stratejileri • 464 DOĞRU BİLİNEN YANLIŞ Mit: Pozisyonun bir kısmını kârla kapattığım anda artık kaybedemem. Gerçeklik: Partial fiyatı, kapatılan miktar, kalan stop mesafesi ve maliyetler toplam işlem sonucunu belirler. 23.5 Break-Even: Risk Azaltma mı, Erken Çıkış mı? Break-even stop — BE (stop seviyesini entry fiyatına veya maliyet düzeltilmiş entry’ye taşıma), yeni bir yönetim kuralıdır. Trade biraz yeşile döndüğünde otomatik ödül olarak kullanılmaz. Fiyatın risk alanından çıktığını gösteren yapı veya hedef kanıtı gerekir. Şekil 23.4 – Break-even karar kapısı BE aktivasyon adayı Neden daha anlamlı? Erken BE riski T1/önemli engel görüldü Piyasa başlangıç riskinin bir bölümünü ödedi. T1 çok yakınsa normal gürültü sürer. Yeni confirmed HL/LH oluştu Stop yeni yapısal savunmaya taşınabilir. Swing onaylanmadan hareket etmek. Breakout acceptance + retest Entry artık yeni desteğin/direncin gerisinde kalır. False breakout sonrası entry testi normal olabilir. Partial toplam riski karşıladı Worst-case matematiksel olarak azaldı. Maliyet ve gap riskini yok saymak. Haber/session riski yaklaşıyor Exposure azaltma gerekçesi oluşabilir. Kötü time planning’i BE ile yamamak. Tablo 23.5 – Break-even kapıları İKİ BAŞABAŞ AYRIMI 1) Stop-based BE: kalan pozisyonun stopu entry/maliyet seviyesine taşınır. 2) Portfolio/trade-based BE: gerçekleşen partial kârı kalan pozisyonun stop zararını karşılar. İkisi aynı anda olmak zorunda değildir. DOĞRU BİLİNEN YANLIŞ Mit: BE stop zararı tamamen ortadan kaldırır ve ücretsiz trade yaratır. …

**Bölüm/alt başlık:** 23 / 23.5 — Break-Even: Risk Azaltma mı, Erken Çıkış

**Kaynak özeti (`source`):** DOĞRU BİLİNEN YANLIŞ Mit: Pozisyonun bir kısmını kârla kapattığım anda artık kaybedemem. Gerçeklik: Partial fiyatı, kapatılan miktar, kalan stop mesafesi ve maliyetler toplam işlem sonucunu belirler. 23.5 Break-Even: Risk Azaltma mı, Erken Çıkış mı?

### 4. PTA-C1-2026 — PDF s. 40

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 40 Yaklaşım Avantaj Risk Sadece 1×ATR Otomatik ve kolay İşlem fikrinin bozulduğu seviyeyle ilişkili olmayabilir Yapı + ATR ek payı Yapı ve fiyat hareketliliğini birleştirir Katsayı yine test/strateji gerektirir “1 ATR” VE “2 ATR” SİHİRLİ SAYI DEĞİLDİR Katsayı büyüdükçe stop genişler, pozisyon büyüklüğü aynı tutulursa parasal risk de artar. Profesyonel kullanımda stop mesafesi ile pozisyon büyüklüğü birlikte ele alınmalıdır. 6.6 — Başlangıç stopu ile takip eden stop aynı görev değildir Başlangıç stopunun yeri 6.5’teki gibi önce işlem fikrinin bozulduğu seviyeye göre belirlenir. Burada ek soru, bu sınırın normal fiyat hareketi içinde gereğinden fazla yakın kalıp kalmadığıdır. Stop normal fiyat hareketinin çok içinde kalıyorsa fiyat yapısı bozulmadan da çalışabilir. ATR, yapısal stopun güncel hareket genişliğiyle uyumunu kontrol etmeye yardım eder; stopun yerini tek başına belirlemez. ATR tabanlı takip eden stop ve Chandelier Exit Başlangıç stopu ile takip eden stop aynı görev değildir. Başlangıç stopu işlem fikrinin ilk risk sınırını tanımlar; takip eden stop ise fiyat trend yönünde ilerledikçe açık pozisyonun yönetim sınırını taşır. ATR tabanlı takip eden stopta mesafe güncel ATR’ye bağlıdır. Fiyat hareketliliği yükselirse ATR ve stop mesafesi genişleyebilir; hareketlilik düşerse mesafe daralabilir. Katsayı büyüdükçe stop fiyata daha fazla hareket alanı bırakır. Hesap riski sabit tutulacaksa daha geniş stop daha küçük pozisyon büyüklüğü gerektirir. Chandelier Exit bu yaklaşımın otomatik çizgi biçimindeki uygulamalarından biridir. …

**Bölüm/alt başlık:** 6 / 6.7 — Düşük ATR ve kırılım beklentisi

**Kaynak özeti (`source`):** Yaklaşım Avantaj Risk Sadece 1×ATR Otomatik ve kolay İşlem fikrinin bozulduğu seviyeyle ilişkili olmayabilir Yapı + ATR ek payı Yapı ve fiyat hareketliliğini birleştirir Katsayı yine test/strateji gerektirir “1 ATR” VE “2 ATR” SİHİRLİ SAYI DEĞİLDİR Katsayı büyüdükçe stop genişler, pozisyon büyüklüğü aynı tutulursa parasal risk de artar. Profesyonel kullanımda stop mesafesi ile pozisyon büyüklüğü birlikte ele alınmalıdır. 6.6 — Başlangıç stopu ile takip eden stop aynı görev değildir Başlangıç stopunun yeri 6.5’teki gibi önce işlem fikrinin bozulduğu seviyeye göre belirlenir.

### 5. ATK-TR-D1.0-2026-08 — PDF s. 308

> ANA TRADING KİTABI | BÖLÜM 15 TradingView, Grafik Araçları ve Test İş Akışı • 293 Kontrol Ne zaman kullanırım? Dikkat Auto scale Mevcut görünümü ekrandaki veri ve çizimlere sığdırma. Uzak çizimler fiyatı sıkıştırabilir. Timeframe Bağlam, setup veya tetik görevi. Zaman dilimi değişince yapı sınıfı da değişebilir. Tablo 15.3 – Chart type, timeframe ve ölçek görevleri EKRANDA NE ARIYORUM? • Üst sol köşede doğru sembol ve timeframe yazıyor mu? • Fiyat ekseni lineer mi log mu; neden? • Auto scale uzak bir çizim yüzünden grafiği sıkıştırıyor mu? • Heikin Ashi kullanıyorsam gerçek fiyatı ikinci grafikte doğruluyor muyum? • Zoom seviyesi yalnız son birkaç mumu gösterip ana yapıyı saklıyor mu? DOĞRU BİLİNEN YANLIŞ Mit: Logaritmik ölçek daha doğru sinyal üretir. Gerçeklik: Log ölçek yüzdesel hareketleri daha dengeli gösterir; sinyal üretmez. Hangi ölçeğin uygun olduğu analiz ufkuna bağlıdır. Uygulama Görseli 15.3 – Aynı XAGTRYG haftalık grafiğinin lineer ve log ölçekle yan yana karşılaştırılması; aynı swing noktalarının farklı görsel mesafeleri. Temsilî eğitim şeması.

**Bölüm/alt başlık:** 15 / 15.3 — Chart Type, Zaman Dilimi, Ölçek ve

**Kaynak özeti (`source`):** Dikkat Auto scale Mevcut görünümü ekrandaki veri ve çizimlere sığdırma. Uzak çizimler fiyatı sıkıştırabilir. Timeframe Bağlam, setup veya tetik görevi.

### 6. PTA-C1-2026 — PDF s. 82

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 82 Piyasa Supertrend davranışı Daha doğru okuma Düzenli trend Pozisyonu uzun süre takip edebilir Takip eden stop / piyasa ortamı filtresi için uygun Yatay piyasa Sık yön değişimi üretebilir Tek başına giriş sistemi yapma Ani fiyat hareketliliği şoku ATR genişler, bant mesafesi değişir Stop/risk mantığını ayrıca kontrol et 13.6 — Supertrend çizgisini stop olarak kullanmak Supertrend takip eden stop referansı olabilir; ancak teknik stop mesafesi ile hesap başına para riski ayrı konulardır. Stop uzaksa pozisyon büyüklüğü buna göre ayarlanmalıdır. MİNİ ÖRNEK Giriş 100 TL, Supertrend 92 TL ise teknik mesafe %8’dir. Hesap risk limiti %1 ise stopu keyfî biçimde daraltmak yerine pozisyon büyüklüğü azaltılır. Stop konumu ile pozisyon büyüklüğü aynı problem değildir.

**Bölüm/alt başlık:** 13 / 13.6 — Supertrend çizgisini stop olarak kullanmak

**Kaynak özeti (`source`):** Piyasa Supertrend davranışı Daha doğru okuma Düzenli trend Pozisyonu uzun süre takip edebilir Takip eden stop / piyasa ortamı filtresi için uygun Yatay piyasa Sık yön değişimi üretebilir Tek başına giriş sistemi yapma Ani fiyat hareketliliği şoku ATR genişler, bant mesafesi değişir Stop/risk mantığını ayrıca kontrol et 13.6 — Supertrend çizgisini stop olarak kullanmak Supertrend takip eden stop referansı olabilir; ancak teknik stop mesafesi ile hesap başına para riski ayrı konulardır. Stop uzaksa pozisyon büyüklüğü buna göre ayarlanmalıdır. MİNİ ÖRNEK Giriş 100 TL, Supertrend 92 TL ise teknik mesafe %8’dir.

### 7. PTA-C1-2026 — PDF s. 12

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 12 2.3 — Hareketli ortalamaya tek bir görev verin Görev Ne için kullanılır? Tek başına giriş verir mi? Trend filtresi İşlemleri ana yönle aynı tarafta aramaya yardım eder. Hayır Geri çekilme bölgesi Fiyat ortalamaya yaklaştığında izlenecek bölgeyi gösterir. Hayır Takip eden stop İşlem açıldıktan sonra çıkış için referans olabilir. Hayır; yönetim için kullanılır Kesişim Hızlı ortalama yavaş ortalamayı geçtiğinde yön değişimini takip eder. Olabilir; ama gecikebilir NEDEN SORUN OLUR? Aynı EMA’yı hem yön, hem giriş, hem destek hem de stop için kullanırsanız bütün kararları tek çizgiye bağlamış olursunuz. EMA yanlış sinyal verdiğinde sistemin tamamı etkilenebilir. Bu yüzden hareketli ortalamaya bir ana görev verin. 2.4 — Dinamik destek: temas değil, bağlam EMA çevresindeki tekrar eden tepkiler, çizginin fiyatı “taşıdığı” anlamına gelmez. EMA trend içindeki geri çekilmelerde yalnızca bir referans bölgesidir; temas tek başına giriş değildir. YANLIŞ / DOĞRU Yanlış: “EMA’ya değdi, al.” Doğru: “Trend var; fiyat referans bölgesine çekildi. Şimdi yapının ve hareket gücünün yeniden trend yönüne dönüp dönmediğine bak.” 2.5 — 50/200 (Golden Cross) kesişimi neden gecikir? Kesişim için hızlı ortalamanın önce fiyat hareketine tepki verip yavaş ortalamayı aşması gerekir. Bu yüzden kesişim çoğu zaman hareket başladıktan sonra gelir; gecikme hesap yapısının doğal sonucudur.

**Bölüm/alt başlık:** 2 / 2.5 — 50/200 (Golden Cross) kesişimi neden gecikir?

**Kaynak özeti (`source`):** 2.3 — Hareketli ortalamaya tek bir görev verin Görev Ne için kullanılır? Trend filtresi İşlemleri ana yönle aynı tarafta aramaya yardım eder. Hayır Geri çekilme bölgesi Fiyat ortalamaya yaklaştığında izlenecek bölgeyi gösterir.

### 8. PTA-C1-2026 — PDF s. 52

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 52 Eksik parça Sadece Donchian varsa sorun Tamamlayıcı Risk Stop/pozisyon büyüklüğü yok Yapı + ATR / risk planı 8.4 — Donchian + ATR neden güçlü bir rol kombinasyonudur? ATR “piyasa ne kadar hareket ediyor?”, Donchian “son N periyot sınırı hangi yönde kırıldı?” sorusuna cevap verir. Böylece fiyat hareketliliği koşulu ile yönlü giriş işareti birbirinden ayrılır. Şekil 8.3 — Sentetik örnek: önce dar fiyat aralığı, ardından Donchian sınırının kırılması ve hareket genişliğinin artması. Daralma yönü önceden söylemez. PERFORMANS İDDİASINA DİKKAT ATR + Donchian rol açısından uyumludur; ancak başarı oranı ayrıca test edilmelidir. Araçların görev ayrımı, performans garantisi değildir. 8.5 — Orta bant takip eden stop için nasıl kullanılabilir? Trend başladıktan sonra orta bant yönetim referansı olarak kullanılabilir. Örneğin satış yönlü pozisyonda orta bant üstü kapanış çıkış kuralı olabilir. Daha gevşek takip trendi daha uzun taşır; karşılığında daha fazla kâr geri verilebilir. TAKİP EDEN STOPTA DENGE Daha gevşek stop, trendi daha uzun süre taşıyabilir; ancak daha fazla kâr geri verilebilir. Daha sıkı stop kârı daha erken korur; fakat trendden erken çıkarabilir. Tek bir “en iyi” ayar yoktur; seçim sistemin amacına göre yapılır.

**Bölüm/alt başlık:** 8 / 8.5 — Orta bant takip eden stop için nasıl kullanılabilir?

**Kaynak özeti (`source`):** Eksik parça Sadece Donchian varsa sorun Tamamlayıcı Risk Stop/pozisyon büyüklüğü yok Yapı + ATR / risk planı 8.4 — Donchian + ATR neden güçlü bir rol kombinasyonudur? ATR “piyasa ne kadar hareket ediyor?”, Donchian “son N periyot sınırı hangi yönde kırıldı?” sorusuna cevap verir. Böylece fiyat hareketliliği koşulu ile yönlü giriş işareti birbirinden ayrılır.

## Test fikri (`hypothesis`)

Bu konuya ait kaynak varyantları korunur. İlk aşamada sabit eşik seçilmez; geniş sembol evreninde aynı tanımların amaçladığı davranışa katkısı karşılaştırılır.
