# Emtia bazında düzenlenmiş BIST risk arşivi

Bu arşiv mevcut tarihsel sonuçları **yeniden hesaplamadan** emtialara ayırır. Her klasörde hisseler için kolay filtrelenebilir CSV ve tüm bölümleri, hisseleri, endeksleri ve duyarlılıkları içeren sıkıştırılmış tam sonuç vardır.

| Emtia | Hisse özeti | Tam sonuçlar | Açıklama |
|---|---|---|---|
| Altın | [CSV](madenler/altin/ozet-hisseler.csv) | [CSV.gz](madenler/altin/tum-sonuclar.csv.gz) | [Oku](madenler/altin/README.md) |
| Bakır | [CSV](madenler/bakir/ozet-hisseler.csv) | [CSV.gz](madenler/bakir/tum-sonuclar.csv.gz) | [Oku](madenler/bakir/README.md) |
| Gümüş | [CSV](madenler/gumus/ozet-hisseler.csv) | [CSV.gz](madenler/gumus/tum-sonuclar.csv.gz) | [Oku](madenler/gumus/README.md) |
| Paladyum | [CSV](madenler/paladyum/ozet-hisseler.csv) | [CSV.gz](madenler/paladyum/tum-sonuclar.csv.gz) | [Oku](madenler/paladyum/README.md) |
| Platin | [CSV](madenler/platin/ozet-hisseler.csv) | [CSV.gz](madenler/platin/tum-sonuclar.csv.gz) | [Oku](madenler/platin/README.md) |
| Brent petrol | [CSV](petrol/brent/ozet-hisseler.csv) | [CSV.gz](petrol/brent/tum-sonuclar.csv.gz) | [Oku](petrol/brent/README.md) |
| WTI petrol | [CSV](petrol/wti/ozet-hisseler.csv) | [CSV.gz](petrol/wti/tum-sonuclar.csv.gz) | [Oku](petrol/wti/README.md) |

## Hangi dosya ve filtre?

Hisse özeti `time_split=total`, `jump_filter=all`, `target_group=bist_equities` satırlarıdır. Tam dosya bunlara ek olarak 10 endeksi, `train`, `validation`, `test` dönemlerini ve `no_jump10` duyarlılığını içerir. Sıfır olaylı ve küçük örnekli kombinasyonlar da korunur. `dosya-kontrol.csv`, ana tablo ve bu dışa aktarımların satır sayılarını ve SHA-256 değerlerini kaydeder.

Örneğin altın düştükten sonraki risk için altın hisse özetinde `source_condition=down0`, `unit=USD`, `interval=4h`, `response=post_open` seçin. İstenen hisse için `target_symbol`, düşüş sayısı için `negative_count`, bilinen olay sayısı için `n` ve oran için `negative_rate` sütununa bakın. `0.7` %70 demektir; −%3 veya daha kötü düşüş ayrı `down3_count` sütunundadır.

- `down0` / `up0`: kaynak <0 / >0; `down2` / `up2`: ≤−%2 / ≥+%2; `down4` / `up4`: ≤−%4 / ≥+%4.
- `same`: aynı 10 mumdaki geçmiş eşzamanlı hareket. `post_open`: sinyal kapanışından kesinlikle sonra başlayan ilk uygun barın açılışından 10 ortak mumluk hareket. Bunlar birbirinin yerine kullanılmaz.
- `selected_source_signals` tüm seçilen kaynak olayları, `n` sonucu bilinen olayları gösterir. Sonucu eksik olaylar n dışındadır. `baseline_negative_rate` koşulsuz sabit ızgara bazıdır; `negative_rate_difference` farkı eşleştirilmiş veya nedensel değildir.
- `risk_flag`: n≥10 ve düşüş oranı ≥%70 için `tarihsel_uyari`, n<10 için `ornek_yetersiz`; bunlar keyfi tarama eşikleridir. `no_jump10` sıçrama duyarlılığıdır, veri hatası teşhisi değildir.

[Dosya kontrol listesi](dosya-kontrol.csv) · [Tam yöntem, örnekler ve sınırlamalar](../README.md) · [Plan](../PLAN.md)

**Uyarı:** Tarihsel oranlar geleceğin olasılığı, neden-sonuç ilişkisi veya yatırım tavsiyesi değildir. Çoklu tarama, küçük örnekler, dönem sınırları, örtüşen sonraki pencereler, veri/nominal zaman ve işlem maliyetleri sonuçların kullanımını sınırlar.

Arşivi ana tablodan tekrar oluşturmak için depo kökünde `.venv/bin/python -m tools.organize_macro_risk` çalıştırın. Ana ölçüm komutu da arşivi yeniler. Önceki ana dosyalar ve bağlantılar korunur.
