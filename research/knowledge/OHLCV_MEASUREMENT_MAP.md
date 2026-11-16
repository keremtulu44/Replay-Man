# Kitap Bilgilerinin OHLCV ile Ölçülebilirlik Haritası

## Amaç ve sınır

Bu belge, üç kitaptan çıkarılan bilgileri iki ana sınıfa ayırır:

1. **Ek veri veya harici sistem gerektirmeden mevcut OHLCV ile ölçülebilenler**
2. **Ölçmek için ek veri, model, etiketleme veya yürütme sistemi gerekenler**

OB ve FVG kaynaklarda korunur fakat kullanıcının mevcut sistemi daha sonra geleceği için bu aşamanın uygulama önceliğine alınmaz.

“Ek işlemsiz” ifadesi burada yeni veri sağlayıcısı, haber, temel veri, emir defteri veya kullanıcı etiketlemesi gerektirmemek anlamındadır. OHLCV'den deterministik türetilen özellikler ek veri sayılmaz.

---

# A. Yalnız OHLCV ile doğrudan ölçülebilenler

## A1. Tek mum geometrisi

Gerekli alanlar: `open, high, low, close`.

Ölçülebilir özellikler:

- Mum yönü: `close-open`
- Toplam aralık: `high-low`
- Gövde büyüklüğü: `abs(close-open)`
- Gövde/aralık oranı
- Üst fitil ve alt fitil uzunluğu
- Fitil/aralık ve fitil/gövde oranları
- Kapanışın mum aralığındaki konumu
- Açılışın mum aralığındaki konumu
- Doji benzerliği
- Güçlü kapanış / zayıf kapanış
- Marubozu benzerliği
- Pin bar/hammer/shooting-star gibi adlandırılmış yapıların parametrik varyantları
- Önceki muma göre dış bar, iç bar ve örtüşme
- Gap: önceki high/low/close'a göre boşluk

Not: Kitap adları tek doğru formül olarak alınmamalı; gövde ve fitil oranları sürekli değişken olarak saklanmalı, adlandırılmış eşikler deney varyantı olmalıdır.

## A2. Çoklu mum dizileri

Gerekli alanlar: Ardışık OHLC barları.

Ölçülebilirler:

- Ardışık yükseliş/düşüş mum sayısı
- Engulfing varyantları
- Harami/inside dizileri
- Morning/evening star benzeri üçlü diziler
- Üç asker/üç karga benzeri devam dizileri
- Ardışık mumların gövde büyüme/küçülme eğilimi
- Fitillerin yönsel yoğunlaşması
- Kapanış sürekliliği
- Barlar arası örtüşme oranı
- Sıkışma → genişleme dizisi
- İlk sinyalden sonraki takip barı
- İlk sinyalden sonra kazanılan alanın korunması

## A3. Volatilite ve aralık

Gerekli alanlar: OHLC; bazı ölçüler yalnız close kullanabilir.

Ölçülebilirler:

- True Range ve ATR
- Rolling range
- Close-to-close gerçekleşen volatilite
- Bar aralığının geçmiş dağılımdaki yüzdelik konumu
- Volatilite genişlemesi/daralması
- Bollinger bant genişliği
- Standart sapma
- Sıkışma süresi
- Dar bar / geniş bar
- Volatilite rejimi
- Gap büyüklüğü
- Seans açılış aralığı

## A4. Trend ve rejim

Gerekli alanlar: OHLC.

Ölçülebilirler:

- Hareketli ortalama eğimi
- Fiyatın ortalamaya göre konumu
- Kısa/uzun ortalama ilişkisi
- Donchian kanal konumu
- Ardışık yüksek dip/yüksek tepe veya düşük tepe/düşük dip
- Rolling regresyon eğimi ve uyumu
- Yönsel verimlilik
- Trendin sürekliliği
- Trend, range ve geçiş rejimi için çoklu özellik skoru
- ADX/DMI
- Supertrend
- Ichimoku'nun fiyat/zaman türevleri

Önemli ayrım: Rejim etiketi yalnız geçmiş ve mevcut bardan üretilmelidir. Gelecekteki barlarla sonradan çizilen “ideal trend” eğitim etiketi canlı/replay sinyali sayılamaz.

## A5. Swing ve piyasa yapısı

Gerekli alanlar: OHLC.

Ölçülebilirler:

- Yerel tepe/dip adayları
- Pivot oluşum zamanı ve teyit zamanı
- Major/minor swing hiyerarşisi
- Swing mesafesi
- Swing süresi
- Swing hızı
- Swing içindeki toplam yol
- Swing verimliliği
- Higher high / higher low / lower high / lower low
- Önceki teyitli swing'in kırılması
- Yapı kırılımı adayları
- İlk kırılma ile kapanış teyidi arasındaki fark
- Yeni uç üretiminin başarısı/başarısızlığı

Lookahead kuralı: Pivotun geometrik olarak ait olduğu eski bar ile pivotun doğrulandığı bar ayrı tutulmalıdır. Replay olayı doğrulama barından önce görünemez.

## A6. Hareket kalitesi ve baskı kaybı

Gerekli alanlar: OHLC.

Ölçülebilirler:

- Net mesafe / toplam yol
- Net mesafe / bar sayısı
- Yönlü gövde toplamı
- Karşı yönlü gövde toplamı
- Örtüşme oranı
- Ortalama kapanış konumu
- Aynı yöndeki bar oranı
- Yeni uçların artış/azalış miktarı
- Gövde büyüklüğünün eğimi
- Hareket ilerledikçe volatilite değişimi
- Aynı mesafe için gereken bar sayısındaki değişim
- İkinci bacağın ilk bacağa göre mesafe, süre ve hız oranı
- Beklenen yeni tepe/dibin üretilememesi
- Baskı devamı, baskı kaybı ve karşı baskı ayrımı

Bu alan kitaplardan çıkan en değerli OHLCV-yerel araştırma ailelerinden biridir; doğrudan “dönüş” etiketi vermeden hareket kalitesini ölçer.

## A7. Destek, direnç ve bölge davranışı

Gerekli alanlar: OHLC.

Ölçülebilirler:

- Teyitli swing tabanlı yatay seviyeler
- Aynı fiyat çevresindeki temas yoğunluğu
- Seviyeye yaklaşma hızı
- Seviyedeki fitil/gövde tepkisi
- Seviyede kalma süresi
- Kırılım öncesi sıkışma
- Seviyenin kapanışla aşılması
- Kırılım sonrası geri test
- Geri testte alanın korunması
- Seviyenin rol değiştirmesi
- Başarılı/başarısız kırılım
- Dinamik ortalama/kanal temasları

Bölge genişliği mutlak fiyatla değil ATR, yüzde veya tick ölçeğiyle normalize edilmelidir.

## A8. Kırılım, kabul ve başarısızlık

Gerekli alanlar: OHLC.

Ölçülebilir olay zinciri:

1. Önceden bilinen seviyeye yaklaşma
2. Fitille dışarı çıkma
3. Dışarıda kapanma
4. Sonraki barlarda takip
5. Yeni alanda kalma süresi
6. Seviyeye geri test
7. Eski alana geri giriş
8. Karşı tarafa genişleme

Bunlardan üretilebilecek durumlar:

- Deneme
- Kapanış kırılımı
- Kabul
- Retest
- Başarılı devam
- Fakeout
- Failure
- Trap adayı

“Likidite alındı” gibi niyet bildiren ifade yerine gözlenebilir fiyat olayları kaydedilmelidir.

## A9. Pullback ve ikinci deneme

Gerekli alanlar: OHLC.

Ölçülebilirler:

- Ana harekete göre geri çekilme derinliği
- Pullback süresi
- Pullback hızı
- Pullback içi örtüşme
- Pullback volatilitesi
- Pullback bar sayısı
- Tek/iki/çok bacaklı geri çekilme
- İlk ve ikinci deneme mesafe oranı
- İlk ve ikinci deneme süre oranı
- Yeni uç üretme başarısı
- Ana hareketin yeniden başlaması için teyit davranışı

Fibonacci oranları aynı OHLC hareketine uygulanabilir; ancak hangi anchorların seçileceği olay anında belirlenebilir olmalıdır.

## A10. Formasyon geometrisi

Gerekli alanlar: OHLC ve önceden tanımlı pivot algoritması.

Ölçülebilir adaylar:

- İkili tepe/dip
- Üçlü tepe/dip
- Omuz-baş-omuz ve ters varyant
- Üçgen
- Kama
- Bayrak/flama
- Kanal
- Rectangle/range
- Cup-and-handle benzeri eğrisel yapı adayları

Formasyon adı doğrudan sonuç olmamalı. Geometrik parçalar ayrıca saklanmalı:

- Tepe/dip sayısı
- Fiyat toleransı
- Süre
- Eğim
- Boyun çizgisi
- Kırılım zamanı
- Hedefe gitmeden önce bilinen bilgiler

## A11. Klasik indikatörler

Gerekli alanlar: OHLCV; bazıları yalnız fiyatla çalışır.

Doğrudan üretilebilir:

- SMA/EMA/WMA ve türevleri
- RSI
- MACD
- Stochastic
- ROC/momentum
- CCI
- Williams %R
- ATR
- Bollinger
- Donchian
- Keltner
- ADX/DMI
- Parabolic SAR
- Supertrend
- Ichimoku
- Pivot point türleri
- OBV
- MFI
- VWAP (intraday veri ve doğru hacimle)

Araştırma kuralı: Aynı bilgi ailesini ölçen indikatörlerin birlikte kullanımı otomatik olarak yeni bilgi üretmez. Her araç rol bazında sınıflanmalıdır: trend, momentum, volatilite, konum, hacim veya tetik.

## A12. Hacim tabanlı ölçüler

Gerekli alanlar: `volume`.

Mevcut veri izin verdiği ölçüde:

- Ham hacim
- Göreceli hacim
- Rolling z-score/yüzdelik
- Fiyat yönü ile hacim ilişkisi
- Hacim genişlemesi/daralması
- OBV
- MFI
- Volume ROC
- VWAP
- Kırılım hacmi
- Pullback hacmi
- Aynı saat dilimine göre hacim anomalisi

Sınırlama: Hacim kalitesi enstrümana göre değişir. Endeks, döviz veya bazı sağlayıcı serilerindeki hacim gerçek merkezi işlem hacmi olmayabilir. Bu nedenle hacim özelliği veri güvenilirlik etiketi taşımalıdır.

## A13. Çoklu zaman dilimi

Gerekli alanlar: Mevcut 1h veriden deterministik 2h/4h üretimi ve mevcut 1g veri.

Ölçülebilirler:

- Üst zaman dilimi trendi
- Alt zaman dilimi tetikleri
- Zaman dilimleri arası yön uyumu
- Üst zaman dilimi seviyesine uzaklık
- Alt zaman diliminde sıkışma/kırılım
- 1h sinyalinin 2h/4h/1g rejimine göre sonucu
- Aynı olayın farklı periyotlarda görünürlüğü

Gelecek sızıntısı önlemi: Tamamlanmamış üst zaman dilimi barı kapanmış bar gibi kullanılamaz.

## A14. Seans ve takvim içi zaman

Gerekli alanlar: Bar zaman damgası. Harici veri gerekmez.

Ölçülebilirler:

- Saat dilimi
- Seansın başından itibaren geçen süre
- Açılışa/kapanışa yakınlık
- Haftanın günü
- Ayın günü
- Ay/çeyrek
- Açılış aralığı
- Gün içi volatilite/hacim profili
- Öğle ve kapanış davranışı
- Gece/hafta sonu gap'i

Resmî tatil, erken kapanış veya özel seans nedenini açıklamak için ayrıca borsa takvimi gerekebilir; fakat gerçekleşmiş barlardan seansın fiilî varlığı ölçülebilir.

## A15. OHLCV tabanlı strateji ve sonuç ölçümü

Yeni veri gerektirmez; olay motoru ve test kodu gerekir.

Ölçülebilirler:

- Sinyal sonrası N-bar getiri
- Maksimum olumlu hareket (MFE)
- Maksimum olumsuz hareket (MAE)
- Hedefe/stopa ilk erişim
- Bar bazlı elde tutma süresi
- İsabet oranı
- Ortalama/medyan getiri
- Beklenen değer
- Getiri dağılımı
- Drawdown
- Rejim bazlı sonuç
- Sembol bazlı tutarlılık
- Zaman dilimi bazlı tutarlılık
- Yaklaşık 70–80 sembolde pozitiflik ve benzerlik

OHLC belirsizliği: Aynı bar içinde hem hedef hem stop görülürse hangisinin önce olduğu bilinmez. Muhafazakâr sonuç, alt zaman dilimine inme veya “belirsiz” etiketi kullanılmalıdır.

---

# B. Mevcut çoklu sembol OHLCV ile ölçülebilenler

Bunlar harici veri istemez; ancak tek sembol yerine depodaki diğer OHLCV serilerinin zaman hizalamasını gerektirir.

## B1. Göreceli güç

- Hisse/endeks getiri farkı
- Oran serisi
- Beta düzeltilmiş getiri
- Sektör/endeks karşısında momentum
- Piyasa düşerken dayanıklılık
- Piyasa yükselirken katılım

## B2. Korelasyon ve ayrışma

- Rolling korelasyon
- Downside/upside korelasyon
- Korelasyon rejimi
- Fiyat ayrışması
- Volatilite ayrışması
- Hacim ayrışması

## B3. Lead-lag araştırması

- Endeks → hisse
- Döviz → endeks/hisse
- Maden/enerji → ilgili hisseler
- Küresel endeks → BIST açılışı
- Varlık grupları arasında gecikmeli korelasyon
- Olay öncesi/sonrası çapraz piyasa tepki süresi

Uyarı: Lead-lag yalnız korelasyondan çıkarılmamalı; saat dilimi, seans çakışması ve veri kapanış zamanı hizalanmalıdır.

## B4. Piyasa genişliği için yaklaşık ölçüler

Mevcut hisse havuzundan üretilebilir:

- Yükselen/düşen sembol oranı
- Hareketli ortalama üstündeki sembol oranı
- Yeni kısa dönem zirve/dip sayısı
- Pozitif momentumlu sembol oranı
- Kesitler arası getiri dağılımı

Tam borsa genişliği için tarihsel üyelik listesi gerekir; mevcut sabit havuzla hesaplanan sonuç “araştırma evreni genişliği” olarak adlandırılmalıdır.

## B5. Portföy korelasyonu ve eşzamanlı sinyal yoğunluğu

- Aynı anda aktif sinyal sayısı
- Sinyal veren sembollerin korelasyonu
- Endeks/sector faktör yoğunluğu
- Tek stratejinin farklı sembollerde aynı olaya bağımlılığı
- Basit eşit ağırlıklı sonuç
- Maksimum eşzamanlı risk için yaklaşık senaryolar

Bu hesaplar OHLCV ile yapılabilir. Gerçek portföy/işlem simülasyonu şimdilik öncelik değildir.

---

# C. OHLCV yeterli, fakat önce ayrı algoritmik sistem kurulması gerekenler

Burada yeni veri gerekmez; fakat güvenilir ve testli bir özellik/olay altyapısı gerekir.

## C1. Teyitli swing motoru

Gerekli sistem:

- Pivot adayları
- Teyit gecikmesi
- Major/minor hiyerarşi
- Eşit tepe/dip toleransı
- Olay zamanı ile geometrik pivot zamanı ayrımı

Bu motor olmadan yapı kırılımı, formasyon ve trend çizgisi ölçümleri tutarlı olmaz.

## C2. Seviye ve bölge motoru

Gerekli sistem:

- Swinglerden seviye üretimi
- ATR/yüzde tabanlı tolerans
- Temas sayımı
- Kırılım ve retest state machine
- Bölge yaşı ve geçerlilik politikası

## C3. Fiyat davranışı özellik motoru

Gerekli sistem:

- Mum geometrisi
- Örtüşme
- Yol verimliliği
- Hareket kalitesi
- Baskı kaybı
- Takip davranışı
- İlk/ikinci deneme karşılaştırması

Bu, kitapların OHLCV'den en doğrudan uygulanabilir çekirdeğidir.

## C4. Rejim motoru

Gerekli sistem:

- Trend/range/geçiş
- Volatilite rejimi
- Hacim rejimi
- Rejim başlangıç/bitiş zamanı
- Parametre değişimine dayanıklılık

Tek bir indikatör rejim hakikati kabul edilmemeli; birkaç özellik ailesi karşılaştırılmalıdır.

## C5. Formasyon aday motoru

Gerekli sistem:

- Teyitli swing dizileri
- Geometri toleransları
- Süre ve simetri ölçüleri
- Kırılım teyidi
- Birden fazla tanım varyantı

## C6. Çoklu zaman dilimi hizalama motoru

Gerekli sistem:

- 1h→2h/4h seans içi resampling
- Yalnız tamamlanmış üst periyot
- 1g ile intraday eşleme
- Saat dilimi ve seans sınırı

Veri üretimi depoda vardır; replay sırasında görünürlük/hizalama kuralı ayrıca uygulanmalıdır.

## C7. Olay ve deney motoru

Gerekli sistem:

- Sürümlü olay tanımı
- Sembol/zaman dilimi evreni
- Girişte mevcut özellik snapshot'ı
- N-bar sonuçları
- MFE/MAE
- Belirsiz intrabar sonucu
- Rejim ve sembol kırılımı
- Eğitim/doğrulama/out-of-sample ayrımı
- Parametre taraması ve çoklu deneme yanlılığı kaydı

## C8. Replay görünürlük motoru

Gerekli sistem:

- Bar bar ilerleme
- Gelecek barın erişilemez olması
- Göstergelerin yalnız mevcut geçmişten hesaplanması
- Pivotların ancak teyit barında görünmesi
- Üst zaman diliminin yalnız kapanınca güncellenmesi
- Sinyal/karar/sonuç zamanlarının ayrı kaydı

## C9. Sonuç ve araştırma günlüğü

Gerekli sistem:

- Deney kimliği
- Strateji sürümü
- Veri sürümü
- Parametre sürümü
- Sembol listesi
- Sonuç tablosu
- Hipotez ve karar notu
- Model değişikliği geçmişi

Bu kayıt harici veri istemez; tekrar üretilebilir araştırma için uygulama altyapısı ister.

---

# D. Ek veri veya ek dış sistem gerektirenler

## D1. Gerçek emir yürütme ve mikro yapı

OHLCV ile tam ölçülemez:

- Bid/ask spread'in gerçek zaman serisi
- Emir defteri derinliği
- Queue position
- Market impact
- Gerçek fill olasılığı
- Tick sırası
- Bar içinde olayların gerçek sırası
- Footprint
- Gerçek bid/ask delta
- Cumulative volume delta

Gerekli ekler:

- Tick/trade verisi
- Quote verisi
- Level 2/order-book verisi
- Yürütme simülatörü

OHLCV ile yalnız muhafazakâr spread/slippage senaryoları yapılabilir; gerçek mikro yapı iddiası yapılamaz.

## D2. Haber ve olay nedeni

OHLCV olayın fiyat etkisini gösterir fakat nedenini söylemez:

- Merkez bankası kararı
- Enflasyon verisi
- Şirket haberi
- Bilanço açıklaması
- KAP bildirimi
- Jeopolitik gelişme
- Derecelendirme kararı

Gerekli ekler:

- Zaman damgalı ekonomik takvim
- Haber akışı
- KAP/şirket olayları
- Olay sınıflandırma sistemi

## D3. Temel analiz ve değerleme

OHLCV yeterli değildir:

- Gelir
- Kâr
- Marj
- Borç
- Nakit akışı
- F/K
- PD/DD
- EV/EBITDA
- Temettü
- Şirket değeri ve bilanço kalitesi

Gerekli ekler:

- Point-in-time finansal tablolar
- Açıklanma tarihi
- Revizyon geçmişi
- Kurumsal işlem bilgisi
- Survivorship-bias önlemli şirket evreni

## D4. Makro ve faiz ilişkisini açıklama

Piyasa serileriyle fiyat ilişkisi ölçülebilir; fakat makro değişkenin kendisi için ek veri gerekir:

- Politika faizi
- TÜFE/ÜFE
- İşsizlik
- PMI
- Tahvil getirileri
- Getiri eğrisi
- Merkez bankası karar/sürpriz verisi

Gerekli ekler:

- Point-in-time makro veri
- Açıklanma takvimi
- Beklenti/gerçekleşme farkı

## D5. Opsiyon ve türev ayrıntısı

Dayanak OHLCV tek başına yeterli değildir:

- Opsiyon zinciri
- Strike/vade
- Implied volatility
- Greeks
- Open interest
- Futures basis
- Vade geçişi
- Sürekli kontrat ayarı

Gerekli ekler:

- Opsiyon/futures sözleşme verisi
- Vade ve sözleşme metadata'sı
- Risksiz faiz ve gerektiğinde temettü varsayımı
- Türev fiyatlama/pozisyon sistemi

## D6. Kriptoya özgü metrikler

Spot kripto OHLCV ile fiyat davranışı ölçülür; şu alanlar ek veri ister:

- Funding rate
- Open interest
- Likidasyon akışı
- On-chain transferler
- Borsa giriş/çıkışları
- Cüzdan dağılımı
- Stablecoin akışları

## D7. Gerçek piyasa genişliği ve tarihsel evren

Mevcut sembol havuzuyla yaklaşık genişlik mümkündür. Tam ve hatasız tarihsel genişlik için:

- Tarihsel endeks üyeliği
- Delist olmuş şirketler
- Halka arz tarihleri
- İşlemden çıkarılma tarihleri
- Sektör sınıfları

verisi gerekir.

## D8. Kurumsal işlem düzeltmesi

Büyük fiyat sıçramalarını OHLCV'den aday olarak tespit edebiliriz; nedenini kesinleştirmek için:

- Split/bölünme
- Bedelli/bedelsiz
- Temettü
- Birleşme
- Sembol değişimi

metadata'sı gerekir. Mevcut veri denetiminde büyük aykırılıklar filtrelenebilir, fakat ekonomik getiri hesabı için point-in-time corporate-action kaydı daha doğrudur.

## D9. Psikoloji ve uygulama disiplini

OHLCV, kullanıcının neden karar verdiğini ölçmez:

- FOMO
- Kural ihlali
- Plansız giriş
- Duygusal çıkış
- Ekran başında karar değişimi

Gerekli ek sistem:

- Replay karar günlüğü
- İşlem öncesi plan
- Kullanıcı eylem kaydı
- Süreç puanı
- Model sinyali ile kullanıcı eylemi karşılaştırması

## D10. Görsel ve öznel grafik yorumunun doğrulanması

Kitaplardaki bazı grafik örnekleri, çizilmiş trend çizgileri ve dalga sayımları yalnız PDF metninden tam formüle dönüşmez.

Gerekli ek çalışma:

- Şekil görselinin incelenmesi
- Anchor/etiketlerin manuel veya görüntü tabanlı çıkarımı
- Ardından test edilebilir algoritmik tanım

## D11. Elliott/Wyckoff gibi esnek model etiketleri

OHLCV verisi yeterli girdidir; fakat “doğru sayım” kendiliğinden oluşmaz. Ek sistem gerekir:

- Birden fazla formal tanım
- Alternatif sayım motoru
- Kullanıcı/uzman etiketleri veya katı kurallar
- Varyant karşılaştırması

Bu nedenle veri olarak OHLCV-yeterli, bilgi tanımı olarak ek model gerektirir.

---

# E. Şimdilik bekletilecek OB/FVG alanı

Kaynak kartları ve ilgili sayfalar korunmuştur. Bu aşamada:

- Yeni OB tanımı kurulmayacak
- Yeni FVG tanımı seçilmeyecek
- Kitaptaki tanım kullanıcının sistemi yerine geçirilmeyecek
- Uygulama önceliğinde fiyat davranışı, swing, hareket kalitesi, kırılım ve takip davranışı öne alınacak

Kullanıcının mevcut OB/FVG sistemi geldiğinde:

1. Kitaptaki varyantlarla karşılaştırılır.
2. Çelişen tanımlar silinmeden ayrı tutulur.
3. Aynı replay/test altyapısında ölçülür.

---

# F. Önerilen geliştirme sırası

## Faz 1 — OHLCV özellik çekirdeği

1. Mum geometrisi
2. Örtüşme ve kapanış konumu
3. ATR ve volatilite rejimi
4. Hareket mesafe/süre/yol verimliliği
5. Baskı kaybı
6. Takip davranışı

Neden: En az varsayım ve en az öznel anchor gerektirir.

## Faz 2 — Swing ve olay motoru

1. Teyitli pivot
2. Major/minor swing
3. Yeni uç üretimi
4. Yapı kırılımı
5. İlk/ikinci deneme
6. Seviye kırılımı, kabul, retest ve failure

## Faz 3 — Çoklu zaman dilimi ve bağlam

1. 1h/2h/4h/1g hizalama
2. Trend/range rejimi
3. Seans bağlamı
4. Göreceli güç
5. Endeks ve çapraz piyasa bağlamı

## Faz 4 — Deney ve replay

1. Olay snapshot'ı
2. N-bar sonuç
3. MFE/MAE
4. 70–80 sembol tutarlılığı
5. Out-of-sample dönem
6. Parametre hassasiyeti
7. Replay görünürlük kontrolü

## Faz 5 — Harici veri isteyen modüller

Öncelik ihtiyaca göre:

- Kurumsal işlemler
- Ekonomik takvim
- Temel veriler
- Haber
- Tick/quote/order-book
- Opsiyon zinciri
- Kripto türev/on-chain

---

# G. Karar özeti

## Bugün elimizdeki OHLCV ile yapılabilecek ana işler

- Mum ve mum dizisi ölçümü
- Volatilite
- Trend/rejim
- Swing ve yapı
- Hareket kalitesi ve baskı kaybı
- Kırılım/kabul/failure
- Pullback ve ikinci deneme
- Destek/direnç davranışı
- Formasyon adayları
- Klasik indikatörler
- Hacim özellikleri
- Çoklu zaman dilimi
- Seans/zaman özellikleri
- Göreceli güç ve çapraz piyasa
- Sinyal sonrası MFE/MAE ve tutarlılık

## OHLCV var fakat önce sistem kurulması gerekenler

- Teyitli swing motoru
- Seviye/bölge motoru
- Fiyat davranışı özellik motoru
- Rejim motoru
- Formasyon motoru
- Çoklu zaman dilimi hizalama
- Olay/deney motoru
- Gelecek göstermeyen replay

## Ek veri/sistem isteyenler

- Gerçek bid/ask ve order flow
- Haber ve ekonomik olay nedeni
- Temel analiz
- Makro gerçekleşme/beklenti
- Opsiyon zinciri ve Greeks
- Futures open interest/basis
- On-chain/funding/likidasyon
- Tam tarihsel piyasa üyeliği
- Kurumsal işlem metadata'sı
- Kullanıcı psikolojisi ve kural ihlali

İlk ürün çekirdeği için harici veri beklemeye gerek yoktur. Kitapların fiyat davranışı, swing, hareket kalitesi, kırılım, takip, volatilite, çoklu zaman dilimi ve çapraz piyasa bölümlerinin büyük kısmı mevcut OHLCV arşiviyle ölçülebilir.
