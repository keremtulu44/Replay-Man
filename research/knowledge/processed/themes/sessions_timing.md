# sessions_timing

**Kapsam:** 31 sayfa eşleşmesi

## Proje yorumu (`inference`)

Aynı olay farklı seans ve gün içi konumda farklı katılımcı/likidite koşullarına sahip olabilir.

## Nasıl kullanılabilir?

Seans, gün içi zaman ve farklı piyasa saatlerinin olay bağlamı

## Kaynak şeritleri

### 1. ATK-TR-D1.0-2026-08 — PDF s. 470

> ANA TRADING KİTABI | BÖLÜM 22 İşlem Seansları, Likidite ve Gün İçi Zamanlama • 455 22.15 Tam Gün İçi Zamanlama İş Akışı Şekil 22.7 – Tam gün içi zamanlama iş akışı Aşama Eylem Çıktı 1 Takvim Venue tatili/erken kapanış ve ekonomik olayları kontrol et. Normal, özel veya no-trade gün. 2 Saat UTC, yerel offset, DST ve grafik timezone’unu doğrula. Doğru seans çizimi. 3 Bağlam Üst TF yapı, günlük bias ve beklenen gün tipini yaz. Yön/alternatif/no-trade. 4 Seviye Önceki gün/seans high–low, open, range ve VWAP çiz. Likidite rotası. 5 Pencere Stratejiye uygun seans/overlap ve no-trade window seç. Aktif işlem saatleri. 6 Tetik Close, reclaim, retest, displacement ve güncel hedef alanını kontrol et. Emir veya bekleme. 7 Risk Spread, hız, slippage, stop ve kalan süreyi yeniden hesapla. Uygulanabilir boyut. 8 Yönetim Haber/seans geçişi yaklaşınca Bölüm 23 planına göre yönet. Taşı / azalt / çık. 9 Kayıt Seans, haber, maliyet ve sonuç verisini günlüğe yaz. Kişisel zaman edge’i. Tablo 22.15 – Tam uygulama sırası TAM VAKA — LONDRA’DAN NEW YORK’A XAGTRYG  Takvim: ABD verisi ve yerel ürün takvimi kontrol edilir.  Saat: Londra/NY pencereleri güncel UTC ve grafik timezone’unda işaretlenir.  Bağlam: Günlük XAGUSD trendi, USDTRY yönü ve XAGTRYG 4S yapı yazılır.  Seviyeler: Asya high–low, önceki gün high–low ve ilgili session VWAP çizilir.  Londra: Asya high sweep’i sonrası reclaim var; fakat ABD verisi yakınsa tetik bekletilir.  New York: Veri sonrası spread normalleşir, 30D micro BOS + retest oluşur ve hedef alanı hâlâ yeterlidir. …

**Bölüm/alt başlık:** 22 / 22.15 — Tam Gün İçi Zamanlama İş Akışı

**Kaynak özeti (`source`):** 22.15 Tam Gün İçi Zamanlama İş Akışı Şekil 22.7 – Tam gün içi zamanlama iş akışı Aşama Eylem Çıktı 1 Takvim Venue tatili/erken kapanış ve ekonomik olayları kontrol et. 2 Saat UTC, yerel offset, DST ve grafik timezone’unu doğrula. 3 Bağlam Üst TF yapı, günlük bias ve beklenen gün tipini yaz.

### 2. ATK-TR-D1.0-2026-08 — PDF s. 463

> ANA TRADING KİTABI | BÖLÜM 22 İşlem Seansları, Likidite ve Gün İçi Zamanlama • 448 22.6 New York Seansı: Haber, Hisse Açılışı ve Katılım New York penceresi USD pair’leri, ABD hisseleri, endeksler, değerli metaller ve kriptoda önemli bir katılım değişimi yaratabilir. Makro veri, merkez bankası iletişimi veya ABD hisse açılışı aynı pencereye yığıldığında hız, spread ve slippage artabilir. Bu durum fırsat kadar uygulama riski de üretir. Alt pencere Tipik görev Risk NY öncesi makro veri Yeni bilgi fiyatlaması ve önceki seans seviyelerinin testi. Spread genişlemesi, stop gap’i ve ilk yönün geri alınması. Londra–NY overlap İki büyük merkezin eşzamanlı katılımı. Hızlı trend kadar çift yönlü likidite temizliği. ABD hisse açılışı Auction sonrası fiyat keşfi ve volume artışı. Opening noise, gap ve yüksek slippage. Londra kapanışı sonrası Katılım bileşimi değişir; trend sürer veya yavaşlar. Eski momentum varsayımını sürdürmek. NY sonu / settlement Pozisyon ayarlaması ve likidite azalması olabilir. Yeni intraday trade için hedef alanı ve süre azalır. Tablo 22.6 – New York penceresini alt görevlere ayırmak VAKA ANALİZİ — XAGTRYG İKİ BACAKLI ZAMANLAMA XAGTRYG’de gümüş bacağı XAGUSD, kur bacağı USDTRY üzerinden etkilenebilir. New York’ta XAGUSD hızlanırken USDTRY aynı yönde veya ters yönde hareket edebilir. Yalnız “New York’ta gümüş yükseldi” diye XAGTRYG sonucu varsaymam; iki bacağı, feed’i ve işlem ürününün açık olduğu saatleri birlikte kontrol ederim. DOĞRU BİLİNEN YANLIŞ Mit: New York seansı en volatil olduğu için her strateji için en iyi zamandır. …

**Bölüm/alt başlık:** 22 / 22.7 — Overlap ve Seans Geçişleri

**Kaynak özeti (`source`):** 22.6 New York Seansı: Haber, Hisse Açılışı ve Katılım New York penceresi USD pair’leri, ABD hisseleri, endeksler, değerli metaller ve kriptoda önemli bir katılım değişimi yaratabilir. Makro veri, merkez bankası iletişimi veya ABD hisse açılışı aynı pencereye yığıldığında hız, spread ve slippage artabilir. Bu durum fırsat kadar uygulama riski de üretir.

### 3. ATK-TR-D1.0-2026-08 — PDF s. 228

> ANA TRADING KİTABI | BÖLÜM 11 İşlem Stilleri, Piyasa Seçimi ve Uygulama Rutinleri • 213 Şekil 11.5 – Yaklaşık küresel seans pencereleri Pencere Genel davranış eğilimi İzlenebilecek bağlam Uyarı Asya Daha sakin ve range ağırlıklı olabilir. JPY/AUD/NZD, range veya hazırlık. Kriptoda düşük likiditeyle ani hareket. Londra Forex likiditesi ve trend/breakout artabilir. EUR/GBP/CHF ve Avrupa haberleri. Açılışın ilk bölümünde fakeout. Londra–New York örtüşmesi Aktivite ve volatilite zirvesi olabilir. Majör forex, endeks, metal ve haber. Spread/volatilite şoku ve hızlı risk. New York ABD hisseleri, USD ve makro haber. Day trade ve momentum. Veri açıklamaları sırasında normal setup bozulabilir. Seans sonrası Likidite ve hareket azalabilir. Pozisyon yönetimi ve inceleme. Zayıf breakout ve genişleyen spread. Tablo 11.11 – Seans bağlamları EKRANDA NE ARIYORUM? • Piyasanızın gerçek işlem saatini ve yaz/kış saati değişimini doğrulayın. • Setup’ınızın en sık hangi saatlerde oluştuğunu günlüğünüzden çıkarın. • Haber saatlerini seans planının üzerine işaretleyin. • Açılışın ilk dakikalarını ayrı test edin. • Seans dışı düşük likiditede hedef ve stop davranışını ayrıca değerlendirin.

**Bölüm/alt başlık:** 11 / 11.11 — Seans ve Saat Seçimi

**Kaynak özeti (`source`):** Kriptoda düşük likiditeyle ani hareket. Londra Forex likiditesi ve trend/breakout artabilir. Londra–New York örtüşmesi Aktivite ve volatilite zirvesi olabilir.

### 4. ATK-TR-D1.0-2026-08 — PDF s. 468

> ANA TRADING KİTABI | BÖLÜM 22 İşlem Seansları, Likidite ve Gün İçi Zamanlama • 453 Strateji İhtiyaç Seans testi Breakout Yeterli katılım, range dışı close, follow- through. Açılış/overlap ile normal saat performansını karşılaştır. Trend pullback Yönlü kabul, kontrollü pullback, VWAP/yapı uyumu. İlk impulse sonrası retest kalitesini ölç. Mean reversion Dengeli range, başarısız sınır aşımı, uygun maliyet. Yüksek haber hızında sonuç bozuluyor mu? Liquidity sweep Görünür session high–low, hızlı reclaim, hedef rota. Sweep ile gerçek breakout oranını kaydet. Scalping Dar spread, yüksek fill kalitesi, kısa latency. Venue ve saat bazında slippage günlüğü. News momentum Özel olay planı ve yüksek risk toleransı. Normal stratejiden ayrı örneklem. Tablo 22.12 – Strateji–seans eşleştirmesi EYLEM DİLİ Strateji günlüğüne “seans” sütunu eklerim. Aynı setup’ın Asya, Londra, overlap, New York ve düşük katılım pencerelerindeki net R, win rate, MAE/MFE ve slippage sonucunu ayrı ölçerim. 22.13 Forex, Hisse, Kripto ve XAGTRYG Zamanlaması Piyasa Öncelikli zaman sorusu Özel kontrol Forex Pair’in iki para birimi hangi merkezlerde aktif? Rollover, makro veri, DST ve broker spread’i. Hisse / ETF Ana seans mı, pre/after market mi? Opening auction, gap, earnings ve regular VWAP. Kripto Hangi venue ve bölgesel katılım? 24/7 volume, hafta sonu depth, funding ve exchange bakımı. Emtia / XAGUSD Londra/NY katılımı ve makro veri hangi bacağı etkiliyor? Futures/spot feed ve settlement penceresi. …

**Bölüm/alt başlık:** 22 / 22.13 — Forex, Hisse, Kripto ve XAGTRYG

**Kaynak özeti (`source`):** Strateji İhtiyaç Seans testi Breakout Yeterli katılım, range dışı close, follow- through. Açılış/overlap ile normal saat performansını karşılaştır. Trend pullback Yönlü kabul, kontrollü pullback, VWAP/yapı uyumu.

### 5. PTA-C1-2026 — PDF s. 62

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 62 Şekil 10.2 — Eğitim şeması: sıfırlama VWAP yeni dönemlerde yeniden başlar; AVWAP seçilen olay/belirgin dönüş noktasından itibaren kesintisiz hesaplanır. Araç Başlangıç mantığı En doğal rol Seans / periyodik VWAP Tanımlı dönemlerde sıfırlama Seans/periyot içi hacim ağırlıklı konum Anchored VWAP Kullanıcının seçtiği olay/pivot O olaydan sonraki hacim ağırlıklı maliyet referansı SMA / EMA Sabit kayan geriye bakılan dönem penceresi Trend/yumuşatma; hacim ağırlığı yok 10.4 — Seans VWAP ile AVWAP’ın zaman ufku farklıdır Seans VWAP her yeni seansta sıfırlanır ve ağırlıklı olarak mevcut seansın hacim ağırlıklı ortalama fiyatını temsil eder. Anchored VWAP (AVWAP) ise seçilen olay veya başlangıç noktasından itibaren birikmeye devam eder. Bu nedenle soru “hangisi daha iyi?” değildir. Asıl soru, hangi zaman ufkundaki maliyet/konum bilgisinin istendiğidir. Gün içi seans davranışı için Seans VWAP, belirli bir olay veya belirgin fiyat hareketi sonrasındaki daha uzun dönem maliyet yapısı için AVWAP daha uygun bir referans olabilir. 10.5 — AVWAP için iyi başlangıç noktası nedir? AVWAP’ta kritik karar başlangıç noktasıdır. Büyük tepe/dip, önemli kırılım, fiyat boşluğu veya belirgin bir olay kullanılabilir. Bugünkü fiyata iyi otursun diye geçmişte farklı başlangıçlar denemek analizi geçmişe uydurur.

**Bölüm/alt başlık:** 10 / 10.5 — AVWAP için iyi başlangıç noktası nedir?

**Kaynak özeti (`source`):** Araç Başlangıç mantığı En doğal rol Seans / periyodik VWAP Tanımlı dönemlerde sıfırlama Seans/periyot içi hacim ağırlıklı konum Anchored VWAP Kullanıcının seçtiği olay/pivot O olaydan sonraki hacim ağırlıklı maliyet referansı SMA / EMA Sabit kayan geriye bakılan dönem penceresi Trend/yumuşatma; hacim ağırlığı yok 10.4 — Seans VWAP ile AVWAP’ın zaman ufku farklıdır Seans VWAP her yeni seansta sıfırlanır ve ağırlıklı olarak mevcut seansın hacim ağırlıklı ortalama fiyatını temsil eder. Anchored VWAP (AVWAP) ise seçilen olay veya başlangıç noktasından itibaren birikmeye devam eder. Bu nedenle soru “hangisi daha iyi?” değildir.

## Test fikri (`hypothesis`)

Bu konuya ait kaynak varyantları korunur. İlk aşamada sabit eşik seçilmez; geniş sembol evreninde aynı tanımların amaçladığı davranışa katkısı karşılaştırılır.
