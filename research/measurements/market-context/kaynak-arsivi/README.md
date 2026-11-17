# Endeks ve döviz kaynak arşivi

Bu klasör mevcut hisse özetini kaynaklara ayırır; hesapları yeniden yapmaz. Her CSV 100 hisseyi, 1h/4h, altı kaynak koşulunu ve aynı dönem (`same`) ile sinyal sonrası (`post_open`) sonuçlarını ayrı içerir. Özette dönem toplamı ve `jump_filter=all` vardır. **Tüm dönemler, sıçrama duyarlılığı ve boş örnekler** [tam tabloda](../risk-table.csv.gz) saklanır.

| Grup | Kaynak ID | Kaynak sembolü | Hisse sonuçları |
|---|---|---|---|
| BIST endeksi | IDX_XBANK | XBANK.IS | [2,400 satır](bist-endeksleri/IDX_XBANK.csv) |
| BIST endeksi | IDX_XHOLD | XHOLD.IS | [2,400 satır](bist-endeksleri/IDX_XHOLD.csv) |
| BIST endeksi | IDX_XU030 | XU030.IS | [2,400 satır](bist-endeksleri/IDX_XU030.csv) |
| BIST endeksi | IDX_XU100 | XU100.IS | [2,400 satır](bist-endeksleri/IDX_XU100.csv) |
| BIST endeksi | IDX_XUHIZ | XUHIZ.IS | [2,400 satır](bist-endeksleri/IDX_XUHIZ.csv) |
| BIST endeksi | IDX_XULAS | XULAS.IS | [2,400 satır](bist-endeksleri/IDX_XULAS.csv) |
| BIST endeksi | IDX_XUMAL | XUMAL.IS | [2,400 satır](bist-endeksleri/IDX_XUMAL.csv) |
| BIST endeksi | IDX_XUSIN | XUSIN.IS | [2,400 satır](bist-endeksleri/IDX_XUSIN.csv) |
| BIST endeksi | IDX_XUTEK | XUTEK.IS | [2,400 satır](bist-endeksleri/IDX_XUTEK.csv) |
| BIST endeksi | IDX_XUTUM | XUTUM.IS | [2,400 satır](bist-endeksleri/IDX_XUTUM.csv) |
| Döviz kuru | FX_EURTRY | EURTRY=X | [2,400 satır](doviz-kurlari/FX_EURTRY.csv) |
| Döviz kuru | FX_USDTRY | TRY=X | [2,400 satır](doviz-kurlari/FX_USDTRY.csv) |
| Küresel gösterge | IDX_DJI | ^DJI | [2,400 satır](kuresel-gostergeler/IDX_DJI.csv) |
| Küresel gösterge | IDX_DXY | DX-Y.NYB | [2,400 satır](kuresel-gostergeler/IDX_DXY.csv) |
| Küresel gösterge | IDX_GDAXI | ^GDAXI | [2,400 satır](kuresel-gostergeler/IDX_GDAXI.csv) |
| Küresel gösterge | IDX_GSPC | ^GSPC | [2,400 satır](kuresel-gostergeler/IDX_GSPC.csv) |
| Küresel gösterge | IDX_IXIC | ^IXIC | [2,400 satır](kuresel-gostergeler/IDX_IXIC.csv) |
| Küresel gösterge | IDX_VIX | ^VIX | [2,400 satır](kuresel-gostergeler/IDX_VIX.csv) |

## Nasıl okunur?

- `target_symbol` hisse; `interval` 1h/4h; `source_condition` kaynak yönü ve eşik; `response` zamanlamadır. `same` kaynakla aynı mumdaki geçmiş harekettir, `post_open` sinyal kapanışından sonraki 10 mumluk vekildir.
- `down0` / `up0`: kaynak <0 / >0; `down2` / `up2`: ≤−%2 / ≥+%2; `down4` / `up4`: ≤−%4 / ≥+%4. Çok küçük yön hareketleri `down0` / `up0` içinde yer alır.
- `negative_count` / `n` düşen / sonucu bilinen olaylar; `selected_source_signals` hedef sonucundan önce seçilmiş olaylardır. `0.70` = %70. `available_baseline_*` ve `baseline_*` farklı çakışmasız ızgaraları kullanır; iki baz da eşleştirilmiş kontrol değildir.
- Düşük veya sıfır n değerleri dosyalardan çıkarılmaz. Özellikle ABD endekslerinde seans uyumu nedeniyle 4h örnekleri sıfırdır; bu, etki bulunmadığını göstermez. `risk_flag` içindeki eşikler keyfidir, otomatik al/sat kararı değildir.

[Ayrıntılı yöntem, veri kapsamı ve sınırlamalar](../README.md) · [Tüm hisse özetleri](../hisse-ozet.csv) · [Dosya kontrol özeti](dosya-kontrol.csv) · [Bütün araştırma arşivleri](../../README.md)

Kaydedilen ölçümler geçmişe yöneliktir; geleceğin kesin olasılığı veya neden-sonuç kanıtı değildir. Canlı fiyat, sektör üyeliği veya birleşik indikatör ekranı içermez. Hacim analiz edilmez.

Arşivi mevcut özetten yeniden oluşturmak: `.venv/bin/python -m tools.organize_market_context`. Ana ölçüm komutu da arşivi yeniler. Özet kaydın girdi dosyaları `data/ohlcv` içindedir; proje tarafından Git'e dahil edilmez, buradaki manifest yalnız yol ve hash bilgisidir. Ham girdi dosyalarını korumak için ayrıca saklamak gerekir.
