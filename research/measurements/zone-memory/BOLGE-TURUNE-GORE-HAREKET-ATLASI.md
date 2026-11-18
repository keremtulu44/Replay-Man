# Bölge türüne göre hareket atlası — ilk gözlem sınıflaması

**Amaç:** Bölge türüne göre fiyatın ne yapabileceğini anlaşılır hareket çeşitlerine ayırmak; bunların hangilerinin kayıtlarımızda görülebildiğini göstermek. Bu bir hareket tahmini, başarı sıralaması veya al/sat sistemi değildir.

Bu çalışma mevcut ziyaret ve ziyaret içi olay kayıtlarını yeniden sınıflandırır. İlk ölçüm **ASELS, THYAO ve TUPRS; 4 saatlik** üç hisseyle sınırlı bir pilot. Dört tür için aynı hisse/periyot kapsamı kullanıldı. Önceden incelenmiş yaklaşık bir yıllık veri kullanılmıştır. Hacim kullanılmaz. Aşağıdaki çeşitler grafik değil, insanın replay kayıtları üzerinden takip edebileceği bir davranış dilidir.

## 1. Önce ortak dil: Bir bölgede hangi hareketleri ayırt edebiliriz?

Yukarı ve aşağı örnekler birbirinin simetriği olarak okunabilir; ama bu simetrinin aynı sıklık veya sonuç verdiği varsayılmaz.

| Hareket ailesi | Kayıtlarda aradığımız şey | Nasıl yorumlamamalıyız? |
|---|---|---|
| **Geldiği tarafta kapanışlar** | Ziyaretin sonunda iki ardışık dış kapanış, kayıtlı geliş tarafında. | Otomatik olarak güçlü dönüş veya kârlı işlem değil. |
| **Karşı tarafta kapanışlar** | Ziyaretin sonunda iki ardışık dış kapanış, geliş tarafının karşısında. | Bar içinde tam hangi sırayla geçildiği veya kalıcı kırılım bilinmez. |
| **Birden fazla temaslı ziyaret** | Aynı ziyaret içinde en az üç farklı temas mumu. | Temas mumu sayısı ayrı ziyaret sayısı değildir; eşik keşif amaçlıdır. |
| **Dış kapanıştan sonra içeri dönüş** | Ziyarette bir dış kapanıştan sonra daha sonraki bir mum bölge içinde kapanmış. | Tek başına sahte kırılım veya sonrasında hangi tarafa gidileceği anlamına gelmez. |
| **Sınır dışı fitil** | Sınırın dışına taşan high/low, ilgili sınırın iç tarafında kapanış. | Barın içindeki fiyat sırası bilinmez. |
| **Aynı bölgeye yeniden ziyaret** | Bir ziyaret bittikten sonraki 10 kullanılabilir bar içinde aynı bölge kimliğine yeni ziyaret. | Tekrarın başarılı destek/direnç testi olduğunu göstermez; veri yetersizse sansürlenir. |
| **Belirsiz / açık** | Başlangıç tarafı veya iki son dış kapanış tutarlı değil; ya da ziyaret veri sonunda bitmemiş. | Zorla dönüş ya da kırılım sınıfına atanmaz. |

Bu aileler **birbirini dışlamaz**: bir ziyaret hem birden fazla temas içerebilir, hem dış kapanıştan içeri dönebilir, hem sonra karşı tarafta bitebilir. İki sınırın aynı mumda aşılması da ayrıca belirsizlik olarak saklanır.

## 2. Yatay tepe/dip bölgesinde hareket çeşitleri

Burada soru, fiyatın daha önce tepki üreten yatay alanla tekrar karşılaştığında **hangi tarafta kaldığı ve aynı alanı nasıl yeniden kullandığı**dır.

1. **Temas → geldiği tarafta kapanış:** Örneğin üstten geliş ve iki üst dış kapanış. Kapanış vekiliyle aynı taraftadır; daha uzun ayrılış henüz gösterilmez.
2. **Temas → karşı tarafta kapanış:** Örneğin alttan geliş ve iki üst dış kapanış. Yatay alanın diğer tarafına geçmiş kapanışlar vardır.
3. **Fitille taşma → içeride kapanış:** Sınırın test edilip kapanışın iç tarafta olması; aynı mumdaki hareketin sırası ve niyet bilinmez.
4. **Tek ziyaret içinde birden çok temas:** Bölgenin çevresinde birden fazla mum harcanır; bu, üç ayrı ziyaret anlamına gelmez.
5. **Çıkış → sonraki ziyaret:** Bölge aynı kimliğiyle yeniden ziyaret edilir. Sonraki ziyaret önceki karşı taraftan gerçekleşirse iki taraflı kullanım ayrıca incelenebilir; kalıcı rol değişimi henüz otomatik ölçülmedi.

**Kayıt örneği:** ASELS 4s, `z1:v3`, 1 Aralık 2025 10:30 UTC etiketli barda üstten ziyaret; 1 Aralık 10:30 ve 2 Aralık 06:30 etiketli iki mumda bölge üstü kapanış. Ziyaret sonrası 10 kullanılabilir bar içinde aynı bölgeye yeniden ziyaret var. Bu örnekte giriş bandı yaklaşık 184,49–186,31; etiketler gerçek kapanış saati değildir.

## 3. Oyalanma bölgesinde hareket çeşitleri

Bölge geçmişte tanımlı süre boyunca dar bir kapanış aralığında oluşmuştur. Fiyat tekrar geldiğinde, **eski aralığa giriş ve orada geçirdiği yol** özellikle ilginçtir:

1. **Kenardan temas → aynı tarafta kapanışlar:** Eski alanın içine derinleşme olmadan, kapanış vekili geldiği tarafta sonuçlanır.
2. **Bölge içinde çok mum → aynı tarafta çıkış:** Çok sayıda temas ile birlikte geldiği tarafa iki dış kapanış görülür.
3. **Bölge içinden diğer tarafa geçiş:** Geliş tarafının karşısında iki dış kapanış görülür. Bu, kaynak oyalanma alanının gelecekte aynı biçimde işlev göreceği iddiası değildir.
4. **Dışarı kapanış → içeri dönme:** Ziyaret sürerken dış kapanış sonrasında başka bir mum bölgede kapanır. Birkaç kez gerçekleşebilir.
5. **Yeniden gelme ve tekrar oyalanma:** İki ayrı ziyaret üzerinden araştırılabilir. Pilot yeniden ziyareti sayıyor; ikinci ziyaretin tüm karakterini ilkine bağlayarak sınıflandırmıyor.

**Kayıt örneği:** THYAO 4s, oyalanma `z6:v3`: 27 Şubat 2026 10:30 UTC etiketiyle üstten ziyaret; 2 Mart'ta alt sınır dışı fitil kaydı ve sonrasında 2 Mart 10:30 ile 3 Mart 06:30 etiketlerinde iki alt dış kapanış. Aynı ziyarette dört temas mumu var; 10 bar içinde aynı bölgeye yeniden ziyaret gözleniyor. Bu geçişin bar içi sırası veya kalıcılığı bilinmez.

## 4. Hızlı uzaklaşma kaynağında hareket çeşitleri

Bölge, önceden gerçekleşmiş hızlı bir net hareketin kaynak barından oluşur ve ancak hareket eşiği bilindiğinde oluşturulur. Özellikle **kaynağa dönüş ve sonrasında kaynak hareketinin yönüyle ilişkinin** ayrı tutulması gerekir:

1. **Kaynağa dönüş → geldiği tarafta kapanış:** Örneğin önceden yukarı uzaklaşma, sonra üstten bölgeye ziyaret ve iki üst dış kapanış. Kaynak yönüyle uyumlu kapanış vekilidir; hareketin devam edeceği garantisi değildir.
2. **Kaynağa dönüş → karşı tarafta kapanış:** Fiyat kaynak bandının diğer tarafında iki kapanış yapar.
3. **Kaynakta çok temas:** İlk temasla bitmeyip birden fazla mum bölgeyle kesişir.
4. **Dış kapanış → yeniden içeride kapanış:** Ziyaretin yolunda en az bir geri giriş vardır; sonucu ayrıca kaydedilir.
5. **Kaynak bölgeye yeniden geliş:** Bitmiş ziyaret sonrasında yeni ziyaret oluşabilir. Eski kaynak kimliği ve tüm geçmişi korunur.

**Kayıt örneği:** ASELS 4s, yukarı yönlü hızlı çıkış kaynağı `z5:v1`: 22 Ocak 2026 06:30 UTC etiketli barda üstten ziyaret; hem 06:30 hem 10:30 etiketli mumlar bölge üstünde kapanıyor. Bandın ziyaret başlangıcındaki yaklaşık sınırları 280,88–294,63. Sonraki 10 kullanılabilir bar içinde aynı bölgeye yeni ziyaret kaydı yok. Bu, gelecekte yeniden ziyaret olmayacağı anlamına gelmez.

## 5. Eğimli hizada hareket çeşitleri

Burada bandın merkezi her kullanılabilir barda eğime göre hareket eder. Bu nedenle sadece fiyatın değişimini değil, **fiyatın o andaki hareketli banda göre konumunu** inceleriz:

1. **Hizaya yaklaşma → geldiği tarafta kapanış:** İki dış kapanış girişin aynı tarafında; eğimli bandın ilerleyişi de hesaba katılır.
2. **Hizanın karşı tarafında kapanış:** İki dış kapanış girişin karşı tarafında görülür. Bu, kalıcı trend kırılımı değildir.
3. **Hiza çevresinde çok temas:** Ziyaret süresince birkaç mum hareketli bantla kesişir.
4. **Bant etrafında sınır taşmaları:** Fitiller, bazen karşılıklı sınır taşmaları kaydedilir; iki sınır aynı barda aşıldığında sıra belirsizdir.
5. **Ayrılış ve yeniden temas:** Aynı çizgi kimliği sonraki barda veya birkaç bar sonra yeniden ziyaret edilebilir.

Eğim, gerçek geçen saatten değil, **kullanılabilir bar sırasından** hesaplanır. Kısmi 4s mumlar dışlandığından duvar saatinde eğim yorumuyla aynı olmak zorunda değildir. Karma tepe–dipten geçen çizgiler otomatik olarak anlamlı trend çizgisi sayılmamalı.

**Kayıt örneği:** ASELS 4s karma eğimli `z12:v2`: 11 Aralık 2025 06:30 UTC etiketiyle üstten ziyaret, üç temas mumu, 12 Aralık 06:30 ve 10:30 etiketlerinde hareketli bandın altında iki kapanış. Sonraki 10 kullanılabilir barda aynı çizgiye yeni ziyaret kaydı var. Başlangıçta bant yaklaşık 204,56–206,10; eğimi bar başına yaklaşık +1,127 olduğundan sonraki bant sınırları sabit değildir.

## 6. İlk pilotta hangi çeşitler gözlendi?

Aşağıdaki tablo, her tür içinde hisse/bar başına önceden belirlenen kimlik sırasına göre **tek temsilî ziyaret** seçilerek oluşturuldu. Türler arasında aynı hisse/mum hâlâ ortak olabilir. Bölge genişlikleri, seçilen adaylar ve geometri yöntemleri farklıdır; sayılardan türler arası üstünlük veya genel olasılık çıkmaz.

| Bölge | Ziyaret | Aynı tarafta biten | Karşı tarafta biten | Belirsiz | Açık/sansürlü | 3+ temas mumu |
|---|---:|---:|---:|---:|---:|---:|
| Yatay | 766 | 454 | 212 | 98 | 2 | 244 |
| Oyalanma | 349 | 284 | 55 | 1 | 9 | 205 |
| Hızlı uzaklaşma | 487 | 363 | 106 | 12 | 6 | 226 |
| Eğimli | 1.262 | 726 | 336 | 195 | 5 | 341 |

Son sütun diğerleriyle **örtüşür**. Aynı/karşı taraf, ziyaret sonundaki iki ardışık dış kapanışa dayalı bir vekildir; birbirini izleyen iki kapanış karşılıklı taraflarda ise `unknown`. Bölge geometrileri farklı olduğundan ve günlük dönemler ya da bütün hisseler karşılaştırılmadığından örneğin “oyalanma bölgesi daha güçlüdür” sonucu çıkarılamaz. Tam ziyaretli görünüm ve ek olay sayıları [summary.csv](path-taxonomy-pilot/summary.csv); olay bazında bandın başlangıcı, kimlik, sınıflar ve sansür bilgisi [paths.csv.gz](path-taxonomy-pilot/paths.csv.gz).

**Ne henüz genellenmedi?** Hangi türde hangi biçimin daha sık olduğu; hızlanma/yavaşlama ile sınıfların ilişkisi; iki tepki sonrası sonraki ziyaret; gerçek bölge–bölge yol ve kesişimi; ayrılışın büyüklüğü; türlerin 1s/2s/4s/günlük evren genelinde aynı tanımla karşılaştırılması; bağımsız uzun geçmiş doğrulaması. Mevcut üç-hisse 4s pilotu bunları kanıtlamaz.

## 7. Çalışma mantığı ve tekrar üretim

Bölgenin türünü ve başlangıçta bilinen geçmişini kaydet. Her ziyaret için **geliş tarafı → temas mumları / kapanışlar / fitiller → bitiş → sonraki aynı-bölge ziyareti** dizisini üret. Ziyaretin sonucu yalnız son gerekli kapanıştan sonra bilinir; 10 bar içinde yeniden ziyaret özelliği de ancak yeni temas gerçekleştiğinde veya 10 bar tamamlandığında bilinebilir. Bunlar önceki karar anlarına taşınmaz.

```bash
.venv/bin/python -m tools.describe_zone_paths \
  --output research/measurements/zone-memory/path-taxonomy-pilot
.venv/bin/python -m pytest -q
```

Girdi dosyaları ve SHA-256 değerleri [summary.json](path-taxonomy-pilot/summary.json)'da. Ham [yatay](pilot-4h-atr025/visit-events.csv.gz), [oyalanma](pilot-multiframe-dwell-atr025/visit-events.csv.gz), [hızlı çıkış](pilot-multiframe-impulse-atr025/visit-events.csv.gz) ve [eğimli](pilot-4h-sloped-atr025/visit-events.csv.gz) ziyaret içi olay kayıtları örneklerin tekrar incelenmesini sağlar. `bar_ts` seans kapanışı değil veri etiketidir; 4s seride kısmi mumlar çıkarılmıştır.
