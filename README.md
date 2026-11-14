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

İlk gerçek indirme için önce küçük test önerilir:

```bash
python run.py --symbols ASELS,THYAO,XU100,GC=F,BZ=F --interval 1d
python run.py --symbols ASELS,THYAO,XU100,GC=F,BZ=F --interval 1h
```

Sonra tüm havuz:

```bash
python run.py
```

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
| `data/prices/<asset_id>/1h.csv` | Saatlik OHLCV + temettü/bölünme kolonları |
| `data/prices/<asset_id>/1d.csv` | Günlük OHLCV + temettü/bölünme kolonları |
| `data/derived/<asset_id>/2h.csv` | 1s veriden türetilmiş 2s |
| `data/derived/<asset_id>/4h.csv` | 1s veriden türetilmiş 4s |
| `data/derived/<asset_id>/1d_from_1h.csv` | 1s veriden türetilmiş günlük |
| `data/derived/<asset_id>/daily_comparison.csv` | Native günlük ile türetilmiş günlük karşılaştırması |
| `data/reports/latest.md` | İnsan-okunur son rapor |
| `data/reports/summary.json` | Makine-okunur özet |
| `data/reports/tasks.csv` | Tüm görevler, deneme sayıları, sonraki deneme zamanları |
| `data/reports/errors.csv` | Hatalı/başarısız görevler |
| `data/reports/coverage.csv` | Varlık/periyot kapsama özeti |
| `data/state.sqlite3` | Görev kuyruğu ve kaldığı yerden devam durumu |
| `data/cache/` | Yahoo yanıt önbelleği |
| `logs/replayman.log` | Çalıştırma günlüğü |

CSV fiyat kolonları:

```text
ts_utc, session_date, open, high, low, close, adj_close, volume,
dividends, stock_splits, capital_gains,
asset_id, symbol, interval, currency, source, auto_adjust, fetched_at
```

Varsayılan olarak `auto_adjust=false`: ham OHLC korunur, `adj_close` ayrı tutulur.

---

## Bekleme, yeniden deneme ve bot korumasına saygı

Sistem **engeli aşmaya çalışmaz**; istekleri sınırlar ve erişim engeliğinde durur.

Varsayılan korumalar:

- Tek iş parçacığı / sıralı indirme.
- Her ağ isteği arasında en az **5 sn + 0–1.5 sn jitter**.
- Saatlik ağ isteği bütçesi: **200 istek/saat**.
- Çalıştırma başına ağ isteği bütçesi: **1500 istek**.
- İstek zaman aşımı: **25 sn**.
- Geçici hatalarda üstel bekleme: **30 sn → 60 sn → … → en fazla 900 sn**.
- Görev başına en fazla **3 ağ denemesi**.
- HTTP **429**: `Retry-After` varsa dikkate alınır; yoksa en az **30 dk cooldown**.
- HTTP **429 tekrar sınırı**: 2 kez hız sınırı görülürse çalıştırma `blocked` olur.
- HTTP **401/403**: erişim reddedildi olarak durdurulur; CAPTCHA/proxy/kimlik taklidi denenmez.
- Art arda **6 geçici hata**: devre kesici açılır.
- Aynı anda ikinci indiriciyi engellemek için kilit dosyası.
- Atomik CSV yazımı ve SQLite görev durumu.
- Tamamlanan görevler tekrar indirilmez; disk önbelleği kullanılır.

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
  - Öğle arası nedeniyle 12:00–14:00 ve 10:00–14:00 barları eksik saat içerebilir; `bar_count`, `expected_bars`, `complete` kolonları bunu gösterir.
- BIST olmayan varlıklarda UTC tabanlı genel birleştirme kullanılır.
- Türetilmiş günlük ile native günlük `daily_comparison.csv` içinde karşılaştırılır. Uyuşmazlık varsa rapora yazılır; sessizce düzeltilmez.

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

Testler ağa çıkmaz. Katalog, ayarlar, OHLC doğrulama, BIST seans türetimi, SQLite retry/resume, istek bütçesi, cooldown, 401/403/429 davranışı ve önbellek kontrol edilir.

---

## Sık durumlar

### `limited`

Çalıştırma istek bütçesi doldu. İlerleme kaydedildi. Aynı komutu tekrar çalıştırın:

```bash
python run.py
```

### `blocked`

Yahoo 401/403 veya tekrarlayan 429 döndürdü. Raporu inceleyin:

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

Sonraki doğal adım: küçük sembol grubuyla gerçek Yahoo uygunluk testi, ardından tüm havuzun indirilmesi ve replay arayüzüne bağlanması.
