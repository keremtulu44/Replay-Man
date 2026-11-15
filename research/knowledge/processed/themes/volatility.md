# volatility

**Kapsam:** 146 sayfa eşleşmesi

## Proje yorumu (`inference`)

Volatilite yön söylemez; normalizasyon, rejim, sıkışma/genişleme ve risk ölçeği olarak kullanılabilir.

## Nasıl kullanılabilir?

Risk normalizasyonu ve volatilite rejimi

## Kaynak şeritleri

### 1. PTA-C1-2026 — PDF s. 41

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 41 DOĞRU ÇEVİRİ Düşük ATR = sakin piyasa. Donchian/fiyat yapısı kırılımı = yönlü giriş işareti. İlki yön vermez; ikincisi kırılımı gösterir. 6.8 — ATR’yi tek sayı yerine fiyat hareketliliği rejimi olarak okumak Piyasanın hareket genişliği zaman içinde sabit değildir. Düşük fiyat hareketliliği dönemlerini genişleme, yüksek hareketlilik ve yeniden sakinleşme dönemleri izleyebilir. ATR bu değişimin yönünü değil, hareket genişliğinin hangi evrede olduğunu izlemeye yardım eder. ATR uzun süre düşüyorsa fiyatın tipik hareket genişliği daralıyor; daha sonra yükselmeye başlıyorsa hareket genişliği yeniden büyüyor olabilir. Bu süreç yukarı veya aşağı yönde gerçekleşebilir. Dolayısıyla fiyat hareketliliği rejimi ile fiyat yönü ayrı tutulmalıdır. Güncel ATR ayrıca enstrümanın kendi geçmiş ATR değerleriyle karşılaştırılabilir. Tarihsel olarak sıra dışı derecede düşük ATR, piyasanın kendi yakın geçmişine göre sıkıştığını gösterir; hangi yönde kırılacağını söylemez. 6.9 — Hareketi ATR birimiyle ifade etmek Aynı yüzde hareket iki farklı enstrümanda aynı büyüklükte davranış anlamına gelmeyebilir. Bunun yerine güncel hareket, enstrümanın kendi ATR’sine bölünerek “normal” hareket genişliğine göre ifade edilebilir: Hareket büyüklüğü / ATR Örneğin 0,5 ATR’lik bir hareket son dönem tipik genişliğin yaklaşık yarısı, 2 ATR’lik bir hareket ise tipik genişliğin yaklaşık iki katıdır. Bu oran yön veya dönüş söylemez; yalnız hareketin enstrümanın kendi son dönem davranışına göre sıradan mı, olağan dışı mı olduğunu gösterir. …

**Bölüm/alt başlık:** 6 / 6.10 — ATR penceresi ve zaman dilimi “normal” tanımını değiştirir

**Kaynak özeti (`source`):** DOĞRU ÇEVİRİ Düşük ATR = sakin piyasa. Donchian/fiyat yapısı kırılımı = yönlü giriş işareti. İlki yön vermez; ikincisi kırılımı gösterir.

### 2. PTA-C1-2026 — PDF s. 38

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 38 SAYISAL ÖRNEK Önceki kapanış 100, en yüksek 108, en düşük 104. En yüksek−en düşük=4; |108−100|=8; |104−100|=4. True Range = 8. Yalnız mum boyuna bakılsaydı hareketin yarısı görünmezdi. 6.2 — ATR’deki ortalama ne yapar? ATR tek bir barın True Range değerini değil, True Range serisinin dönemsel ve yumuşatılmış ölçümünü izler. Böylece tek bar şokunun etkisi azalırken kalıcı genişleme veya daralma daha görünür olur. TEKNİK AYRINTI ATR’yi yalnız basit aritmetik ortalama gibi düşünmeyin. True Range serisi zaman içinde yumuşatılır; platformdaki yumuşatma yöntemi ayara göre değişebilir. 6.3 — ATR yükseliyor: ne söyleyebilir, ne söyleyemez? Gözlem Söylenebilir Söylenemez ATR yükseliyor Son dönem gerçek hareket genişliği artıyor “Yükseliş yönlü.” ATR düşüyor Hareket genişliği daralıyor “Fiyat kesin yatay kalacak.” ATR çok yüksek Fiyat hareketliliği yüksek/geniş “Tepe oluştu.” ATR çok düşük Fiyat hareketliliği düşük/dar “Kırılım kesin geliyor.” KRİTİK TEKNİK SORUN — ATR ≠ PARA AKIŞI ATR artışını “piyasaya para/spekülasyon geri geliyor” diye yorumlamak desteklenmeyen bir nedenselliktir. ATR’nin formülünde sermaye girişi, alıcı-satıcı agresyonu veya hacim yoktur; yalnız fiyat hareket genişliği vardır. 6.4 — Ham ATR neden iki farklı varlık arasında doğrudan karşılaştırılmaz? ATR fiyat birimiyle ölçüldüğü için varlığın fiyat seviyesine bağlıdır. 20 TL’lik ve 200 TL’lik iki varlıkta 1 TL ATR aynı göreli hareketi ifade etmez. Varlıklar arası karşılaştırmada ATR yüzdesi gibi göreli ölçüler daha anlamlıdır.

**Bölüm/alt başlık:** 6 / 6.4 — Ham ATR neden iki farklı varlık arasında doğrudan karşılaştırılmaz?

**Kaynak özeti (`source`):** SAYISAL ÖRNEK Önceki kapanış 100, en yüksek 108, en düşük 104. En yüksek−en düşük=4; |108−100|=8; |104−100|=4. Yalnız mum boyuna bakılsaydı hareketin yarısı görünmezdi.

### 3. ATK-TR-D1.0-2026-08 — PDF s. 159

> ANA TRADING KİTABI | BÖLÜM 8 İndikatörler: Momentum, Trend, Volatilite ve Ortalama Değer • 144 8.11 ATR: Yönsüz Volatilite ve Risk Ölçeği Average True Range, seçilen periyottaki true range değerlerini yumuşatarak piyasanın tipik hareket genişliğini ölçer. True range; barın high–low aralığı ile önceki kapanışa göre oluşan gap etkisini birlikte dikkate alır. Standart length çoğunlukla 14, smoothing ise RMA’dır. Şekil 8.6 – Yükselişte de düşüşte de ATR artabilir ATR durumu Ne söyler? Ne söylemez? ATR yükseliyor Bar aralıkları veya gap etkisi genişliyor. Yönün bullish olduğunu. ATR düşüyor Piyasa sakinleşiyor veya sıkışıyor. Yakında mutlaka breakout olacağını. Fiyat hareketi 2 ATR Yakın ortalamaya göre olağan dışı geniş hareket. Hareketin devam edeceğini. ATR tabanlı stop Volatiliteye göre ölçeklenen mesafe. Tek başına doğru stop konumunu. ATR tabanlı trailing Trend ilerledikçe oynaklığa uyarlanan takip. Range’de whipsaw riskini ortadan kaldırmayı. Tablo 8.11 – ATR’nin doğru ve yanlış anlamları ATR ile risk arasında köprü ATR, sabit yüzde stop yerine enstrümanın hareket genişliğini hesaba katmaya yardım eder. Ancak stop, yalnız ATR katı olarak seçilmez; geçersizlik seviyesi ve piyasa yapısı önce gelir. ATR, bu yapısal stop’un normal oynaklık içinde gereksiz yere dar kalıp kalmadığını kontrol eden ölçek olabilir. Ayrıntılı pozisyon büyüklüğü ve trailing stop Bölüm 13 ve 23’te ele alınacaktır.

**Bölüm/alt başlık:** 8 / 8.11 — ATR: Yönsüz Volatilite ve Risk Ölçeği

**Kaynak özeti (`source`):** 8.11 ATR: Yönsüz Volatilite ve Risk Ölçeği Average True Range, seçilen periyottaki true range değerlerini yumuşatarak piyasanın tipik hareket genişliğini ölçer. True range; barın high–low aralığı ile önceki kapanışa göre oluşan gap etkisini birlikte dikkate alır. Standart length çoğunlukla 14, smoothing ise RMA’dır.

### 4. PTA-C1-2026 — PDF s. 42

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 42 6.11 — ATR hangi araçlarla tamamlanır? Kombinasyon Rol dağılımı Değerlendirme ATR + Fiyat yapısı Fiyat hareketliliği/risk + yapısal seviye Çok güçlü ATR + Donchian Fiyat hareketliliği koşulu + kırılım tetiği Çok güçlü ATR + RSI/Stoch Risk/koşul + hareket gücü zamanlama Tamamlayıcı ATR + MACD Fiyat hareketliliği + hareket gücü Tamamlayıcı ATR + Supertrend ATR + ATR-tabanlı trend çizgisi Bağımsız iki teyit değildir ATR + Bollinger İki farklı fiyat hareketliliği ölçümü Görev ayrımı yoksa tekrar BÖLÜM SONUCU ATR yön değil hareket genişliği aracıdır. En doğal rolleri fiyat hareketliliğini ölçmek, yapısal stopa gerektiğinde ek pay bırakmak ve kırılım öncesi sıkışma/genişlemeyi izlemektir. ATR’den para akışı veya kırılım yönü çıkarmayın.

**Bölüm/alt başlık:** 6 / 6.11 — ATR hangi araçlarla tamamlanır?

**Kaynak özeti (`source`):** 6.11 — ATR hangi araçlarla tamamlanır? Kombinasyon Rol dağılımı Değerlendirme ATR + Fiyat yapısı Fiyat hareketliliği/risk + yapısal seviye Çok güçlü ATR + Donchian Fiyat hareketliliği koşulu + kırılım tetiği Çok güçlü ATR + RSI/Stoch Risk/koşul + hareket gücü zamanlama Tamamlayıcı ATR + MACD Fiyat hareketliliği + hareket gücü Tamamlayıcı ATR + Supertrend ATR + ATR-tabanlı trend çizgisi Bağımsız iki teyit değildir ATR + Bollinger İki farklı fiyat hareketliliği ölçümü Görev ayrımı yoksa tekrar BÖLÜM SONUCU ATR yön değil hareket genişliği aracıdır. En doğal rolleri fiyat hareketliliğini ölçmek, yapısal stopa gerektiğinde ek pay bırakmak ve kırılım öncesi sıkışma/genişlemeyi izlemektir.

### 5. PTA-C1-2026 — PDF s. 54

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 54 Özellik Bollinger Bands Donchian Kanalı En iyi tamamlayıcı Fiyat yapısı / Hacim ATR / Fiyat yapısı / Hacim TEKRAR RİSKİ Bollinger + Donchian ancak görevleri ayrılırsa anlamlıdır: Bollinger bant yapısını, Donchian ise kırılım sınırını gösterir. Aksi halde iki kanal yalnız grafiği kalabalıklaştırır. 8.8 — Kırılım sistemi için pratik akış Adım Soru Araç örneği 1. Koşul Fiyat hareketliliği dar mı / genişliyor mu? ATR veya Bollinger 2. Sınır Kırılım seviyesi nerede? Donchian / yapı 3. Giriş işareti N-periyot zirvesi/dibi gerçekten kırıldı mı? Donchian 4. Katılım Hareket destekleniyor mu? Hacim 5. Risk İşlem fikri nerede bozulur ve stop nerede olmalı? Yapı + ATR 6. Yönetim Trend nasıl taşınacak? Donchian orta bant / takip eden stop BÖLÜM SONUCU Donchian Kanalı son N-periyot fiyat sınırlarını gösterir. En doğal rolleri kırılım tetiği ve trend takibidir. ATR ile birlikte kullanıldığında biri yönlü sınırı, diğeri yönsüz fiyat hareketliliği koşulunu ölçer. ARA ÖZET — ATR, Bollinger ve Donchian aynı şey değildir Araç Ana soru Matematik sınıfı Yanlış eşitleme ATR Ne kadar hareket ediyor? True Range / fiyat hareketliliği “Yön gösterir.” Bollinger Dağılım ne kadar geniş/dar? Ortalama + standart sapma “Bant = dönüş.”

**Bölüm/alt başlık:** 8 / 8.8 — Kırılım sistemi için pratik akış

**Kaynak özeti (`source`):** Özellik Bollinger Bands Donchian Kanalı En iyi tamamlayıcı Fiyat yapısı / Hacim ATR / Fiyat yapısı / Hacim TEKRAR RİSKİ Bollinger + Donchian ancak görevleri ayrılırsa anlamlıdır: Bollinger bant yapısını, Donchian ise kırılım sınırını gösterir. Aksi halde iki kanal yalnız grafiği kalabalıklaştırır. 8.8 — Kırılım sistemi için pratik akış Adım Soru Araç örneği 1.

### 6. ATK-TR-D1.0-2026-08 — PDF s. 481

> ANA TRADING KİTABI | BÖLÜM 23 Pozisyon Yönetimi, Kâr Alma ve Çıkış Stratejileri • 466 23.7 Sabit Yüzde ve Sabit Tutar Trailing Fixed-percentage trailing, fiyatın ulaştığı en avantajlı seviyeden sabit yüzde uzaklıkta stop tutar. Long için kavramsal formül: trail adayı = highest high since activation × (1 − yüzde). Short için lowest low × (1 + yüzde). Fixed-amount yönteminde yüzde yerine fiyat/tutar mesafesi kullanılır. Karar alanı Kontrol Anchor Entry’den mi, aktivasyondan mı, gün içi high/low’dan mı takip? Yüzde/tutar Sembolün ATR’si ve tick value’su ile uyumlu mu? Güncelleme Intrabar mı, bar close sonrası mı? Backtest ile aynı mı? One-way kural Long stop = max(eski stop, yeni aday); short = min(eski stop, yeni aday). Gap/kurumsal olay Overnight taşıma ve haber riski kabul edildi mi? Farklı fiyat ölçekleri Aynı 5% her sembol ve timeframe’de aynı davranışı üretmez. Tablo 23.7 – Sabit trail sözleşmesi VAKA ANALİZİ — 5% NEDEN EVRENSEL DEĞİL? Günlük BTC’de %5 normal dalgalanma içinde kalabilirken düşük volatil bir hissede olağanüstü geniş; 30 dakikalık XAGTRYG trade’inde ise hedef horizon’a göre aşırı geniş olabilir. Mesafe, sembolün ölçülmüş hareketine göre test edilir. 23.8 ATR ve Volatilite Tabanlı Trailing ATR-based trailing (stop mesafesini Average True Range’in belirli katıyla uyarlama), volatilite genişlediğinde daha fazla nefes; daraldığında daha yakın koruma sağlayabilir. Long için yaygın kavramsal aday: highest high since activation − k × ATR. Short için lowest low + k × ATR. …

**Bölüm/alt başlık:** 23 / 23.8 — ATR ve Volatilite Tabanlı Trailing

**Kaynak özeti (`source`):** 23.7 Sabit Yüzde ve Sabit Tutar Trailing Fixed-percentage trailing, fiyatın ulaştığı en avantajlı seviyeden sabit yüzde uzaklıkta stop tutar. Long için kavramsal formül: trail adayı = highest high since activation × (1 − yüzde). Short için lowest low × (1 + yüzde).

### 7. ATK-TR-D1.0-2026-08 — PDF s. 164

> ANA TRADING KİTABI | BÖLÜM 8 İndikatörler: Momentum, Trend, Volatilite ve Ortalama Değer • 149 Hızlı Başvuru Araç Neyi ölçer? En büyük hata SMA / EMA / WMA / HMA / RMA Fiyatın farklı ağırlık ve hızla yumuşatılmış ortalaması. Çoklu MA’yı bağımsız teyit saymak. MACD İki EMA farkı üzerinden trend– momentum değişimi. Her signal cross’u giriş yapmak. RSI Yakın yükseliş–düşüş momentumunu 0–100 arasında normalize eder. 70 sell, 30 buy kuralı. Stochastic RSI RSI’nın kendi yakın aralığındaki konumu. Hassas crossover’ları filtresiz kullanmak. CCI Fiyatın dönem ortalamasından sapması. ±100’ü kesin dönüş sınırı saymak. Bollinger Bands Ortalama çevresindeki standart sapma ve volatilite. Band touch’ı otomatik ters sinyal yapmak. ATR True range’in yumuşatılmış, yönsüz hareket genişliği. ATR yükselişini bullish sanmak. Ichimoku Denge çizgileri ve ileri kaydırılmış trend bulutu. Bulutu geleceği gören araç saymak. Parabolic SAR Trend takip noktaları ve mekanik trailing referansı. Range’de sürekli flip kovalamak. VWAP / OBV Hacim ağırlıklı ortalama ve kümülatif hacim teyidi. Bölüm 7’deki veri sınırlarını unutmak. VIX / Korelasyon Dış duyarlılık ve iki seri arasındaki rolling ilişki. Sabit eşik ve kalıcı hedge varsaymak. …

**Bölüm/alt başlık:** 8 / 8.15 — İndikatör Seçme ve Birleştirme İş Akışı

**Kaynak özeti (`source`):** En büyük hata SMA / EMA / WMA / HMA / RMA Fiyatın farklı ağırlık ve hızla yumuşatılmış ortalaması. MACD İki EMA farkı üzerinden trend– momentum değişimi. RSI Yakın yükseliş–düşüş momentumunu 0–100 arasında normalize eder.

### 8. ATK-TR-D1.0-2026-08 — PDF s. 166

> ANA TRADING KİTABI | BÖLÜM 8 İndikatörler: Momentum, Trend, Volatilite ve Ortalama Değer • 151 Terim Kısa tanım Squeeze Bollinger bant genişliğinin daralması. ATR True range’in ortalaması; yönsüz volatilite ölçümü. Ichimoku / Kumo Denge çizgileri ve ileri kaydırılmış bulut içeren trend sistemi. Parabolic SAR Trend takip ve stop-and-reverse noktaları. VIX ABD hisse piyasası oynaklık/korku beklentisi için kullanılan gösterge. Correlation Coefficient İki seri arasındaki rolling doğrusal ilişkiyi −1 ile +1 arasında özetleyen ölçüm. Tablo 8.17 – Bölüm 8 temel sözlüğü Bölüm Sonu Kontrol Soruları 1. İndikatör neden fiyatın yerine geçemez? 2. Leading ve lagging ayrımı hangi yanlış beklentiyi doğurabilir? 3. Kısa ve uzun periyot ayarlarının temel ödünleşimi nedir? 4. SMA, EMA ve WMA arasındaki ağırlık farkı nedir? 5. HMA’nın hızlı tepki avantajı hangi riski artırır? 6. Hareketli ortalama crossover neden gecikmelidir? 7. MACD çizgisi ve signal çizgisi nasıl hesaplanır? 8. Histogramın küçülmesi neden otomatik trend dönüşü değildir? 9. RSI 70 üstünde neden doğrudan satış sinyali değildir? 10. RSI 50 çizgisi trend rejiminde nasıl kullanılabilir? 11. Regular ve hidden divergence arasındaki fark nedir? 12. Divergence hangi fiyat olayıyla teyit edilmelidir? 13. Stochastic RSI neden normal RSI’dan daha fazla sinyal üretir? 14. CCI neden “unbounded” olarak adlandırılır? 15. Bollinger squeeze neyi gösterir, neyi göstermez? 16. Band walk ile aşırı sapma nasıl ayrılır? 17. ATR neden yönsüzdür ve true range neden gap’i dikkate alır? 18. …

**Bölüm/alt başlık:** 8 / 8.15 — İndikatör Seçme ve Birleştirme İş Akışı

**Kaynak özeti (`source`):** Terim Kısa tanım Squeeze Bollinger bant genişliğinin daralması. ATR True range’in ortalaması; yönsüz volatilite ölçümü. Ichimoku / Kumo Denge çizgileri ve ileri kaydırılmış bulut içeren trend sistemi.

### 9. PTA-C2-2026 — PDF s. 43

> PROFESYONEL TEKNİK ANALİZ — CİLT 2 43 Aşama Fiyat ne yapıyor? Okuma 1. İlk genişleme Dar alanın dışına çıkmayı deniyor. Yeni alan kazanma girişimi 2. Başarısızlık / geri dönüş İlk hareket sürdürülemiyor. İlk genişleme yeterli değil 3. Yeniden sıkışma Fiyat tekrar dar bir alana giriyor. Piyasa yeniden dengeleniyor 4. İkinci deneme Dar alandan yeniden çıkış aranıyor. Yeni genişleme girişimi 6.8 — Alt sınırı kısa süre aşmak, geri almak ve karşı tarafa genişlemek Sıkışma her zaman temiz bir şekilde üst veya alt sınırdan çıkmaz. Kaynakta dar fiyat aralığının alt sınırı kısa süre aşılır; ardından fiyat yeniden aralığın içine döner ve daha sonra üst taraftan genişler. Bu sıra, tek adımlı bir kırılım yerine üç parçalı bir davranış gösterir: alt sınırı aşma (undercut), aralığı geri alma (reclaim) ve karşı yönde genişleme. Bu örneğin değeri “altı süpürdü, o halde kesin yukarı gider” gibi bir kural üretmesi değildir. Asıl bilgi, ilk aşağı denemenin dar alanın altında kalıcı hareket üretememesi ve fiyatın tekrar fiyat aralığının içine dönmesidir. Ardından üst taraftaki genişleme yeni bir aşamadır. Bir sonraki bölümde, bu tür sınır aşımlarında fitille geçmek ile dışarıda kapanmak arasındaki farkı daha ayrıntılı inceleyeceğiz. Şekil 6.7 — Fiyat dar alanın alt sınırını kısa süre aşıyor, yeniden aralığın içine dönüyor ve daha sonra karşı tarafa doğru genişliyor. Bu, tek adımlı değil çok aşamalı bir çözülmedir. BÖLÜM 7’YE KÖPRÜ Bu bölümde sıkışmanın nasıl çözüldüğünü gördük. Ancak “sınır aşıldı” ile “fiyat o sınırın dışında kabul gördü” aynı şey değildir. …

**Bölüm/alt başlık:** 6 / 6.8 — Alt sınırı kısa süre aşmak, geri almak ve karşı tarafa genişlemek

**Kaynak özeti (`source`):** İlk genişleme Dar alanın dışına çıkmayı deniyor. Başarısızlık / geri dönüş İlk hareket sürdürülemiyor. Yeniden sıkışma Fiyat tekrar dar bir alana giriyor.

### 10. PTA-C2-2026 — PDF s. 40

> PROFESYONEL TEKNİK ANALİZ — CİLT 2 40 6.5 — Aynı sıkışma neden her yerde aynı anlamı taşımaz? Çift iç mum veya yoğun sıkışma tek başına bağlamdan bağımsız bir mesaj değildir. Kaynağa göre aynı double inside bar önemli bir teknik bölge yakınında duygu değişimine eşlik edebilir; belirgin bir engelden uzakta, mevcut trend içindeki kısa bir duraklama olarak da kalabilir. Bu yüzden şekli gördükten sonra ikinci soru mutlaka “nerede oluştu?” olmalıdır. Bu ayrım kitabın ana yaklaşımıyla uyumludur: önce davranış, sonra yerleşim. Sıkışma bir üst sınırın hemen altında oluşuyorsa alıcıların o sınırı genişletip genişletemediği izlenir. Trendin ortasında oluşuyorsa, ana yönün kısa duraklamadan sonra yeniden genişleyip genişlemediği daha anlamlı hale gelir. Aynı mum dizisi, farklı yerde farklı bir hikâyenin parçası olabilir. Şekil 6.4 — Aynı sıkışma yapısı önemli bir üst bölge yakınında ve trend içindeki kısa duraklamada aynı şekilde yorumlanmaz. Şekil aynı, bağlam farklıdır. Sıkışmanın yeri Öne çıkan soru Tek başına yapılmaması gereken çıkarım Önemli sınır yakınında Mevcut taraf bu sınırı artık genişletebiliyor mu? “Sıkışma varsa kesin dönüş.” Trend içinde Kısa duraklama sonrası ana yön yeniden alan kazanıyor mu? “Her inside bar dönüş işaretidir.” Belirsiz orta bölge Sıkışmadan hangi tarafa anlamlı genişleme geliyor? Yönü önceden tahmin etmek 6.6 — Küçük mum kümesinden genişlemeye geçiş Kaynaklardan biri sıkışmayı birkaç küçük gövdeli mumun ardından gelen büyük yönlü mumla açıklar. Küçük mumlar geçici dengeyi ve sınırlı ilerlemeyi, büyük mum ise bu dengeden çıkışı temsil eder. …

**Bölüm/alt başlık:** 6 / 6.6 — Küçük mum kümesinden genişlemeye geçiş

**Kaynak özeti (`source`):** 6.5 — Aynı sıkışma neden her yerde aynı anlamı taşımaz? Çift iç mum veya yoğun sıkışma tek başına bağlamdan bağımsız bir mesaj değildir. Kaynağa göre aynı double inside bar önemli bir teknik bölge yakınında duygu değişimine eşlik edebilir; belirgin bir engelden uzakta, mevcut trend içindeki kısa bir duraklama olarak da kalabilir.

## Test fikri (`hypothesis`)

Bu konuya ait kaynak varyantları korunur. İlk aşamada sabit eşik seçilmez; geniş sembol evreninde aynı tanımların amaçladığı davranışa katkısı karşılaştırılır.
