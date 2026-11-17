# Brent ve BIST: aynı 10 mumda ne oldu?

**Kısa cevap:** Kullanıcının verdiği türden örnekler bu arşivde gerçekten var. Ancak Brent +%4 olduğunda TUPRS'nin her zaman veya çoğunlukla -%3 düştüğü sonucunu bu veriden çıkaramıyoruz. Sonucu hem **aynı 10 mumda** hem de **sonraki 10 mumda** ayrı ölçtük.

## Önce örneğin kendisi

4 saatlik, birbirleriyle çakışmayan kaynak-şok pencerelerinden test dönemindeki iki örnek:

| BIST 10 mumluk pencere, UTC | Brent değişimi | TUPRS aynı 10 mum | TUPRS sonraki 10 mum |
|---|---:|---:|---:|
| 1 Eylül 2026 10:30 → 8 Eylül 2026 10:30 | +%6,48 | -%5,00 | +%4,49 |
| 14 Ekim 2026 10:30 → 21 Ekim 2026 10:30 | +%4,08 | -%9,07 | -%0,91 |

Bu iki örnekte Brent'in ölçülen saatlik kapanışları, BIST pencere uçlarından **30 dakika önceye** aittir. Brent yönünü ancak pencerenin sonunda biliyoruz; aynı 10 mumdaki TUPRS düşüşünü önceden bilip ilk mumdan işlem yapmış gibi yorumlayamayız. Sonraki 10 mum da kapanıştan kapanışa, masrafsız bir **fiyat etiketi**; gerçekleştirilebilir emir fiyatı değildir.

## Kaç kez görüldü?

Brent USD değişimi ≥+%4 iken TUPRS aynı pencerede ≤-%3 düşmüş mü? Bütün 10 bar pencerelerinde:

| BIST mum periyodu | Eğitim | Doğrulama | Test |
|---|---:|---:|---:|
| **1 saatlik** | 7 / 145 | 4 / 49 | 1 / 36 |
| **4 saatlik** | 7 / 65 | 0 / 30 | 7 / 22 |

Pay, Brent koşulu sağlanıp TUPRS düşüşü de görülen pencere; payda, Brent koşuluna uyan ve hisse sonucu geçerli olan pencere sayısıdır. Toplam **26 pencere**, fakat art arda kayan pencereler aynı mumları paylaşır; 26 bağımsız olay değildir. Aynı piyasa hareketi hem 1h hem 4h tabloda bulunabilir.

Çakışmayı azaltmak için, her dönemde Brent koşulunu sağlayan **ilk 10 mumluk pencereyi**, sonra yalnız başlangıcı önceki seçilen pencerenin sonundan sonra olan yeni pencereyi tuttuk. Seçim TUPRS sonucuna bakmaz:

| BIST mum periyodu | Eğitim | Doğrulama | Test |
|---|---:|---:|---:|
| **1 saatlik** | 1 / 28 | 1 / 8 | 0 / 13 |
| **4 saatlik** | 4 / 12 | 0 / 5 | 2 / 6 |

Bu seçim de piyasa şoklarını istatistiksel olarak bağımsız yapmaz; 5–13 gibi sayılar özellikle küçük. Seçilen pencerelerde tüm hisse sonuçlarının görülebilmesi, ileri dönemde aynı oranın tekrarlanacağı anlamına gelmez.

## Baz oran ve alternatif

4h **test** döneminde, Brent +%4 pencerelerinde TUPRS ≤-%3 sonucu **7/22**; Brent yönüne bakılmayan tüm geçerli 10-bar pencerelerinde **33/93**. Bu iki grup iç içedir ve kayan pencereler tekrarlıdır: bunları nedensel etki veya istatistiksel üstünlük diye okumamak gerekir. Aynı dönemde Brent ≤-%4 pencerelerinde TUPRS ≤-%3 **11/24**. Sonuç, petrol ve rafineri hissesinin her dönemde mekanik ters hareket ettiği varsayımını desteklemiyor; ancak örnekteki eşzamanlı hareketin varlığını açıkça gösteriyor.

4h testte Brent +%4 koşulunun **çakışmayan altı penceresinin** ikisinde TUPRS aynı pencerede ≤-%3. Bu altı sinyalin **sonraki** 10 mumunda da ≤-%3 iki kez görüldü; fakat aynı iki olay olmak zorunda değil. Bu, tek başına işlem kuralı veya maliyet sonrası getiri hesabı değildir.

## Nasıl hesaplandı?

- 100 BIST hissesi ve 10 endeks; Brent, WTI ve beş metal ayrı kaynak. **1h ve 4h** ayrı ölçüldü. 10 mum, XU100 takviminde mevcut 10 BIST barıdır; hafta sonları ve seans araları nedeniyle 10 takvim saati veya 40 takvim saati değildir.
- Pencere başındaki ilk hedef bar **açılışı → 10. bar kapanışı** ve aynı aralıkta Brent'in as-of USD değişimi karşılaştırıldı. Hedefte 10 referans barının tamamı aynı zamanlarda ve sırada mevcut olmalı.
- **Sonraki 10 mum:** Olay barının kapanışı → sonraki 10. ortak bar kapanışı. Aynı mumda görülen fiyat değişiminden ayrı; gecelik boşluk bu ikinci fiyat değişimine dahildir.
- USD ve emtia×USD/TRY yaklaşık TRY vekili ayrı hesaplandı. Emtia ve kur için yalnızca pencere uçlarında nominal olarak tamamlanmış, en fazla 90 dakika eski 1h barlar kullanıldı. USD vadeli kontratı, gerçek TRY maliyetini veya kontrat roll etkisini doğrudan temsil etmez.
- Önceki araştırmalarda kullanılan UTC eğitim/doğrulama/test bölümleri yeniden kullanıldı; pencere sonucu bölüm sınırından taşarsa boş bırakıldı. Bunlar **daha önce incelenmiş** dönemlerdir. Maliyet, spread, finansman, portföy ve açığa satış uygulanabilirliği ölçülmedi.
- Tüm kayan pencereler yanında sabit takvimde çakışmayan pencereler ve kaynak koşuluna göre seçilen şok pencereleri ayrı. Şok seçiminin baz oranı, bütün pencerelerle birebir eşleştirilmiş kontrol grubu değildir.

## Büyük kaynak sıçraması duyarlılığı

İlk sonuçlara baktıktan sonra, bazı Brent pencerelerinde ardışık mevcut saatlik kapanışlar arasında %10'u aşan değişimler görüldüğü için **sonradan eklenen** ayrı bir duyarlılık kontrolü uygulandı. Bu hareketlerin hata, kontrat geçişi ya da gerçek fiyat hareketi olduğunu doğrulamadık; ana sonuçlardan otomatik silmedik. `no_jump10` görünümü bu pencereleri ayrı tutar, kaynak koşulu için şok pencerelerini yeniden seçer.

Örneğin 4h testte Brent +%4 / TUPRS ≤-%3: bütün kayan pencerelerde **7/22**, çakışmayan şok pencerelerinde **2/6**; %10 sıçrama dışı duyarlılıkta da bu test sayıları aynıdır. 1h doğrulamada ise 4 eşleşen kayan pencerenin tamamı bu sonradan eklenen filtre dışında kalır. Yani veri/kontrat duyarlılığını sayılarda göstermek gerekir; bu gözlem bütün verinin hatalı olduğu anlamına gelmez.

## Dosyalar

- [Brent–TUPRS eşleşen tarihlerin tamamı](brent-tuprs-matches.csv): USD Brent ≥%4 ve aynı 10 mumda TUPRS ≤-%3; iki periyot ve tüm bölümler, fiyatlar/tarih, sonraki getiri ve çakışma bayrakları.
- [Brent–TUPRS özet sonuçları](brent-tuprs-ozet.csv): tüm bazlar, Brent ±%4, ham/duyarlılık ve aynı/sonraki 10 mum; `down3_count / n` ilgili düşüş oranıdır.
- `conditional-statistics.csv.gz`: 7 kaynak × 110 hedef, 1h/4h, USD/TRY vekili, ≥+%2/+%4, ≤-%2/-%4, sakin/tüm pencere, örnekleme ve bölümler.
- `source-windows.csv.gz`: as-of kaynak ve kur fiyatları, zamanları, kaynak sıçraması ve kaynak şoku seçim bayrakları.
- `target-availability.csv`, `input-manifest.csv`, `summary.json`: hedef geçerlilik sayıları, 228 kaynak dosya SHA-256 kayıtları ve koşu özeti.
- [Sabitlenen araştırma planı](PLAN.md).

```bash
.venv/bin/python -m tools.measure_tenbar_reactions
.venv/bin/python -m pytest -q
```

Girdi arşivi `data/ohlcv/` Git dışında olabilir. Eşikler kullanıcı örneğinden ve önceden yazılan plandan alınmıştır; 10-gözlem etiketi istatistiksel anlamlılık değil, yalnız örnek büyüklüğü göstergesidir. Tek bir yıl, çoklu denemeler, vadeli ürün roll'u ve ortak piyasa hareketleri nedeniyle **al-sat önerisi, nedensellik veya kârlılık ispatı yoktur**.
