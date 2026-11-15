# journal_review

**Kapsam:** 13 sayfa eşleşmesi

## Proje yorumu (`inference`)

Deney, karar ve uygulama kayıtları model hatası ile süreç ihlalini sonradan ayırabilecek kimlikler taşımalıdır.

## Nasıl kullanılabilir?

Model sonucu ile uygulama hatasını ayıran deney günlüğü

## Kaynak şeritleri

### 1. ATK-TR-D1.0-2026-08 — PDF s. 258

> ANA TRADING KİTABI | BÖLÜM 12 İşlem Kurulumu, Strateji Tasarımı ve Doğrulama • 243 canlıymış gibi ilerletme), forward test (kuralları yeni gelen piyasa verisinde izleme) ve paper trading (gerçek para riske etmeden sanal emirle uygulama) farklı soruları cevaplar. Şekil 12.7 – Strateji doğrulama merdiveni Aşama Ana soru Kaydedilecek veri Yaygın hata Kural denetimi Kural objektif ve tekrar edilebilir mi? Her koşulun evet/hayır tanımı. Belirsiz sıfatlarla test yapmak. Geçmiş grafik taraması Model farklı dönemlerde gerçekten görülüyor mu? Setup örneği, bağlam, sonuç, no-trade. Yalnız güzel örnek seçmek. Bar replay Geleceği görmeden kuralları uygulayabiliyor muyum? Karar zamanı, screenshot, kaçırılan/uydurulan kural. Mum ilerledikçe seviyeyi değiştirmek. Backtest Kurallar geçmişte hangi sonuç dağılımını üretiyor? Trade sayısı, win/loss, ortalama R, maliyetli/maliyetsiz sonuç. Komisyon ve slippage’i yok saymak. Forward / paper Canlı veri akışında emir ve rutin uygulanabiliyor mu? Dolum, slippage, alarm, gecikme, kural ihlali. Sanal işlemde gerçekçi olmayan dolum kullanmak. Günlük ve iyileştirme Hata modelde mi, uygulamada mı? Setup kodu, süreç puanı, değiştirilen tek kural. Birkaç kayıptan sonra bütün sistemi değiştirmek. Tablo 12.16 – Doğrulama basamakları EKRANDA NE ARIYORUM? • Test başlangıcında kuralları ve tarih aralığını sabitliyorum. • Geçmiş grafikte gelecekte oluşmuş sonucu görmeden karar anını işaretliyorum. • Maliyetli ve maliyetsiz sonuçları ayrı kaydediyorum. • Kârlılık kadar maksimum kayıp serisi ve uygulama hatasını inceliyorum. …

**Bölüm/alt başlık:** 12 / 12.15 — Backtest, Replay, Forward/Paper Test ve

**Kaynak özeti (`source`):** canlıymış gibi ilerletme), forward test (kuralları yeni gelen piyasa verisinde izleme) ve paper trading (gerçek para riske etmeden sanal emirle uygulama) farklı soruları cevaplar. Geçmiş grafik taraması Model farklı dönemlerde gerçekten görülüyor mu? Setup örneği, bağlam, sonuç, no-trade.

### 2. ATK-TR-D1.0-2026-08 — PDF s. 232

> ANA TRADING KİTABI | BÖLÜM 11 İşlem Stilleri, Piyasa Seçimi ve Uygulama Rutinleri • 217 Şekil 11.6 – Üç aşamalı uygulama rutini Aşama Yapacağım işler Yapmayacağım işler Piyasa öncesi Takvim, seans, watchlist, HTF bağlam, setup seviyesi, alarm ve günlük sınır. Canlı fiyat gelmeden rastgele yön tahmini. İşlem sırası Yalnız planlı setup, risk kontrolü, ekran görüntüsü ve kısa duygu notu. Kayıp sonrası yeni model icat etmek. Piyasa sonrası Entry/exit değil süreç puanı, hata sınıfı ve sonraki aksiyon. Tek işlem sonucuyla sistemi değiştirmek. Tablo 11.14 – Günlük rutin VAKA ANALIZI — XAGTRYG DAY TRADING GÜNÜ Günlük grafik range içinde; 1 saatte üst sınıra yaklaşım var. Kullanıcı New York/ABD veri saatlerinde metal volatilitesinin artabileceğini biliyor ve yalnız iki saatlik pencere ayırıyor. Sonraki adımlarım: 1. Piyasa öncesinde günlük range sınırını ve 1 saatlik setup alanını çizerim. 2. Veri saatini işaretler, açıklama çevresinde normal mum davranışı beklemem. 3. Planım breakout ise close+acceptance; failure ise range içine geri kapanış şartını yazarım. 4. İki saatlik pencere dışında yeni işlem açmam. 5. Gün sonunda sonuçtan bağımsız olarak plan, tetik ve uygulama hatasını ayrı puanlarım.

**Bölüm/alt başlık:** 11 / 11.14 — Piyasa Öncesi–Sırası–Sonrası Vaka

**Kaynak özeti (`source`):** Canlı fiyat gelmeden rastgele yön tahmini. İşlem sırası Yalnız planlı setup, risk kontrolü, ekran görüntüsü ve kısa duygu notu. Kayıp sonrası yeni model icat etmek.

### 3. ATK-TR-D1.0-2026-08 — PDF s. 236

> ANA TRADING KİTABI | BÖLÜM 11 İşlem Stilleri, Piyasa Seçimi ve Uygulama Rutinleri • 221 Kavram Eylem En büyük hata Günlük rutin Hazırlık–uygulama–inceleme sırasını sabitle. Yalnız P&L kaydetmek. Tablo 11.15 – Bölüm 11 hızlı başvuru Grafik ve Rutin Başı Kontrol Listesi  Seçtiğim stil gerçek ekran zamanıma uyuyor mu?  Pozisyonu gece veya hafta sonu taşıma kuralım net mi?  Stil ile setup’ı birbirine karıştırıyor muyum?  Piyasanın veri ve likidite kalitesi yeterli mi?  Spread, ücret, funding/premium ve slippage hedefe göre kabul edilebilir mi?  Volatilite setup’ımın ihtiyacıyla uyumlu mu?  İşlem göreceğim seans ve haber penceresi belli mi?  Watchlist sınırlı ve güncel mi?  HTF bağlam ve setup seviyesi fiyat gelmeden yazıldı mı?  Bugün izin verilen setup sayısı belli mi?  Günlük maksimum işlem ve kayıp sınırı tanımlı mı?  Options, hedge veya kaldıraç kullanımının ayrı riski anlaşılmış mı?  Day trade’i plansız swing’e çevirmeme kuralım var mı?  Piyasa sonrası süreç puanı ve ekran görüntüsü kaydı yapacak mıyım?  Tek sonuçla stil veya sistem değiştirmeyecek miyim?  Bugün işlem yapmamak da planlı bir karar olabilir mi? Temel Sözlük Terim Aksiyon tanımı Trading style Elde tutma, karar hızı ve ekran biçimini tanımlayan çalışma modeli. Scalping Saniye–dakika süren küçük hareketleri yüksek uygulama hızıyla işleme. Day trading Pozisyonu tanımlı işlem günü/seans içinde açıp kapatma. Swing trading Birkaç gün–hafta süren fiyat salınımını işleme. Position trading Hafta–ay süren aktif trend veya makro pozisyonu yönetme. …

**Bölüm/alt başlık:** 11 / 11.15 — Kendi Çalışma Modelini Kurma

**Kaynak özeti (`source`):** Kavram Eylem En büyük hata Günlük rutin Hazırlık–uygulama–inceleme sırasını sabitle.  Pozisyonu gece veya hafta sonu taşıma kuralım net mi?  Stil ile setup’ı birbirine karıştırıyor muyum?

### 4. ATK-TR-D1.0-2026-08 — PDF s. 289

> ANA TRADING KİTABI | BÖLÜM 14 Trading Psikolojisi, Piyasa Duygusu ve Süreç Disiplini • 274 Yanlılık Grafikte/kararda görülen işaret Koruyucu kayıt Recency Son üç kayıptan sonra sistemi aniden değiştirme. Rolling örneklem, rejim ve kural uyumu ayrı incelenir. Confirmation Kırılan trendline’ı tezi korumak için yeniden çizme. İşlem öncesi ekran görüntüsü ve karşı kanıt alanı. Outcome Plan dışı kazancı “iyi trade” sayma. Süreç puanı P&L’den önce verilir. Hindsight Sonucu gördükten sonra “zaten belliydi” deme. Entry anındaki bilgi seti saklanır. Overconfidence Kazanç serisinden sonra size/leverage artırma. Risk oranı yalnız planlı dönemsel incelemede değişir. Anchoring İlk hedefe veya analist fiyatına takılma. Canlı yapı ve geçersizlik yeniden okunur. Tablo 14.6 – Bilişsel yanlılıklar ve davranış korumaları DOĞRU BİLİNEN YANLIŞ Mit: Kazanan işlem doğru analiz, kaybeden işlem yanlış analizdir. Gerçeklik: Doğru uygulanmış olumlu expectancy işlemi kaybedebilir; plansız işlem kazanabilir. Kalite, işlem anındaki bilgi ve kurala göre değerlendirilir. VAKA ANALİZİ — KURAL DEĞİŞTİRME Dört zarar sonrası “breakout modeli artık çalışmıyor” diyorum. Önce dört işlemin de aynı model, piyasa rejimi ve kuralla gerçekleşip gerçekleşmediğini kontrol ederim. İki işlemde geç giriş, birinde haber filtresi ihlali varsa sorun edge değil uygulamadır. Kural değişikliğini tek seriyle değil, tanımlı inceleme örneklemiyle yaparım. 14.7 Korku: Tereddüt, Donma ve Erken Çıkış Korku yalnız zarar korkusu değildir. …

**Bölüm/alt başlık:** 14 / 14.7 — Korku: Tereddüt, Donma ve Erken Çıkış

**Kaynak özeti (`source`):** Yanlılık Grafikte/kararda görülen işaret Koruyucu kayıt Recency Son üç kayıptan sonra sistemi aniden değiştirme. Rolling örneklem, rejim ve kural uyumu ayrı incelenir. Confirmation Kırılan trendline’ı tezi korumak için yeniden çizme.

### 5. PTA-C2-2026 — PDF s. 108

> PROFESYONEL TEKNİK ANALİZ — CİLT 2 108 EK 4 Editoryal Not Bu cildin araştırma sürecinde 66 ayrı kaynak parçası çıkarıldı. Otomatik altyazı/ASR hataları temizlendi; tekrarlar, konuşma dolguları, reklam bölümleri ve konu dışı performans anlatıları çıkarıldı. Teknik terimler standartlaştırıldı; anlamı güvenilir biçimde çıkarılamayan ifadeler tahmin edilerek yeni teknik iddiaya dönüştürülmedi. Kitap metni transkript çevirisi değildir. Kaynakların desteklediği gözlenebilir fiyat davranışları; Türkçe, sade ve eğitim amaçlı bir anlatımla yeniden düzenlenmiştir. Aynı konu birden fazla kaynakta tekrar ediyorsa içerik birleştirilmiş, gereksiz tekrar azaltılmıştır. KAPSAM SINIRI Bu kitap FVG, Order Block, likidite veya belirli bir ekolün terminolojisini merkezine almaz. Odağı; mum dizisi, ilerleme kalitesi, swing geometrisi, ikinci deneme, kırılım, geri çekilme, bağlam ve takip davranışıdır. Görseller hakkında Kitaptaki şematik grafikler gerçek piyasa verisinin birebir ekran görüntüsü değildir. Bir davranış farkını açık biçimde göstermek için sadeleştirilmiş öğretim şemalarıdır. Bu nedenle bir görseldeki mum sayısı veya fiyat oranı mekanik işlem kuralı olarak kullanılmamalıdır. Yayın öncesi son kontrolde bölüm içi terminoloji, görsel etiketler, tablo başlıkları ve sayfa referansları tek biçime getirilmelidir. İçerik değişirse içindekiler sayfa numaraları da yeniden güncellenmelidir.

**Bölüm/alt başlık:** 13 / 13.10 — Son kontrol: karar vermeden önce 10 soru

**Kaynak özeti (`source`):** EK 4 Editoryal Not Bu cildin araştırma sürecinde 66 ayrı kaynak parçası çıkarıldı. Otomatik altyazı/ASR hataları temizlendi; tekrarlar, konuşma dolguları, reklam bölümleri ve konu dışı performans anlatıları çıkarıldı. Teknik terimler standartlaştırıldı; anlamı güvenilir biçimde çıkarılamayan ifadeler tahmin edilerek yeni teknik iddiaya dönüştürülmedi.

## Test fikri (`hypothesis`)

Bu konuya ait kaynak varyantları korunur. İlk aşamada sabit eşik seçilmez; geniş sembol evreninde aynı tanımların amaçladığı davranışa katkısı karşılaştırılır.
