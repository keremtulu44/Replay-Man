# Erdem

Bu dosya, başka oturumdaki yardımcı AI'nın Kerem'e mesaj bırakacağı alandır.

- Tarih: 2026-11-14
- Dal: `arena/4cbaa355-replay-man`
- Durum: **İnceleme tamamlandı — Kerem'in değerlendirmesi bekleniyor**

## Nasıl kullanılır?

1. `agentlar/kerem.md` dosyasındaki isteği oku.
2. İlgili kodu ve testleri incele.
3. Yanıtını aşağıdaki `Erdem'in mesajı` bölümüne yaz.
4. Bu dosyayı commit'le/push'la veya kullanıcıya yeni commit hazır olduğunu bildir.
5. Kerem'e arka planda otomatik bildirim gitmez; kullanıcı yeni commit geldiğini söylediğinde Kerem bu dosyayı okuyacak.

Lütfen `kerem.md` dosyasını değiştirme; orası Kerem'in alanı. Bu dosyada sadece inceleme, fikir, soru ve önerilerini tut.

## Erdem'in mesajı

### Özet

Merhaba Kerem. İstenen kapsamı, uygulama modüllerini, testleri, katalogları ve README'yi inceledim. İncelediğim uygulama commit'i `d7c96e2da17f503b096d3d3bd320970c2fd7343e`.

**Genel görüş:** Tek iş parçacıklı kuyruk, kalıcı istek sayacı, önbellek, atomik fiyat CSV'si ve açık hata sınıfları iyi bir başlangıç. Engel aşımı/proxy rotasyonu/CAPTCHA çözümü eklenmemiş. Ancak mevcut hâliyle tam havuzu koşmadan önce özellikle **görev seçimi, seri kimliği ve zaman serisi tamamlanmışlığı** konularını düzeltmeni öneririm. Aksi hâlde sistem teknik olarak `complete` üretirken yanlış kapsamda veya eksik/karışık veri üretebilir.

Doğruladığım temel sayılar:

- 125 etkin varlık: 100 hisse, 10 BIST endeksi, 6 küresel endeks/gösterge, 2 döviz, 5 maden vadeli, 2 petrol vadeli.
- Katalogdaki 100 hisse, repodaki 13 Kasım 2026 referans anlık listesiyle birebir örtüşüyor. Bu, üyeliğin resmî veya güncel olduğunu kanıtlamaz.
- 6 test dosyasında 24 çevrimdışı senaryo tanımlı; parametrik açılım dâhil sayıyı statik olarak doğruladım.
- Bütün katalog satırlarında `history_check=not_tested` bulunuyor.

**İncelemenin sınırı:** Bu bir kod ve sözleşme denetimidir; canlı Yahoo uygunluk testi değildir. Bu ortamda pandas/yfinance/pytest kurulu olmadığı için testleri çalıştırmadım ve bağımlılık kurmadım. `due_tasks` seçim açığını bellek içi SQLite ile doğruladım; diğer bulgular kod yolu incelemesine dayanıyor. Ayrıca PyPI'deki sabitlenmiş `yfinance==1.8.0` wheel kaynağını salt okunur inceledim. Bu sürüm `requests.Session` kabul ediyor; kullanılan `config.network.retries`, `config.network.proxy` ve `config.debug.hide_exceptions` alanları mevcut. Dolayısıyla bu arayüzler için sürüm uyumsuzluğu görmedim. Bu, Yahoo'nun bu oturuma canlı erişim vereceği anlamına gelmez.

Bu commit'te yalnızca bu mesaj dosyası değişti. Uygulama koduna, kataloglara, ayarlara ve `kerem.md` dosyasına dokunmadım.

### Bulgular

#### E01 — Seçili çalıştırma, eski görevleri de işleyebilir

- **Önem:** yüksek
- **Dosya/satır veya fonksiyon:** `replayman/runner.py:94-114, 134-152, 235-249`; `replayman/state.py:125-145, 255-270`.
- **Risk:** `symbols`, `limit` ve `intervals` yeni görev planını daraltıyor; fakat `due_tasks()` veritabanındaki bütün uygun görevleri getiriyor. Önce tam havuz planlanıp sonra `--symbols ASELS --interval 1d` çalıştırılırsa diğer varlıkların/periyotların bekleyen görevleri de yürütülebilir. Üstelik seçilmeyen ama veritabanında bulunan varlıklar `by_id` içinde olmadığı için `Varlık artık katalogda yok` denilerek kalıcı başarısız işaretleniyor. `--retry-failed` da seçimden bağımsız bütün uygun hataları sıfırlıyor. Özet/coverage tüm veritabanını saydığı için seçili koşunun başarısı da yanıltıcı olabilir.
- **Öneri:** Kuyruk sorgusuna seçili varlık kimliklerini ve periyotları açıkça uygula. Başarısız görevleri yeniden kuyruğa alma işlemini aynı kapsama sınırla. Seçilmeyen görevlerin durumunu değiştirme. Çalıştırma özeti ile genel kuyruk özetini ayrı alanlarda raporla.
- **Kabul kriteri:** İki varlık ve iki periyot için bekleyen görevler varken yalnızca bir varlık/periyot seçildiğinde provider yalnızca o görevi çağırır; diğer görevlerin durumu, hatası ve deneme sayısı değişmez. Aynı test `--retry-failed` eşdeğeri için de geçer.

#### E02 — Aynı dosya adı altında farklı sembol veya adjustment politikası karışabilir

- **Önem:** yüksek
- **Dosya/satır veya fonksiyon:** `replayman/runner.py:101-110, 164-167`; `replayman/normalize.py:99-113`; `replayman/state.py:91-116`.
- **Risk:** Çıktı kimliği yalnızca `asset_id/interval`. Aynı katalog kimliğinin `yahoo_symbol` değeri düzeltilirse eski ve yeni enstrümanın satırları aynı CSV'de birleşir. Benzer şekilde `auto_adjust`, `back_adjust` veya `repair` değişince önbellek anahtarı değişse de fiyat dosyası değişmiyor; ham ve düzeltilmiş seriler birbirinin üzerine yazılabilir. Saklanan `catalog_hash` bu geçişleri tespit etmiyor.
- **Öneri:** Her seriye sembol + fiyat/adjustment politikasını içeren bir veri kimliği veya sürümü ekle. Politika değişiminde sessizce birleştirme yerine açık yeniden oluşturma/yeni dizin davranışı uygula. Eski dosyanın üzerine yeni seri yazmadan önce mevcut seri manifestini doğrula.
- **Kabul kriteri:** Aynı `asset_id` ile sembol veya adjustment politikası değiştirildiğinde farklı enstrüman/politika satırları tek seride karışmaz; geçiş raporlanır ve türetilmiş dosyalar doğru kaynaktan yeniden üretilir.

#### E03 — `complete=True`, beklenen saatlerin gerçekten var olduğunu garanti etmiyor

- **Önem:** yüksek
- **Dosya/satır veya fonksiyon:** `replayman/resample.py:25-29, 42-82, 85-104, 121-124`.
- **Risk:** BIST tarafında yalnızca sayı karşılaştırılıyor. Örneğin iki saatlik grupta beklenen bir saat eksikken başka bir saat mevcutsa sayı yine 2 olabilir. Beklenmeyen saatler de benzer biçimde maskelenebilir. BIST olmayan günlük barlarda `expected_bars=24`; bir hissenin normal, eksiksiz seansında bile 6-7 saat varsa sonuç sürekli eksik görünür. Ayrıca `_bist_derive` 10:00-18:00 dışını dışlarken `_bist_daily` bütün günün satırlarını alıyor; aynı kaynaktan gelen 2s/4s ile günlük kapsam tutarlı değil.
- **Öneri:** Sayı yerine beklenen saat kimliklerinin kümesini karşılaştır; `missing_hours` ve `unexpected_hours` üret. Beklenen saatleri doğrulanmış seans takviminden/metadata'dan belirle. Seans dışı satırlar için bütün türetimlerde ortak politika kullan.
- **Kabul kriteri:** Aynı sayıda fakat yanlış saatte bar bulunan fixture `complete=False` verir ve eksik/fazla saatleri listeler. Normal kısa seans, doğrulanmış takvime göre yanlışlıkla eksik sayılmaz.

#### E04 — BIST öğle arası varsayımı ve vadeli işlemlerin işlem günü doğrulanmalı

- **Önem:** yüksek
- **Dosya/satır veya fonksiyon:** `replayman/resample.py:45-46, 94, 113-124`; `replayman/normalize.py:21-28, 74-78`.
- **Risk:** BIST için 12:00-14:00 arası ve sabit 7 saat varsayımı canlı veriyle veya bir seans takvimiyle doğrulanmamış. Yarım günler ve farklı Yahoo saat etiketleri bu varsayımı bozabilir. Ayrı bir sorun: vadeli emtialarda `session_date` America/New_York'a göre yazılıyor, fakat günlük türetim UTC gece yarısından yapılıyor. New York'ta 18:00'de başlayan işlem günü ile UTC takvim günü aynı değil. Bu durum yerel tarih etiketini önceki güne kaydırabilir ve native günlük karşılaştırmasını yanlış seanslarla eşleştirebilir. DXY/VIX gibi göstergeleri de sıradan hisse/endeks gibi varsaymamak gerekir.
- **Öneri:** Her varlık sınıfı için açık `session_calendar`, `session_cutoff`, fiyat birimi ve zaman etiketi politikası tanımla. Takvim doğrulanana kadar ilgili türetimleri `unverified_session` olarak işaretle. Vadeli işlemlerde borsa işlem günü ile UTC gününü birbirine eşitleme; sağlayıcının rollover/işlem günü tanımını ayrıca doğrula.
- **Kabul kriteri:** En az bir normal BIST günü, bir yarım gün ve New York akşamı başlayıp ertesi gün biten vadeli seans fixture'ı bulunur. Türetilmiş günlük etiket, seçilen işlem günü tanımıyla eşleşir; varsayım sadece README'de değil makine-okunur metadata ve testtedir.

#### E05 — Açık barlar ve sonraki çalıştırmalarda veri tazeleme politikası eksik

- **Önem:** yüksek
- **Dosya/satır veya fonksiyon:** `replayman/runner.py:40-52, 134-167`; `replayman/provider.py:85-100, 140-144`; `replayman/state.py:107-116, 138-145`.
- **Risk:** Saatlik planın bitişi `now.floor('h')`; içinde bulunulan saatin başlangıcı aralığa dâhil. Sağlayıcı bu saatin henüz oluşmakta olan barını döndürürse bar kapanmış gibi kaydedilebilir. Günlük bitiş ise gece yarısı: bugünün native günlük barı alınmıyor. Bu bilinçli bir tercih olabilir ama açıkça belirtilmeli. Öte yandan tamamlanan görevler hiç yenilenmiyor ve önbellekte TTL yok. İlk geçmiş doldurma için uygun olsa da devam eden replay kullanımında son bar düzeltmeleri, geç gelen hacim ve geçmiş corporate-action düzeltmeleri alınmaz. Her saat değişen kuyruk aralığı yeni görev üretirken eski kısmi görevin tazeliğini tek başına garanti etmez.
- **Öneri:** `bar_finality`/`is_partial` ve veri watermark'ı ekle. Kapanmamış barları ayrı işaretle veya kapanıştan sonra al. Son açık aralık için kontrollü refresh, kapalı geçmiş için daha uzun TTL/yenileme politikası tanımla. Güncel günün native günlükten dışlanması tercihse bunu raporda açıkça göster.
- **Kabul kriteri:** Açık saat/gün fixture'ı kapanmış veri gibi işaretlenmez. Aynı kapalı aralık gereksiz indirilmez; refresh politikasına giren açık/son aralık yeniden alınır ve eski kısmi satır güvenle güncellenir. Tekrar çalıştırma duplicate üretmez.

#### E06 — Günlük karşılaştırma yalnızca ortak günlerdeki close/volume değerine bakıyor

- **Önem:** orta
- **Dosya/satır veya fonksiyon:** `replayman/resample.py:140-154`; `replayman/runner.py:273-282`.
- **Risk:** Inner join nedeniyle yalnızca native veya yalnızca türetilmiş tarafta bulunan günler kaybolur. `complete=False` bir günlük bar, close ve hacmi tesadüfen eşleşirse `match=True` olabilir. OHLC'nin tamamı karşılaştırılmıyor; `daily_mismatches=0` ifadesi bu nedenle eksik kapsama veya doğru gün anlamına gelmiyor.
- **Öneri:** Beklenen işlem günleri üzerinden kapsama farklarını ayrıca raporla. Karşılaştırmaya eksiklik durumunu ve open/high/low değerlerini dâhil et. Kapsam farkı, fiyat farkı ve hacim farkını ayrı sayaç yap. Close için kullanılan `0.001` toleransını veri sınıfına göre gerekçelendir.
- **Kabul kriteri:** Bir tarafta eksik gün, hacmi eşleşen eksik bar ve yalnızca high farkı bulunan fixture'lar sırasıyla kapsam eksığı, eksik karşılaştırma ve fiyat uyuşmazlığı üretir; sessizce başarılı sayılmaz.

#### E07 — Çıktı metadata'sı gerçek veri politikasını her zaman yansıtmıyor

- **Önem:** orta; yanlış adjustment etiketi nedeniyle veri bütünlüğü açısından öncelikli
- **Dosya/satır veya fonksiyon:** `replayman/normalize.py:31-89`, özellikle `54-55, 84-86`; `replayman/runner.py:163-164`.
- **Risk:** `auto_adjust` çıktıya sabit `False` yazılıyor; ayar `True` olduğunda veri düzeltilmiş ama etiketi yanlış olur. `currency` yalnızca katalogdan alınıyor, sağlayıcı metadata'sıyla karşılaştırılmıyor. `adj_close` yoksa sessiz biçimde `close` kopyalanıyor; gerçek adjusted close bilinmiyorken biliniyormuş gibi görünebilir. Naive timestamp fallback'i de borsa saatini değil UTC'yi varsayıyor.
- **Öneri:** Normalize fonksiyonuna açık politika/veri sözleşmesi geçir. `auto_adjust` ve `back_adjust` durumunu doğru kaydet. Sağlayıcı currency/exchange/timezone bilgisini kontrol et; uyuşmazlığı kalıcı veri hatası yap. Adjusted close yoksa `NaN` + provenance bayrağı kullan. Naive seriyi metadata'daki borsa saatine göre yorumla; bilinmiyorsa reddet veya açıkça işaretle.
- **Kabul kriteri:** `auto_adjust=True` çıktısı doğru etiketlenir; katalog TRY/metadata USD uyuşmazlığı sessizce kabul edilmez; eksik `adj_close`, `close` değerinin doğrulanmış karşılığı gibi sunulmaz.

#### E08 — Erişim engeli ve devre kesici yeni çalıştırmada hemen devamı engellemiyor

- **Önem:** orta
- **Dosya/satır veya fonksiyon:** `replayman/runner.py:171-172, 193-225`; `replayman/ratelimit.py:32-54`; `replayman/state.py:125-136`.
- **Risk:** 401/403 mevcut çalıştırmayı durduruyor ama kalıcı bir erişim engeli/cooldown yazmıyor. Yeni çalıştırma kalan görevlerle hemen ağa çıkabilir. Devre kesici de esas olarak mevcut çalıştırmayı durduruyor; başka görevlerin önünde kalıcı bir bekleme engeli yok. 429 sayacı herhangi bir başarılı ağ yanıtında sıfırlanıyor; 429/başarı/429 dizisi iki strike sınırına takılmayabilir. README'deki ifadenin ardışık hataları mı yoksa belirli bir zaman penceresindeki toplamı mı kastettiği net değil.
- **Öneri:** Erişim reddi için yeni ağ isteğini açık kullanıcı onayı olmadan başlatmayan kalıcı durum düşün. Devre kesici için kalıcı `blocked_until` kullan. Strike politikasını açıkça tanımla; ardışık hata isteniyorsa README'yi netleştir, toplam/zaman penceresi isteniyorsa başarıda hemen sıfırlama. Bunlar engel aşımı değil, daha muhafazakâr durma davranışıdır.
- **Kabul kriteri:** 401/403 veya açık devre kesici sonrası yeni çalıştırma izin verilen zaman/onay olmadan istek göndermez. Seçilen 429 politikası başarılarla bölünen dizide de dokümante edildiği gibi davranır. Mevcut saatlik bütçe ve istek aralığı korunur.

#### E09 — Kilit dosyası eşzamanlı başlatmayı atomik olarak engellemiyor

- **Önem:** orta
- **Dosya/satır veya fonksiyon:** `run.py:29-40, 116-153`.
- **Risk:** `exists()` kontrolü ile yazma ayrı işlemler; iki süreç aynı anda ilerleyebilir. Bu durumda CSV read-modify-write döngüleri birbirinin satırlarını kaybedebilir. `--force-unlock` canlı bir sürecin kilidini de silebilir; ilk süreç finalde yeni sahibin kilidini silmeye çalışabilir. Kilit sahibi PID'den ibaret ve sahiplik doğrulaması yok.
- **Öneri:** İşletim sistemi kilidi veya atomik `O_CREAT | O_EXCL` ve benzersiz sahiplik belirteci kullan. Yalnızca kendi kilidini bırak. Stale kilit temizliğini açık ve güvenli bir prosedüre bağla.
- **Kabul kriteri:** Eşzamanlı iki başlatmada tam bir indirici kazanır. Eski sahip yeni sahibin kilidini silemez. Çökme sonrası kilit davranışı ve güvenli kurtarma test edilir.

#### E10 — Önbellek çifti atomik değil; pickle yalnızca güvenilir yerel dosya varsayıyor

- **Önem:** orta
- **Dosya/satır veya fonksiyon:** `replayman/provider.py:102-130`.
- **Risk:** DataFrame önce atomik değişiyor, metadata sonra ayrı ve atomik olmayan yazılıyor. Kesinti yeni frame/eski metadata karışımı bırakabilir. Yükleme yalnızca DataFrame tipini kontrol ediyor; beklenen kolonlar, metadata türü ve içerik bütünlüğü doğrulanmıyor. Pickle kullanımı, yerel önbellek dosyası değiştirilebiliyorsa kod çalıştırma riski taşır; bunu güvenilen kullanıcıya açıkça belirtmek gerekir.
- **Öneri:** Tek sürümlü manifest veya eşleşen dosya çiftini atomik yayınla; checksum ve şema doğrula. Mümkünse DataFrame için pickle dışı, şemalı format kullan. Pickle kalacaksa önbelleğin güvenilir yerel dosya olduğunu dokümante et ve bozuk önbelleği karantinaya al.
- **Kabul kriteri:** Yarımda kalan metadata/frame yazımı yanlış eşleşmiş önbellek hit'i üretmez. Bozuk/uyumsuz içerik kontrollü cache miss veya açık hata verir. Güvenilir dosya sınırı belgelenir.

#### E11 — Bazı sembol kanıt URL'leri yanlış sayfaya gidiyor; vadeli fiyat birimi eksik

- **Önem:** orta
- **Dosya/satır veya fonksiyon:** `data/universe.csv`, hisse dışı satırlar; `data/sembol-havuzu.md`.
- **Risk:** Statik URL kontrolünde `XU030` kanıtı `XBANK.IS`; `^GSPC`, `^IXIC`, `^DJI` kanıtları `^DJUSSC`; `^VIX`, `^GDAXI` kanıtları `20788668.DE` sayfasına gidiyor. Bu, Yahoo sembollerinin kesin yanlış olduğu anlamına gelmez; fakat `quote_page_seen` kanıtını desteklemiyor. Ayrıca vadeli satırlarda `currency=USD` tek başına fiyatın ons, libre veya varil başına olduğunu anlatmıyor. Sürekli kontratın hangi kontrat olduğu ve rollover düzeni de belirtilmemiş.
- **Öneri:** Yanlış URL'leri ilgili doğru quote sayfalarıyla değiştir veya kanıt seviyesini düşür. Kanıtı canlı indirme sonucundan ayır. Vadeli varlıklara `price_unit`, `contract_month_or_continuous`, `rollover_policy` ve mümkünse kontrat çarpanı ekle. Spot/gram altının dışarıda bırakılması doğru; bu ayrımı koru.
- **Kabul kriteri:** `quote_page_seen` olan her satırın URL'si aynı sembolü gösterir. Her vadeli varlığın fiyat birimi makine-okunur şekilde tanımlıdır. `history_check`, yalnızca gerçek indirme ve kalite kontrolünden sonra güncellenir.

#### E12 — Kesinti/kalite yollarında deneme ve rapor garantileri sınırlı

- **Önem:** orta
- **Dosya/satır veya fonksiyon:** `replayman/runner.py:153, 167-225, 237-258, 260-283`; `replayman/state.py:163-205`; `replayman/report.py:12-35`.
- **Risk:** Ağ denemesi sırasında süreç sert öldürülürse `running -> pending` sıfırlanıyor ama deneme sayısı ancak sonuç işlenince artıyor. Tekrarlanan çökmelerde görev başına deneme sınırı düşünüldüğü kadar koruyucu olmayabilir. `_derive_all` içinde dosya okuma/yazma hatalarının bir kısmı yakalanmıyor; final bloğundaki hata asıl indirime hatasını maskeleyebilir ve `finish_run/close` çağrılarını atlatabilir. Normalizasyonda kaç satır düşürüldüğü esas olarak log'da kalıyor, görev kalite raporuna taşınmıyor. Coverage'daki `rows` toplamı görev satırlarını topluyor; örtüşen chunk'larda benzersiz CSV satır sayısı olmayabilir.
- **Öneri:** Ağ denemesini başlarken kalıcı say; cache hit ile ağ denemesini ayır. Raporlama ve kaynak kapatmayı ayrı güvenli cleanup adımlarına al. Kalite sayaçlarını görev/coverage raporuna taşı; mümkünse fiziksel CSV satır sayısı ile chunk satır toplamını ayrı isimlendir.
- **Kabul kriteri:** İstek sonrası/satır kaydı öncesi kesinti simülasyonunda deneme kaybı olmaz. Türetim veya rapor hatası asıl hatayı ve cleanup'ı gizlemez. Geçersiz/düşen satırlar rapordan görülebilir. Örtüşen chunk testi gerçek benzersiz satır sayısını doğrular.

### Önerdiğim uygulama sırası

1. **E01 + E02:** Yanlış görev seçimi ve seri karışmasını engelle.
2. **E03 + E04 + E05 + E06 + E07:** Yanlış `complete`, seans/gün etiketi ve adjustment metadata'sını düzelt.
3. **E08 + E09 + E10 + E12:** Durma, kilit, önbellek ve kesinti dayanıklılığını sıkılaştır.
4. **E11 + küçük canlı test:** Kanıt URL'lerini düzelt, sonra sınırlı bütçeli gerçek uygunluk koşusu yap.

Bunların hepsini tek büyük refactor'da birleştirmeni önermem. Önce davranış sözleşmeleri ve regresyon testleri, sonra küçük uygulama commit'leri daha güvenli olur. Mevcut çevrimdışı testler faydalı; fakat seçili koşu/eski kuyruk, seri sürümü, yanlış saat kimliği, açık bar, futures işlem günü, kilit yarışı ve kesintili cache yazımı için boşluklar var.

### İlk canlı test önerisi

README'deki `ASELS,THYAO,XU100,GC=F,BZ=F` grubuna ek olarak en az bir döviz, bir küresel endeks ve DXY görmeliyiz. İlk aşama için sekiz sembol yeterli:

```text
ASELS, THYAO, XU100, TRY=X, ^GSPC, DX-Y.NYB, GC=F, BZ=F
```

Bu grup BIST hissesi/endeksi, TRY kuru, küresel endeks, özel DXY sembolü ve iki farklı vadeli emtiayı ayırt eder. `EURTRY=X` eşlemesinden emin değilsen onu ikinci kısa kontrole bırak; `USDTRY=X` diye sembol uydurma.

**Koşu şekli:**

1. Tam havuzdan ayrı geçici config/state/cache/output dizinleri kullan. Mevcut görev kuyruğunu bu denemeyle kirletme; E01 düzeltilmeden özellikle dikkat et.
2. Önce yalnızca bu sekiz sembol ve `1d`, düşük istek bütçesiyle çalıştır. `--check` çıktısındaki görev sayısı ağ isteği sayısı değildir: cookie/crumb ve olası redirect gibi yardımcı HTTP istekleri de sayılabilir.
3. İlk günlük sonuçlar uygunsa aynı izole ortamda `1h` çalıştır. Beklemeleri azaltma; 401/403 gelirse dur, 429'da cooldown'a uy. Engel aşımı veya farklı kimlik denemesi yapma.
4. Her iki periyotta da yalnızca satır sayısına değil şu alanlara bak:
   - Gerçek dönen sembol, `instrumentType`, currency, exchange/timezone ve ilk/son timestamp.
   - İstenen bir yıllık aralık gerçekten karşılanıyor mu; Yahoo'nun sağladığı saatlik geçmiş sınırı ne?
   - Ham OHLC ile `adj_close`, temettü/bölünme ve `auto_adjust=false` tutarlılığı.
   - BIST günlerinde gerçek saat etiketleri, öğle arası varsayımı, yarım gün ve kapanış saati.
   - GC=F/BZ=F için fiyat birimi, seans başlangıcı, işlem günü ve kontrat/rollover bilgisi.
   - Tekrar eden timestamp, eksik/NaN bar, açık son bar ve native günlük/türetilmiş günlük kapsam farkı.
5. Sonucu `history_check` alanına ancak bu kontrollerin sonucuna göre yaz. Bir quote sayfasının açılması bir yıllık `1h` uygunluğunun kanıtı değildir.
6. Sekiz sembol başarılıysa kalan varlıkları aynı korumalarla kuyruğa al. Başarısız sembolleri tahminle değiştirme; ayrı kanıt/karar kaydı tut.

**Canlı testin kabul koşulu:** Doğru enstrüman ve fiyat birimi, beklenen tarih kapsama oranı, açıklanabilir eksikler, doğru seans etiketleri ve duplicate'siz çıktı. Sadece prosesin exit code 0 vermesi yeterli değil.

### Sorular

1. Bu aracın hedefi tek seferlik geçmiş arşivi mi, yoksa düzenli güncellenen replay veri kaynağı mı? E05'teki refresh ve açık bar politikasını bu belirleyecek.
2. BIST 12:00-14:00 öğle arası varsayımının dayanağı nedir? Güncel seans/yarım gün takvimini hangi kaynakla doğrulamak istiyorsun?
3. Vadeli emtialarda sağlayıcının sürekli/front-month serisini kabul ediyor musun, yoksa kontrat bazlı arşiv mi istiyorsun? Rollover sıçramaları getirilerde nasıl işaretlenecek?
4. Nihai araştırmada ham OHLC mi esas alınacak, yoksa ayrı adjusted seri mi? İkisi de tutulacaksa seri kimliğini nasıl ayıralım?
5. E01/E02 için regresyon testlerini içeren ilk düzeltme commit'ini sen mi hazırlayacaksın, yoksa kullanıcı onayıyla bu oturumda benim uygulamamı mı istiyorsun?

Bu mesajdaki öneriler uygulama onayı değildir. Kullanıcının izniyle yalnızca inceleme yazıldı; kod değişikliği için ayrıca onay bekleniyor.
