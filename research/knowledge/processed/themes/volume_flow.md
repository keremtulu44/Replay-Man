# volume_flow

**Kapsam:** 147 sayfa eşleşmesi

## Proje yorumu (`inference`)

Hacim fiyat davranışının yerine değil, göreceli katılım katmanı olarak ve kendi periyodu içinde normalize edilerek kullanılmalıdır.

## Nasıl kullanılabilir?

Göreceli katılım ve hacim özellikleri

## Kaynak şeritleri

### 1. ATK-TR-D1.0-2026-08 — PDF s. 134

> ANA TRADING KİTABI | BÖLÜM 7 Hacim, Volume Profile, Order Flow ve Mikro Yapı • 119 Tablo 7.5 – Volume spike’ı fiyat sonucuyla sınıflandırma Exhaustion düşük hacim mi, yüksek hacim mi? İki farklı exhaustion davranışı vardır. Birincisinde trend uzarken katılım giderek azalır; hareket yeni ekstrem üretse bile destek daralır. İkincisinde son bir yüksek hacimli climax oluşur fakat fiyat bu çabaya rağmen ilerleyemez. Bu nedenle yalnız hacim yüksekliği değil, “çaba karşılığında ne kadar fiyat yolu üretildiği” sorulur. 7.6 OBV ve Hacim Divergence On-Balance Volume (OBV), kapanış önceki kapanışın üzerindeyse bar hacmini kümülatif toplama ekler; altındaysa çıkarır; eşitse değeri değişmeden bırakır. Böylece fiyat yönü ile hacmi tek kümülatif çizgide birleştirir. OBV HESAP MANTIĞI Close[t] > Close[t-1] ise OBV[t] = OBV[t-1] + Volume[t]; close düşükse hacim çıkarılır; eşitse OBV değişmez. OBV kullanımı Olumlu okuma Sınır Trend teyidi Fiyat ve OBV birlikte HH/HL veya LH/LL üretir. Aynı hacim, gün içindeki gerçek agresyonu göstermez. Bullish divergence Fiyat lower low, OBV higher low. Dönüş için yapı ve price action gerekir. Bearish divergence Fiyat higher high, OBV lower high. Güçlü trendde divergence uzun süre sürebilir. Breakout teyidi Fiyat sınırı kırarken OBV de kendi sınırını aşar. OBV’nin başlangıç değeri önemsiz; eğim ve swing kıyaslanır. Tablo 7.6 – OBV kullanım alanları ve sınırlamalar VERI DUYARLILIĞI OBV, kullanılan hacim serisi kadar güvenilirdir. Venue-specific kripto hacmi, tick volume veya farklı seans filtreleri OBV çizgisini değiştirebilir. …

**Bölüm/alt başlık:** 7 / 7.7 — VWAP: Hacim Ağırlıklı Ortalama

**Kaynak özeti (`source`):** İki farklı exhaustion davranışı vardır. Birincisinde trend uzarken katılım giderek azalır; hareket yeni ekstrem üretse bile destek daralır. İkincisinde son bir yüksek hacimli climax oluşur fakat fiyat bu çabaya rağmen ilerleyemez.

### 2. ATK-TR-D1.0-2026-08 — PDF s. 142

> ANA TRADING KİTABI | BÖLÜM 7 Hacim, Volume Profile, Order Flow ve Mikro Yapı • 127 Tablo 7.14 – Order-flow davranışlarının çaba–sonuç mantığı Absorption ile exhaustion aynı değildir Absorption’da agresif hacim vardır fakat karşı pasif taraf fiyat ilerlemesini sınırlar. Exhaustion’da ise ekstrem fiyatlara saldıran agresif tarafın aktivitesi azalır veya yeni fiyatlarda işlem devam etmez. İkisi birlikte görülebilir; fakat veri hikâyeleri farklıdır. YAYGIN HATA Negatif delta gördüğünüz her low’u bullish absorption saymak. Absorption için yüksek agresif satışa rağmen aşağı ilerlemenin başarısız olması ve ardından fiyatın bunu doğrulaması gerekir. 7.15 Bütünleşik Hacim ve Mikro Yapı İş Akışı Araçların değeri, aynı sinyali tekrar ettirmelerinde değil farklı soruları yanıtlamalarındadır. Standart volume katılımın zaman içindeki değişimini, profile kabulün fiyat dağılımını, VWAP ağırlıklı ortalamayı, footprint ise mum içindeki gerçekleşen agresyonu gösterir. 11. Önce piyasa ve veri türünü belirle: Merkezi volume mü, tick volume mü, venue-specific veri mi? 12. Ana yapı ve önemli bölgeyi Bölüm 3–4 standardıyla işaretle. 13. Standart hacmi yakın geçmiş ve aynı seans saatiyle karşılaştır. 14. Fiyat ilerlemesi ile hacim çabasının uyumlu olup olmadığını sor. 15. Breakout veya dönüşte close ve follow-through gelmeden hacmi tek başına karar yapma. 16. VWAP kullanıyorsan session veya anchor başlangıcını açıkça tanımla. 17. Volume profile için ölçülen auction/range’i ve row-size ayarını kaydet. 18. POC/HVN/LVN’yi tarihsel kabul haritası olarak kullan; bekleyen likiditeyle karıştırma. 19. …

**Bölüm/alt başlık:** 7 / 7.15 — Bütünleşik Hacim ve Mikro Yapı İş Akışı

**Kaynak özeti (`source`):** Exhaustion’da ise ekstrem fiyatlara saldıran agresif tarafın aktivitesi azalır veya yeni fiyatlarda işlem devam etmez. İkisi birlikte görülebilir; fakat veri hikâyeleri farklıdır. YAYGIN HATA Negatif delta gördüğünüz her low’u bullish absorption saymak.

### 3. ATK-TR-D1.0-2026-08 — PDF s. 129

> ANA TRADING KİTABI | BÖLÜM 7 Hacim, Volume Profile, Order Flow ve Mikro Yapı • 114 Fiyatın Arkasındaki Katılımı Okumak Fiyat grafiği bize hareketin sonucunu gösterir. Hacim ve order-flow araçları ise bu sonucun hangi işlem aktivitesiyle oluştuğunu farklı açılardan inceler. Ancak bütün hacim araçları aynı şeyi ölçmez: standart volume zamana, volume profile fiyata, VWAP hacim ağırlıklı ortalamaya, footprint ise gerçekleşen işlemin bid–ask dağılımına odaklanır. Bu bölümde amaç, ekrana daha fazla gösterge eklemek değildir. Amaç; hangi soruda hangi veri katmanının kullanılacağını, hacmin fiyatı ne zaman desteklediğini, ne zaman çelişki ürettiğini ve mikro yapı verisinin hangi sınırlar içinde yorumlanabileceğini kurmaktır. BU BÖLÜMÜN SONUNDA Standart hacim, OBV, VWAP, volume profile, order book ve footprint verilerini görevlerine göre ayırabilecek; breakout, trend, range ve dönüşlerde hacim davranışını değerlendirecek; POC/value area/HVN/LVN ile bid–ask/delta/imbalance/absorption kavramlarını doğru veri katmanında kullanabileceksiniz. 7.1 Hacim Verisi Ne Ölçer? Hacim, belirli bir zaman aralığında işlem gören miktarı ölçer. Hisse senedinde bu miktar pay adedi, futures piyasasında kontrat adedi, kripto borsasında ilgili işlem çiftinin miktarı olabilir. Spot forex gibi merkezi tek işlem kaydı bulunmayan piyasalarda ise platformlar çoğunlukla tick volume, yani fiyat güncellemesi sayısını kullanır. Piyasa/veri Hacim neyi temsil eder? Ana sınırlama Borsa hissesi İlgili borsada işlem gören pay adedi. Başka venue veya dark-pool işlemleri veri setinde olmayabilir. …

**Bölüm/alt başlık:** 7 / 7.1 — Hacim Verisi Ne Ölçer?

**Kaynak özeti (`source`):** Fiyatın Arkasındaki Katılımı Okumak Fiyat grafiği bize hareketin sonucunu gösterir. Hacim ve order-flow araçları ise bu sonucun hangi işlem aktivitesiyle oluştuğunu farklı açılardan inceler. Ancak bütün hacim araçları aynı şeyi ölçmez: standart volume zamana, volume profile fiyata, VWAP hacim ağırlıklı ortalamaya, footprint ise gerçekleşen işlemin bid–ask dağılımına odaklanır.

### 4. ATK-TR-D1.0-2026-08 — PDF s. 140

> ANA TRADING KİTABI | BÖLÜM 7 Hacim, Volume Profile, Order Flow ve Mikro Yapı • 125 7.12 Delta ve Cumulative Volume Delta Delta, belirli bar veya fiyat seviyesinde ask tarafında gerçekleşen hacim ile bid tarafında gerçekleşen hacim arasındaki farktır. Yaygın convention Delta = Ask Volume − Bid Volume şeklindedir; bazı platformlarda işaret veya sınıflandırma yöntemi farklı olabilir. DELTA FORMÜLÜ Delta = Agresif alış hacmi − agresif satış hacmi. CVD ise seçilen başlangıçtan itibaren deltaların kümülatif toplamıdır. Fiyat–delta ilişkisi İlk yorum Gerekli kontrol Fiyat yükseliyor, delta pozitif Agresif alış fiyat ilerlemesiyle uyumlu. Close, yapı ve sonraki acceptance. Fiyat düşüyor, delta negatif Agresif satış aşağı sonuç üretiyor. Destek/likidite ve follow- through. Fiyat yükseliyor, delta negatif Satış agresyonuna rağmen fiyat yükseliyor; absorption veya pasif alım ihtimali. Veri kalitesi, seviye ve sonraki bullish initiative. Fiyat düşüyor, delta pozitif Alış agresyonuna rağmen fiyat düşüyor; pasif satış/absorption ihtimali. Karşı close ve devam. Fiyat yeni ekstrem, CVD etmiyor Divergence adayı. Tek başına dönüş değil yapı zayıflamasıyla birlikte. Tablo 7.12 – Delta ile fiyat sonucunu birlikte okuma CVD SINIRI CVD “smart money birikimi”ni doğrudan göstermez. Seçilen borsa, session reset, trade classification ve aggregation yöntemi değiştiğinde CVD de değişir. Divergence olasılık filtresidir, kesin dönüş sinyali değildir. …

**Bölüm/alt başlık:** 7 / 7.13 — Footprint Imbalance ve Stacked Imbalance

**Kaynak özeti (`source`):** 7.12 Delta ve Cumulative Volume Delta Delta, belirli bar veya fiyat seviyesinde ask tarafında gerçekleşen hacim ile bid tarafında gerçekleşen hacim arasındaki farktır. Yaygın convention Delta = Ask Volume − Bid Volume şeklindedir; bazı platformlarda işaret veya sınıflandırma yöntemi farklı olabilir. DELTA FORMÜLÜ Delta = Agresif alış hacmi − agresif satış hacmi.

### 5. PTA-C1-2026 — PDF s. 56

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 56 BÖLÜM 9 Hacim (Volume): Katılımı Okumak Hacmi “fiyat yükselecek mi?” göstergesi olarak kullanmayın. Hacim bize fiyat hareketine ne kadar işlem aktivitesinin eşlik ettiğini gösterir. HIZLI ROL — Ana görev: fiyat hareketine ne kadar işlem aktivitesinin eşlik ettiğini görmek. Tek başına yönü, alıcıların mı satıcıların mı üstün olduğunu veya hareketin devam edeceğini söylemez. Ana risk: yüksek hacmi otomatik yükseliş sinyali sanmak. İyi eşleşme: fiyat yapısı veya kırılım aracı. 9.1 — Hacim (Volume) ne ölçer, ne ölçmez? Soru Hacim yardımcı olur mu? Neden? İşlem aktivitesi arttı mı? Evet Doğrudan hacim verisine bakar Hareketin yönü ne? Hayır Aynı yüksek hacim yükselişte de düşüşte de olabilir Alıcılar mı satıcılar mı kesin kazandı? Tek başına hayır Toplam hacim yön/agresyon ayrımı yapmaz Kırılıma katılım var mı? Bağlama göre evet Kırılımdaki aktiviteyi geçmişle kıyaslayabilir Fiyat kesin devam eder mi? Hayır Katılım olasılık bağlamıdır, garanti değil TEKNİK SORUN — HACİM YÖN DEĞİLDİR 10 milyon birim hacim görmek “10 milyon alıcı” demek değildir. Gerçekleşen her işlemde bir alıcı ve bir satıcı vardır. Toplam hacim, işlemlerin ne kadar yoğun olduğunu söyler; yönlü karar için fiyat davranışı ve gerekiyorsa daha ayrıntılı fiyat/işlem verisi gerekir. 9.2 — Göreli Hacim (Relative Volume, RVOL): hacim kendi normaline göre ne kadar sıra dışı? Toplam hacim “ne kadar işlem aktivitesi var?” sorusunu cevaplar. Göreli Hacim (Relative Volume, RVOL) ise güncel hacmi aynı enstrümanın normal hacmiyle karşılaştırır.

**Bölüm/alt başlık:** 9 / 9.2 — Göreli Hacim (Relative Volume, RVOL): hacim kendi normaline göre

**Kaynak özeti (`source`):** BÖLÜM 9 Hacim (Volume): Katılımı Okumak Hacmi “fiyat yükselecek mi?” göstergesi olarak kullanmayın. Hacim bize fiyat hareketine ne kadar işlem aktivitesinin eşlik ettiğini gösterir. HIZLI ROL — Ana görev: fiyat hareketine ne kadar işlem aktivitesinin eşlik ettiğini görmek.

### 6. PTA-C1-2026 — PDF s. 65

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 65 10.9 — VWAP + 50 MA kesişimi neden evrensel kural değildir? VWAP ile 50 günlük hareketli ortalama kesişimini işlem sinyali yapmak, VWAP’ın tanımı değil strateji tercihidir. Test edilmeden evrensel kurala dönüştürülemez. STRATEJİYE ÖZEL ≠ MATEMATİKSEL GERÇEK Geçmişte iyi görünen bir kesişim tek başına istatistiksel avantaj kanıtı değildir. Roller ayrılabilir: MA = trend filtresi, VWAP/AVWAP = hacim ağırlıklı konum. Otomatik kesişim kuralı ayrıca test edilmelidir. 10.10 — VWAP hangi araçlarla birlikte kullanılabilir? Kombinasyon Rol dağılımı Not VWAP/AVWAP + Fiyat yapısı Konum + doğrudan fiyat yapısı Çok güçlü VWAP + RSI/Stoch Konum + hareket gücü Tamamlayıcı VWAP + ATR Konum + fiyat hareketliliği/risk Tamamlayıcı AVWAP + Volume Profile Tek ortalama maliyet eğrisi + fiyat seviyelerine göre hacim dağılımı Farklı sorular VWAP + çoklu MA + VWMA Birçok ortalama fiyat çizgisi Tekrar riski yüksek BÖLÜM SONUCU VWAP, hacmi hesaba katan bir ortalama fiyat ve konum çizgisidir; AVWAP bunu seçtiğiniz bir başlangıçtan itibaren hesaplar. Çizgiyi destek/direnç diye ezberlemek yerine neyi ölçtüğünü ve nereden başladığını bilin. ARA KAVRAM Hacmi Zaman Ekseninden Fiyat Eksenine Taşımak Klasik hacim “ne zaman ne kadar aktivite vardı?” diye sorar. Volume Profile aynı aktiviteyi fiyat

**Bölüm/alt başlık:** 10 / 10.10 — VWAP hangi araçlarla birlikte kullanılabilir?

**Kaynak özeti (`source`):** 10.9 — VWAP + 50 MA kesişimi neden evrensel kural değildir? VWAP ile 50 günlük hareketli ortalama kesişimini işlem sinyali yapmak, VWAP’ın tanımı değil strateji tercihidir. Test edilmeden evrensel kurala dönüştürülemez.

### 7. PTA-C1-2026 — PDF s. 59

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 59 9.6 — Hacim verisinin kendisini kontrol edin “Hacim” verisi her piyasa ve veri sağlayıcısında aynı şeyi temsil etmeyebilir. Önce sembolün hangi hacim verisini sunduğunu doğrulayın; farklı veri akışlarındaki ham hacim sayılarını doğrudan karşılaştırmayın. TEKNİK KONTROL LİSTESİ Hangi borsa/veri akışı? Hacim gerçek işlem adedi, kontrat/adet veya başka bir aktivite göstergesi mi? Zaman dilimi değişince nasıl toplulaştırılıyor? Hacim sinyali kurmadan önce veri tanımını doğrulayın. 9.7 — Hacim ile Volume Profile aynı şey değildir Araç Nasıl gösterir? Ana soru Klasik hacim (Volume) Zaman boyunca barlar “Bu bar/dönemde aktivite ne kadar?” Volume Profile Fiyat seviyeleri boyunca dağılım “Seçili aralıkta hacim hangi fiyatlarda toplandı?” BÖLÜM SONUCU Hacim en doğal olarak katılımı ölçer. Yön veya giriş işaretini fiyat yapısı/kırılım verir; hacim hareketin ne kadar aktiviteyle desteklendiğini gösterir. Yüksek hacmi devam, düşük hacmi başarısızlık garantisine çevirmeyin.

**Bölüm/alt başlık:** 9 / 9.7 — Hacim ile Volume Profile aynı şey değildir

**Kaynak özeti (`source`):** 9.6 — Hacim verisinin kendisini kontrol edin “Hacim” verisi her piyasa ve veri sağlayıcısında aynı şeyi temsil etmeyebilir. Önce sembolün hangi hacim verisini sunduğunu doğrulayın; farklı veri akışlarındaki ham hacim sayılarını doğrudan karşılaştırmayın. TEKNİK KONTROL LİSTESİ Hangi borsa/veri akışı?

### 8. PTA-C1-2026 — PDF s. 60

> PROFESYONEL TEKNİK ANALİZ ARAÇLARI 60 BÖLÜM 10 VWAP ve Anchored VWAP: Hacim Ağırlıklı Ortalama Fiyat VWAP’ı “gerçek fiyat” veya sihirli destek/direnç gibi düşünmeyin. VWAP, daha çok işlem yapılan fiyatlara daha fazla ağırlık vererek hesaplanan bir ortalama fiyat çizgisidir. HIZLI ROL — Ana görev: işlemlerin yoğunluğunu da hesaba katan ortalama fiyatı göstermek. Tek başına “adil değer”, kesin destek/direnç veya yön söylemez. Ana risk: fiyatın mutlaka VWAP’a döneceğini sanmak ve AVWAP başlangıcını sonradan fiyata uydurmak. İyi eşleşme: fiyat yapısı + hareket gücü + ATR. 10.1 — VWAP nasıl hesaplanır? Küçük bir örnek TEMEL FORMÜL VWAP = Σ(Fiyat × Hacim) / Σ(Hacim). Buradaki ana fikir, yüksek hacimli fiyat gözleminin ortalamayı daha fazla çekmesidir. Platformların bar içi fiyat temsilinde ayrıntılar olabilir; burada ağırlıklandırma mantığını öğreniyoruz. Fiyat Hacim Fiyat × Hacim 100 TL 100 10.000 105 TL 900 94.500 Toplam 1.000 104.500 Basitçe iki fiyatın aritmetik ortalaması 102,5 TL’dir. Fakat hacmin %90’ı 105 TL’de gerçekleştiği için VWAP = 104.500 / 1.000 = 104,5 TL olur. Yani VWAP, 105 TL’ye daha fazla ağırlık verir.

**Bölüm/alt başlık:** 10 / 10.1 — VWAP nasıl hesaplanır? Küçük bir örnek

**Kaynak özeti (`source`):** BÖLÜM 10 VWAP ve Anchored VWAP: Hacim Ağırlıklı Ortalama Fiyat VWAP’ı “gerçek fiyat” veya sihirli destek/direnç gibi düşünmeyin. VWAP, daha çok işlem yapılan fiyatlara daha fazla ağırlık vererek hesaplanan bir ortalama fiyat çizgisidir. HIZLI ROL — Ana görev: işlemlerin yoğunluğunu da hesaba katan ortalama fiyatı göstermek.

### 9. PTA-C2-2026 — PDF s. 88

> PROFESYONEL TEKNİK ANALİZ — CİLT 2 88 Şekil 12.2 — Mum boyutu ile hacim dört temel biçimde eşleşebilir. Özellikle küçük mum + yüksek hacim, yüksek aktiviteye rağmen sınırlı fiyat ilerlemesi gösterir; bu durum ancak bağlam ve sonraki davranışla anlam kazanır. Kombinasyon Doğrudan gözlem Yanlış kısa yol Sonraki soru Büyük mum + yüksek hacim Geniş hareket + yüksek katılım “Kesin devam eder” Takip davranışı ve konum hareketi destekliyor mu? Büyük mum + düşük hacim Geniş hareket + düşük aktivite “Hareket sahtedir” Fiyat yapısı ve sonraki mumlar ne yapıyor? Küçük mum + yüksek hacim Yüksek aktivite + az ilerleme “Kesin dönüş / emilim” Hangi taraf ilerleyemedi, sonra yapı değişti mi? Küçük mum + düşük hacim Az hareket + düşük aktivite “Önemsizdir” Sıkışmanın yeri ve sonraki genişleme önemli mi? 12.3 — Fiyat yeni tepe veya dip yaparken hacim azalırsa ne değişir? Kaynak 63 hacmi tek mum üzerinden değil, ardışık swingler arasında karşılaştırır. Fiyat daha yüksek tepeler üretmeye devam ederken hacim adım adım düşüyorsa fiyat hâlâ ilerliyordur fakat bu ilerlemeye eşlik eden katılım zayıflıyordur. Düşüş yönünde de aynı mantık geçerlidir: daha düşük dipler sürerken hacim geriliyorsa satış hareketinin arkasındaki katılım azalıyor olabilir. Bu gözlem “trend birazdan dönecek” anlamına gelmez. Fiyat yeni uç üretmeye devam ettiği sürece yapı hâlâ devam ediyor olabilir. Hacimdeki azalma yalnızca ilerlemenin desteğinin zayıfladığına dair ikinci bir bilgi verir. Dönüş yorumu için önceki bölümlerdeki davranış

**Bölüm/alt başlık:** 12 / 12.3 — Fiyat yeni tepe veya dip yaparken hacim azalırsa ne değişir?

**Kaynak özeti (`source`):** Özellikle küçük mum + yüksek hacim, yüksek aktiviteye rağmen sınırlı fiyat ilerlemesi gösterir; bu durum ancak bağlam ve sonraki davranışla anlam kazanır. Kombinasyon Doğrudan gözlem Yanlış kısa yol Sonraki soru Büyük mum + yüksek hacim Geniş hareket + yüksek katılım “Kesin devam eder” Takip davranışı ve konum hareketi destekliyor mu? Büyük mum + düşük hacim Geniş hareket + düşük aktivite “Hareket sahtedir” Fiyat yapısı ve sonraki mumlar ne yapıyor?

### 10. PTA-C2-2026 — PDF s. 86

> PROFESYONEL TEKNİK ANALİZ — CİLT 2 86 BÖLÜM 12 Hacim ve Çoklu Zaman Dilimi: İkinci Katman Fiyat davranışını önce okuyun. Hacmi ve zaman dilimini, gördüğünüz davranışın gücünü ve bağlamını desteklemek için kullanın. Bu bölüm yeni bir sinyal sistemi kurmuyor. Önceki bölümlerde olduğu gibi ana bilgi hâlâ fiyatın kendisidir: mumların nasıl ilerlediği, nerede zorlandığı, hangi yapıyı kırdığı ve sonraki mumların bu hareketi sürdürüp sürdüremediği. Hacim ve çoklu zaman dilimi bu okumanın üzerine eklenen ikinci katmandır. Hacim, fiyat hareketine ne kadar katılım eşlik ettiğini gösterir. Çoklu zaman dilimi ise aynı fiyat davranışının hangi ölçekte oluştuğunu ayırmamıza yardım eder. İkisini de ana karar mekanizmasının yerine koyarsak kitap boyunca kurduğumuz davranış okuması zayıflar; fiyatı önce, destekleyici katmanı sonra okumak daha tutarlı bir sıradır. BU BÖLÜMÜN ANA FİKRİ Fiyat “ne oldu?” sorusunu cevaplar. Hacim “bu harekete ne kadar katılım eşlik etti?” sorusuna ek bilgi verir. Alt zaman dilimi ise “fiyat bu bölgede gerçekten davranış değiştirdi mi?” sorusunu ayrıntılandırır. 12.1 — Hacim neyi ekler? Kaynak 61 hacmi yön üreten bağımsız bir sinyal gibi değil, fiyat hareketine eşlik eden katılımın ikinci ölçüsü olarak ele alır. Örneğin iki grafikte de benzer büyüklükte bir yükseliş mumu oluşabilir. Birinde hareket yüksek hacimle, diğerinde daha düşük hacimle gerçekleşmişse fiyatın kat ettiği mesafe benzerdir fakat bu harekete eşlik eden kayıtlı aktivite aynı değildir. …

**Bölüm/alt başlık:** 12 / 12.1 — Hacim neyi ekler?

**Kaynak özeti (`source`):** BÖLÜM 12 Hacim ve Çoklu Zaman Dilimi: İkinci Katman Fiyat davranışını önce okuyun. Hacmi ve zaman dilimini, gördüğünüz davranışın gücünü ve bağlamını desteklemek için kullanın. Bu bölüm yeni bir sinyal sistemi kurmuyor.

## Test fikri (`hypothesis`)

Bu konuya ait kaynak varyantları korunur. İlk aşamada sabit eşik seçilmez; geniş sembol evreninde aynı tanımların amaçladığı davranışa katkısı karşılaştırılır.
