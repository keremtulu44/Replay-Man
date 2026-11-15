# OHLCV Replay Ölçümü — Swing ve Yapı Olayları

## Kapsam

- 125 varlık, 500 seri, 558.121 tamamlanmış bar
- 1h 315.801; 2h 142.618; 4h 69.846; 1d 29.856 bar
- Mum geometrisi, örtüşme, volatilite, hareket kalitesi ve baskı kaybı
- Teyit zamanı ayrı minor/major swingler ve swing bacakları
- Swing seviyelerinde kırılım/kabul/retest/failure yaşam döngüsü
- Karar özelliklerinden ayrı 5 ve 20 bar yön düzeltilmiş getiri, MFE ve MAE

## Swing envanteri

| Olay | Sayı |
|---|---:|
| Minor swing (2+2) | 151.450 |
| Major swing (5+5) | 67.705 |
| Karşıt minor swing bacağı | 113.778 |
| Higher high | 51.331 |
| Higher low | 50.471 |
| Lower high | 50.713 |
| Lower low | 50.474 |

## Yapı olayı envanteri

| Olay | Tanım | Sayı |
|---|---|---:|
| `probe_rejection` | Uç seviyeyi aştı, kapanış dışarıda kalmadı | 127.561 |
| `close_break` | Seviye tolerans dışında kapanışla aşıldı | 116.136 |
| `follow_through` | İlk üç bar içinde kırılım yönünde dış kapanış geldi | 91.132 |
| `acceptance` | İki dış kapanış ile yeni alan kabul adayı oldu | 91.351 |
| `retest_hold` | Seviye tekrar test edildi ve kapanış kırılım çevresinde korundu | 62.104 |
| `failure` | İlk on bar içinde kapanış eski alanın içine döndü | 67.971 |

Bu sayılar strateji başarı iddiası değildir. Aynı bar farklı geçmiş swing seviyeleri için birden fazla olay üretebilir. Seviye bir pivot olarak çizildiği anda değil, swing teyit edildikten sonraki bardan itibaren aktiftir.

## Olay yönü

- `close_break`, `follow_through`, `acceptance`, `retest_hold`: hipotez yönü kırılım yönüdür.
- `probe_rejection`, `failure`: hipotez yönü başarısız denemenin tersidir.
- `direction`, sınanan/kırılan tarafı; `thesis_direction`, sonuç ölçümündeki hipotez yönünü gösterir.

## Gelecek sızıntısı sözleşmesi

- Pivotun geometrik barı ve ilk bilinebildiği teyit barı ayrıdır.
- Minor teyit gecikmesi 2, major teyit gecikmesi 5 bardır.
- Seviye teyit barından sonra sınanabilir; pivot ile teyit arasındaki fiyat hareketleri olay sayılmaz.
- Yapı durumu yalnız sıradaki kapanmış OHLC barıyla ilerler.
- Swing bacağı bitiş pivotunda değil, bitiş teyidinde bilinir.
- İleri sonuçlar özellik/replay girdisi değildir.

## Sonuç dosyaları

- `summary.json`: Genel kapsam ve olay sayıları
- `series_inventory.csv`: 500 seri için bar, swing ve yapı olayları
- `structure_event_study.csv`: Grup × periyot × olay × sınanan yön × hipotez yönü kırılımında gözlem, varlık sayısı, medyan yönlü getiri, kazanma oranı, MFE ve MAE

## Sonuçları yorumlamadan önce zorunlu kontroller

1. Ham fiyatlardaki bölünme/kurumsal işlem sıçramaları özellikle aşağı yön olaylarını bozabilir.
2. Aynı semboldeki olaylar bağımsız gözlem değildir.
3. Parametreler ilk varyanttır: tolerans 0,10 ATR; kabul 2 kapanış; takip 3 bar; failure 10 bar; seviye ömrü 100 bar.
4. Çoklu parametre denemesi yapılmadan önce eğitim/doğrulama dönemleri sabitlenmelidir.
5. Medyan getiri işlem maliyeti içermez.
6. Hacim endeks ve FX serilerinde çoğunlukla kullanılamaz.

Bu nedenle rapor keşif ölçümüdür; işlem önerisi veya doğrulanmış avantaj değildir.

## Sıradaki katman

- Olay anındaki hareket kalitesi, volatilite ve baskı kaybı snapshot'ı
- İlk/ikinci deneme eşleştirmesi
- Trend/range bağlamı
- Sembol başına sonuç ve 70–80+ sembolde yön tutarlılığı
- Eğitim/doğrulama/out-of-sample ayrımı
