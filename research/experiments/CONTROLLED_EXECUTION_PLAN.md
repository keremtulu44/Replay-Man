# Kitap Kuralları Kontrollü Uygulama Planı

## Değişmez çalışma döngüsü

Her paket aşağıdaki kapılardan geçmeden sonraki pakete ilerlemez:

1. **Kaynak kapısı:** İddia, kaynak kartı ve PDF sayfasıyla bağlanır; kaynak anlatımı ile asistan yorumu ayrılır.
2. **Tanım kapısı:** Gözlenebilir OHLCV parçaları yazılır. “Güçlü”, “zayıf”, “temiz” gibi sıfatlar doğrudan sonuç sayılmaz.
3. **Nedensellik kapısı:** Olayın geometrik zamanı ile ilk bilinebilir zamanı ayrılır; gelecek bar kullanılmadığı test edilir.
4. **Varyant kapısı:** Tek keyfî eşik doğru ilan edilmez. Az sayıda, önceden kayıtlı komşu varyant tanımlanır.
5. **Birim testi kapısı:** Sentetik küçük serilerde beklenen olay, sınır, eşitlik ve eksik veri davranışı doğrulanır.
6. **Tam evren kapısı:** 125 varlık ve 1h/2h/4h/1d serilerinde olay ve veri uygunluğu sayılır.
7. **Finansal kapı:** Ham getiri, yön düzeltilmiş getiri, BIST için XU100-aşırı getiri, MFE, MAE ve pozitif oran ayrı kaydedilir.
8. **Dayanıklılık kapısı:** Kronolojik eğitim/doğrulama/test, sembol tutarlılığı, örnek sayısı ve komşu parametreler karşılaştırılır.
9. **Tekrar kapısı:** Yeni kuralın mevcut kurallarla olay örtüşmesi ölçülür; aynı bilgi ikinci avantaj diye sayılmaz.
10. **Karar kapısı:** `devam_et`, `baglam_gerekli`, `yazi_tura`, `olumsuz`, `rejime_bagli`, `ornek_yetersiz`, `bilgi_tekrari` veya `veri_uygun_degil` kaydedilir.

Başarısız, saçma veya yazı-tura çıkan sonuç silinmez.

## Uygulama sırası

### Paket 1 — İlk/ikinci deneme ve yeni uç

- Aynı yöndeki ardışık swing bacaklarını eşleştirme
- Mesafe, süre, hız ve yol verimliliği oranları
- Yeni tepe/dip üretimi
- Yeni uç üretememe
- İkinci denemenin başarısızlığı
- Kaynak: ağırlıkla Cilt 2 Bölüm 9–10

### Paket 2 — Pullback geometrisi

- Ana harekete göre geri alma derinliği
- Süre ve hız
- Örtüşme ve volatilite
- Tek/iki/çok bacak
- Eski kırılım bölgesine dönüş
- Kaynak: Cilt 2 Bölüm 8–11

### Paket 3 — Mum geometrisi ve dizileri

- Gövde, fitil, kapanış konumu
- Inside/outside/engulfing
- İki ve üç mum dizileri
- Adlandırılmış şekil ile sürekli geometrik özellik karşılaştırması
- Kaynak: Cilt 2 Bölüm 1–5

### Paket 4 — Trend/range ve yapı bağlamı

- Trend, kanal, range ve geçiş
- Yapı korunurken güç kaybı
- Rejim başlangıç/bitiş gecikmesi
- Ana kitap ve Cilt 2

### Paket 5 — Çoklu zaman dilimi

- Yalnız tamamlanmış üst zaman barı
- 1h→2h/4h/1d bağlamı
- Üst zaman yön/konum uyumu

### Paket 6 — Göreceli güç ve çapraz piyasa

- Hisse/XU100 aşırı getiri
- Endeks, döviz, maden ve enerji bağlamı
- Saat/seans hizalama ve lead-lag

### Paket 7 — Cilt 1 indikatör aileleri

- Trend, momentum, volatilite, konum ve hacim rolleri
- Her indikatörün fiyat davranışı çekirdeğine marjinal katkısı
- Aynı bilgiyi tekrar eden araçların elenmesi

### Paket 8 — Formasyon geometrileri

- İkili/üçlü uç, H&S, üçgen, kama, kanal ve range
- Önceden tanımlı pivot ve tolerans
- Formasyon adı yerine geometrik parçaların korunması

### Paket 9 — Seans ve zamanlama

- Açılış/kapanış, saat, haftanın günü
- Seans içi volatilite ve hacim uygunluğu

### Paket 10 — Risk/sonuç ve pozisyon yönetimi

- Sabit ufuk ile stop/target sonuçlarının ayrımı
- Bar içi sıra belirsizliği
- Maliyet stresi, eşzamanlı sinyal ve korelasyon

## Bekletilenler

- OB/FVG: Kullanıcının mevcut sistemi gelene kadar yeni ana tanım seçilmeyecek.
- Gerçek order flow/emir defteri: OHLCV ile iddia edilmeyecek.
- Temel/makro/haber: Point-in-time ek veri olmadan nedensel test yapılmayacak.

## Kayıt yerleri

- Kaynak bağlantısı ve kural kararı: `research/experiments/book-rule-results/`
- Tam ölçüm tabloları: `research/measurements/`
- Kod: `replayman/`
- Nedensellik ve sınır testleri: `tests/`

Her paket tamamlandığında bu belgeye tamamlanma durumu ve commit kimliği eklenecektir.
