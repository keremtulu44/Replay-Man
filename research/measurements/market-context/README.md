# Endeks ve kur hareketlerinde hisse bağlamı

Bu, hacim hariç genel bağlam sisteminin **ilk endeks/kur ölçümüdür**. Bir alım-satım sistemi değildir. Mevcut [emtia risk arşivi](../macro-risk-screen/README.md) korunmuştur; [genel plan](../../plans/genel-baglam-sistemi.md) sektör eşleştirmesi, ortak durumlar, hisse yapısı/trendi/oynaklığı ve birleşik ekranın sonraki aşamalarını anlatır. Bunlar henüz tamamlanmadı.

## Kapsam ve ilk bulgular

100 hisse; 10 BIST endeksi, 6 küresel endeks/gösterge ve 2 kur; 1h ve 4h; 10 ortak BIST mumunda kaynak yönü veya ±%2/±%4. Her bir kaynak düzeyi **kendi doğal birimindedir**: endeks/gösterge düzeyi veya ilgili döviz kuru; endeksler USD emtia gibi gösterilmez. Kaynak verilerinin fiili kapsamı değişir. Kaynak pencereleri 14 Kasım 2025–13 Kasım 2026 nominal UTC aralığındadır; bu sonuçlar güncel canlı fiyat değildir.

Aşağıdaki örnekler **4h, kaynak herhangi bir miktar değiştiğinde, sinyalden sonraki 10 mum, dönemler toplamı** içindir. Düşüş <0, baz ise kaynak değeri bilinen pencerelerden seçilmiş sabit ızgaradır:

| Kaynak koşulu | Hisse | Sonraki düşüş / bilinen sonuç | Kaynak-seçimli sabit baz | Açıklama |
|---|---|---:|---:|---|
| XU100 düştüğünde | TUPRS | 12/24 = %50 | 19/45 = %42,2 | 26 kaynak olayı seçildi; ikisinin sonucu hesaplanamadı. |
| XU100 düştüğünde | KARSN | 18/24 = %75 | 27/45 = %60 | Test dönemindeki sayı 7/8; tek başına yeterli kanıt değil. |
| USD/TRY yükseldiğinde | TUPRS | 20/45 = %44,4 | 24/45 = %53,3 | Çok küçük kur değişimleri de koşula girer. |
| USD/TRY düştüğünde | TUPRS | 3/7 = %42,9 | 24/45 = %53,3 | **Örnek yetersiz**; oranı güçlü ilişki olarak yorumlama. |

Bu örnekler diğer hisse ve koşullara genellenemez. Dönemler daha önce görülmüştür; ilişkiler neden-sonuç veya geleceğin düşüş olasılığı değildir. Hisse bazlı bütün sonuçlar, olumsuz ve sıfır örnekler dahil tabloda bulunur.

## Dosyalar

**Kaynak bazında arşiv:** [Endeks ve döviz arşiv indeksi](kaynak-arsivi/README.md).

- [hisse-ozet.csv](hisse-ozet.csv): 43.200 satır, tüm 18 kaynak × 100 hisse × iki periyot × altı koşul × iki yanıt; dönem toplamı ve sıçrama filtresiz.
- [risk-table.csv.gz](risk-table.csv.gz): 345.600 satır; buna ek train/validation/test ve sıçrama duyarlılığı. Gzip açılarak CSV filtrelenebilir.
- [source-availability.csv](source-availability.csv): her kaynak ve periyot için bilinen kaynak penceresi sayısı. [target-availability.csv](target-availability.csv): hedef sonuç kapsamı.
- [source-windows.csv.gz](source-windows.csv.gz): kaynak sinyalleri, giriş/çıkış fiyatları, zamanlar ve kaynak-taraflı seçimler. [input-manifest.csv](input-manifest.csv): kullanılan 219 girdi ve SHA-256. [summary.json](summary.json) ve [PLAN.md](PLAN.md): kapsam ve ölçüm sözleşmesi.

Örnek komutlar:

```bash
# XU100 düşmüşken TUPRS, sinyal sonrası 4h
.venv/bin/python -m tools.query_market_context --source IDX_XU100 --target TUPRS --condition down0
# USD/TRY yükselirken tüm hisseler
.venv/bin/python -m tools.query_market_context --source FX_USDTRY --condition up0 --limit 100
# XBANK en az %2 düşüş, eşzamanlı ilişki
.venv/bin/python -m tools.query_market_context --source IDX_XBANK --condition down2 --response same
# Test dönemi ve örnek en az 10; CSV için --csv
.venv/bin/python -m tools.query_market_context --source IDX_DXY --split test --min-n 10
```

Ölçümü yenilemek: `.venv/bin/python -m tools.measure_market_context` (`--root`, `--output` değiştirilebilir). Girdi arşivi veya manifest hash'leri değişirse sonuçlar da değişebilir. Hacim analiz koşulu veya gösterge olarak kullanılmaz.

## Alanlar ve yöntem

- `source_condition`: `down0` / `up0` <0 / >0; `down2` / `up2` ≤−%2 / ≥+%2; `down4` / `up4` ≤−%4 / ≥+%4. Daha az hareketli kurlarda %2/%4 olay sayısı sıfır olabilir; sıfır risk demek değildir.
- `same`: aynı 10 mumdaki hedef hareketi, sinyal bilindiğinde zaten yaşanmıştır. `post_open`: kaynak sinyali nominal kapanışından **kesinlikle sonra** başlayan ilk XU100/target bar açılışından sonraki 10 ortak bar kapanışı; emir gerçekleşmesi garantisi değildir.
- `selected_source_signals`: kaynağa bakılarak hedef sonucundan bağımsız seçilen ve her dönem içinde çakışmayan olaylar. `n` bunlardan hedef sonucu bilinenler. `negative_count`, `flat_count`, `positive_count` sırasıyla <0/=0/>0; toplamı n. `down3_count` ≤−%3 alt kümesidir.
- `available_baseline_*`: kaynak değeri bilinen pencereler arasından, hedef sonucuna bakılmadan kronolojik sabit çakışmasız 10-mum ızgarası seçilir; `available_baseline_n`, `available_baseline_negative_count` ve `available_baseline_negative_rate` hesaplanan sonuçları gösterir. `available_negative_rate_difference` koşullu oran eksi bu bazdır.
- `baseline_*`: önce tüm XU100 pencerelerinde sabit ızgara seçilir, sonra kaynak bilinmeyenler çıkarılır. Önceki emtia çalışmasındaki bazla aynı seçme düzenidir; BIST 4h seans saatleri yüzünden çok seyrek kalabilir (örneğin TUPRS/XU100 `post_open` toplam 6). İki baz farklı zamanları örnekler, birbirinin yerine kullanılmaz. İkisi de şoklarla aynı tarihlerden eşleştirilmiş veya nedensel kontrol değildir; kaynak-seçimli baz da geleceğe yönelik bir güven garantisi değildir.
- `risk_flag`: n≥10 ve düşüş oranı ≥%70 ise `tarihsel_uyari`, n≥10 ama oran düşükse `esik_altinda`, aksi `ornek_yetersiz`. Bu eşikler keyfidir; `sample_status` ifadesi yalnız n≥10 olduğunu belirtir, istatistiksel güvenilirlik sertifikası değildir. `same` bayrağı yalnız geçmiş eşzamanlı ilişkiye aittir.
- `jump_filter=no_jump10`: kaynak penceresinde %10 üzeri gözlenen saatlik kapanış sıçramalarını içermeyen ayrı duyarlılık seçimi; sıçramalar otomatik veri hatası sayılmaz. Üç dönem ve toplamda seçili/geçerli sayılar ayrı tutulur; toplam, dönem oranlarının ortalaması değil sayıların toplamıdır.

## Kapsam ve sınırlamalar

Saatlik kaynağın sadece ilgili uç anlarında bilinen en son kapanışı kullanılır; en fazla 90 dakika eski olabilir. Bu kural sinyalden sonra gelen veriyi kullanmayı önler ama BIST ve küresel seanslar farklıdır. Örneğin 4h XU100 kaynak değişimi 471 pencereden 232'sinde (%49,3) bilinirken, S&P 500, Nasdaq ve Dow kaynaklarının bu kuralla **0/471** penceresi hesaplanabildi. 1h S&P için 143/2.215 (%6,5). Bu “etkileri yok” değil, bu eşleştirmeyle veri uygun değil demektir; daha sonra seansları dikkate alan farklı bir ölçüm ayrı planlanmalıdır. USD/TRY 4h 471/471 kaynaktır; hedefin ileri sonucu ayrıca eksik olabilir.

Kullanılan barların nominal kapanış/seans semantiği, fiyat düzeltmeleri, takvim, ham OHLC ve endeks/fiyat kaynakları sonucu etkileyebilir. Kaynak ve hedef geçmişte örtüşen piyasa olaylarını paylaşabilir; yüksek n bağımsız olay garantisi değildir. Sektör üyelikleri henüz eşlenmedi ve otomatik bir sektör ataması yapılmadı. Çoklu tarama, yaklaşık bir yıllık gözlemlenmiş veri ve tarihsel BIST üyeliği belirsizliği yüzünden güçlü gözüken ilişkiler bile keşifseldir. Farklı kaynakların oranları toplanmaz/çarpılmaz. Yatırım tavsiyesi, canlı veri veya alım-satım kararı değildir.
