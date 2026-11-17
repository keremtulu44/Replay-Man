# Bölge Hafızası ve Hareket Karakteri — araştırma sonucu

**Durum: Mevcut veriyle keşif taraması tamamlandı; tam planın bazı maddeleri ve bağımsız doğrulama açık.**
Hesaplar 100 mevcut BIST hissesi ve yaklaşık bir yıllık arşiv üzerinde yapıldı. Bu rapor yatırım tavsiyesi, canlı sinyal veya kârlılık kanıtı değildir. Ayrıntılı tanımlar, önceki pilotlar ve açık kalan işler [araştırma README'sinde](README.md); hedef kapsam [planda](../../plans/bolge-hafizasi-hareket-karakteri.md).

## Sonuç: araştırmaya değer bir davranış var, doğrulanmış indikatör yok

Günlük oyalanma bölgelerine dönüşlerde, fiyatın bölge yönündeki son beş mumluk net ilerlemesinin önceki beş muma göre arttığı durumlarda, sonraki beş barın **bölgeye yaklaşım yönüne göre XU100-aşırı medyan getirisi** üç tarihsel bölümde de negatiftir. Bu, ilerlemesi azalan grupta aynı şekilde görülmemiştir. Dört farklı bölge genişliğiyle işaret korunmuştur.

Ancak bu karşılaştırma **sonuçlar incelendikten sonra seçilmiş keşif örneğidir**. Bölge hafızasının tek başına ek değer kattığı gösterilmemiştir; ilk ziyaret grubunda da negatif sonuçlar vardır. Hisse bazında işaretler karışıktır; aynı veri daha önce de incelenmiştir. Dolayısıyla karar **`aday / baglam_gerekli`**, otomatik uyarı veya işlem kuralı değil. Daha geniş ve önceden dokunulmamış tarihçe üzerinde ön-kayıtlı test gerekir.

## Kapsam ve olay sayıları

| Tür | Periyotlar | Hisse | Bölge adayı | Ziyaret | Tek ziyaret/bar |
|---|---|---:|---:|---:|---:|
| Teyitli swinglerden yatay | 1h, 2h, 4h, 1d | 100 | 28.808 | 437.673 | 229.695 |
| Oyalanma | 1h, 2h, 4h, 1d | 100 | 25.601 | 349.005 | 141.095 |
| Hızlı uzaklaşma | 1h, 2h, 4h, 1d | 100 | 29.408 | 391.512 | 154.301 |
| İki teyitli uçtan eğimli | 4h, 1d | 100 | 111.942 | 388.270 | 60.017 |
| İki teyitli uçtan eğimli | 1h, 2h | 100 | 521.602 | 2.773.918 | 287.610 |

Eğimli saatlik taramada kaynak tasarrufu için yalnız sonuçtan bağımsız, deterministik olarak seçilmiş **tek ziyaret/bar** satırları saklandı; diğerlerinde tüm ziyaretler ve seçilen satır işareti saklandı. `inventory.csv` toplam sayıları korur. Aynı mum birden fazla bölge veya çizgiyle kesişebilir; milyonlarca ziyaret milyonlarca bağımsız olay demek değildir. Kullanılabilir `2h/4h` mumlarda kısmi barlar çıkarıldı; bu serilerin `complete` işareti resmî işlem seansını doğrulamaz.

## Örnek bulgu: günlük oyalanma bölgesi

Tanım: sabit `0,25 × ATR` bölge genişliği; en az bir **önceden tamamlanmış ziyaret**; aynı hisse/periyot/mum için bölge kimliğine göre bir ziyaret seçimi. `rising`, önceki 10 kapanışın son beşindeki bölge yönlü net değişimin ilk beşinden büyük olmasıdır; `falling` bunun tersidir. Bu koşul, sürekli hızlanma/yavaşlama veya gerçek emir akışı anlamına gelmez.

Beş barlık yönlü XU100-aşırı getiri = `(hisse getirisi − XU100 getirisi) × yaklaşım yönü`. Fiyat bölgenin altındaysa yön yukarı, üstündeyse aşağıdır. Bu, işlem getirisi değildir; giriş fiyatı, komisyon veya uygulanabilir emir varsayımı içermez.

| Bölüm | İlerleme | XU100 ile eşleşen n | Hisse | Yönlü aşırı medyan |
|---|---|---:|---:|---:|
| Eğitim | Artan | 917 | 99 | −%0,30 |
| Doğrulama | Artan | 548 | 95 | −%0,28 |
| Tarihsel test | Artan | 612 | 91 | −%0,78 |
| Eğitim | Azalan | 680 | 99 | +%0,26 |
| Doğrulama | Azalan | 482 | 95 | +%0,02 |
| Tarihsel test | Azalan | 533 | 93 | +%0,24 |

Bu tabloda `hisse`, sonuç için yeterli hisse sayısını; `n`, XU100 başlangıç ve bitiş etiketleri de eşleşen ziyaret sayısını ifade eder. Benzer ziyaretlerin koşulsuz, tek ziyaret/bar bazında aynı 1+ hafıza grubundaki XU100-aşırı medyanı sırayla **−%0,01 / −%0,14 / −%0,27**'dir. Bu basit baz, aynı tarihte eşleştirilmiş karşı-olgusal değildir.

Artan gruptaki tarihsel testte, en az üç benchmark eşleşmesi olan **74 hissenin 42'sinde** hisse bazlı medyan negatif, 32'sinde pozitiftir. Yani toplu medyan her hisse için geçerli değildir. En az üç gözlem de yüksek güven sağlamaz.

### Bölge genişliği duyarlılığı

Aynı günlük / 1+ hafıza / artan yaklaşım koşulunda, tek ziyaret/bar görünümü:

| Yöntem | Eğitim medyanı | Doğrulama medyanı | Tarihsel test medyanı | Testte eşleşen n |
|---|---:|---:|---:|---:|
| ATR × 0,10 | −%0,39 | −%0,34 | −%0,56 | 635 |
| ATR × 0,25 | −%0,30 | −%0,28 | −%0,78 | 612 |
| ATR × 0,50 | −%0,30 | −%0,36 | −%0,48 | 606 |
| Fiyat × %0,50 | −%0,39 | −%0,36 | −%0,50 | 621 |

Bu varyantlar aynı ziyaretleri bire bir seçmez. Ayrı 4h/1d duyarlılık koşularının ortak dönem sınırları, dört periyotlu temel koşunun sınırlarından birkaç saat farklıdır; tarihler [ilgili summary.json](sensitivity-dwell-atr010/summary.json) dosyalarında kayıtlıdır. İşaret tutarlılığı keşif için ilginçtir fakat tekrarlı denemeler, zaman bağımlılığı ve seçilmiş hipotez nedeniyle istatistiksel kanıt değildir. Tam sayılar ve ilk ziyaret / azalan ilerleme karşılaştırmaları [candidate-evidence.csv](candidate-evidence.csv), basit bazlar [candidate-baseline.csv](candidate-baseline.csv) içindedir.

## Başka bulgular ve sınırlamalar

- 4h ve 1h sonuçları günlükle aynı davranışı zorunlu olarak göstermiyor. Örneğin yatay 4h / en az bir teyitli ek tepki / artan ilerleme grubu için yönlü XU100-aşırı medyan eğitimde −%0,10, doğrulamada +%0,02, testte −%0,13. Birden fazla periyodu tek genel kurala indirgemek uygun değil.
- Yatay bölgelerin ilk-tepki/ek-tepki grupları, eğimli çizgilerin iki-kaynak/sonraki-tepki grupları ve davranış bölgelerinin önceki-ziyaret grupları **farklı hafıza tanımlarıdır**; birbirine doğrudan denk değildir.
- Tüm evren kesiti güncel/anlık hisse listesidir; tarihsel üyelik/survivorship yanlılığı olabilir. Yaklaşık bir yıllık veride sonuç ufukları, hisseler ve piyasa rejimleri birbirine bağlıdır. Hacim, slippage, komisyon, gerçek bar içi sıra ve portföy gerçekleşmesi kullanılmamıştır.
- XU100 yalnızca hisse ve endeks başlangıç ve bitiş bar **etiketleri bire bir eşleşirse** hesaplandı; eksik eşleşmelere ileri veri doldurulmadı. Etiketler gerçek seans kapanışını kanıtlamaz. Eğitim/doğrulama/test ayrımı zaman etiketleriyle %60/%20/%20'dir, ufkun son etiketi bölüm sınırına ulaşan/aşanlar dışlanır. Önceden incelenmiş bu bölümler bağımsız ileri test değildir.

## Çıktılar ve tekrar üretim

- `universe-{horizontal,dwell,impulse,sloped,sloped-hourly}/`: girdi ve benchmark hash manifestleri, bölge/ziyaret envanteri, olay sonuçları, grup ve hisse sonuçları. Saatlik eğimli dizinde yalnız tek ziyaret/bar kayıtları vardır.
- `sensitivity-dwell-{atr010,atr050,pct050}/`: temsilî ziyaretli duyarlılık sonuçları.
- `candidate-evidence.csv`, `candidate-baseline.csv`: aday ve basit kontrol karşılaştırmaları.
- `sources/`: raporlanan evren koşularında kullanılan çalıştırıcının SHA-256 ile bire bir doğrulanmış eski sürümleri. Çekirdek modüllerin hash'leri her sonuç dizinindeki `summary.json` içindedir. Mevcut çalıştırıcının ek CLI parametreleri vardır; orijinal kayıtlar değiştirilmemiştir.

```bash
# Dört periyot, tüm mevcut BIST hisseleri; her komut ilgili dizindeki sonuçları yeniden yazar.
.venv/bin/python -m tools.measure_zone_universe --kind horizontal --output research/measurements/zone-memory/universe-horizontal
.venv/bin/python -m tools.measure_zone_universe --kind dwell --output research/measurements/zone-memory/universe-dwell
.venv/bin/python -m tools.measure_zone_universe --kind impulse --output research/measurements/zone-memory/universe-impulse
.venv/bin/python -m tools.measure_zone_universe --kind sloped --intervals 4h,1d --output research/measurements/zone-memory/universe-sloped
.venv/bin/python -m tools.measure_zone_universe --kind sloped --intervals 1h,2h --representative-only --output research/measurements/zone-memory/universe-sloped-hourly
# Duyarlılık örneği; 0.50 ATR ve 0.005 yüzde diğer ayrı varyantlardır.
.venv/bin/python -m tools.measure_zone_universe --kind dwell --intervals 4h,1d --method atr --tolerance 0.10 --representative-only --output research/measurements/zone-memory/sensitivity-dwell-atr010
.venv/bin/python -m tools.report_zone_evidence --output research/measurements/zone-memory/candidate-evidence.csv
.venv/bin/python -m pytest -q
```

## Açık kalan plan maddeleri

Bu çalışma, araştırma planındaki tüm hedeflerin tamamlandığı anlamına gelmez. Paralel kanallar ve eğimli çizgilerin rastgele çizgi kontrolleri; bölge örtüşme ve bölgeler arası yol motoru; temas sonrası tam yaşam döngüsü; bağımlılığı dikkate alan güven aralıkları ve eşleştirilmiş baz/gerçek ablation; bütün olay/ufukların deney bölümü sınırlarıyla ölçülmesi henüz yapılmadı. Çoklu zaman eşleştirmesi, gerçek üst zaman kapanışları doğrulanmadığından uygulanmadı. Daha uzun, daha önce incelenmemiş tarihçe elimizde bulunmadığı için bağımsız ileri doğrulama **`blocked_data`** durumundadır. Bu eksikler kapatılmadan adayın faydalı bir indikatör olduğu söylenemez.
