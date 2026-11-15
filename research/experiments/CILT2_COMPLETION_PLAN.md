# Cilt 2 Tamamlama Programı

## Ana başlık

**Mum Dizileri ve Fiyat Davranışından Nedensel Kural Atlasına: Cilt 2’nin Eksiksiz Replay Doğrulaması**

## Amaç

Cilt 2’nin 109 sayfasındaki her kullanılabilir iddiayı şu sonuçlardan tam olarak birine bağlamak:

1. `tested`: Matematiksel tanımı, birim testi ve tam evren sonucu var.
2. `tested_as_variant`: Yoruma açık tanım birden fazla kayıtlı varyantla ölçüldü.
3. `context_only`: Bağımsız sinyal değil; başka olayın bağlamı olarak ölçüldü.
4. `duplicate_information`: Başka kuralla aynı olay/bilgiyi üretiyor.
5. `chance_like`: Benchmark sonrası yazı-turadan anlamlı biçimde ayrışmıyor.
6. `negative`: Önceden tanımlanan hipotezin tersine veya düzenli olumsuz sonuç verdi.
7. `insufficient_sample`: Karar için yeterli olay yok.
8. `not_ohlcv_testable`: Niyet, psikoloji, gerçek emir akışı veya OHLCV dışı veri istiyor.
9. `deferred_ob_fvg`: Kullanıcının mevcut OB/FVG sistemi gelene kadar bekletiliyor.
10. `reference_only`: Eğitim, terminoloji veya tekrar niteliğinde; ayrı deney iddiası değil.

Hiçbir sayfa veya iddia sonuçsuz bırakılmayacak. Başarısız sonuçlar silinmeyecek.

---

# Mevcut durum

- 109/109 sayfa bilgi kartı hazır.
- 13/13 bölümden deney kaynak bağlantısı var.
- 51 sayfa doğrudan deneylere bağlandı.
- 58 sayfanın doğrudan deney/karar bağlantısı tamamlanacak.
- Swing, kırılım, acceptance, follow-through, failure, ikinci deneme, pullback başlangıcı, mum başlangıcı, rejim ve çoklu zaman altyapısı çalışıyor.
- OB/FVG kaynakları korunuyor fakat uygulama seçimi erteleniyor.

---

# Çalışma paketleri

## C2-P1 — Sayfa ve iddia kapsam matrisi

### Yapılacaklar

- 109 sayfanın her biri için iddia listesi çıkarılacak.
- Aynı iddianın tekrar geçtiği sayfalar tek kural altında birleştirilecek.
- Nüans taşıyan tekrarlar varyant olarak korunacak.
- Her iddia `source`, `inference`, `hypothesis` ayrımıyla kaydedilecek.
- Mevcut BR-001–BR-023 kayıtlarıyla eşleştirme yapılacak.

### Çıktılar

- `cilt2-page-coverage.csv`
- `cilt2-claim-registry.json`
- `cilt2-unresolved-claims.csv`

### Tamamlanma ölçütü

109 sayfanın tamamında boş `disposition` sayısı sıfır.

---

## C2-P2 — Tek mum geometrisi

### Kaynak kapsamı

Ağırlıkla Bölüm 1–3.

### Ölçülecekler

- Gövde/aralık oranı
- Üst ve alt fitil oranı
- Yönsel kapanış konumu
- Doji benzerliği
- Uzun gövdeli mum
- Marubozu benzerliği
- Hammer/pin-bar geometrisi
- Shooting-star geometrisi
- Fitil reddi ile gerçek takip ayrımı
- Mum büyüklüğünün ATR ve yakın geçmişe göre konumu

### Körü körüne kullanılmayacaklar

Adlandırılmış mum için tek keyfî eşik doğru ilan edilmeyecek. Sürekli geometrik değerler korunacak; isimler yalnız kayıtlı varyant olacak.

### Sonuç ayrımları

- Trend/range
- Konum
- 1h/2h/4h/1d
- Yukarı/aşağı
- Üst zaman uyumu
- 5/20/40/60 bar

---

## C2-P3 — İki, üç ve çok mumlu diziler

### Kaynak kapsamı

Ağırlıkla Bölüm 4–5.

### Ölçülecekler

- Engulfing varyantları
- Harami/inside dizileri
- İki mumluk geri alma
- İlk baskının ikinci mum tarafından geri alınması
- Morning/evening-star geometrileri
- Üç asker/üç karga benzeri diziler
- Üç mumluk devam
- İlk güçlü mumdan sonraki mum
- Dördüncü itiş ve taşma
- Dizinin ortak iskeleti: baskı → geri alma → takip

### Bilgi tekrarı kontrolü

Mum adı, gövde/fitil/kapanış özelliklerinden daha fazla bilgi ekliyor mu ölçülecek. Eklemiyorsa `duplicate_information` kararı verilecek.

---

## C2-P4 — Baskı, zayıflama ve hareket kalitesi

### Kaynak kapsamı

Bölüm 2–3 ve ilgili devam bölümleri.

### Ölçülecekler

- Gövdelerin küçülmesi
- Fitillerin büyümesi
- Örtüşmenin artması
- Yeni uç mesafesinin kısalması
- Aynı mesafe için gereken bar sayısının artması
- Karşı yönlü mumların büyümesi
- Net mesafe/toplam yol
- Yönsel mum oranı
- Kapanış sürekliliği
- Baskı kaybı ile gerçek karşı baskı ayrımı

### Birleşik fakat önceden kayıtlı varyantlar

- Yalnız gövde kaybı
- Gövde + ilerleme kaybı
- Gövde + ilerleme + örtüşme
- Baskı kaybı + karşı yönlü güçlü kapanış

Birleşik skor, tek bileşenlerin sonucu görülmeden optimize edilmeyecek.

---

## C2-P5 — Sıkışma, genişleme ve ilk taşma

### Kaynak kapsamı

Bölüm 6.

### Ölçülecekler

- Range genişliğinin ATR’ye oranı
- Örtüşme yoğunluğu
- Sıkışma süresi
- Daralan high-low aralığı
- İlk genişleme
- İlk genişlemenin başarısı/başarısızlığı
- Alt/üst sınırı kısa süre aşıp geri alma
- Karşı tarafa genişleme
- Sıkışma konumunun sonucu

### Kritik karşılaştırma

- Büyük genişleme mumu
- Dar/contracted olay barı
- Dış kapanış
- Fitille taşma
- İkinci bar takibi

Mevcut contracted-bar bulgusu bağımsız tekrar deneyinde doğrulanacak.

---

## C2-P6 — Kırılım yaşam döngüsünü tamamlama

### Kaynak kapsamı

Bölüm 7.

### Mevcut altyapı

- Probe
- Close break
- Follow-through
- Acceptance
- Retest
- Failure

### Eklenecek ayrıntılar

- Kırılım mesafesi/ATR
- Kırılım mumunun gövde ve kapanış kalitesi
- Dışarıda kalma süresi
- Eski alana dönüş derinliği
- Failure sonrası karşı tarafa genişleme
- Retest yaklaşma hızı
- Retest geri alma derinliği
- Retest mumu
- Kırılım öncesi sıkışma
- Aynı seviyedeki tekrar deneme sayısı

### Tekrar kontrolü

Acceptance ve follow-through olay örtüşmesi tam oranla raporlanacak; aynı olay iki avantaj sayılmayacak.

---

## C2-P7 — Swing geometrisi ve hiyerarşi

### Kaynak kapsamı

Bölüm 8.

### Ölçülecekler

- Minor/major swing varyantları
- Mesafe
- Süre
- Hız
- Yol verimliliği
- Geri alma oranı
- Eski kırılım bölgesine dönüş
- Major/minor uyumu
- Swing teyit gecikmesinin sonuç üzerindeki etkisi
- Eşit tepe/dip toleransları

### Parametre komşuluğu

- Minor: 1+1, 2+2, 3+3
- Major: 4+4, 5+5, 7+7
- Eşit uç toleransı: 0,10 / 0,25 / 0,50 ATR

Tek en iyi parametre seçilmeyecek; komşuluk dayanıklılığı aranacak.

---

## C2-P8 — İkinci deneme, yeni uç ve çok bacaklı pullback

### Kaynak kapsamı

Bölüm 9–10.

### Mevcut altyapı

- İlk/ikinci bacak mesafe, süre, hız ve verim oranları
- Yeni uç başarısı/başarısızlığı
- Pullback derinliği

### Eklenecekler

- Tek/iki/çok bacaklı pullback
- İkinci denemenin ilk denemeye uzaklığı
- Küçük çift dip/tepe
- Üç itiş
- Beklenen ikinci bacağın hiç gelmemesi
- Başarısız yeni uçtan karşı yapı teyidine zincir
- İlk güçlü karşı mum
- İlk geri itilme
- Güçlü mum sonrası takip
- Pullback sonu altı adımlı akış

### Örnek güvenliği

18–40 olaylı olumlu alt gruplar bağımsız doğrulama olmadan `devam_et` sayılmayacak.

---

## C2-P9 — Yerleşim ve piyasa bağlamı

### Kaynak kapsamı

Bölüm 11 ve Bölüm 13 bağlam kısımları.

### Ölçülecekler

- Olayın trend başı/ortası/sonuna yaklaşık konumu
- Kanal içindeki konum
- Range sınırı/ortası
- Teyitli destek/dirence uzaklık
- Son major swing’e uzaklık
- Hareketin uzamışlık ölçüsü
- Aynı şeklin farklı konumlardaki sonucu

### Amaç

Şeklin kendisi ile bulunduğu yerin katkısını ayırmak.

---

## C2-P10 — Hacim ve çoklu zaman dilimi

### Kaynak kapsamı

Bölüm 12.

### Hacim uygunluk kapısı

- BIST hisseleri, maden ve enerji: veri uygunluğu kontrolüyle
- Endeks ve FX: sıfır/temsili hacim nedeniyle varsayılan olarak dışarıda

### Ölçülecekler

- Göreceli hacim
- Kırılım hacmi
- Pullback hacmi
- Yeni uç oluşurken hacim değişimi
- Hacim azalması ve fiyat ilerleme kaybı
- 1h olay + tamamlanmış 2h/4h bağlamı
- 4h olay + tamamlanmış günlük bağlam
- Üst zaman yön, rejim ve seviye konumu

Tamamlanmamış üst zaman barı kesinlikle kullanılmayacak.

---

## C2-P11 — Tam okuma zinciri ve karar ağacı

### Kaynak kapsamı

Bölüm 13.

### Kitaptaki sıralamanın ölçülebilir karşılığı

1. Bağlam
2. Mevcut kontrol
3. Hareket kalitesi
4. Dönüş/devam/sıkışma ayrımı
5. Kırılım kabulü
6. İkinci deneme
7. Beklenen yeni uç
8. Pullback bitişi
9. Hacim
10. Çoklu zaman teyidi

### Kontrol

Her yeni aşamanın önceki aşamaya marjinal katkısı ölçülecek. Aşama eklemek yalnız olay sayısını azaltıyor fakat benchmark-aşırı sonucu artırmıyorsa gereksiz filtre olarak işaretlenecek.

---

## C2-P12 — Sağlamlık, maliyet ve yanlış keşif kontrolü

### Zorunlu testler

- Kronolojik `%60/%20/%20`
- Sembol bazlı medyan ve pozitif sembol oranı
- XU100-aşırı getiri
- Parametre komşuluğu
- Olay örtüşme matrisi
- İşlem maliyeti stresleri
- Aynı bar hedef/stop belirsizliği
- Kurumsal işlem/anormal sıçrama filtresi
- Çoklu deneme sayısı kaydı

### Sonuç sınıfları

Her kural için:

- Olumlu
- Olumsuz
- Yazı-tura
- Rejime bağlı
- Bilgi tekrarı
- Örnek yetersiz
- Veri uygun değil
- OB/FVG nedeniyle bekletildi

---

# OB/FVG sınırı

Cilt 2’deki OB/FVG metinleri kapsam matrisine alınacak ve kaynak bağlantısı korunacak. Ancak:

- Yeni ana OB tanımı seçilmeyecek.
- Yeni ana FVG tanımı seçilmeyecek.
- Kitap tanımı kullanıcının mevcut sisteminin yerine geçirilmeyecek.
- Son disposition `deferred_ob_fvg` olacak.

Kullanıcının sistemi geldiğinde varyant karşılaştırması yapılacak.

---

# Tamamlanma kriterleri

Cilt 2 yalnız şu koşulların tamamı sağlandığında “deneysel olarak tamamlandı” sayılacak:

1. 109/109 sayfada disposition var.
2. Test edilebilir bütün iddiaların kural kimliği var.
3. Her kuralın kaynak sayfası, matematiksel tanımı ve kod sürümü kayıtlı.
4. Her çalışan kural için nedensellik testi var.
5. Bütün uygun serilerde olay sayımı tamam.
6. Ham, yönlü ve BIST için XU100-aşırı sonuçlar kayıtlı.
7. Eğitim/doğrulama/test ayrımı var.
8. Sembol tutarlılığı var.
9. Olay örtüşmesi ve bilgi tekrarı raporlandı.
10. Olumsuz/yazı-tura sonuçlar silinmedi.
11. Yetersiz örnekler açıkça işaretlendi.
12. OB/FVG bekletme kararı kaynak bazında kayıtlı.
13. `cilt2-unresolved-claims.csv` boş.
14. Yazılım testleri ve bilgi tabanı denetimi başarılı.

---

# Hedef çıktı düzeni

```text
research/experiments/cilt2-completion/
├── README.md
├── cilt2-page-coverage.csv
├── cilt2-claim-registry.json
├── cilt2-unresolved-claims.csv
├── rule-overlap-matrix.csv
├── final-results.md
├── final-summary.json
└── rules/
    └── C2-XXX-<rule>/
        ├── source-links.json
        ├── definition.json
        ├── full-event-results.csv.gz
        ├── time-split-results.csv
        ├── symbol-results.csv
        ├── parameter-results.csv
        └── decision.md
```

Bu program tamamlandığında Cilt 2 için “okundu” değil, **her iddiasının ölçüldüğü, reddedildiği, bağlama alındığı veya gerekçeli biçimde ertelendiği** söylenebilecektir.
