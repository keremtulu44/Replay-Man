# Lifecycle içinde küçük filtreler — keşif

**Kısa sonuç:** Evet, yaşam döngüsü olaylarını daha küçük ve anlamlı gruplara ayırabiliriz. İlk iki filtreyi mevcut kayıtlarda denedik: **yeniden ziyaretin gecikmesi** ve **ziyaret içindeki temas mumları**. Bir araştırma adayı çıktı; ancak bu aday henüz doğrulanmış sinyal değildir. Tüm veri önceden incelendiği ve çok sayıda alt grup denendiği için sonuçlar keşif niteliğindedir.

## 1. Bu kez hangi soruyu sorduk?

Daha önceki iki olay türünü kullandık:

- **Geçiş → aynı taraftan yeniden ziyaret:** Bölgeyi karşı tarafta iki kapanışla geçen ziyaret, ardından aynı bölgeye yeni taraftan gelen ve o tarafta iki kapanışla biten hemen sonraki ziyaret.
- **Aynı → aynı:** Bir önceki ve sonraki ziyaretin ikisi de kendi geliş tarafında bitmiş; ikinci ziyaret önceki bitiş tarafıyla aynı taraftan gelmiş. Bu, basit bir gözlemsel karşılaştırma grubudur.

İkinci ziyaret bittikten sonra 5 barlık sonucu iki grupta karşılaştırdık. Yine hisse/periyot/tür/bitiş barı için bir temsilci seçildi; türler arasında aynı bar tekrarlanabilir. Kayıtlar nedensel zamanla üretilmiş olsa da gruplar **aynı hisse ve tarihte eşleştirilmiş değildir**. Geçmiş, oynaklık, bölge genişliği veya piyasa koşulları farkı sonuca karışabilir.

### İki küçük filtre

1. **Gecikme:** Önceki ziyaretin bitişinden sonraki ziyaretin **başlangıcına** kadar geçen kullanılabilir bar sayısı `1–10` veya `11+`. Önceki ziyaret oluşmadan bilinmez; bu araştırmada ikinci ziyaretin tamamlandığı andaki karara ait özelliktir.
2. **Temas yoğunluğu:** İkinci ziyaret içinde `1–2` veya `3+` ayrı temas mumu. Bu değer yalnız ziyaret sonunda kesin bilinir; tek bir temas anında 3+ etiketi kullanılamaz. Üç temas mumu, üç ayrı ziyaret değildir.

Filtreler birbirinden ayrı denendi, kombine edilmedi. Bu eşikler **araştırma varyantıdır**, evrensel değer değildir. Daha sonra seçildi ve ön-kayıtlı değildir.

## 2. Dikkat çeken aday: 4s yatay bölge, aşağı senaryo, geç gelen ziyaret

Filtre: **Yatay 4s → üstten geliş ve altta tamamlanan geçiş → aynı bölgeye alttan sonraki ziyaret 11 veya daha fazla kullanılabilir bar sonra başlıyor → o ziyaret altta tamamlanıyor.**

Son ziyaret bittikten sonra beş barlık **aşağı yönlü XU100-aşırı** sonuç medyanı:

| Bölüm | Geçiş → aynı taraf | Aynı → aynı karşılaştırması | Medyan farkı |
|---|---:|---:|---:|
| Eğitim | +%1,10 · n=235 | +%0,84 · n=329 | +0,27 puan |
| Doğrulama | +%1,12 · n=128 | +%0,03 · n=216 | +1,09 puan |
| Tarihsel test | +%0,53 · n=143 | −%0,26 · n=199 | +0,78 puan |

Formül: `(hisse getirisi − XU100 getirisi) × −1`. Pozitif fark, grubun bu ölçüde daha yüksek medyana sahip olduğunu gösterir; fiyatın mutlaka düştüğünü, işlemin kazançlı olduğunu veya bölgenin nedensel etkisini göstermez. Bu örnekte tarihsel testte geçiş grubunun **ham aşağı yönlü** beş bar medyanı +%1,46'dır; bu grup için ham hisse getirisinin medyanı −%1,46'ya karşılık gelir. Başka olaylar ve dönemler farklı olabilir.

İlgili haftalık blok bootstrap medyan-fark aralıkları doğrulamada yaklaşık **[+0,23; +1,72]**, tarihsel testte **[+0,14; +1,29] yüzde puanı**; eğitimde aralık sıfırı kapsar. Bunlar çok sayıda alt grup incelendikten sonra seçilen sonuçlardır, yaklaşık 10–11 haftalık bölümlere dayanır ve haftalar arası örtüşen ufuklar ile tüm bağımlılığı çözmez. Güvenilir bağımsız doğrulama veya çoklu deneme düzeltmesi değildir.

Daha önemli kontrol: Tarihsel testte grupların her birinde en az üç olay bulunan **yalnız 5 ortak hisse** vardı. Bunların 2'sinde geçiş grubunun hisse medyanı daha yüksek, 3'ünde daha düşüktü. Bu az sayı, toplu farkın hisseler arasında ne kadar yaygın olduğunun belirsiz kaldığını gösterir.

### Neden bu filtreyi araştırmaya değer görüyoruz?

Aynı yatay 4s aşağı senaryoda, **1–10 bar içinde** yeniden ziyaret için gruplar arası fark doğrulamada yaklaşık −0,06, testte −0,24 puandı. Dolayısıyla bu keşif, “her yeniden ziyaret aynıdır” yerine **geç gelme ile erken gelmeyi ayrı inceleme** fikrini destekler. Fakat bu iki farkın birbirinden güvenilir biçimde farklı olduğu ayrıca test edilmedi; tek başına bu farklardan işlem kuralı çıkarılmaz.

Bu alt grupta 10 barlık ileri ufuk medyanları da kaynak tabloda vardır. Daha uzun ufukta dönem sınırında daha fazla olay dışlandığından, 5 ve 10 bar grupları bire bir aynı örnek değildir.

## 3. Temas sayısı ve diğer hücreler

`1–2` ve `3+` temas mumu ayrımı da aynı grup ve tarihlerde incelendi. Bazı hücrelerde farklı işaretler veya iki dönemde benzer yönler görülse de az sayıda olay/hisse, geniş aralıklar ve 192 alt karşılaştırma nedeniyle **genellenmiş “çok temas güçlendirir” veya “az temas daha iyidir” kuralı çıkmadı**.

Yalnız karşılaştırma ve tarihsel testte her grupta en az 30 beş bar endeks eşleşmesi olan **56** filtre/tür/yön/periyot hücresinin 33'ünde farkın işareti aynıydı. Bu eşik gözlem sayısına yönelik kaba bir filtredir; hisse bağımsızlığı sağlamaz. Uygun 56 hücreden yalnız 1'inde her iki dönemin haftalık keşif aralığı aynı tarafta sıfır dışındaydı: yukarıdaki 4s yatay/geç/aşağı aday. Bu sayı, **192 karşılaştırmaya bakılıp seçilen bir adayın rastlantısal görünme riskini** ortadan kaldırmaz.

## 4. Kapsam, sınırlamalar ve sonraki sınama

Bu tarama **100 hissenin günlük ve 4s** yatay, oyalanma, hızlı çıkış ve eğimli lifecycle kayıtlarını kullanır. Fiyat/endeks başlangıç ve bitiş etiketleri eşleşmeyen ve beş bar sonucu dönem sınırını aşan olaylar ilgili ölçüden dışlandı. 4s'de `10 bar`, kısmi mumlar çıkarılmış kullanılabilir bar sayısıdır; doğrulanmış 40 saatlik veya eşit işlem süresi değildir. Aynı bölgenin 10 bar sonra yeniden gelişini incelerken gerçekleşmeyen yeniden ziyaretler bu örnekte yoktur; bu yüzden sonuç gerçekleşme olasılığı değildir.

Adayı gerçekçi biçimde sınamak için:

1. Aynı hisse, yakın tarih, aynı yön ve benzer oynaklık/bölge koşullarında geçiş→yeniden ziyaret ile karşılaştırma olaylarını eşleştir; kaç olayın eşleşmediğini açıkça göster.
2. `11+` eşiğinin komşu değerlerini ayrıca, sonuçlara bakıp en iyisini seçmeden test et; çok uzun süreleri ayrı göster.
3. Başlangıçta geçişten itibaren hiç dönmeyenleri ve veri bittiği için sonucu bilinmeyenleri sansürlü olay olarak da ölç.
4. Hipotezi sabitleyip daha önce incelenmemiş, daha uzun veri ve doğrulanmış seans saatleriyle bağımsız test et. Maliyet ve uygulanabilir emir olmadan kârlılık iddiasında bulunma.

## 5. Dosyalar ve tekrar üretim

- [Tüm alt gruplar](lifecycle-filters/groups.csv), [karşılaştırmalar / blok aralıkları / hisse sayıları](lifecycle-filters/comparisons.csv), [girdi ve kod hash'leri](lifecycle-filters/summary.json).
- Kaynak olaylar ve önceki kapsam: [lifecycle raporu](SENARYO-LIFECYCLE-DOGRULAMA.md). `events.csv.xz` dosyaları günlük/4s tür dizinlerindedir.

```bash
.venv/bin/python -m tools.analyze_lifecycle_filters \
  --output research/measurements/zone-memory/lifecycle-filters --draws 500
.venv/bin/python -m pytest -q
```
