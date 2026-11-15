# Replay-Man — Termux'ta adım adım kurulum

> Termux'u Google Play'den değil F-Droid veya resmi GitHub sürümünden kurun. Komutları sırayla çalıştırın. `python run.py` komutunu aynı anda iki terminalde başlatmayın.

## 1. Termux paketlerini hazırlayın

```bash
pkg update -y
pkg upgrade -y
pkg install -y git python clang rust cmake make pkg-config libxml2 libxslt
python --version
```

Python 3.11 veya daha yeni olmalıdır.

## 2. Repoyu indirin

```bash
cd "$HOME"
git clone https://github.com/keremtulu44/Replay-Man.git
cd Replay-Man
```

Repo zaten varsa yeniden klonlamayın:

```bash
cd "$HOME/Replay-Man"
git pull --ff-only
```

## 3. Sanal ortam ve bağımlılıklar

```bash
cd "$HOME/Replay-Man"
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

Her yeni Termux oturumunda projeye dönmek için:

```bash
cd "$HOME/Replay-Man"
. .venv/bin/activate
```

Kurulumda `pandas`, `numpy` veya `curl_cffi` derleme hatası olursa Termux paketlerini güncellediğinizi ve yukarıdaki `clang/rust/cmake` paketlerini kurduğunuzu kontrol edin. Eski Google Play Termux sürümünde devam etmeyin.

## 4. Ağsız yapılandırma kontrolü

```bash
python run.py --check --symbols 'ASELS,THYAO,XU100' --interval 1d
```

Çıktıda `status: check` ve `network_requests: 0` görülmelidir.

## 5. Önce küçük günlük OHLCV testi

```bash
python run.py --symbols 'ASELS,THYAO,XU100' --interval 1d --max-requests 20
```

Sonucu kontrol edin:

```bash
python run.py --status
cat data/reports/latest.md
find data/ohlcv -name '1d.csv' -type f | head
```

Bir CSV'yi görmek için, önce yukarıdaki `find` çıktısındaki gerçek yolu kullanın:

```bash
head -n 5 data/ohlcv/BIST_ASELS/*/bars/1d.csv
```

CSV'de `ts_utc,session_date,open,high,low,close,adj_close,volume` alanları bulunur. Ham OHLC korunur (`auto_adjust=false`); düzeltilmiş kapanış ayrı kolondadır.

## 6. Küçük saatlik test

Günlük test başarılıysa:

```bash
python run.py --symbols 'ASELS,THYAO,XU100' --interval 1h --max-requests 30
python run.py --status
```

Saatlik veri 55 günlük parçalar halinde alınır. Komut bütçe nedeniyle durursa bu hata değildir; aynı komut kaldığı yerden devam eder:

```bash
python run.py --symbols 'ASELS,THYAO,XU100' --interval 1h --max-requests 30
```

## 7. Tam havuzu indirin

Önce yalnız günlük veri:

```bash
python run.py --interval 1d
```

Ardından saatlik veri:

```bash
python run.py --interval 1h
```

Ya da ikisini birlikte sürdürmek için:

```bash
python run.py
```

Termux kapanmasın isterseniz çalıştırmadan önce Android pil optimizasyonunu Termux için kapatın ve:

```bash
termux-wake-lock
python run.py
termux-wake-unlock
```

`termux-wake-lock` yoksa Termux:API uygulaması ve `pkg install termux-api` gerekir; veri indirme için zorunlu değildir.

## 8. Hata ve devam komutları

Geçici başarısız görevleri tekrar sıraya almak:

```bash
python run.py --retry-failed
```

429 hız sınırı görülürse sistemi zorlamayın. Raporda yazan bekleme süresi dolduktan sonra aynı komutu yeniden çalıştırın.

Kilit kaldıysa önce çalışan süreç olup olmadığını kontrol edin:

```bash
pgrep -af 'python.*run.py'
```

Hiç çalışan indirici yoksa:

```bash
python run.py --force-unlock
```

Log ve rapor:

```bash
tail -n 100 logs/replayman.log
cat data/reports/latest.md
python run.py --status
```

## 9. Güncelleme

İndirme çalışmıyorken:

```bash
cd "$HOME/Replay-Man"
. .venv/bin/activate
git pull --ff-only
python -m pip install -r requirements.txt
python run.py --check
```

Veriler `data/` altında kalır. `data/state.sqlite3`, tamamlanan işleri takip eder; devam etmek için bu dosyayı silmeyin.
