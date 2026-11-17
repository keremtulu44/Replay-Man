# Emtia hareketlerinde BIST hisseleri: uzun pozisyon için tarihsel risk ekranı

## Ne soruyor?

Bu çalışma, örneğin **altın düşmüşken hangi hisselerin kaç olayın kaçında düştüğünü** tüm mevcut hisselerde gösterir. Tek bir hisseye veya −%3'e odaklanmaz: hisse getirisi **sıfırdan küçükse düşüş** sayılır. −%3 veya daha büyük düşüş ayrıca gösterilir. Bu, tarihsel gözlemlere dayalı bir risk bağlamıdır; gelecekteki düşüş olasılığı, neden-sonuç ilişkisi ya da otomatik işlem kararı değildir.

**Kapsam:** 100 hisse ve 10 endeks; Brent, WTI, altın, gümüş, bakır, platin ve paladyum vadeli seri vekilleri; USD ve emtia × USD/TRY yaklaşık TL fiyatı; 1 saatlik ve 4 saatlik **10 BIST mumu**. Kaynak pencereleri 14 Kasım 2025–13 Kasım 2026 nominal UTC aralığında; kaynak ve hedeflerin kullanılabilir kapsaması değişebilir. 4 saatlik 10 mum, 10 takvim saati değildir. Verilen şok ve getiri yüzdeleri ondalık biçimdedir: `0.70` %70 demektir.

## İlk örnek: altın düştükten sonra

Aşağıda USD altın vadeli vekili 10 adet 4 saatlik BIST mumu boyunca **herhangi bir miktar düştüğünde** (`down0`), kapanıştan kesinlikle sonra başlayan ilk uygun barın açılışından itibaren sonraki 10 mumdaki hisse düşüşü gösterilir. Kaynak şok pencereleri çakışmadan seçilmiştir. Üç bölüm birleştirilmiştir; filtreli değil, ana sonuçtur.

| Hisse | Düşüş / bilinen sonuç | Oran | ≤−%3 | Koşulsuz sabit ızgara düşüşü | Fark |
|---|---:|---:|---:|---:|---:|
| BRYAT | 24 / 31 | %77,4 | 10 / 31 | 26 / 40 = %65,0 | +12,4 yüzde puan |
| AYGAZ | 22 / 31 | %71,0 | 14 / 31 | 20 / 40 = %50,0 | +21,0 puan |
| ECILC | 22 / 31 | %71,0 | 16 / 31 | 24 / 40 = %60,0 | +11,0 puan |
| TUPRS | 18 / 31 | %58,1 | 9 / 31 | 23 / 40 = %57,5 | +0,6 puan |

Kaynak koşuluna uyan **34** çakışmasız pencere seçildi; bu dört hissede sonraki sonuçların 31'i hesaplanabildi. Eksik sonuçlar paydadan çıkarıldı; yerine başka olay seçilmedi. BRYAT'ın aynı penceredeki eşzamanlı sonucu 25/34 = %73,5'tir; bu, sinyal öğrenilmeden önce zaten yaşanmış harekettir ve 24/31 sonraki hareketle aynı şey değildir. BRYAT için sonraki bölüm sayıları eğitim 13/19, doğrulama 4/4, test 7/8; son iki bölümün örneği 10'dan azdır. Bu üç hisse örneğinde %10 sıçrama duyarlılık filtresi sayıları değiştirmedi; başka kombinasyonlarda değiştirebilir.

`down0` çok küçük altın düşüşlerini de içerir. Daha somut büyüklük için **USD altın ≤−%2**, 4 saatlik 10 mum koşulunda TUPRS sonraki pencerede 15/20 = %75 düşmüştür; aynı koşuldaki toplam seçili kaynak olayı 23, koşulsuz baz 23/40 = %57,5'tir. Bu bir örnektir, bütün hisseler veya diğer eşikler için aynı oranın geçerli olduğu anlamına gelmez.

## Dosyalar ve kullanım

**Emtia bazında düzenlenmiş arşiv:** [Arşiv indeksi](emtia-arsivi/README.md). Her emtia için ayrı hisse özeti, tam sonuç ve açıklama dosyası bulunur. Önceki toplu dosyalar aşağıda korunmuştur.

- [risk-ozet-hisseler.csv](risk-ozet-hisseler.csv): Excel/LibreOffice ile açılıp filtrelenebilen **33.600 satırlık** ana hisse tablosu; tüm 7 kaynak, her eşik, her birim/periyot, `same` ve `post_open`, toplam ve sıçrama filtresiz. Endeks, dönem ve duyarlılıklar tam tablodadır.
- [risk-table.csv.gz](risk-table.csv.gz): **295.680 satırlık tam tablo**; 100 hisse + 10 endeks, ayrı train/validation/test/toplam ve iki sıçrama filtresi. Gzip açılarak CSV kullanılabilir.
- [source-windows.csv.gz](source-windows.csv.gz): bütün kaynak pencereleri, hesaplanan değişim, zamanlar ve sonuçtan bağımsız seçilmiş olay işaretleri.
- [target-availability.csv](target-availability.csv): her hedef/periyot için bilinen sonuç sayıları; [input-manifest.csv](input-manifest.csv): kullanılan veri dosyaları ve SHA-256; [summary.json](summary.json): teknik kapsam.
- [PLAN.md](PLAN.md): hesaplama tasarımı. Yeniden üretim: `.venv/bin/python -m tools.measure_macro_risk` (girdi varsayılanı `data/ohlcv`, çıktı bu dizin; `--root`, `--output` değiştirilebilir).

Örnek terminal sorguları (bağımlılıkları kurulu ortamda):

```bash
# Altın düşmüşken, sinyal sonrası 4h, bütün hisseler/endeksler
.venv/bin/python -m tools.query_macro_risk --source METAL_GOLD --condition down0 --interval 4h
# En az %2 altın düşüşü, özellikle TUPRS
.venv/bin/python -m tools.query_macro_risk --source METAL_GOLD --condition down2 --target TUPRS
# Brent, sinyal sonrası test dönemi, örnek yetersizleri de dahil
.venv/bin/python -m tools.query_macro_risk --source OIL_BRENT --condition down4 --split test
# Geçmiş eşzamanlı hareket ve TL vekili, örnek en az 10
.venv/bin/python -m tools.query_macro_risk --source METAL_GOLD --response same --unit TRY_proxy --min-n 10
```

Komut varsayılan olarak ilk 30 sonucu gösterir; `--limit 110`, `--warning-only`, `--jump-filter no_jump10` veya `--csv` kullanılabilir. Hisse ve endeksler birlikte döner; yalnız hisseler istenirse `target_group=bist_equities` ile CSV'yi filtreleyin. Çıktıdaki `n` ve sayılar oranlardan önemlidir.

## Alanlar ve yöntem

- `source_condition`: `down0` / `up0` kaynak getirisi <0 / >0; `down2` / `up2` ≤−%2 / ≥+%2; `down4` / `up4` ≤−%4 / ≥+%4. Her eşik ayrı taranır, birbirlerini içerir.
- `response=same`: aynı 10 BIST mumu başlangıç açılışından son kapanışa hedef getirisi. **Sinyal bitince öğrenilen geçmiş ortak hareket; işlem sonrası tahmin değildir.**
- `response=post_open`: kaynak penceresinin nominal kapanışından **kesinlikle sonra** başlayan ilk XU100 barında hedef açılışı, onu izleyen 10 ortak barın son kapanışı. Sinyal kapanışına tam denk gelen açılış atlanır; eksik hedef veya benchmark barı varsa sonuç bilinmez. Getiri o giriş açılışından hesaplanır; önceki kayıp tekrar sayılmaz. Gecikmeli açılış vekili, ulaşılabilir fiyat veya işlem garantisi değildir.
- `selected_source_signals`: hedef sonucuna bakılmadan, koşula göre ayrı ayrı ve her dönem içinde çakışmasız seçilmiş kaynak penceresi. `n`: bunların geçerli hedef sonucu bulunanları. `negative_count`, `positive_count`, `flat_count`: sırasıyla <0, >0 ve tam 0; toplamları n. `down3_count` ≤−%3'ü gösterir, ayrı bir alt kümedir. Oranlar sayılar/n'dir.
- `baseline_*`: aynı hedef, kaynak, birim, periyot, bölüm ve sonuç ufkunda, kaynak değişimi bilinen tüm pencerelerden oluşturulan sabit çakışmasız 10-mum ızgarası. `negative_rate_difference` = koşullu düşüş oranı − baz oranı; örnek dönemleri eşleştirilmiş değildir, nedensel etki olarak okunmamalıdır.
- `risk_flag`: `tarihsel_uyari` için n≥10 ve düşüş oranı ≥%70; `esik_altinda` n≥10 ve oran <%70; `ornek_yetersiz` n<10. %70 ve 10 kullanıcı örneğini filtreye çevirmek için **keyfi** seçildi; güvenilirlik veya işlem veto sınırı değildir. `same` bayrağı yalnız geçmiş eşzamanlılığı anlatır; işlem öncesi bakış için `post_open` ayrı incelenmelidir.
- `jump_filter=no_jump10`: kaynak penceresinde gözlenen en büyük saatlik emtia kapanış sıçraması %10'u aşmayan durumlar; kaynak olayları bu filtreyle baştan seçilir. Bu sonradan eklenen duyarlılık kontrolü, sıçramaların hata olduğunu göstermez; kur sıçramasını ayrı filtrelemez.
- Dönemler: train 2026-07-01 UTC öncesi, validation 2026-09-01 UTC öncesi, sonrası test. Kaynak başlangıcından sonucun nominal bitişine dönem sınırı geçilirse sonuç dışlanır. `total` geçerli bölüm sayılarının toplamıdır, bölüm yüzdelerinin ortalaması değildir.

## Önemli sınırlamalar

Çakışmasız **kaynak** pencereleri bağımsız olay anlamına gelmez; sonraki hedef pencereleri çakışabilir. Farklı emtia ve eşikler aynı piyasa olaylarını paylaşır; oranlar çarpılmaz/toplanmaz. Çok sayıda kombinasyon tarandığından yüksek oranlar tesadüfi olabilir. Test dönemi daha önce incelendiği için bağımsız, el değmemiş ileri test değildir. Alış-satış farkı, kayma, komisyon, likidite, emir gerçekleşmesi ve portföy yönetimi hesaba katılmadı.

Emtia ve kur için bilinen son saatlik kapanışlar azami 90 dakika bayatlıkla eşlenir; TL vekili gerçek işlem fiyatı değildir. Vadeli kontrat roll'u, fiyat kaynakları, nominal bar kapanışı ve seans semantiği sonucu etkileyebilir; `complete` filtresi ve eksik/uyumsuz OHLC verileri n'i azaltır. Bu nedenle mevcut veriler üzerinde betimleyici tarama yapılmış, küçük veri oynamaları çalışmayı durduran koşul yapılmamıştır. Bu tablo yatırım tavsiyesi değildir.
