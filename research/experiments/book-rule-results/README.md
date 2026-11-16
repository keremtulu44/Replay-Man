# Kitap Kuralı Sonuç Arşivi

Bu dizin kitaptan çıkarılan her ölçülebilir iddiayı kaynak kartı, matematiksel uygulama, tam sonuç tablosu ve araştırma kararıyla bağlar.

- `registry.json`: Kural kimliği, kaynak sayfaları, durum ve karar
- `RESULTS.md`: İnsan-okunur ayrıntılı sonuç
- `BR-*` klasörleri: Kurala ait `source-links.json` ve azaltılmamış filtreli sonuç CSV'leri

Durumlar başarı etiketi değildir; `devam_et`, `baglam_filtresi_gerekli`, `bilgi_tekrari`, `yazi_turaya_yakin`, `rejime_bagli`, `kararsiz`, `ornek_yetersiz_bant_var` ve `altyapi_kurali` olarak açıkça kaydedilir.

Ana ölçüm tabloları `research/measurements/ohlcv-baseline/` altında korunur. Kural klasörlerindeki tablolar aynı ana tablonun ilgili olaya filtrelenmiş tam satırlarıdır; rapor özeti uğruna periyot, yön, grup, zaman bölümü veya sembol sonucu silinmez.
