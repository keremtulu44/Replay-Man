# Kitap Kuralları — Ölçüm, Sonuç ve Kaynak Bağlantısı

## Kayıt politikası

Bu rapordaki her kural `registry.json` içinde benzersiz kimliğe sahiptir. Her kural klasöründe:

- Kitaptaki sayfa kartlarının tam kaynak şeridi: `source-links.json`
- Bütün grup/periyot/yön sonuçları: `structure_event_study.csv`
- Eğitim/doğrulama/test sonuçları: `structure_time_split_study.csv`
- Sembol bazlı sonuçlar: `structure_symbol_results.csv`
- İlgiliyse bağlam bantlarının tüm sonuçları: `book_context_rule_study.csv`

bulunur. Rapor özetler; CSV'ler azaltılmamış sonuç tablolarını korur.

## BR-001 — Swing ancak teyitten sonra bilinir

**Kitap bağlantıları:** Cilt 2, s.54–55 ve 58–59; özellikle “Her tepe ve dip aynı ağırlıkta değildir”, “Major swing bazen ancak daha sonra kesinleşir” ve swing hız/geometri bölümleri.

**Uygulama:** Minor swing 2 sol + 2 sağ, major swing 5 sol + 5 sağ barla teyit edilir. Geometrik pivot zamanı ile ilk bilinebilir teyit zamanı ayrıdır.

**Sonuç:** 151.450 minor, 67.705 major swing ve 113.778 karşıt swing bacağı üretildi. Bu bir getiri kuralı değil, geleceği göstermeyen replay için zorunlu altyapı kuralıdır. Geçmişe ideal pivot çizip pivot barında işlem varsaymak geçersizdir.

**Karar:** `altyapi_kurali` — korunacak.

## BR-002 — Seviyeyi geçmek değil, dışarıda kapanmak

**Kitap bağlantıları:** Cilt 2 s.45, 47, 52.

**Uygulama:** Teyitli swing seviyesi 0,10 ATR toleransın dışında kapanışla aşılır.

**Ölçüm:** 116.136 kapanış kırılımı.

**Çıkan:** Ham aşağı sonuçlar güçlü görünse de XU100 çıkarıldığında 4h testte 20 bar medyanı -%0,87'ye düştü. 4h 60 barda eğitim %3,01, doğrulama -%0,03, test %0,80 XU100-aşırı medyandır.

**Yorum:** Tek kapanış, kısa ufukta piyasa yönünden bağımsız avantaj değildir. 60 bar test pozitif olsa da doğrulama yazı-tura seviyesindedir.

**Karar:** `baglam_filtresi_gerekli`.

## BR-003 — İlk kapanıştan sonra takip davranışı

**Kitap bağlantıları:** Cilt 2 s.48, 50–52.

**Uygulama:** Kırılımdan sonraki ilk üç bar içinde kırılım tarafında yeni dış kapanış.

**Ölçüm:** 91.132 follow-through olayı.

**Çıkan:** 4h aşağı, 60 bar XU100-aşırı medyan eğitim/doğrulama/testte sırasıyla %2,82 / %0,63 / %1,40. Fakat acceptance sonuçlarıyla ve olay sayılarıyla neredeyse aynıdır.

**Saçma/tekrar kontrolü:** Bunu acceptance'tan bağımsız ikinci avantaj saymak çift sayımdır. Mevcut tanımlar aynı davranış zincirinin yakın aşamalarını ölçüyor.

**Karar:** `bilgi_tekrari` — tekilleştirilecek.

## BR-004 — Kırılımın yeni alanda kabul görmesi

**Kitap bağlantıları:** Cilt 2 s.45, 48, 52, 96.

**Uygulama:** Kırılım tarafında iki kapanış. İlk sürümde seviye ömrü 100 bar, tolerans 0,10 ATR.

**Ölçüm:** 91.351 acceptance olayı.

**Olumlu sonuç:** 4h aşağı acceptance, 60 bar:

| Bölüm | Geçerli olay | XU100-aşırı medyan | Pozitif oran |
|---|---:|---:|---:|
| Eğitim | 2.264 | %2,83 | %59,72 |
| Doğrulama | 853 | %0,63 | %50,88 |
| Test | 582 | %1,40 | %54,64 |

**Olumsuz sonuç:** 4h kısa 20 bar testte benchmark sonrası medyan -%0,77 ve pozitif oran %44,52. Günlük 20 bar doğrulama da -%0,12'dir. Kural “her ufukta çalışıyor” değildir.

**Karar:** `devam_et` — şu anki ana araştırma adayı, fakat yalnız 4h/60-bar aşağı varyantında.

## BR-005 — Retest ve seviyenin tutulması

**Kitap bağlantıları:** Cilt 2 s.57, 76, 91, 96.

**Uygulama:** Kırılan seviyeye temas ve kapanışın kırılım çevresinde korunması.

**Ölçüm:** 62.104 retest-hold olayı.

**Çıkan:** 4h aşağı 60 bar XU100-aşırı medyan eğitim/doğrulama/testte %2,67 / %0,07 / -%0,41. Test pozitif oranı %49,40.

**Yorum:** Doğrulama ve test yaklaşık yazı-turadır. Mevcut “dokunma + kapanışı koruma” tanımı retestin kalitesini ayrıştırmıyor. Yaklaşma hızı, geri alma derinliği ve retest mumu eklenmeden kullanışlı görünmüyor.

**Karar:** `yazi_turaya_yakin`.

## BR-006 — Başarısız kırılım

**Kitap bağlantıları:** Cilt 2 s.41, 43, 46, 49, 70.

**Uygulama:** Dış kapanıştan sonraki ilk 10 bar içinde eski alana kapanışla dönüş; sonuç ilk kırılım yönünün tersinde ölçülür.

**Ölçüm:** 67.971 failure olayı.

**Çıkan:** 4h aşağı kırılım failure → yukarı hipotezi 60 barda eğitim -%3,48, doğrulama %0,69, test %1,25 XU100-aşırı medyan verdi.

**Yorum:** İşaret dönemler arasında değişmektedir. “Eski alana döndü” tek başına yeterli değil; dönüş derinliği, karşı tarafa genişleme ve önceki takip gücü gerekir.

**Karar:** `rejime_bagli`; genel kural olarak olumlu sayılamaz.

## BR-007 — Fitille taşma/rejection

**Kitap bağlantıları:** Cilt 2 s.17, 43, 73.

**Uygulama:** Uç seviye aşılır fakat tolerans dışında kapanış yoktur; sonuç denemenin ters yönünde ölçülür.

**Ölçüm:** 127.561 probe-rejection olayı.

**Çıkan:** Günlük yukarı seviye rejection → aşağı hipotezi 20 barda eğitim %2,91, doğrulama -%1,03, test %3,20 XU100-aşırı medyan. 4h 60 barda aynı hipotez eğitim %3,40, doğrulama -%2,66, test -%2,17.

**Yorum:** Zaman dilimi ve dönem değişince işaret değişiyor. Kitabın “fitil tek başına dönüş değildir” uyarısı ölçümle destekleniyor.

**Karar:** `kararsiz`; bağlamsız rejection kullanılmamalı.

## BR-008 — Hareket kalitesi ve yol verimliliği

**Kitap bağlantıları:** Cilt 2 s.13, 15–16, 94.

**Uygulama:** Son 10 barda net kapanış mesafesi / toplam kapanış yolu. Sabit ilk bantlar: düşük ≤0,30; orta 0,30–0,60; yüksek >0,60.

**4h aşağı acceptance, 60 bar XU100-aşırı sonuç:** 

| Bant | Eğitim | Doğrulama | Test | Test hazır | Test pozitif |
|---|---:|---:|---:|---:|---:|
| Düşük | %4,17 | %2,64 | %3,56 | 66 | %54,55 |
| Orta | %1,88 | -%1,21 | %0,56 | 247 | %54,66 |
| Yüksek | %3,22 | %1,44 | %1,44 | 269 | %54,65 |

**Çıkan:** Yüksek kalite üç bölümde pozitif. Düşük verim de pozitif çıktığı için ilişki doğrusal değil; düşük bant muhtemelen sıkışma bağlamını da taşıyor. “Verim yükseldikçe sonuç sürekli iyileşir” iddiası yanlış.

**Karar:** `olumlu_baglam`, fakat düşük ve yüksek bantların farklı piyasa yapıları olarak ayrılması gerekir.

## BR-009 — Örtüşme

**Kitap bağlantıları:** Cilt 2 s.15, 38, 44.

**Uygulama:** Son 10 bardaki ardışık high-low örtüşmelerinin ortalaması; düşük ≤0,25, orta 0,25–0,55, yüksek >0,55.

**4h aşağı acceptance, test/60 bar:** düşük örtüşme 40 geçerli olayda %5,05 medyan ve %65 pozitif; orta örtüşme 538 olayda %0,91 ve %53,53 pozitif.

**Saçma/geçersiz bölüm:** Yüksek örtüşme testinde 60 bar hazır olay sayısı sıfırdır. Bu bant için sonuç çıkarmak mümkün değildir; boş hücre “başarısız” veya “başarılı” sayılamaz. Ayrıca düşük bant örneği küçüktür.

**Karar:** `ornek_yetersiz_bant_var`.

## BR-010 — Sıkışma ve volatilite bağlamı

**Kitap bağlantıları:** Cilt 2 s.38, 41, 44.

**Uygulama:** Olay barının aralığı/ATR: contracted ≤0,80; normal 0,80–1,50; expanded >1,50.

**4h aşağı acceptance, 60 bar XU100-aşırı sonuç:** 

| Bant | Eğitim | Doğrulama | Test | Test hazır | Test pozitif |
|---|---:|---:|---:|---:|---:|
| Contracted | %3,32 | %1,64 | **%6,50** | 221 | **%73,76** |
| Normal | %2,67 | -%0,39 | **-%2,38** | 235 | %42,98 |
| Expanded | %1,24 | -%4,97 | **-%2,79** | 126 | %42,86 |

**Olumlu:** Contracted grup üç zaman bölümünde de pozitif ve testte 221 olayla belirgin ayrışıyor.

**Olumsuz:** Expanded kırılım barları doğrulama ve testte negatif. “Büyük kırılım mumu daha iyidir” varsayımı bu örnekte tersine dönüyor.

**Karar:** `devam_et`; şu an kitap bilgisinden çıkan en güçlü bağlam ayrımı.

## BR-011 — Gövde/baskı küçülmesi

**Kitap bağlantıları:** Cilt 2 s.18–19, 22, 33.

**Uygulama:** Son üç bar ortalama gövdesinin önceki üç bara oranı; decaying ≤0,80, stable 0,80–1,20, expanding >1,20.

**4h aşağı acceptance, 60 bar XU100-aşırı sonuç:** 

| Bant | Eğitim | Doğrulama | Test | Test hazır | Test pozitif |
|---|---:|---:|---:|---:|---:|
| Decaying | %2,90 | %0,72 | **%4,85** | 114 | **%65,79** |
| Stable | %1,82 | %0,81 | %0,56 | 85 | %57,65 |
| Expanding | %3,10 | %0,12 | %0,50 | 383 | %50,65 |

**Çıkan:** Decaying bant üç bölümde pozitif ve testte daha güçlü. Expanding eğitimde iyi görünürken testte neredeyse yazı-turaya düşüyor. Kitaptaki “gövde küçülmesi mevcut baskının niteliğini değiştirir” bilgisi bu olay bağlamında ölçülebilir ayrım üretti.

**Karar:** `olumlu_baglam`; volatilite filtresiyle birleşimi sonraki deneydir.

# Toplu sınıflama

## Olumlu ve devam edilecek

1. 4h aşağı acceptance, 60 bar.
2. Acceptance olayında contracted aralık/ATR bağlamı.
3. Acceptance olayında decaying gövde baskısı.
4. Yüksek hareket verimliliği; ancak doğrusal ilişki varsayılmayacak.

## Olumsuz veya avantaj göstermeyen

1. 4h kısa 20-bar aşağı kırılım, benchmark sonrası.
2. Günlük çıplak kapanış kırılımı.
3. Expanded kırılım/acceptance barı, doğrulama ve testte.
4. Bağlamsız yukarı kırılım devamı.

## Yazı-turaya yakın

1. Mevcut retest-hold tanımı.
2. 4h/60 çıplak close-break doğrulama bölümü.
3. Expanding body-pressure test sonucu.
4. Birçok bağlamsız olayda XU100-aşırı pozitif oran `%48–52` çevresi.

## Saçma, geçersiz veya yanıltıcı okuma

1. Ham aşağı getiriyi avantaj saymak: genel XU100 düşüşü sonucu şişiriyor.
2. Acceptance ve follow-through'u iki bağımsız avantaj saymak: bilgi tekrarı.
3. Günlük 60-bar test medyanını kullanmak: birçok hücrede yalnız 1–13 hazır olay var.
4. Yüksek overlap test sonucu çıkarmak: hazır 60-bar olay yok.
5. Pivotu geometrik barında biliniyormuş gibi işlem yapmak: geleceği gösterir.
6. Fitil/rejection'ı tek başına dönüş kabul etmek: dönem ve periyot arasında işaret değiştiriyor.

## BR-012 — İlk ve ikinci deneme karşılaştırması

**Kitap bağlantıları:** Cilt 2 s.63–65, 71 ve 97.

**Uygulama:** Aynı yöndeki ardışık minor swing bacakları mesafe, süre, hız ve yol verimliliği oranlarıyla karşılaştırıldı. Olay ikinci bacağın bitiş swing'i teyit edildiğinde yayımlandı.

**Kapsam:** 112.790 olay; 60.400 yeni uç başarısızlığı ve 52.390 yeni uç başarısı.

**Karar:** `altyapi_tamam`. Çıplak sonuç yerine bacak oranları ve yeni uç sonucu ayrı kaydediliyor.

## BR-013 — Beklenen yeni ucun üretilmesi

**Uygulama:** İkinci yönlü bacak önceki aynı yönlü bacağın ucunu 0,10 ATR toleransla geçti; hipotez devam yönüdür.

**4h/60 bar test:** Aşağı başarı→aşağı devam 217 olayda -%0,92 XU100-aşırı medyan ve %48,85 pozitif; yukarı başarı→yukarı devam 172 olayda %1,97 ve %58,14.

**Kontrol:** Eğitim döneminde işaretler bunun tersidir. Dolayısıyla “yeni uç yaptıysa devam eder” genel kuralı kararlı değildir.

**Karar:** `rejime_bagli`.

## BR-014 — Beklenen yeni ucun üretilememesi

**Uygulama:** İkinci deneme önceki ucu 0,10 ATR ötesinde geçemedi; hipotez denemenin ters yönüdür.

**4h/60 bar test:** Aşağı deneme failure→yukarı 203 olayda %1,46 ve %57,64 pozitif; yukarı failure→aşağı 259 olayda -%0,70 ve %47,10 pozitif. Çıplak olay yönler arasında kararlı değildir.

**Daha düzenli fakat küçük alt gruplar:** Yukarı deneme failure sonrası aşağı hipotezinde ikinci bacağın daha zayıf mesafeli olması eğitim/doğrulama/testte %4,02 / %0,04 / %1,68; daha uzun sürmesi %2,99 / %0,69 / %1,17; benzer hızlı olması %3,24 / %3,98 / %0,73 medyan verdi. Test örnekleri sırasıyla 42, 18 ve 29'dur.

**Karar:** `baglam_gerekli`; alt gruplar olumlu işaret taşıyor fakat örnek sınırlı ve kombinasyon testi yapılmadı.

## BR-015 — Pullback geometrisi

85.475 teyitli pullback ölçüldü. 4h/60 bar testte yukarı devam 297 olayda %1,57 XU100-aşırı medyan, aşağı devam 285 olayda -%2,11 verdi; eğitimde işaretler ters olduğu için çıplak sonuç rejime bağlıdır. Sığ pullback sonuçları güçlü görünse de test örnekleri yalnız 18–21'dir.

**Karar:** `rejime_bagli`; sığlık adayı `ornek_yetersiz`.

## BR-016 — Mum geometrisi ve dizileri

223.992 güçlü kapanış ve engulfing olayı ölçüldü. 4h/60 testte güçlü boğa kapanışı %1,30, bullish engulfing %1,15; güçlü ayı kapanışı -%0,76, bearish engulfing -%0,78 XU100-aşırı medyan verdi. Eğitim dönemi işaretleri ters olduğundan tek mum/dizi kararlı avantaj değildir.

**Karar:** `tek_basina_kararsiz`; mum adı bağlam yerine geçmez.

## BR-017 — Trend/range rejimi

EMA20/EMA50, ATR-normalize eğim ve yol verimliliğiyle trend_up, trend_down, range ve transition üretildi. Rejim olay sonuçlarını değiştiriyor fakat bütün olay/yön/dönemlerde üstün tek rejim yok.

**Karar:** `baglam_gerekli`; rejim tek başına sinyal değil.

## BR-018 — Çoklu zaman dilimi

1h/2h olayları yalnız 4h bar süresi tamamlandıktan sonra üst-zaman rejimiyle eşlendi. 1h güçlü aşağı kapanış + tamamlanmış 4h düşüş hizası 20 barda eğitim/doğrulama/testte %0,18 / %0,07 / %0,45 XU100-aşırı medyan verdi; pozitif oranlar %53,1 / %51,4 / %55,3. Yukarı hizalı karşılık kararlı değil.

**Karar:** `olumlu_baglam`, fakat avantaj küçük ve maliyet testi gerekli.

## BR-019–023 — Çapraz piyasa, indikatör, formasyon, seans ve risk

XU100, GSPC, USDTRY, altın ve Brent geçmiş bağlamları bağlandı; bütün olayları havuzlayan evrensel çapraz piyasa yönü bulunmadı. RSI/MACD/Bollinger olayları eğitim ve test arasında işaret değiştirdi; çıplak indikatör avantajı yok. 23.136 ikili tepe ve 22.435 ikili dip yalnız eşit uç geometrisiyle kararlı sonuç vermedi. Tek seans bütün olaylarda üstün çıkmadı. 1 ATR hedef/stop testinde 75.054 hedef, 74.662 stop ve 2.037 aynı-bar belirsiz sonuç oluştu; çıplak 1:1 yönetim yazı-turaya yakındır.

# Sonraki kitap kuralları

İlk on paket için başlangıç ölçüm katmanı tamamlandı. Bundan sonraki tur, olumlu adayların kombinasyon ve maliyet/parametre dayanıklılığı ile indikatörlerin fiyat davranışı çekirdeğine marjinal katkısını ayrıştıracaktır.
