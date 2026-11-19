# İleri gözlem hazırlığı ve yerel arşiv

**19 Kasım 2026 · Durum: `blocked_data`.** Bu hazırlık dondurulmuş dip ileri motorunu veya kilidi değiştirmez. Kilitli ileri gözlem **dip deneyidir; P6 için ileri gözlem sistemi kurulduğu anlamına gelmez**. Yeni piyasa verisi, gerçek emir, işlem getirisi ya da harici zaman damgası üretmez.

## Yapılanlar

- [Yerel arşiv](../../../data/forward-archives/forward-baseline-20261119.tar.gz) ve [SHA-256 dosyası](../../../data/forward-archives/forward-baseline-20261119.tar.gz.sha256) üretildi. Arşiv boyutu **2.424.836 bayt**, SHA-256:

  `daac3f044af9f1aae562d10b79292609f2138b585fb37e613b711714f5a5db79`

- Arşivde özgün kilit, **202 ısınma fiyat CSV'si**, **101 fiyat-politikası manifesti**, sekiz kilitli plan/kod dosyası ve ilk kesitin manifestiyle altı çıktısı vardır. Geri kalan beş yardımcı dosyanın hash'leri arşiv manifestinde yazılıdır; yardımcı dosyalar özgün kilidin kod kapsamına dahil değildir. Diğer OHLCV periyotları, harici geçmiş veri ve yeni ileri veri arşive dahil değildir.
- Arşiv, içindeki her dosya için SHA ve özgün kilit/ilk kesit ilişkileri bakımından **çıkarılmadan doğrulandı**. Ayrıca ayrı, geçici bir dizine geri yüklenerek 202 seriyle `verify_freeze`, ilk kesit zinciri ve veri olmayan durumda `blocked_data` sonucu denendi. Bu prova üretim kesiti değildir.
- Python **3.11.2**, pandas **3.1.1**, NumPy **2.4.6** ile kilitli ortam yeniden kuruldu. Sanal ortamın kendisi kalıcı saklama değildir; aşağıdaki komutla tekrar kurulabilir.
- [Güncel ön-kontrol raporu](preflight-2026-11-19-v3.json), 19 Kasım 17:32 UTC itibarıyla ilk kesit öneklerini ve 202 kilitli girdiyi doğruladı. **Yeni veri dosyası 0/202**, yeni uygun hisse barı **0**, beklenen bar takvimi **bilinmiyor**; kurumsal işlem durumu da yeni veri olmadan bilinmiyor. İlk ileri kesit hâlâ `blocked_data`. [17:17](preflight-2026-11-19.json) ve [17:29 UTC](preflight-2026-11-19-v2.json) raporları tarihçe için korunur; araç daha sonra iyileştirildiği için sonraki işlemde kullanılmamalıdır.
- [İzole indirme ayarı](../../../config/forward-settings.example.json) ağa çıkmadan sınandı: mevcut fiyat politikası, 202 kilitli seri kimliği ve üretilecek `series.json` hash'leriyle eşleşiyor, bütün çalışma yolları yeni veri kökünde. [Toplama/türetme bağlamının hash listesi](ingestion-context.sha256) ayrıca kaydedildi; bu liste özgün kilidin parçası değildir. Canlı sağlayıcı uyumluluğu sınanmadı.

**Önemli:** Arşivin 19 Kasım 17:10 UTC'de, ileri başlangıçtan önce üretildiği **yerel saat kaydıdır**. Bu saat ve yerel hash bağımsız zaman damgası veya değiştirilemez saklama değildir. Arşiv ve SHA dosyası Git'e eklenmez; bunları ayrıca güvenli bir yere kopyalayıp bağımsız zaman damgası sağlamak gerekir. Henüz dışarıya yayınlanmadı. `data/ohlcv/`, `data/forward-archives/`, `data/forward-ohlcv/` ve `data/forward-observations/` Git dışında kalır.

## Hemen gerekli olanlar

1. **Özgün kilidi yeniden oluşturmayın.** Mevcut `forward-freeze.json` ve ısınma dosyalarının yerini değiştirmeden arşivi ve SHA dosyasını çalışma alanı dışında da koruyun. İleri başlangıç **20 Kasım 00:00 İstanbul / 19 Kasım 21:00 UTC**.
2. **Yeni veriyi ayrı ağaçta sağlayın.** Kilitli günlük hisselerin son etiketi 12 Kasım 21:00 UTC (13 Kasım İstanbul), 4s hisselerin son etiketi 13 Kasım 10:30 UTC'dir. 13 Kasım sonrasındaki gerçek işlem günleri, ileri başlangıç öncesi ısınma boşluğu dahil doğrulanmalıdır. Bu ortamın Yahoo'ya doğrudan ağ erişimi yoktur; veri, erişimi olan bir ortamdan sağlanmalıdır.
3. **Takvim ve fiyat politikasını doğrulayın.** Dosyalar ve `series.json`, kilitli varlık/seri/periyot ve fiyat politikasıyla uyumlu olmalıdır. Bir manifesti kopyalamak tek başına sağlayıcı veya fiyat doğrulaması değildir. Tam/kısmi 4s barlar, tatiller, eksik seanslar ve split/temettü kayıtları ayrıca incelenmelidir.
4. **Yalnız ön-kontrol ve insan incelemesinden sonra yeni kesit oluşturun.** Motorun kaydettiği zaman, hesaplamanın başlatıldığı gerçek saattir; çıktıların tamamlanma veya yayımlanma zamanı değildir. Yeni kurala veya farklı-hisse kontrolüne geçilirse bu, mevcut kilit değiştirilmeden ayrı bir ileri protokol gerektirir.

## Giriş zamanlamasında önemli sınırlama

Kilitli motor, bar etiketinden **günlükte 24 saat**, **4s'te 4 saat** geçmeden barı uygun kabul etmez; zamanında kayıt bayrağı da kaydın giriş barı **etiketinden** geç olmamasını ister. İç tarihsel 100 hisse üzerinde bütün ardışık tam bar çiftlerinin etiketleri tarandığında:

| Periyot | Sonraki kullanılabilir bar çifti | Olgunlaşma ile sonraki giriş etiketi arasında sıfır pencere |
|---|---:|---:|
| Günlük | 24.995 | 19.296 (%77,20) |
| 4s | 49.654 | 24.677 (%49,70) |

Sıfır pencere, bu muhafazakâr **etiket kuralında** ancak tam zaman eşitliğinin bayrağı geçebileceği anlamına gelir; fiilî borsa açılışı veya gerçekleşebilirlik ölçümü değildir. Bunlar **tüm bar çiftleri**, A sinyali veya ileri sonuç sayıları değildir. Tarihsel örnekte bir bar daha gecikmeli giriş pencereleri pozitifti; gelecekte de böyle olacağı garanti edilmez. Dönem başından geriye dönük sinyal doldurmak veya bayrağı gevşetmek yasaktır. Bu sınırlama gelecekte `next_open` örneğini azaltabilir ve seçilim yaratabilir; sonuçları yorumlarken açıkça raporlanmalıdır.

**Ek kayıt sınırı:** Kilitli motor `recorded_at_utc` / `first_observed_at_utc` değerini komutun **başında**, hesaplama ve çıktı dosyalarının yazımı tamamlanmadan alır. Dolayısıyla `registered_before_entry_label=true` tek başına sinyal dosyasının girişten önce var olduğunu kanıtlamaz; işlem birkaç dakika sonra bitmiş olabilir. `outcome_summary_timely.csv` de yalnız bu motor bayrağına dayanır ve bağımsız kayıt kanıtı olarak kullanılmamalıdır. Her sinyalin ilk bulunduğu tamamlanmış kesiti ve hash'ini giriş etiketinden önce haricen zaman damgalayın; kanıt yoksa zamanında kaydedilmiş saymayın. Bu daha sıkı değerlendirmeyi orijinal bayrağı koruyarak ayrı raporlayın. Aşağıdaki kesit doğrulaması yerel `verified_at_utc` zamanı kaydeder, fakat yerel saat dış kanıt değildir.

## Ortamı ve arşivi yeniden doğrulama

```bash
# Depo kökünde; Python 3.11.2 gerekir. .venv sonraki ortamda kaybolabilir.
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt \
  -r research/measurements/dip-research/requirements-forward.txt

.venv/bin/python -m tools.archive_forward_research verify \
  --archive data/forward-archives/forward-baseline-20261119.tar.gz

# Alternatif olarak SHA dosyasını kendi dizininde kontrol edin.
(cd data/forward-archives && sha256sum -c forward-baseline-20261119.tar.gz.sha256)

.venv/bin/python - <<'PY'
from pathlib import Path
from tools.forward_dip_research import verify_freeze
m = verify_freeze(Path('research/measurements/dip-research/forward-freeze.json'), Path('data/ohlcv'))
print('Doğrulanan seri:', len(m['baseline_files']))
PY
```

Doğrulama, yerelde bulunan arşiv ve SHA dosyasının tutarlılığını gösterir. Saldırgan ikisini birlikte değiştirebilir; haricen önceden kaydedilmiş, güvenilir bir hash ile karşılaştırmak bağımsız koruma için gereklidir. Arşivi geri yüklerken önce güvenilir hash'i ve içeriği doğrulayın; ayrı ve boş bir dizine çıkarın.

## Yeni veri ve ön-kontrol

Yeni veriyi `data/forward-ohlcv/` altında özgün göreli yollarla sağlayın. Örneğin bir hisse için `bist_equities/BIST_AEFES/<series_id>/series.json` ve `bars/1d.csv`, `bars/4h.csv`; ayrıca XU100'ün aynı yapıdaki dosyaları gerekir. Dosyalar yalnız yeni veya eski+yeni satırları içerebilir: kilitli ısınmadan sonraki ve kesit saatinde olgunlaşmış satırlar kullanılır. Yeni CSV `ts_utc` etiketleri açık UTC ofseti içermelidir. Sağlayıcının eski fiyat düzeltmeleri otomatik olarak içeri alınmaz. Donmuş ısınma ağacını güncellemeyin.

**Varsayılan `run.py` ayarları eski `data/ohlcv` üzerine yazar; bunları ileri veri için kullanmayın.** Yahoo erişimi olan ayrı bir ortamda örnek ayar `--config config/forward-settings.example.json` ile seçilmelidir. Örnek ayar tüm 125 katalog varlığını planlar; gözlem için kilitli 100 hisse ve XU100'ün iki periyotta tamamı gerekir. Düşük istek sınırında indirme eksik kalabilir; ağ erişimi ve Yahoo koşulları kullanıcı tarafından sağlanmalı, indirme raporları ve kapsam incelenmelidir. Bu hazırlıkta canlı istek yapılmadı.

```bash
# İsteğe bağlı: toplama bağlamında yerel değişiklik olup olmadığını ve ağsız planı kontrol edin.
sha256sum -c research/measurements/forward-preparation/ingestion-context.sha256
.venv/bin/python run.py --check --config config/forward-settings.example.json

# Yalnız Yahoo erişimi/izni olan ortamda, kullanıcı isterse; bütçe örnektir.
.venv/bin/python run.py --config config/forward-settings.example.json --max-requests 20
```

İndirmeler ve 4s türetimi bittiğinde ön-kontrol/gözlem sırasında yeni veri dosyalarını güncellemeyin. Her takip kesitinden sonra, yeni veri eklenmeden önce önceki kesit ve hash'leri korunmalıdır. Aynı sağlayıcıdan gelen ileri veri farklı bir sağlayıcı doğrulaması sayılmaz.

**4s türetim sınırı:** Özgün kilit nihai 4s CSV'lerini sabitler, fakat `replayman/resample.py`, ham 1s girdileri ve indirme kodu özgün kilitte veya ana arşivde değildir. Şu anki kod, gün içindeki sıralı 1s barları dörderli gruplayıp dört kayıt varsa `complete=true` işaretler; dört kaydın gerçekten ardışık ve seansa uygun olduğunu tek başına kanıtlamaz. Yukarıdaki ek hash listesi yalnız 19 Kasım'da yerel olarak görülen toplama bağlamını kaydeder; geçmiş verinin nasıl üretildiğinin veya harici ön kaydın kanıtı değildir. Ham 1s etiketlerini, gruplamayı ve sağlayıcı düzeltmelerini bağımsız inceleyin.

Ön-kontrol; kilit/ortamı, önceki kesit çıktılarını ve veri öneklerini, yeni seri kimliğini, fiyat politikasını, sıralamayı, bozuk OHLC'yi, tamamlanma bayraklarını ve görünen kurumsal işlemleri inceler. 4s girdide ayrıca `derived_from=1h`, `expected_bars=4`, `bar_count` ve `complete` tutarlılığını zorunlu tutar; bu, özgün motoru değiştirmeyen ek ve muhafazakâr bir ön-kontroldür. Kullanıcıdan alınan beklenen etiketlerle eksik/fazla barları ayrıca karşılaştırır. Takvim yoksa eksik sayısını **sıfır değil, bilinmiyor** yazar. Kurumsal işlem veya kayıtları belirsizse `blocked_corporate_actions` üretir; engeller giderilip etkiler belgelenmeden gözleme geçmeyin, gerçek işlemi veriden silerek engeli aşmayın. Program çıktısı ve kullanıcı takvimi piyasa kaynağının doğruluğunu veya ham 1s barların doğru türetildiğini garanti etmez.

Beklenen **tam kullanılabilir bar etiketleri** için kaynak ve kapsamı belirtilmiş bir JSON hazırlanır. Aşağıdaki yalnız biçim örneğidir, gerçek BIST takvimi değildir; boş listeleri veri yerine kullanmayın:

```json
{
  "schema_version": 1,
  "source": "Doğrulanan kaynak ve bar türetme yöntemi",
  "coverage_start_utc": "2026-11-12T21:00:00Z",
  "coverage_end_utc": "2026-11-30T00:00:00Z",
  "labels": {"1d": [], "4h": []}
}
```

Etiketler UTC ofsetli, tekil ve sıralı olmalı; takvim kapsamı kilitli son etiketten kesit saatinin sonrasına uzanmalıdır. 4s listesi resmî seans saatlerinden ibaret değildir: kullanılan türetme/tam-bar kuralına göre beklenen etiketler ayrıca doğrulanmalıdır. Takvimin sağlanması onu otomatik olarak bağımsız doğrulanmış yapmaz.

```bash
# İsimleri benzersiz tutun; ön-kontrol sonucu var olan dosyayı ezmez.
PRE=data/forward-observations/preflight-unique.json
PREV=research/measurements/dip-research/forward-initial
SNAP=data/forward-observations/unique-first-snapshot
.venv/bin/python -m tools.preflight_forward_observation \
  --new-root data/forward-ohlcv --previous "$PREV" \
  --calendar path/to/verified-labels.json --output "$PRE"
```

Program engel varsa durum ve nedenleri yazarak **2** koduyla çıkar; uygun göründüğünde bile `manual_review_required` der, başarı veya işlem onayı vermez. Engelleri ve doğrulanmamış noktaları insan incelemesiyle ele alın; veri veya takvim değişirse yeni ön-kontrol yapın. Bir sonraki kesitten önce takvim kapsamı ve önceki kesit öneki tekrar kontrol edilmelidir.

**Ön-kontrol ve gözlem atomik değildir.** İndirici kapalıyken, onaylanan ön-kontrolün `as_of_utc` değerini özgün motora aynen geçirin; böylece arada olgunlaşan ama henüz kontrol edilmemiş barlar kesite girmez. Bu seçenek motorun başlangıç zamanı alanını geriye almaz; fakat yukarıda açıklandığı gibi çıktıların gerçekten hazır olduğu zamanı da kanıtlamaz. Kontrol tamamlanıp insan tarafından incelendikten sonra:

```bash
ASOF=$(.venv/bin/python -c 'import json,sys; print(json.load(open(sys.argv[1]))["as_of_utc"])' "$PRE")
.venv/bin/python -m tools.forward_dip_research observe \
  --freeze research/measurements/dip-research/forward-freeze.json \
  --warmup-root data/ohlcv --new-root data/forward-ohlcv \
  --previous "$PREV" --as-of "$ASOF" --output "$SNAP"

# Kesitteki gerçek giriş SHA'ları, sayılar, önceki kesit ve as-of ile ön-kontrolü karşılaştırın.
.venv/bin/python -m tools.verify_forward_snapshot_preflight \
  --preflight "$PRE" --snapshot "$SNAP" --previous "$PREV" \
  --output data/forward-observations/verification-unique.json
```

Doğrulama başarısızsa o kesiti araştırma sonucu olarak kullanmayın; farkın nedenini çözmeden ve yeni, benzersiz bir kesitle zinciri yeniden kontrol etmeden devam etmeyin. Doğrulama yalnız kaydedilen dosya hash'lerini/kapsamı karşılaştırır; eşzamanlı değişikliklere karşı atomiklik, bağımsız veri, harici zaman damgası veya işlem kanıtı sağlamaz.

Daha sonraki kesitte `--previous` olarak **bir önceki geçerli gerçek kesit** kullanılır. Yalnız hash değil, o kesitte gerçekten kullanılan yeni CSV'leri, ilgili `series.json`, mümkünse ham 1s verisini, takvimi, ön-kontrolü ve doğrulama raporunu da kesitle birlikte güvenle saklayın; indirme düzeltmeleri eski dosyaları değiştirebilir. Her kesit ve hash'i ayrıca kalıcı ve mümkünse haricen zaman damgalı saklanmalıdır. Gerçek veri, seans doğrulaması ve yeterli olgunlaşmış örnek gelmeden deney sonuçlandırılamaz.

## Doğrulama kapsamı

Bu hazırlıkta arşiv, ön-kontrol ve kesit eşleştirmesi için sentetik hata, yinelenme, zaman dilimi, fiyat-politikası, kısmi bar, 4s türetim tutarlılığı, takvim boşluğu, kurumsal işlem, önceki önek değişikliği, değişmiş giriş ve sıfır kayıt penceresi testleri eklendi. Tam test paketi **214 geçti**, `pip check` ve `git diff --check` başarılıdır. Bunlar bağımsız piyasa verisi, dış zaman damgası veya strateji başarısı doğrulaması değildir.
