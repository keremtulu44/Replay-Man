# OHLCV Replay — Başlangıç Ölçümü

Bu klasör Replay-Man'in ilk çalışan, gelecek sızıntısız ölçüm turudur.

## Kapsam

- 125 varlık
- 500 seri (`1h`, `2h`, `4h`, `1d`)
- Tamamlanmamış türetilmiş barlar dışarıda bırakıldıktan sonra 558.121 bar
- Mum geometrisi, örtüşme, volatilite, göreceli hacim, hareket kalitesi ve baskı kaybı adayları
- Karar özelliklerinden fiziksel olarak ayrı ileri getiri ve MFE/MAE sonuç katmanı

## İlk sonuç kapsamı

| Periyot | Bar | ATR hazır | Hareket kalitesi hazır | 20 bar sonuç hazır |
|---|---:|---:|---:|---:|
| 1h | 315.801 | 314.176 | 314.551 | 313.301 |
| 2h | 142.618 | 140.993 | 141.368 | 140.118 |
| 4h | 69.846 | 68.221 | 68.596 | 67.346 |
| 1d | 29.856 | 28.303 | 28.660 | 27.470 |

Pencerenin başındaki ve sonuç ufkunun sonundaki boşluklar beklenir; bunlar ileri/geri doldurulmaz.

## Hacim uyarısı

Sıfır hacim oranı yaklaşık olarak:

- BIST hisseleri: `%6,25`
- BIST endeksleri: `%97,39`
- Küresel endeksler: `%71,38`
- Döviz: `%100`
- Madenler: `%2,65`
- Enerji: `%2,38`

Bu nedenle hacim özellikleri tüm evrene kör biçimde uygulanmayacaktır. Endeks ve FX için Yahoo `volume=0`, “işlem olmadı” değil, kullanılabilir merkezi hacim bulunmadığı anlamına gelir. Hacim deneyleri veri uygunluk filtresi isteyecektir.

## Gelecek sızıntısı sözleşmesi

- `causal_features` yalnız mevcut ve geçmiş barı kullanır.
- Negatif `shift` ve merkezlenmiş pencere özellik katmanında yasaktır.
- `ReplayEngine.history`, yalnız açılmış bara kadar savunmalı kopya verir.
- İleri getiri ve MFE/MAE `forward_outcomes` içinde ayrı üretilir; karar girdisi değildir.
- Türetilmiş 2h/4h serilerinde `complete=false` barlar varsayılan olarak kullanılmaz.

## Dosyalar

- `summary.json`: Kapsam özeti
- `series_inventory.csv`: Her seri için bar, dönem, hazır özellik/sonuç sayısı ve sıfır hacim oranı

Bu ilk tur strateji başarısı iddiası değildir. Yalnız ölçüm altyapısının tüm evrende çalıştığını ve sonuç etiketlerinin üretilebildiğini doğrular.

## Sonraki adım

1. Teyitli swing motoru
2. Hareket kalitesi ve baskı kaybı için olay adayları
3. Kırılım/takip/failure durum makinesi
4. Olayların 70–80+ sembolde MFE/MAE dağılımı
5. Eğitim/doğrulama dönem ayrımı ve parametre hassasiyeti
