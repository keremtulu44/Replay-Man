# OHLCV Replay Başlangıç Ölçümü

## Kapsam

- 125 varlık, 500 seri ve 558.121 tamamlanmış bar
- 1h: 315.801; 2h: 142.618; 4h: 69.846; 1d: 29.856 bar
- Mum geometrisi, örtüşme, volatilite, göreceli hacim, hareket kalitesi ve baskı kaybı
- Teyit zamanı ayrı minor/major swingler ve karşıt swing bacakları
- Karar özelliklerinden ayrı ileri getiri ve MFE/MAE sonuçları

## İlk swing ölçümü

| Olay | Sayı |
|---|---:|
| Minor swing (2 sol + 2 sağ) | 151.450 |
| Major swing (5 sol + 5 sağ) | 67.705 |
| Karşıt minor swing bacağı | 113.778 |
| Higher high | 51.331 |
| Higher low | 50.471 |
| Lower high | 50.713 |
| Lower low | 50.474 |

Bunlar başarı sonucu değil, bütün evrende üretilen olay envanteridir. Aynı geometrik uç minor ve major seviyede ayrı olay olabilir.

## Gelecek sızıntısı sözleşmesi

- Pivotun geçmişte ait olduğu bar `pivot_position` olarak saklanır.
- Olay ancak sağ teyit barları kapandığında `confirmed_position` zamanında yayımlanır.
- Minor swing için teyit gecikmesi 2, major swing için 5 bardır.
- HH/HL/LH/LL ilişkisi yalnız o ana kadar teyit edilmiş aynı tür swinglerle karşılaştırılır.
- Swing bacağı bitiş pivotunda değil, bitiş pivotu teyit edildiğinde bilinir (`known_at_position`).
- Özellikler yalnız mevcut/geçmiş barı kullanır; ileri sonuçlar ayrı sonuç tablosudur.

## Hacim uyarısı

Sıfır hacim oranı BIST hisselerinde yaklaşık %6,25, BIST endekslerinde %97,39, küresel endekslerde %71,38, FX'te %100, madenlerde %2,65 ve enerjide %2,38'dir. Endeks/FX sıfırları işlemsizlik değil, kullanılabilir merkezi hacim olmamasıdır. Hacim deneyleri uygunluk filtresi gerektirir.

## Dosyalar

- `summary.json`: Genel kapsam ve olay sayıları
- `series_inventory.csv`: Seri bazında bar, hazır ölçüm, swing ve yapı ilişkisi sayıları

## Sonraki adım

Teyitli swinglerden seviyeler üretilecek; seviye yaklaşımı, dışarı çıkış, dış kapanış, takip, kabul, retest ve failure durum makinesi kurulacaktır. Daha sonra olay anındaki özellikler ileri MFE/MAE ile 70–80+ sembolde ölçülecektir.
