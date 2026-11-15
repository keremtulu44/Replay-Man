# Bilgi Tabanı Kalite İncelemesi

## İnceleme kapsamı

Bu inceleme kaynak PDF, sayfa arşivi, 778 sayfa kartı, 58 bölüm dosyası, konu sınıflaması, tematik dosyalar ve indekslerin birbirini doğru işaretleyip işaretlemediğini kontrol eder.

## Bulunan ve düzeltilen sorunlar

### 1. Aşırı geniş konu eşleşmeleri

İlk sürümde `piyasa`, `yüksek`, `düşük`, `tepe` ve `dip` gibi genel kelimeler tek başına konu eşleşmesi oluşturuyordu. Bu nedenle temel analiz veya faiz sayfaları yanlışlıkla market structure/OHLC çekirdeği sayılabiliyordu.

**Düzeltme:** Genel kelimeler kaldırıldı; `swing high`, `swing low`, `yapı kırılımı`, `kapanış fiyatı`, `grafik verisi` gibi daha seçici terimler kullanıldı. Eşleşmeler kelime sınırıyla yapılıyor.

### 2. Kitap başlığının kaynak özeti sanılması

Sayfa başlıkları ve tekrar eden kitap adı bazı otomatik özetlerin ilk cümlesine giriyordu.

**Düzeltme:** Kitap üstbilgisi ve yalın sayfa numarası özet üretiminden önce temizleniyor. Şekil/Tablo başlığı tek başına özet cümlesi seçilmiyor. Tam kaynak metni hiçbir zaman temizlenmiyor; kanonik kartta korunuyor.

### 3. Cilt 2 bölüm algılama hatası

Bir sayfada “Bölüm 2'de gördüğümüz” gibi iç atıflar bulunduğunda ilk sürüm gerçek bölüm başlığını kaçırabiliyordu. Cilt 2 yalnız Bölüm 1–2 görünüyordu.

**Düzeltme:** Yalnız sayfanın ilk 100 karakterindeki bölüm başlığı geçiş sayılıyor. Cilt 2'nin 13, Cilt 1'in 21, ana kitabın 24 bölümünün tamamı doğrulandı.

### 4. Alt başlığın yeni bölüme taşınması

Yeni bölüm açıldığında önceki bölümün son alt başlığı kısa süre taşınabiliyordu.

**Düzeltme:** Bölüm değişiminde alt başlık sıfırlanıyor; yeni alt başlık bulunduğunda güncelleniyor.

### 5. Ön maddelerin çekirdek içerik sayılması

Kapak, telif, içindekiler ve önsöz sayfaları kelime eşleşmeleri nedeniyle çekirdek olarak etiketlenebiliyordu.

**Düzeltme:** Bölüm başlamadan önceki sayfalar `front_matter/reference` olarak işaretleniyor; metinleri yine kayıpsız saklanıyor.

### 6. Bölüm bazlı görünüm eksikliği

Sayfa kartları ve konu dosyaları vardı fakat 58 bölümün her biri için ayrı okunabilir dosya yoktu.

**Düzeltme:** Her bölüm için sayfa aralığı, alt başlıklar, konu dağılımı ve sayfa şeritlerini içeren 58 bölüm dosyası üretildi.

## Bilerek korunmuş sınırlamalar

### Görseller

PDF içindeki şekil başlıkları ve çevresindeki açıklamalar metin katmanından alınır; çizgi, mum, ok ve görsel geometrinin piksel düzeyinde anlamı henüz ayrı görüntü analiziyle çıkarılmamıştır. Bu bilgi “atlanmış metin” değildir fakat görsel semantik ikinci bir çalışma gerektirir.

### Otomatik kaynak özeti

`source_extract_summary` kaynaktan seçilmiş cümlelerden oluşur; yaratıcı özet değildir. Kötü PDF metin sırası olan tablolarda tam kart metnine geri dönülmelidir.

### Formül ve eşikler

Kullanıcı kararı gereği ilk okuma aşamasında kesin parametre/eşik üretilmemiştir. “Nasıl kullanılabilir?” kayıtları uygulama garantisi değil araştırma yönüdür.

### OB/FVG

Kitaplardaki OB/FVG bölümleri kaynak olarak indekslenmiştir. Kullanıcının mevcut sistematiği gelmeden yeni ana OB/FVG tanımı seçilmemiştir.

### Çelişkiler

Birbiriyle uyuşmayan görüşler otomatik olarak çözümlenmez veya silinmez. İlgili sayfa kartları aynı tema indeksinde korunur; kavram ayrıntılandırılırken varyant deneylerine dönüştürülür.

## Tamlık tanımı

Buradaki `%100 kapsam`, 778 PDF sayfasının kayıpsız kaynak kartına ve bölüm/konu indeksine girdiğini ifade eder. Her iddianın doğrulandığı veya her görselin matematikleştirildiği anlamına gelmez. Doğrulama, sonraki deney ve replay aşamasının görevidir.
