# liquidity_imbalance

**Kapsam:** 102 sayfa eşleşmesi

## Proje yorumu (`inference`)

Likidite, OB ve FVG tek başına sonuç değil; konum, olay yaşam döngüsü ve geçersizlik taşıyan modüller olarak ele alınmalıdır.

## Nasıl kullanılabilir?

Kullanıcının OB/FVG sistemi için kaynak ve olay bağlantısı

## Kaynak şeritleri

### 1. ATK-TR-D1.0-2026-08 — PDF s. 109

> ANA TRADING KİTABI | BÖLÜM 5 Likidite, FVG ve Fiyat Boşlukları • 94 Terim Tanım External liquidity Seçilen ana yapının dışındaki major ekstrem çevresindeki likidite adayı. FVG Üç mumda birinci ve üçüncü mum wick aralıklarının örtüşmediği fiyat alanı. Gap fill Fiyatın klasik gap veya işaretli dengesizlik alanına geri dönerek alanı işlemesi. Inducement Ana alan öncesinde erken işlemleri ve stopları çekebilecek minor bait seviyesi. Internal liquidity Ana yapının içinde kalan minor swing çevresindeki likidite adayı. Liquidity grab Seviyenin hızlı, çoğunlukla fitilli aşımı ve derhal geri alınması. Liquidity pool Belirgin fiyat alanında stop/trigger emirlerinin kümelenme ihtimali. Liquidity run Likidite seviyesi aşıldıktan sonra yeni alanda kabul ve devam oluşması. Liquidity sweep Seviye ötesindeki emirler tetiklendikten sonra fiyatın eski yapıya dönmesi; grab’a göre daha geniş süreç olabilir. Liquidity void Fiyatın az overlap ve güçlü momentumla hızlı geçtiği ince alan. SSL Belirgin diplerin altında tetiklenmesi beklenen satış yönlü emir kümeleri. Tablo 5.18 – Bölüm 5 temel sözlüğü Bölüm Sonu Kontrol Soruları 1. Piyasa likiditesi ile grafikteki likidite adayı arasındaki fark nedir? 2. Limit, market ve stop emirleri likiditeyi nasıl farklı biçimde etkiler? 3. Bir tepenin üzerindeki BSL tetiklendiğinde ilk emir akışı neden alış yönlüdür? 4. BSL tetiklenmesi neden fiyatın yükselmeye devam edeceğini garanti etmez? 5. Major swing ile minor iç pivotun likidite ağırlığı nasıl ayrılır? 6. Equal highs/lows neden stop kümelenmesi adayıdır? 7. …

**Bölüm/alt başlık:** 5 / 5.15 — Gap–FVG Ayrımı ve Okuma İş Akışı

**Kaynak özeti (`source`):** ANA TRADING KİTABI | BÖLÜM 5 Likidite, FVG ve Fiyat Boşlukları • 94 Terim Tanım External liquidity Seçilen ana yapının dışındaki major ekstrem çevresindeki likidite adayı. FVG Üç mumda birinci ve üçüncü mum wick aralıklarının örtüşmediği fiyat alanı. Gap fill Fiyatın klasik gap veya işaretli dengesizlik alanına geri dönerek alanı işlemesi.

### 2. ATK-TR-D1.0-2026-08 — PDF s. 107

> ANA TRADING KİTABI | BÖLÜM 5 Likidite, FVG ve Fiyat Boşlukları • 92 Özellik Klasik gap FVG Liquidity void Grafik boşluğu İki bar/seans arasında gerçek işlem boşluğu. Üç mum içinde Candle 1–3 wick’leri örtüşmez; Candle 2 alanı geçmiştir. Tam boşluk gerekmez; hızlı, az overlap’li geçiş. Sık görüldüğü piyasa Seanslı hisseler ve futures. Bütün mum grafiklerinde oluşabilir. Bütün piyasalarda güçlü impuls içinde. Ana sınıflandırma Common, breakaway, runaway, exhaustion. Bullish/bearish ve yaşam döngüsü. İnce/hızlı fiyat koridoru. Fill yorumu Gap türüne göre fill hızı değişir. Kısmi/tam dolum olabilir; garanti değildir. Yeniden girişte hızlı geçiş olabilir; garanti değildir. Tablo 5.15 – Klasik gap, FVG ve liquidity void ayrımı On adımlı likidite ve boşluk iş akışı Adım Görev Çıktı 1 Ana yapıyı seç Trend, range veya transition; major timeframe. 2 En yakın önemli bölgeleri işaretle Bölüm 4’ten support/resistance veya supply–demand. 3 Görünür likidite adaylarını bul Major high/low, equal high/low, range sınırı, trendline. 4 External/internal etiketi koy Ana hedef mi, iç pullback seviyesi mi? 5 Fiyat yaklaşımını izle Momentum artıyor mu, hugging/sıkışma mı var? 6 Aşımı sınıflandır Fitil, gövde, kapanış ve seviye ötesi mesafe. 7 Takibi bekle Grab/sweep ile run ayrımı; acceptance veya rejection. 8 Displacement/FVG kontrol et Yapısal sonuç üreten anlamlı dengesizlik var mı? 9 Gap türünü belirle Gerçek gap ise trend konumu, hacim ve follow-through. …

**Bölüm/alt başlık:** 5 / 5.15 — Gap–FVG Ayrımı ve Okuma İş Akışı

**Kaynak özeti (`source`):** ANA TRADING KİTABI | BÖLÜM 5 Likidite, FVG ve Fiyat Boşlukları • 92 Özellik Klasik gap FVG Liquidity void Grafik boşluğu İki bar/seans arasında gerçek işlem boşluğu. Üç mum içinde Candle 1–3 wick’leri örtüşmez; Candle 2 alanı geçmiştir. Tam boşluk gerekmez; hızlı, az overlap’li geçiş.

### 3. ATK-TR-D1.0-2026-08 — PDF s. 97

> ANA TRADING KİTABI | BÖLÜM 5 Likidite, FVG ve Fiyat Boşlukları • 82 Fiyatın Hızlandığı ve Karar Verdiği Alanlar Grafikte belirgin bir tepenin birkaç tik üzerinde oluşan ani fitil neden sert düşüşe dönüşür? Aynı tepe başka bir gün güçlü gövdeli mumla kırıldığında fiyat neden ilerlemeye devam eder? Bir impulsun ortasında kalan ince fiyat alanı neden bazen retest bölgesi olurken bazen tamamen görmezden gelinir? Bu soruların ortak noktası likidite, emir tetiklenmesi ve fiyatın belirli alanlarda kabul görüp görmemesidir. Fakat likidite geleceği kesin olarak açıklayan gizli bir güç değildir. Trader yalnızca görünür yapıyı, olası emir kümelerini ve fiyatın bu alanlara geldiğinde gerçekten ne yaptığını gözleyebilir. Bu bölümde market order, limit order ve stop emirlerinin likiditeyle ilişkisi kısa biçimde kurulacak; buy-side ve sell-side liquidity adayları haritalanacak; sweep, grab ve run davranışları ayrılacak; ardından displacement, FVG ve klasik fiyat gap’leri tek bir karşılaştırmalı sistem içinde ele alınacaktır. Bu bölümün sonunda Piyasa likiditesi ile grafik likiditesini ayırabilecek, olası BSL/SSL alanlarını belirleyebilecek, likidite aşımını sweep/grab/run olarak sınıflandırabilecek, displacement ve FVG kalitesini değerlendirebilecek ve klasik gap türlerini FVG’den ayırarak koşullu analiz cümlesi kurabileceksiniz. 5.1 Likidite: İki Farklı Anlam Trading dilinde likidite iki bağlantılı fakat farklı anlamda kullanılır. Birinci anlam, bir varlığın önemli fiyat bozulması oluşturmadan ne kadar kolay alınıp satılabildiğidir. …

**Bölüm/alt başlık:** 5 / 5.1 — Likidite: İki Farklı Anlam

**Kaynak özeti (`source`):** ANA TRADING KİTABI | BÖLÜM 5 Likidite, FVG ve Fiyat Boşlukları • 82 Fiyatın Hızlandığı ve Karar Verdiği Alanlar Grafikte belirgin bir tepenin birkaç tik üzerinde oluşan ani fitil neden sert düşüşe dönüşür? Aynı tepe başka bir gün güçlü gövdeli mumla kırıldığında fiyat neden ilerlemeye devam eder? Bir impulsun ortasında kalan ince fiyat alanı neden bazen retest bölgesi olurken bazen tamamen görmezden gelinir?

### 4. ATK-TR-D1.0-2026-08 — PDF s. 106

> ANA TRADING KİTABI | BÖLÜM 5 Likidite, FVG ve Fiyat Boşlukları • 91 İsimden önce fiyat davranışı Bir alanı “order block”, “demand zone” veya “FVG” diye adlandırmak onu çalışır hâle getirmez. Önce güçlü departure, yapısal sonuç, tazelik ve dönüşteki price action değerlendirilmelidir. 5.14 Klasik Fiyat Boşlukları Klasik gap, bir barın işlem aralığı ile sonraki barın işlem aralığı arasında gerçek fiyat boşluğu bulunmasıdır. Seanslı hisse piyasalarında gece, hafta sonu, haber veya kazanç açıklaması sonrasında sık görülür. Kesintisiz kripto spot piyasasında daha nadirdir; ancak seanslı futures grafiklerinde gap oluşabilir. Gap türü Trend konumu Hacim/takip Genel beklenti Common gap Range veya sıradan yatay alan içinde. Genellikle düşük önem, sınırlı takip. Sık ve hızlı dolabilir; güçlü yön sinyali değildir. Breakaway gap Konsolidasyon, pattern veya major S/R kırılımında. Tercihen yüksek hacim ve güçlü devam. Yeni trend/move başlangıcı olabilir; hızlı dolmama ihtimali daha yüksek. Runaway / continuation gap Başlamış trendin orta evresinde. Trend yönünde momentum ve takip. Mevcut move’un hızlandığını gösterebilir; retest/fill olsa da trend sürebilir. Exhaustion gap Uzamış trendin sonlarına yakın. Görece zayıf follow-through, bazen düşen hacim ve reversal price action. Momentumun tükendiği yerel tepe/dip adayı; teyit gerekir. Tablo 5.14 – Dört klasik gap türü Gap türü ilk anda kesin bilinmeyebilir Açılışta görülen büyük gap’in breakaway mi exhaustion mı olduğu yalnız konum ve sonraki davranışla anlaşılır. …

**Bölüm/alt başlık:** 5 / 5.15 — Gap–FVG Ayrımı ve Okuma İş Akışı

**Kaynak özeti (`source`):** ANA TRADING KİTABI | BÖLÜM 5 Likidite, FVG ve Fiyat Boşlukları • 91 İsimden önce fiyat davranışı Bir alanı “order block”, “demand zone” veya “FVG” diye adlandırmak onu çalışır hâle getirmez. Önce güçlü departure, yapısal sonuç, tazelik ve dönüşteki price action değerlendirilmelidir. 5.14 Klasik Fiyat Boşlukları Klasik gap, bir barın işlem aralığı ile sonraki barın işlem aralığı arasında gerçek fiyat boşluğu bulunmasıdır.

### 5. PTA-C2-2026 — PDF s. 108

> PROFESYONEL TEKNİK ANALİZ — CİLT 2 108 EK 4 Editoryal Not Bu cildin araştırma sürecinde 66 ayrı kaynak parçası çıkarıldı. Otomatik altyazı/ASR hataları temizlendi; tekrarlar, konuşma dolguları, reklam bölümleri ve konu dışı performans anlatıları çıkarıldı. Teknik terimler standartlaştırıldı; anlamı güvenilir biçimde çıkarılamayan ifadeler tahmin edilerek yeni teknik iddiaya dönüştürülmedi. Kitap metni transkript çevirisi değildir. Kaynakların desteklediği gözlenebilir fiyat davranışları; Türkçe, sade ve eğitim amaçlı bir anlatımla yeniden düzenlenmiştir. Aynı konu birden fazla kaynakta tekrar ediyorsa içerik birleştirilmiş, gereksiz tekrar azaltılmıştır. KAPSAM SINIRI Bu kitap FVG, Order Block, likidite veya belirli bir ekolün terminolojisini merkezine almaz. Odağı; mum dizisi, ilerleme kalitesi, swing geometrisi, ikinci deneme, kırılım, geri çekilme, bağlam ve takip davranışıdır. Görseller hakkında Kitaptaki şematik grafikler gerçek piyasa verisinin birebir ekran görüntüsü değildir. Bir davranış farkını açık biçimde göstermek için sadeleştirilmiş öğretim şemalarıdır. Bu nedenle bir görseldeki mum sayısı veya fiyat oranı mekanik işlem kuralı olarak kullanılmamalıdır. Yayın öncesi son kontrolde bölüm içi terminoloji, görsel etiketler, tablo başlıkları ve sayfa referansları tek biçime getirilmelidir. İçerik değişirse içindekiler sayfa numaraları da yeniden güncellenmelidir.

**Bölüm/alt başlık:** 13 / 13.10 — Son kontrol: karar vermeden önce 10 soru

**Kaynak özeti (`source`):** PROFESYONEL TEKNİK ANALİZ — CİLT 2 108 EK 4 Editoryal Not Bu cildin araştırma sürecinde 66 ayrı kaynak parçası çıkarıldı. Otomatik altyazı/ASR hataları temizlendi; tekrarlar, konuşma dolguları, reklam bölümleri ve konu dışı performans anlatıları çıkarıldı. Teknik terimler standartlaştırıldı; anlamı güvenilir biçimde çıkarılamayan ifadeler tahmin edilerek yeni teknik iddiaya dönüştürülmedi.

## Test fikri (`hypothesis`)

Bu konuya ait kaynak varyantları korunur. İlk aşamada sabit eşik seçilmez; geniş sembol evreninde aynı tanımların amaçladığı davranışa katkısı karşılaştırılır.
