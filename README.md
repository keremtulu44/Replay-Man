# Replay-Man — Yahoo Veri İndirme Sistemi

BIST odaklı replay/araştırma havuzu için **tek Python komutuyla çalışan**, beklemeli, yeniden denemeli ve kaldığı yerden devam eden veri indirici.

Bu sürümün kapsamı:

- `data/universe.csv` içindeki **125 etkin varlık**: 100 BIST 100 hissesi, 10 BIST endeksi, 6 küresel endeks/gösterge, 2 döviz, 5 maden vadeli, 2 petrol vadeli.
- Varsayılan geçmiş: **1 yıl**.
- Varsayılan periyotlar: **1 saat (`1h`) + 1 gün (`1d`)**.
- Saatlik veriden **2s / 4s / türetilmiş günlük** üretimi.
- SQLite görev kuyruğu, disk önbelleği, CSV fiyat çıktıları ve raporlar.

> Bu bir canlı alım-satım sistemi değildir. Yahoo/yfinance araştırma amaçlıdır; veri uygunluğu sembol bazında değişebilir. `yfinance`, Yahoo ile bağlantılı/resmî olarak onaylı bir ürün değildir ve Yahoo kullanım koşullarına uyulmalıdır.

---

## Hızlı kurulum

Python **3.11+** önerilir.

### Windows

PowerShell veya CMD içinde proje klasöründe:

```bat
python -m venv .venv
.venv\Scripts\python.exe run.py --install
.venv\Scripts\python.exe run.py --check
.venv\Scripts\python.exe run.py --limit 3 --interval 1d
.venv\Scripts\python.exe run.py
```

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python run.py --install
.venv/bin/python run.py --check
.venv/bin/python run.py --limit 3 --interval 1d
.venv/bin/python run.py
```

Sanal ortam oluşturmadan da kurabilirsiniz:

```bash
python run.py --install
python run.py
```

İlk gerçek uygunluk testi için önerilen sekiz sembol:

```text
ASELS,THYAO,XU100,TRY=X,^GSPC,DX-Y.NYB,GC=F,BZ=F
```

Bu test canlı ağ erişimi gerektirir ve **henüz yapılmadı**. Tam havuzdan ayrı `--config` dosyasında `cache_dir`, `output_dir`, `derived_dir`, `report_dir`, `state_path`, `lock_path` ve `log_dir` yollarını izole edin; göreli yollar depo köküne göre çözülür. Önce yalnızca `1d`, düşük `--max-requests` bütçesiyle; günlük sonuçlar uygunsa aynı izole ortamda `1h` denenmelidir. Örnek seçimi ağa çıkmadan doğrulamak için:

```bash
python run.py --check --symbols 'ASELS,THYAO,XU100,TRY=X,^GSPC,DX-Y.NYB,GC=F,BZ=F' --interval 1d
```

E03–E06 veri sözleşmesi bulguları ve canlı uygunluk kontrolleri tamamlanmadan tam havuzu araştırma için onaylanmış kabul etmeyin. `python run.py` tüm etkin varlıkların indirmesini başlatır; yukarıdaki kurulum örneği bir veri kalitesi onayı değildir.

---

## Komutlar

```bash
python run.py --install        # bağımlılıkları kur
python run.py --check          # ağa çıkmadan katalog/ayar/görev planını doğrula
python run.py                  # tüm etkin varlıkları indir/sürdür
python run.py --status         # son rapor özetini göster
```

Seçici indirme:

```bash
python run.py --symbols ASELS,THYAO,XU100
python run.py --symbols GC=F,BZ=F,TRY=X
python run.py --limit 10
python run.py --interval 1h
python run.py --interval 1d
```

Yeniden deneme ve devam:

```bash
python run.py                  # tamamlanan görevleri atlar, bekleyenleri sürdürür
python run.py --retry-failed   # geçici/hız sınırı kaynaklı başarısız görevleri yeniden kuyruğa al
python run.py --max-requests 50
```

Kilit dosyası kaldıysa ve **başka indirici çalışmadığından eminseniz**:

```bash
python run.py --force-unlock
```

---

## Çıktılar

| Yol | İçerik |
|---|---|
| `data/prices/<asset_id>/<series_id>/series.json` | Enstrüman ve fiyat politikası manifesti |
| `data/prices/<asset_id>/<series_id>/1h.csv` | Saatlik OHLCV + temettü/bölünme kolonları |
| `data/prices/<asset_id>/<series_id>/1d.csv` | Günlük OHLCV + temettü/bölünme kolonları |
| `data/derived/<asset_id>/<series_id>/2h.csv` | 1s veriden türetilmiş 2s |
| `data/derived/<asset_id>/<series_id>/4h.csv` | 1s veriden türetilmiş 4s |
| `data/derived/<asset_id>/<series_id>/1d_from_1h.csv` | 1s veriden türetilmiş günlük |
| `data/derived/<asset_id>/<series_id>/daily_comparison.csv` | Native günlük ile türetilmiş günlük karşılaştırması |
| `data/reports/latest.md` | İnsan-okunur son rapor |
| `data/reports/summary.json` | Makine-okunur özet |
| `data/reports/tasks.csv` | Seçili varlık/seri/periyot görevleri, deneme sayıları, sonraki deneme zamanları |
| `data/reports/errors.csv` | Seçili kapsamdaki hatalı/başarısız görevler |
| `data/reports/coverage.csv` | Seçili varlık/seri/periyot kapsama özeti |
| `data/state.sqlite3` | Görev kuyruğu ve kaldığı yerden devam durumu |
| `data/cache/` | Yahoo yanıt önbelleği |
| `logs/replayman.log` | Çalıştırma günlüğü |

CSV fiyat kolonları:

```text
ts_utc, session_date, open, high, low, close, adj_close, volume,
dividends, stock_splits, capital_gains,
asset_id, series_id, symbol, interval, currency, source,
auto_adjust, back_adjust, repair, adj_close_source, exchange_timezone,
timestamp_basis, session_date_basis, fetched_at
```

Varsayılan olarak `auto_adjust=false`: ham OHLC korunur, sağlayıcının verdiği `adj_close` ayrı tutulur. Sağlayıcı `adj_close` vermezse veya NaN/sonsuz değer verirse `close` kopyalanmaz; değer boş kalır ve `adj_close_source=missing` yazılır. Sağlayıcının ilettiği sembol/para birimi/enstrüman türü uyuşmazlığı reddedilir; eksik metadata doğrulanmış sayılmaz. `POINTS` katalog biriminin para birimi/birim anlamı ayrıca doğrulanacaktır. Naive timestamp ancak sağlayıcı borsa zaman dilimi varsa yorumlanır; yoksa reddedilir.

`series_id`; sembol, varlık sınıfı, katalog para birimi ve fiyat politikasının SHA-256 kimliğidir. Sembol veya `auto_adjust/back_adjust/repair/keepna/actions/prepost` değişirse yeni dizin ve yeni görev kuyruğu oluşur; eski seri silinmez. Seri kimliği olmayan eski SQLite görevleri `tasks_legacy_v1` tablosunda korunur ve yeni seriye otomatik `complete` olarak taşınmaz. Eski `/data/prices/<asset_id>/1h.csv` düzenindeki dosyalar da yerinde bırakılır; yeni düzen sürümlü dizindir.

`--symbols`, `--limit`, `--interval` ve `--retry-failed` yalnızca seçili varlık/seri/periyot görevlerini etkiler. `task_counts` seçili koşuyu, `queue_task_counts` tüm veritabanını gösterir. `coverage.csv` yalnızca seçili kapsamı içerir; `task_rows` görev satırları toplamıdır, benzersiz fiziksel CSV satır sayısı değildir.

**Henüz açık olan veri sözleşmesi riskleri:** Seans takvimi ve öğle arası varsayımı doğrulanmadı; `session_date` şimdilik takvim günü etiketidir. 2s/4s `complete` alanı yalnızca mevcut saat sayısı varsayımını kontrol eder; seans takvimiyle doğrulanmış kabul edilmemeli. Açık bar/refresh (E05), vadeli işlem günü (E04), günlük karşılaştırma kapsamı (E06), kalıcı erişim engeli (E08), atomik kilit (E09), önbellek çifti (E10) ve kesinti/rapor garantileri (E12) henüz tamamlanmadı. Bu nedenle tam havuz araştırma verisi olarak onaylanmış değildir.

---

## Bekleme, yeniden deneme ve bot korumasına saygı

Sistem **engeli aşmaya çalışmaz**; istekleri sınırlar ve erişim engeliğinde durur.

Varsayılan korumalar:

- Tek iş parçacığı / sıralı indirme.
- Her ağ isteği arasında **2,5 sn + 0–0,5 sn jitter**.
- Saatlik ağ isteği bütçesi: **1200 istek/saat**; bu sınır dolarsa boşluk açılana kadar beklenir.
- Çalıştırma başına ağ isteği bütçesi: **2500 istek**.
- İstek başına zaman aşımı: **en fazla 15 sn** (bağlantı/okuma zaman aşımları, toplam işlem süresi garantisi değildir).
- Geçici hatalarda üstel yeniden deneme: **10 sn → 20 sn → … → en fazla 120 sn**; diğer hazır görevler önce işlenebilir.
- Görev başına en fazla **3 ağ denemesi**.
- HTTP **429**: ilk yanıtın ardından işlem beklemede tutulmaz, `blocked` durumuyla durur. `Retry-After` ve en az **30 dk cooldown** kaydedilir; süre dolmadan yeniden çalıştırmak istek göndermeden durur. Süre dolunca komutu tekrar çalıştırın. Eski `rate_limit_strike_limit` ayarı geriye dönük yüklenebilir ama artık kullanılmaz.
- HTTP **401/403**: mevcut çalıştırma erişim reddedildi olarak durdurulur; CAPTCHA/proxy/kimlik taklidi denenmez. Yeni çalıştırmalar arası kalıcı erişim engeli henüz yoktur (E08); reddedilme sonrası tekrar zorlamayın.
- Art arda **6 geçici hata**: devre kesici açılır.
- Aynı anda ikinci indiriciyi engellemeyi amaçlayan kilit dosyası; eşzamanlı başlatma yarışı henüz giderilmedi (E09). İki indirici başlatmayın.
- Atomik CSV yazımı ve SQLite görev durumu.
- Tamamlanan görevler tekrar indirilmez; disk önbelleği kullanılır. Önbellek çifti atomik değildir (E10). Pickle dosyaları yalnızca güvenilir yerel dosya olmalıdır; dışarıdan alınan önbelleği yüklemeyin.

Ayarlar: `config/settings.json`.

Örnek daha yavaş profil:

```json
{
  "min_request_interval_seconds": 10,
  "jitter_seconds": 3,
  "max_requests_per_hour": 120,
  "max_requests_per_run": 500
}
```

Bu değerler erişim garantisi vermez. Yahoo hız sınırı/erişim politikası değiştirirse sistem raporlayıp durabilir.

---

## Zaman dilimi ve türetme mantığı

- Saatlik istekler 55 günlük parçalara bölünür.
- Günlük veri ayrı çekilir.
- BIST için 2s/4s türetimi `Europe/Istanbul` seansına göre yapılır:
  - 2s sınırları: 10:00, 12:00, 14:00, 16:00.
  - 4s sınırları: 10:00, 14:00.
  - Mevcut, **doğrulanmamış** öğle arası varsayımı 12:00–14:00 arasıdır. `bar_count` ve `expected_bars` yalnızca sayı karşılaştırır; `complete` yanlış/eksik saat kimliklerini veya yarım günü güvenilir biçimde ayırt etmez (E03/E04).
- BIST olmayan varlıklarda UTC tabanlı genel birleştirme kullanılır; bu, doğrulanmış borsa işlem günü değildir.
- Türetilmiş günlük ile native günlük `daily_comparison.csv` içinde karşılaştırılır. Şimdilik yalnızca ortak günlerde close/hacim karşılaştırılır; eksik günler ve OHLC farkları için E06 açıktır. Bu rapor tam doğrulama yerine geçmez.

Önemli: **Günlük veriden saatlik/dakikalık veri üretilmez.** Bu sürüm dakikalık veri indirmez.

---

## Katalog ve sembol ekleri

Katalog: `data/universe.csv`.

Yahoo sembolleri otomatik uydurulmaz; katalogdaki `yahoo_symbol` aynen kullanılır. Örnekler:

- BIST hisse/endeks: `ASELS.IS`, `XU100.IS`, `XBANK.IS`
- USD/TRY: `TRY=X`
- EUR/TRY: `EURTRY=X`
- DXY: `DX-Y.NYB`
- Altın vadeli: `GC=F`
- Brent: `BZ=F`
- WTI: `CL=F`
- S&P 500: `^GSPC`
- VIX: `^VIX`

BIST 100 listesi 13 Kasım 2026 tarihli ikincil kaynak anlık listesidir; resmî dönemsel üyelik listesi değildir. Endeks üyeleri zamanla değişebilir. Vadeli emtialar sürekli kontrat/rollover etkisi taşıyabilir; spot/gram altınla aynı seri değildir.

---

## Testler

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Testler ağa çıkmaz. Katalog, ayarlar, OHLC doğrulama, mevcut BIST seans varsayımı, SQLite retry/resume, istek bütçesi, cooldown, 401/403/429 davranışı ve önbellek kontrol edilir. Gerçek yfinance akışı sahte HTTP yanıtlarıyla ayrıca sınanır; canlı Yahoo bağlantısı ve Termux uyumluluğu kanıtlanmış değildir. E01/E02/E07 için seçili kuyruk izolasyonu, sembol/politika seri ayrımı, sürümlü türetim, eski görevlerin korunması ve metadata regresyonları da vardır. Bu testler canlı Yahoo uygunluğunu veya henüz doğrulanmamış seans takvimini kanıtlamaz.

---

## Sık durumlar

### `limited`

Çalıştırma istek bütçesi doldu. İlerleme kaydedildi. Aynı komutu tekrar çalıştırın:

```bash
python run.py
```

### `blocked`

Yahoo 401/403 veya 429 döndürdü. Raporu inceleyin:

```bash
python run.py --status
cat data/reports/latest.md
```

Cooldown süresi dolmadan tekrar zorlamayın. Gerekirse `config/settings.json` içinde bekleme sürelerini artırın.

### `completed_with_errors`

Bazı görevler indirildi, bazıları kalıcı/veri yok hatası aldı. `data/reports/errors.csv` ve `coverage.csv` dosyalarına bakın. Yahoo’da sembol/periyot mevcut olmayabilir.

### `incomplete`

Yeniden deneme hakkı olan görevler kaldı. Tekrar çalıştırın veya geçici hatalar için:

```bash
python run.py --retry-failed
```

---

## Bu sürümde olmayanlar

- Dakikalık veri arşivi.
- Supabase senkronizasyonu.
- Canlı replay arayüzü.
- Otomatik strateji keşfi/backtest.
- CAPTCHA çözme, proxy rotasyonu veya cihaz kimliği taklidi.

Sonraki veri katmanı adımı: E03–E12 arasında kalan sözleşme/dayanıklılık düzeltmeleri ve küçük canlı uygunluk testi. Replay/strateji motoru bu paketin kapsamında değildir ve ayrıca kullanıcı onayı gerektirir.
