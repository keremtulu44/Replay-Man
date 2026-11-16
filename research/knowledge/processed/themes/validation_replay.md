# validation_replay

**Kapsam:** 45 sayfa eşleşmesi

## Proje yorumu (`inference`)

Toplu ölçüm, bar replay ve forward gözlem farklı sorular cevaplar; kanıt türleri birbirinin yerine geçmez.

## Nasıl kullanılabilir?

Araştırma doğrulama ve future-leak denetimi

## Kaynak şeritleri

### 1. ATK-TR-D1.0-2026-08 — PDF s. 259

> ANA TRADING KİTABI | BÖLÜM 12 İşlem Kurulumu, Strateji Tasarımı ve Doğrulama • 244 DOĞRU BİLİNEN YANLIŞ Mit: Backtest kârlıysa strateji gerçek piyasada çalışmaya hazırdır. Gerçeklik: Backtest yalnız geçmiş kuralların sonucudur; geleceği garanti etmez. Replay karar disiplinini, paper/forward test ise canlı akış ve emir uygulanabilirliğini sınar. DOĞRULAMA VAKA AKIŞI • Strateji kartı v1.0 ile 120 geçmiş setup taranır; komisyon/slippage eklenir. • Bar replay’de en az farklı trend, range ve volatilite dönemleri uygulanır. • Paper trading sırasında gerçek seans, alarm ve emir kısıtları korunur. • Kayıpların setup kaynaklı mı, kural ihlali mi olduğu ayrılır. • Yalnız bir kural değiştirilir ve v1.1 ayrı sonuç setiyle karşılaştırılır. Uygulama Görseli 12.8 – Aynı stratejinin geçmiş tarama, bar replay ve paper trading ekranlarının yan yana karşılaştırılması. Temsilî eğitim şeması.

**Bölüm/alt başlık:** 12 / 12.15 — Backtest, Replay, Forward/Paper Test ve

**Kaynak özeti (`source`):** DOĞRU BİLİNEN YANLIŞ Mit: Backtest kârlıysa strateji gerçek piyasada çalışmaya hazırdır. Gerçeklik: Backtest yalnız geçmiş kuralların sonucudur; geleceği garanti etmez. Replay karar disiplinini, paper/forward test ise canlı akış ve emir uygulanabilirliğini sınar.

### 2. ATK-TR-D1.0-2026-08 — PDF s. 314

> ANA TRADING KİTABI | BÖLÜM 15 TradingView, Grafik Araçları ve Test İş Akışı • 299 15.8 Community Script, Repaint ve Otomatik Araç Sınırları Community script, yararlı fikirler ve özel araçlar sağlayabilir; ancak yayınlanmış veya popüler olması metodolojiyi doğrulamaz. Repaint (geçmişte görünen sinyalin yeni veri geldikçe değişmesi, silinmesi veya konum değiştirmesi), özellikle MTF, pivot, future-looking veya açık bar kullanan araçlarda test sonucunu yanıltabilir. Denetim Kontrol edeceğim Açıklama Araç ne ölçüyor, sinyal hangi bar kapanışında kesinleşiyor? Kaynak kod / şeffaflık Kod açık mı; hesap mantığı açıklanmış mı? Repaint davranışı Canlı bar, geçmiş bar ve replay’de işaret değişiyor mu? Veri bağımlılığı Volume/feed/session eksikse ne olur? Alarm Alarm koşulu plotla aynı anda ve aynı kapanış kuralında mı? Sürüm Güncelleme geçmiş testi sessizce değiştiriyor mu? Bağımsız test Farklı dönem, sembol ve rejimde kayıt var mı? Tablo 15.8 – Community script ve repaint denetimi EYLEM DİLİ Bir script’i grafiğe eklediğimde önce sinyale bakmam. Açıklamasını, ayarlarını, bar kapanış davranışını ve replay/live farkını incelerim. “Non-repainting” yazısını kanıt saymam; kendi ekran kaydı ve bar replay testiyle doğrularım. DOĞRU BİLİNEN YANLIŞ Mit: Çok kullanılan veya yüksek beğenili community indikatörü güvenilir ve kârlıdır. Gerçeklik: Popülerlik yalnız görünürlük ve ilgi göstergesidir. Veri, metodoloji, repaint, maliyet ve bağımsız test ayrıca incelenmelidir. VAKA ANALİZİ — OTOMATİK SİNYAL Bir community script XAGTRYG 2S grafikte geçmişte kusursuz dip okları gösteriyor. …

**Bölüm/alt başlık:** 15 / 15.8 — Community Script, Repaint ve Otomatik

**Kaynak özeti (`source`):** 15.8 Community Script, Repaint ve Otomatik Araç Sınırları Community script, yararlı fikirler ve özel araçlar sağlayabilir; ancak yayınlanmış veya popüler olması metodolojiyi doğrulamaz. Repaint (geçmişte görünen sinyalin yeni veri geldikçe değişmesi, silinmesi veya konum değiştirmesi), özellikle MTF, pivot, future-looking veya açık bar kullanan araçlarda test sonucunu yanıltabilir. Denetim Kontrol edeceğim Açıklama Araç ne ölçüyor, sinyal hangi bar kapanışında kesinleşiyor?

### 3. ATK-TR-D1.0-2026-08 — PDF s. 261

> ANA TRADING KİTABI | BÖLÜM 12 İşlem Kurulumu, Strateji Tasarımı ve Doğrulama • 246 Terim Aksiyon tanımı Invalidation İşlem tezinin artık geçerli olmadığı fiyat/davranış. No-trade Kurallar nedeniyle bilinçli olarak işlem yapılmayan durum. Confluence Farklı veri ailelerinin aynı tezi desteklemesi. Backtest Kuralların geçmiş verideki davranışını test etme. Bar Replay Gelecek mumları gizleyerek geçmişi canlı akış gibi uygulama. Forward Test Kuralları yeni gelen veride izleme. Paper Trading Gerçek para riske etmeden sanal emirle uygulama. Edge Uzun örnek dizisinde olumlu beklenen değer üretmesi beklenen istatistiksel avantaj. Tablo 12.18 – Bölüm 12 temel sözlüğü Bölüm Sonu Kontrol Soruları 1. Strateji ile setup arasındaki temel fark nedir? 2. Signal neden trigger değildir? 3. İşlem kurulumunun dokuz parçası nelerdir? 4. İşlem tezi hangi koşullu cümleyle yazılır? 5. No-trade kuralı neden stratejinin aktif bir parçasıdır? 6. Location ile trigger hangi farklı soruları cevaplar? 7. Likidite rotası hedef planını nasıl değiştirir? 8. Confluence neden gösterge sayısı değildir? 9. RSI, MACD ve Stochastic RSI neden üç bağımsız kanıt sayılmayabilir? 10. Tetik hiyerarşisinde gözlem, uyarı, teyit ve aktivasyon nasıl ayrılır? 11. Agresif girişin görünmeyen maliyeti nedir? 12. Retest girişinin temel avantajı ve riski nedir? 13. Invalidation ile stop-loss emri arasındaki fark nedir? 14. Dar stop neden otomatik olarak düşük risk anlamına gelmez? 15. Pullback setup’ında güçlü karşı displacement neden uyarıdır? 16. Breakout’ın güçlü sayılması için hangi kanıtlar aranır? 17. …

**Bölüm/alt başlık:** 12 / 12.15 — Backtest, Replay, Forward/Paper Test ve

**Kaynak özeti (`source`):** Terim Aksiyon tanımı Invalidation İşlem tezinin artık geçerli olmadığı fiyat/davranış. No-trade Kurallar nedeniyle bilinçli olarak işlem yapılmayan durum. Confluence Farklı veri ailelerinin aynı tezi desteklemesi.

### 4. ATK-TR-D1.0-2026-08 — PDF s. 319

> ANA TRADING KİTABI | BÖLÜM 15 TradingView, Grafik Araçları ve Test İş Akışı • 304 Şekil 15.6 – Kuraldan replay ve paper testine doğrulama merdiveni Replay adımı Yapacağım 1 Test kimliği Strateji sürümü, sembol, timeframe, dönem ve piyasa rejimi. 2 Kör başlangıç Setup öncesine git; gelecek barları ve sonuç notlarını gizle. 3 Karar kaydı Bağlam, setup, trigger, entry, stop, target ve no-trade. 4 Bar ilerletme Sabit hız veya tek bar; karar sonradan değiştirilmez. 5 Sonuç R, MFE/MAE, maliyet varsayımı ve kural ihlali. 6 Örneklem Sadece iyi örnekleri değil uygun tüm oluşumları kaydet. 7 Değerlendirme Tek trade değil yeterli seri ve rejim karşılaştırması. Tablo 15.11 – Bar Replay test protokolü EKRANDA NE ARIYORUM? • Replay başlangıcı setup sonucunu saklıyor mu? • İndikatör veya pattern geçmişte geleceği kullanıyor olabilir mi? • Kararımı bar ilerlemeden önce ekran görüntüsüyle kaydettim mi? • No-trade örneklerini de sayıyor muyum? • Spread, slippage ve işlem saatini varsayıma ekledim mi? DOĞRU BİLİNEN YANLIŞ Mit: Replay’de yüksek win rate stratejinin doğrulandığını kanıtlar. Gerçeklik: Seçim yanlılığı, az örneklem, geleceği görme, maliyet eksikliği ve repaint sonucu şişirebilir. Replay karar pratiği ve veri toplama aracıdır; tam doğrulama zincirinin tek basamağıdır.

**Bölüm/alt başlık:** 15 / 15.11 — Bar Replay ile Kör Karar Pratiği

**Kaynak özeti (`source`):** 2 Kör başlangıç Setup öncesine git; gelecek barları ve sonuç notlarını gizle. 3 Karar kaydı Bağlam, setup, trigger, entry, stop, target ve no-trade. 4 Bar ilerletme Sabit hız veya tek bar; karar sonradan değiştirilmez.

### 5. PTA-C1-2026 — PDF s. 8

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 8 Kombinasyon Rol dağılımı Değerlendirme RSI + Stoch + Stoch RSI Hareket gücü + hareket gücü + hareket gücü Yüksek tekrar riski MA + MACD kesişim Trend bilgisi + MA farkından gelen benzer trend/hareket gücü bilgisi Kısmi tekrar MA + RSI + ATR Yön + hareket gücü + fiyat hareketliliği/risk Daha tamamlayıcı Fiyat yapısı + AVWAP + RSI Yapı + konum + hareket gücü Daha bağımsız bilgi 1.4 — “Klasik kural” neden bazen bozulur? Teknik analiz eğitimlerinde kısa kurallar işe yarar: “RSI 70 üstü aşırı alım”, “ADX 25 üstü güçlü trend”, “fiyat 200 MA üstünde yükseliş yönlü”. Sorun, bu cümleleri her piyasada geçerli yasa gibi kullanmaktır. Aynı kural trendli piyasada, yatay piyasada veya hareketliliğin çok arttığı bir dönemde farklı sonuç verebilir. ÖRNEK — RSI 70 Güçlü bir yükselişte RSI 70’in üzerinde uzun süre kalabilir. Bu nedenle 70 seviyesi “satış düğmesi” değil, yüksek hareket gücü bölgesidir. Dönüş için ayrıca fiyat davranışı gerekir. ÖRNEK — ATR YÜKSELİYOR ATR yükseliş ya da düşüş yönü söylemez. Sert düşüşte de ATR yükselebilir. “ATR arttı, para piyasaya geliyor ve fiyat yükselecek” çıkarımı ölçülen değişkene uymayan bir nedensellik kurar. ÖRNEK — ADX YÜKSELİYOR ADX trend gücünü anlatır. Fiyat düşerken ADX yükselebilir; çünkü güçlenen şey aşağı trend olabilir. “ADX yükseldi = yükseliş yönlü” yorumunda yön ve güç birbirine karıştırılır. 1.5 — Ayarları geçmişe uydurma riski (geçmişe aşırı uyum) Varsayılan parametreler kutsal değildir. Ancak geçmiş grafiğe en iyi oturan değeri bulana kadar ayar değiştirmek de profesyonel optimizasyon değildir. …

**Bölüm/alt başlık:** 1 / 1.5 — Ayarları geçmişe uydurma riski (geçmişe aşırı uyum)

**Kaynak özeti (`source`):** Kombinasyon Rol dağılımı Değerlendirme RSI + Stoch + Stoch RSI Hareket gücü + hareket gücü + hareket gücü Yüksek tekrar riski MA + MACD kesişim Trend bilgisi + MA farkından gelen benzer trend/hareket gücü bilgisi Kısmi tekrar MA + RSI + ATR Yön + hareket gücü + fiyat hareketliliği/risk Daha tamamlayıcı Fiyat yapısı + AVWAP + RSI Yapı + konum + hareket gücü Daha bağımsız bilgi 1.4 — “Klasik kural” neden bazen bozulur? Teknik analiz eğitimlerinde kısa kurallar işe yarar: “RSI 70 üstü aşırı alım”, “ADX 25 üstü güçlü trend”, “fiyat 200 MA üstünde yükseliş yönlü”. Sorun, bu cümleleri her piyasada geçerli yasa gibi kullanmaktır.

### 6. PTA-C1-2026 — PDF s. 69

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 69 Profil şekli Hacmin ağırlığı Genel yorum Tek başına söylemez b biçimli Alt bölgede Hacim daha düşük fiyatlarda yoğunlaşıyor Otomatik SAT İnce Profil Belirgin bir merkez oluşmamış Yönlü hareket sırasında orta bölgede daha az oyalanma görülebilir Hareketin yönü 11.5 — FRVP aralığını nasıl seçmeli? Fixed Range Volume Profile (FRVP) analiz aralığını kullanıcıya bırakır. Bu esneklik geçmişe uydurma riski yaratır; yatay sıkışma, belirgin hareket veya önemli olay gibi önceden açıklanabilen bir aralık seçme kuralı kullanın. Aralık seçimi Değerlendirme “Sonuç güzel göründüğü için başlangıcı birkaç mum geri aldım.” Sonradan bakarak seçme / geçmişe aşırı uyum riski “Bu konsolidasyonun başı ve kırılım barı arasında profiliyorum.” Önceden tanımlı piyasa fazı “Son güçlü hareketin tamamını ölçüyorum.” Yapısal gerekçe var “Her analizde farklı noktayı deneyip en iyi POC’u seçiyorum.” Yöntem zayıf 11.6 — Profil renkleri gerçek alıcı/satıcı emir akışını göstermez Volume Profile’daki yükseliş/düşüş renkleri gerçek emir akışında hangi tarafın ne kadar agresif olduğunu göstermez. Renk sınıflamasından kesin alıcı/satıcı gücü çıkarımı yapmayın. Kavram Ne anlatır? Ne anlatmaz? TradingView profil renk sınıflaması Alt zaman dilimi barlarının yönüne göre hacim sınıflaması Gerçek alış/satış emirlerinin hangi tarafın başlattığı Gerçek alış/satış tarafı emir akışı İşlemlerin alış veya satış tarafında gerçekleşmesini ayırmaya çalışır Standart VP bar rengi sınıflamasıyla aynı değildir

**Bölüm/alt başlık:** 11 / 11.6 — Profil renkleri gerçek alıcı/satıcı emir akışını göstermez

**Kaynak özeti (`source`):** Profil şekli Hacmin ağırlığı Genel yorum Tek başına söylemez b biçimli Alt bölgede Hacim daha düşük fiyatlarda yoğunlaşıyor Otomatik SAT İnce Profil Belirgin bir merkez oluşmamış Yönlü hareket sırasında orta bölgede daha az oyalanma görülebilir Hareketin yönü 11.5 — FRVP aralığını nasıl seçmeli? Fixed Range Volume Profile (FRVP) analiz aralığını kullanıcıya bırakır. Bu esneklik geçmişe uydurma riski yaratır; yatay sıkışma, belirgin hareket veya önemli olay gibi önceden açıklanabilen bir aralık seçme kuralı kullanın.

### 7. PTA-C1-2026 — PDF s. 118

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 118 Şekil 19.3 — Sonradan seçilen alternatif pivotlar geçmiş fiyatı daha güzel sarabilir; bu durum öngörü gücü kanıtı değildir. Kontrol Geçerli yaklaşım Geçmişe aşırı uyum işareti A–B–C Önceden tanımlı büyük belirgin dönüş noktaları Fiyat ilerledikçe pivot kaydırmak Varyant Kullanım kuralı analizden önce belli Geçmişe en iyi oturan türü seçmek İhlal İhlali kaydet, yapı teyidini ayrı değerlendir Kırılan Pitchfork’u silip yenisini çizmek 19.5 — Küçük pivot hatası ileri bölgelerde büyüyebilir Pitchfork’un eğimi seçilen A–B–C pivotlarından türetilir. Başlangıç pivotlarından biri küçük miktarda kaydırıldığında ilk bölümde fark az görünebilir; çizgi ileri uzadıkça orta çizgi ve paralel sınırlar arasındaki konum farkı büyür. Bu nedenle pivotu birkaç bar ileri veya geri taşımak yalnız başlangıç noktasını değil, ilerideki bütün geometrik alanı değiştirir. Mıknatıs (Magnet) gibi araçların amacı “daha iyi sinyal” üretmek değil, seçilen gerçek tepe veya dip noktasına daha kesin bağlanmaktır.

**Bölüm/alt başlık:** 19 / 19.5 — Küçük pivot hatası ileri bölgelerde büyüyebilir

**Kaynak özeti (`source`):** Kontrol Geçerli yaklaşım Geçmişe aşırı uyum işareti A–B–C Önceden tanımlı büyük belirgin dönüş noktaları Fiyat ilerledikçe pivot kaydırmak Varyant Kullanım kuralı analizden önce belli Geçmişe en iyi oturan türü seçmek İhlal İhlali kaydet, yapı teyidini ayrı değerlendir Kırılan Pitchfork’u silip yenisini çizmek 19.5 — Küçük pivot hatası ileri bölgelerde büyüyebilir Pitchfork’un eğimi seçilen A–B–C pivotlarından türetilir. Başlangıç pivotlarından biri küçük miktarda kaydırıldığında ilk bölümde fark az görünebilir; çizgi ileri uzadıkça orta çizgi ve paralel sınırlar arasındaki konum farkı büyür. Bu nedenle pivotu birkaç bar ileri veya geri taşımak yalnız başlangıç noktasını değil, ilerideki bütün geometrik alanı değiştirir.

### 8. PTA-C1-2026 — PDF s. 133

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 133 Alan Yazılması gereken kural Bağlam Trend veya yatay piyasa nasıl tanımlanıyor? Yön Alış veya satış yönü hangi açık koşulla belirleniyor? Konum İşlem yalnız nerede aranacak? Giriş işareti Tam olarak hangi kapanış veya olay giriş izni veriyor? Fikrin bozulduğu seviye Hangi fiyat davranışı fikri yanlışlıyor? Risk Stop, pozisyon büyüklüğü ve maksimum hesap riski nasıl hesaplanıyor? Yönetim Takip eden stop, kâr alma veya çıkış kuralı ne? İşlem yok Hangi koşullarda sistem bilinçli olarak işlem üretmiyor? Test Hangi veri aralığı ve ölçülerle test edilecek? SON KONTROL Bir işlem düzenini açıklamak için beş indikatörün adını söylemeniz gerekiyorsa sistemi yeniden sadeleştirin. İyi bir işlem planı birkaç net cümleyle bağlamı, yönü ve piyasa ortamını, konumu, giriş işaretini, fikrin nerede bozulacağını, riski ve yönetimi anlatabilmelidir. 21.9 — Sistemi kurduktan sonra: beklenen değer ve sermaye dalgalanması Sistemin kurallarını yazmak ilk adımdır. İkinci soru, geçmişte iyi görünen sonucun gerçekten dayanıklı bir avantaj mı, yoksa tesadüf ve geçmişe aşırı uyum mu olduğudur. Bu bölümde amaç ileri istatistik yapmak değil; sistemin sonuçlarını birkaç temel ölçüyle daha gerçekçi sınamaktır. Bir sistemin kalitesi yalnız kazanma oranıyla ölçülemez. …

**Bölüm/alt başlık:** 21 / 21.9 — Sistemi kurduktan sonra: beklenen değer ve sermaye

**Kaynak özeti (`source`):** Alan Yazılması gereken kural Bağlam Trend veya yatay piyasa nasıl tanımlanıyor? Yön Alış veya satış yönü hangi açık koşulla belirleniyor? Konum İşlem yalnız nerede aranacak?

## Test fikri (`hypothesis`)

Bu konuya ait kaynak varyantları korunur. İlk aşamada sabit eşik seçilmez; geniş sembol evreninde aynı tanımların amaçladığı davranışa katkısı karşılaştırılır.
