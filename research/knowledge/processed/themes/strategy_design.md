# strategy_design

**Kapsam:** 153 sayfa eşleşmesi

## Proje yorumu (`inference`)

Strateji; bağlam, konum, setup, tetik, geçersizlik, hedef, no-trade ve kayıt alanlarından oluşan sürümlü sözleşmedir.

## Nasıl kullanılabilir?

Deney ve strateji kartı

## Kaynak şeritleri

### 1. ATK-TR-D1.0-2026-08 — PDF s. 260

> ANA TRADING KİTABI | BÖLÜM 12 İşlem Kurulumu, Strateji Tasarımı ve Doğrulama • 245 Bölüm Özeti Bölüm 12’nin ana sonucu, grafikteki teknik araçların tek tek “sinyal” üretmesi değil; her birinin bağlamdan hedefe uzanan karar zincirinde belirli bir görev üstlenmesidir. Strateji tekrarlanan sistem, setup güncel düzen, trigger kesin aktivasyon olayı ve trade gerçek uygulamadır. Kontrol alanı Kısa soru Bağlam Hangi piyasa hâli ve hangi üst zaman senaryosu? Konum Fiyat neden tam burada izleniyor? Rota Önce hangi likidite/engel ve sonra hangi hedef? Setup Hangi aile: pullback, breakout, range/failure, reversal? Trigger Hangi kesin kapanış veya yapı olayı? Entry Hangi emir ve hangi fiyat? Invalidation Hangi davranış tezi bozar? Target İlk gerçekçi hedef ve ara engel? Validation Bu kurallar hangi test basamaklarından geçti? Tablo 12.17 – Hızlı setup kontrolü Grafik Başı Kontrol Listesi 1. Bugün hangi strateji ve setup ailesini arıyorum? 2. Üst zaman bağlamı trend, range veya geçiş mi? 3. Fiyat anlamlı bir structure/zone/liquidity alanında mı? 4. Hedefe giden rotada yakın major engel var mı? 5. Trigger seviyesi hareketten önce tanımlı mı? 6. Fitil, kapanış, follow-through ve retest ayrımı yapıldı mı? 7. Entry türü stratejinin test edilen sürümüyle aynı mı? 8. Invalidation ve uygulama stopu açık mı? 9. İlk hedef stop mesafesine göre işlem yapılabilir alan bırakıyor mu? 10. No-trade kurallarından biri aktif mi? 11. İşlem setup kodu ve strateji sürümüyle kaydedilecek mi? 12. …

**Bölüm/alt başlık:** 12 / 12.15 — Backtest, Replay, Forward/Paper Test ve

**Kaynak özeti (`source`):** Bölüm Özeti Bölüm 12’nin ana sonucu, grafikteki teknik araçların tek tek “sinyal” üretmesi değil; her birinin bağlamdan hedefe uzanan karar zincirinde belirli bir görev üstlenmesidir. Strateji tekrarlanan sistem, setup güncel düzen, trigger kesin aktivasyon olayı ve trade gerçek uygulamadır. Kontrol alanı Kısa soru Bağlam Hangi piyasa hâli ve hangi üst zaman senaryosu?

### 2. ATK-TR-D1.0-2026-08 — PDF s. 241

> ANA TRADING KİTABI | BÖLÜM 12 İşlem Kurulumu, Strateji Tasarımı ve Doğrulama • 226 düzeni), sistemin güncel adayıdır. Trigger (setup’ı gerçek işleme dönüştüren kesin fiyat olayı), “şimdi aktif” dediğim noktadır. Trade ise gerçek emir, stop, hedef ve kayıtla birlikte uygulanan pozisyondur. Şekil 12.1 – Strateji, setup, tetik ve işlem ayrımı Kavram Cevapladığı soru Örnek Strateji Tekrar eden sistemim nedir? Yükseliş trendinde demand/FVG pullback’i ve bullish yapı teyidi. Setup Şu an uygun yapı oluştu mu? Fiyat 4 saatlik demand’e kontrollü geri döndü. Signal / ipucu Setup lehine hangi bilgi geldi? Satış hacmi azalıyor veya RSI hidden divergence oluşuyor. Trigger Hangi olay işleme izin verir? 1 saatlik bullish CHoCH ve retest kapanışı. Trade Emri nasıl uyguladım? Belirlenmiş giriş, stop, hedef ve işlem günlüğü. Tablo 12.1 – Strateji dilinin görev ayrımı EKRANDA NE ARIYORUM? • Önce hangi stratejiyi aradığımı tek cümleyle yazıyorum. • Grafikte yalnız setup koşullarını işaretliyorum; her olumlu ipucunu giriş sanmıyorum. • Trigger gerçekleşmeden emir vermiyorum. • Gerçekleşen işlemi setup sonucundan ayrı kaydediyorum. DOĞRU BİLİNEN YANLIŞ Mit: Grafikte bullish bir işaret gördüysem setup vardır. Gerçeklik: Bir mum, FVG veya indikatör sinyali yalnız bir parçadır. Setup; doğru bağlam, konum ve tetik zinciriyle oluşur.

**Bölüm/alt başlık:** 12 / 12.1 — Strateji, Setup, Tetik ve İşlem Ayrımı

**Kaynak özeti (`source`):** Trigger (setup’ı gerçek işleme dönüştüren kesin fiyat olayı), “şimdi aktif” dediğim noktadır. Trade ise gerçek emir, stop, hedef ve kayıtla birlikte uygulanan pozisyondur. Yükseliş trendinde demand/FVG pullback’i ve bullish yapı teyidi.

### 3. ATK-TR-D1.0-2026-08 — PDF s. 257

> ANA TRADING KİTABI | BÖLÜM 12 İşlem Kurulumu, Strateji Tasarımı ve Doğrulama • 242 12.14 Kural Tabanlı Strateji Kartı Rules-based strategy (girişten önce bütün karar alanları yazılmış ve farklı grafiklerde aynı biçimde uygulanabilen sistem), yoruma tamamen kapalı olmak zorunda değildir; fakat karar noktaları gözlenebilir ve kaydedilebilir olmalıdır. “Güçlü trend” dersem güçlü trendin ölçütünü, “iyi mum” dersem mumun kapanış ve gövde koşulunu tanımlarım. Kart alanı Yazılacak kural Piyasa / enstrüman Hangi semboller, minimum likidite ve spread koşulu? Stil / zaman dilimi Pozisyon süresi; HTF–MTF–LTF görevleri. Seans / zaman Hangi saatlerde setup geçerli; haber filtresi var mı? Piyasa hâli Trend, range, breakout veya reversal koşulu. Location Kullanılacak zone, swing, liquidity veya average-value alanı. Setup Pullback, breakout, failure, reversal veya tanımlı pattern. Trigger Kesin kapanış, BOS/CHoCH, retest veya footprint şartı. Entry Emir türü ve giriş fiyatı kuralı. Invalidation / stop Tezi bozan fiyat ve uygulama payı. Target Teknik hedef, projection ve yakın engel kuralı. No-trade Hangi eksik veya olumsuz koşulda işlem yok? Kayıt Setup kodu, ekran görüntüsü, sonuç, MAE/MFE veya uygulama hatası. Tablo 12.15 – Kural tabanlı strateji kartı ÖRNEK STRATEJİ CÜMLESİ — XAGTRYG • Günlük bullish structure korunurken 4 saatlik demand/eski BOS alanına pullback ararım. • 1 saatlik SSL sweep sonrası bullish CHoCH ve retest kapanışı trigger’dır. • Entry retestte; invalidation sweep dibi altındaki kabul; ilk hedef önceki 4 saatlik tepedir. …

**Bölüm/alt başlık:** 12 / 12.15 — Backtest, Replay, Forward/Paper Test ve

**Kaynak özeti (`source`):** 12.14 Kural Tabanlı Strateji Kartı Rules-based strategy (girişten önce bütün karar alanları yazılmış ve farklı grafiklerde aynı biçimde uygulanabilen sistem), yoruma tamamen kapalı olmak zorunda değildir; fakat karar noktaları gözlenebilir ve kaydedilebilir olmalıdır. “Güçlü trend” dersem güçlü trendin ölçütünü, “iyi mum” dersem mumun kapanış ve gövde koşulunu tanımlarım. Kart alanı Yazılacak kural Piyasa / enstrüman Hangi semboller, minimum likidite ve spread koşulu?

### 4. ATK-TR-D1.0-2026-08 — PDF s. 240

> ANA TRADING KİTABI | BÖLÜM 12 İşlem Kurulumu, Strateji Tasarımı ve Doğrulama • 225 Bu Bölümün Amacı İlk on bir bölümde grafiğin parçalarını öğrendik: piyasa ve emirler, mum davranışı, market structure, önemli bölgeler, likidite, formasyonlar, hacim, indikatörler, Fibonacci/Elliott, top-down analiz ve çalışma stili. Fakat bu parçalar tek bir karar sistemine bağlanmadığında grafik yalnız işaretlerle dolar. Bölüm 12’nin görevi, “ne görüyorum?” sorusunu “hangi koşul gerçekleşirse işlem yaparım; hangi koşulda hiçbir şey yapmam?” sorusuna dönüştürmektir. Bu bölümde hazır bir kutsal strateji aramam. Önce strateji, setup, trigger ve trade kavramlarını ayırırım. Sonra her işlem fikrini bağlam, konum, rota, tetik, giriş, geçersizlik, hedef ve kayıt zincirinden geçiririm. Bir halka eksikse işlemi zorlamam. BÖLÜM SONUNDA • Strateji, setup, signal, trigger ve trade kavramlarını ayırabileceksiniz. • Bağlamdan hedefe dokuz parçalı işlem kurulumu yazabileceksiniz. • Pullback, breakout, range/failure ve reversal setup ailelerini doğru piyasa hâliyle eşleştirebileceksiniz. • Zone, FVG, indicator ve footprint araçlarını görevlerine göre kullanabileceksiniz. • Kural setini backtest, replay, forward/paper test ve günlükle doğrulayabileceksiniz. Uygulama Görseli 12.1 – XAGTRYG grafiğinde günlük bağlamdan 1 saatlik tetik ve hedefe uzanan tam işlem kurulumunun tek sayfalık görünümü. Temsilî eğitim şeması. 12.1 Strateji, Setup, Tetik ve İşlem Ayrımı Trading strategy (hangi piyasa koşulunda hangi kuralları tekrar tekrar uygulayacağımı belirleyen sistem), tek bir grafikte gördüğüm fırsat değildir. …

**Bölüm/alt başlık:** 12 / 12.1 — Strateji, Setup, Tetik ve İşlem Ayrımı

**Kaynak özeti (`source`):** Bu Bölümün Amacı İlk on bir bölümde grafiğin parçalarını öğrendik: piyasa ve emirler, mum davranışı, market structure, önemli bölgeler, likidite, formasyonlar, hacim, indikatörler, Fibonacci/Elliott, top-down analiz ve çalışma stili. Fakat bu parçalar tek bir karar sistemine bağlanmadığında grafik yalnız işaretlerle dolar. Bölüm 12’nin görevi, “ne görüyorum?” sorusunu “hangi koşul gerçekleşirse işlem yaparım; hangi koşulda hiçbir şey yapmam?” sorusuna dönüştürmektir.

### 5. PTA-C1-2026 — PDF s. 65

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 65 10.9 — VWAP + 50 MA kesişimi neden evrensel kural değildir? VWAP ile 50 günlük hareketli ortalama kesişimini işlem sinyali yapmak, VWAP’ın tanımı değil strateji tercihidir. Test edilmeden evrensel kurala dönüştürülemez. STRATEJİYE ÖZEL ≠ MATEMATİKSEL GERÇEK Geçmişte iyi görünen bir kesişim tek başına istatistiksel avantaj kanıtı değildir. Roller ayrılabilir: MA = trend filtresi, VWAP/AVWAP = hacim ağırlıklı konum. Otomatik kesişim kuralı ayrıca test edilmelidir. 10.10 — VWAP hangi araçlarla birlikte kullanılabilir? Kombinasyon Rol dağılımı Not VWAP/AVWAP + Fiyat yapısı Konum + doğrudan fiyat yapısı Çok güçlü VWAP + RSI/Stoch Konum + hareket gücü Tamamlayıcı VWAP + ATR Konum + fiyat hareketliliği/risk Tamamlayıcı AVWAP + Volume Profile Tek ortalama maliyet eğrisi + fiyat seviyelerine göre hacim dağılımı Farklı sorular VWAP + çoklu MA + VWMA Birçok ortalama fiyat çizgisi Tekrar riski yüksek BÖLÜM SONUCU VWAP, hacmi hesaba katan bir ortalama fiyat ve konum çizgisidir; AVWAP bunu seçtiğiniz bir başlangıçtan itibaren hesaplar. Çizgiyi destek/direnç diye ezberlemek yerine neyi ölçtüğünü ve nereden başladığını bilin. ARA KAVRAM Hacmi Zaman Ekseninden Fiyat Eksenine Taşımak Klasik hacim “ne zaman ne kadar aktivite vardı?” diye sorar. Volume Profile aynı aktiviteyi fiyat

**Bölüm/alt başlık:** 10 / 10.10 — VWAP hangi araçlarla birlikte kullanılabilir?

**Kaynak özeti (`source`):** 10.9 — VWAP + 50 MA kesişimi neden evrensel kural değildir? VWAP ile 50 günlük hareketli ortalama kesişimini işlem sinyali yapmak, VWAP’ın tanımı değil strateji tercihidir. Test edilmeden evrensel kurala dönüştürülemez.

### 6. PTA-C1-2026 — PDF s. 25

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 25 AYAR UYARISI K=20, D=1 gibi ayarlar yalnız bir kullanım tercihi olabilir. Bu değerler “Stochastic’in doğru ayarı” değildir. Ayar, strateji ve zaman dilimiyle birlikte değerlendirilmelidir. 4.6 — Stochastic RSI neden daha hassastır? Stochastic RSI fiyat aralığını değil, RSI’nın kendi yakın dönem aralığını 0–100 arasında yeniden ölçekler. Bu yüzden RSI’nın mutlak seviyesi çok değişmese bile, RSI kendi son dönem aralığının üst veya alt ucuna hızla yaklaştığında Stoch RSI 0 veya 100 bölgelerine daha hızlı gidebilir. FORMÜL MANTIĞI Stoch RSI = 100 × (Güncel RSI − N periyotluk en düşük RSI) / (N periyotluk en yüksek RSI − N periyotluk en düşük RSI). Bu formül, Stoch RSI’nın doğrudan RSI’dan türetildiğini açıkça gösterir. SAYISAL ÖRNEK — AYNI RSI, FARKLI YORUM Son 14 periyotta RSI 40 ile 70 arasında dolaşmış ve güncel RSI 64 olsun. Stoch RSI = (64−40)/(70−40)×100 = 80. RSI 64 klasik 70 eşiğinin altında iken Stoch RSI 80 olabilir. Çelişki yoktur: iki araç farklı sorular sorar. RSI hareket gücü seviyesini, Stoch RSI ise RSI’nın kendi yakın dönem aralığındaki konumunu gösterir. Şekil 4.3 — Aynı sentetik fiyat serisinde Stoch RSI, RSI’ya göre daha hızlı 0/100 uçlarına hareket eder. Daha hassas olmak daha az yanlış sinyal anlamına gelmez.

**Bölüm/alt başlık:** 4 / 4.6 — Stochastic RSI neden daha hassastır?

**Kaynak özeti (`source`):** AYAR UYARISI K=20, D=1 gibi ayarlar yalnız bir kullanım tercihi olabilir. Bu değerler “Stochastic’in doğru ayarı” değildir. Ayar, strateji ve zaman dilimiyle birlikte değerlendirilmelidir.

### 7. PTA-C1-2026 — PDF s. 44

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 44 Şekil 7.1 — Beş değerlik basitleştirilmiş eğitim örneği: 98, 99, 100, 101, 102 ortalaması 100; standart sapma yaklaşık 1,41. ±2σ aralığı yaklaşık 97,17–102,83. NEDEN 5 VERİ KULLANDIK? Gerçek Bollinger ayarı çoğunlukla daha uzun bir pencere kullanır; burada amaç yalnız standart sapmanın ne yaptığını görünür kılmaktır. Küçük örnek hesap kolaylığı içindir, strateji parametresi değildir. 7.2 — %B: bant içindeki konumu tek sayıya dönüştürmek %B, fiyatın Bollinger bantlarına göre nerede bulunduğunu sayısallaştırır. Temel okuma şöyledir: %B = 1 → fiyat üst bantta %B = 0,5 → fiyat orta bantta %B = 0 → fiyat alt bantta %B > 1 → fiyat üst bandın üzerinde %B < 0 → fiyat alt bandın altında Bu değer “pahalı–ucuz” ölçümü değildir. Fiyatın mevcut Bollinger yapısı içindeki göreli konumunu nicel hale getirir. 7.3 — Üst banda temas neden otomatik SAT değildir? Üst banda temas, fiyatın ortalamadan belirgin biçimde uzaklaştığını gösterir; formülde dönüş şartı yoktur. Güçlü yükselişte fiyat üst bant boyunca ilerleyebilir.

**Bölüm/alt başlık:** 7 / 7.3 — Üst banda temas neden otomatik SAT değildir?

**Kaynak özeti (`source`):** Gerçek Bollinger ayarı çoğunlukla daha uzun bir pencere kullanır; burada amaç yalnız standart sapmanın ne yaptığını görünür kılmaktır. Küçük örnek hesap kolaylığı içindir, strateji parametresi değildir. 7.2 — %B: bant içindeki konumu tek sayıya dönüştürmek %B, fiyatın Bollinger bantlarına göre nerede bulunduğunu sayısallaştırır.

### 8. PTA-C1-2026 — PDF s. 46

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 46 Gözlem Doğru yorum Yanlış yorum Bantlar daralıyor Fiyat hareketliliği/dağılım daralıyor “Yukarı kırılım geliyor.” Bantlar genişliyor Hareket genişliği artıyor “Trend kesin güçlü.” Fiyat üst bantta Üst bant bölgesinde “Aşırı alım → satış yönlü işlem.” Fiyat alt bantta Alt bant bölgesinde “Ucuz → hemen al.” 7.5 — Bant Genişliği (BandWidth): sıkışmadan genişlemeye hareketlilik döngüsü Bant Genişliği (BandWidth), üst ve alt Bollinger bantları arasındaki genişliği ayrı bir seri halinde izlemeye yarar. Bant Genişliği düşerken bantlar daralır; yükselirken genişler. Sıkışmayı yalnız “bantlar dar görünüyor” diye değerlendirmek yerine, Bant Genişliği’nin enstrümanın kendi geçmişindeki konumuna bakılabilir. Sıra dışı derecede düşük Bant Genişliği sıkışma rejimini, sıra dışı derecede yüksek Bant Genişliği ise geniş hareketlilik rejimini gösterir. Kullanılan tarih penceresi bir strateji ayarıdır; tek bir evrensel sayı yoktur. Düşük Bant Genişliği tek başına yön vermez. Ancak Bant Genişliği çok düşük bir bölgeden yeniden yükselmeye başladığında fiyat hareketliliğinin genişleme evresine geçtiği görülebilir. Sıkışma, genişleme ve aşırı genişleme aynı döngünün farklı evreleridir Bollinger yapısı kabaca şu fiyat hareketliliği döngüsüyle okunabilir: sıkışma → Bant Genişliği tabanı → genişleme → yüksek Bant Genişliği / aşırı genişleme → daralma Burada ölçülen yön değil, hareket genişliğidir. Yüksek Bant Genişliği sonrasında hareketlilik azalabilir; fakat bu mutlaka trendin tersine döneceği anlamına gelmez. …

**Bölüm/alt başlık:** 7 / 7.5 — Bant Genişliği (BandWidth): sıkışmadan genişlemeye hareketlilik

**Kaynak özeti (`source`):** Gözlem Doğru yorum Yanlış yorum Bantlar daralıyor Fiyat hareketliliği/dağılım daralıyor “Yukarı kırılım geliyor.” Bantlar genişliyor Hareket genişliği artıyor “Trend kesin güçlü.” Fiyat üst bantta Üst bant bölgesinde “Aşırı alım → satış yönlü işlem.” Fiyat alt bantta Alt bant bölgesinde “Ucuz → hemen al.” 7.5 — Bant Genişliği (BandWidth): sıkışmadan genişlemeye hareketlilik döngüsü Bant Genişliği (BandWidth), üst ve alt Bollinger bantları arasındaki genişliği ayrı bir seri halinde izlemeye yarar. Bant Genişliği düşerken bantlar daralır; yükselirken genişler. Sıkışmayı yalnız “bantlar dar görünüyor” diye değerlendirmek yerine, Bant Genişliği’nin enstrümanın kendi geçmişindeki konumuna bakılabilir.

## Test fikri (`hypothesis`)

Bu konuya ait kaynak varyantları korunur. İlk aşamada sabit eşik seçilmez; geniş sembol evreninde aynı tanımların amaçladığı davranışa katkısı karşılaştırılır.
