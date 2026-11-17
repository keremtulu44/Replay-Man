# Piyasa ve hisse araştırmaları — kayıtlı sonuçlar

Bu indeks, mevcut araştırma sonuçlarını tek yerden bulmak içindir. Sonuçlar **tarihsel ölçümlerdir**; canlı indikatör, emir veya alım/satım önerisi değildir. Genel bağlam sisteminin sonraki aşamaları ve mevcut durumu [plan dosyasında](../plans/genel-baglam-sistemi.md) açıklanır. Kullanıcı tercihiyle hacim kapsam dışındadır.

## Endeksler ve döviz

- [Kaynak bazında arşiv](market-context/kaynak-arsivi/README.md): 10 BIST endeksi, 6 küresel gösterge ve 2 kur için ayrı, filtrelenebilir hisse CSV'leri.
- [Sonuçların açıklaması ve örnekleri](market-context/README.md) · [Tüm özetler](market-context/hisse-ozet.csv) · [Tüm dönemler ve duyarlılık](market-context/risk-table.csv.gz).
- [Kaynak veri kapsamı](market-context/source-availability.csv) · [Kaynak pencere kayıtları](market-context/source-windows.csv.gz) · [Girdi manifesti](market-context/input-manifest.csv) · [Dosya kontrol özeti](market-context/kaynak-arsivi/dosya-kontrol.csv).

## Emtia

- [Emtia bazında arşiv](macro-risk-screen/emtia-arsivi/README.md): petrol ve maden kaynakları için ayrı özetler ve tam sonuçlar.
- [Emtia ölçüm raporu](macro-risk-screen/README.md) · [Tüm hisse özetleri](macro-risk-screen/risk-ozet-hisseler.csv) · [Tüm dönemler ve duyarlılık](macro-risk-screen/risk-table.csv.gz).

## Önceki ayrıntılı çalışmalar

- [Altın ve gümüş sanal karşılaştırması](metal-filter-backtest/README.md): geçmiş adaylar üzerindeki deneydir; genel bir indikatörün değerini kanıtlamaz.
- [10 mumluk emtia tepkileri](10bar-commodity-reactions/README.md): önceki ölçümler ve Brent–TUPRS örnekleri.

## Okuma ve saklama notları

`same` kaynakla aynı geçmiş 10 mum; `post_open` sinyalden sonra başlayan 10 mumluk vekildir. `negative_count/n` düşen / sonucu bilinen olaydır. Eksik veya küçük örnekler korunur. Endeks/kur ve emtia tablolarının baz ızgaraları aynı yöntem olmayabilir; yöntemleri kendi raporlarında anlatılır. Özellikle ABD endekslerinin 4 saatlik 90 dakikalık eşleştirmesinde n=0 olması, etkinin yokluğu değil, veri/seans kapsamı sınırlamasıdır. Oranlar neden-sonuç veya gelecek için kesin olasılık değildir.

**Saklama:** Bu klasörde sonuç tabloları, olay kaynak pencereleri, yöntemler, kapsam ve girdi hash manifestleri saklanır. Orijinal OHLCV girdileri `data/ohlcv/` altındadır ve `.gitignore` nedeniyle Git'e dahil değildir; manifest ham girdinin kendisi değildir. Tekrar üretim veya ham fiyatların uzun vadeli korunması için orijinal veri ayrıca yedeklenmelidir.
