# Dip pilotu ve P6 düzeltmesi — sonuçlar

**Tarih:** 19 Kasım 2026. **Genel karar: `exploratory`, işlem kuralı onaylanmadı.** İleri gözlem henüz `blocked_data`. Mevcut dönemler önceden incelenmiş, harici dönem ise aynı piyasa sağlayıcı ailesinden alınmış geçmiş veridir. Aşağıdakiler yatırım tavsiyesi, gerçek emir veya portföy getirisi değildir.

> **Ek genel inceleme:** [Eşzamanlı farklı-hisse kontrolü ve sonuçların yeniden denetimi](../general-review/README.md), A'nın dip vekiliyle ilişkisi için işlem getirisi avantajını doğrulamayan ek karşılaştırmaları ve eski acceptance adayının kısıtlarını içerir. Buradaki 7–9 haftalık kısa dönem bootstrap aralıkları ek incelemenin daha ihtiyatlı eşiklerini karşılamaz; teyit edici kanıt değildir.

## Dört aşamanın durumu

1. **Nedensellik ve hizalama düzeltildi.** P6 karşı genişleme, failure satırına gelecekten yazılmak yerine teyit edildiği barda ayrı olaydır. XU100 başlangıç **ve** bitiş etiketi hisseyle eşleştirilir. Eski ileri-bilgili sonuç ve `continue` kararı geri çekildi; [ayrıntılı P6 sonuçları](../p6-causal/README.md).
2. **Dar dip pilotu uygulandı.** [Keşif sözleşmesi](PLAN.md) ile hacimsiz A, B ve C adayları; yerel dip vekili, sansür ve geçmişte bilinebilirlik ayrıldı. A/B/C'nin başarılı olması varsayılmadı.
3. **Getiri, risk ve maliyet ölçüldü.** İki periyot, iki ufuk, sonraki/gecikmeli açılış, stop/hedef sırası belirsizliği ve dört maliyet senaryosu hesaplandı. Son tarihsel dönemde aday bazında olumlu net medyan gösterilemedi; B için karşılaştırma aralıkları sıfırı kapsıyor.
4. **İleri gözlem altyapısı kuruldu, doğrulama henüz yapılamadı.** Kurallar ve 202 ısınma dosyasının hash'leri 19 Kasım 2026 14:55 UTC'de yerel olarak kaydedildi; ileri başlangıç 20 Kasım İstanbul günüdür. İlk kayıt 0 yeni bar ile `blocked_data`. Yerel hash/saat bağımsız zaman damgası değildir; haricen sabitlenmesi gerekir. [İleri protokol ve komutlar](FORWARD.md).

## Ne ölçüldü?

- **A — failed_low5:** önceki beş barın dibinin altı görülüp üzerinde ve bar açılışından yukarıda kapanış. Aynı hisse/periyotta seçilen A'lar arasında en az 10 kullanılabilir bar bırakıldı.
- **B — destekli A:** A'dan önce 2+2 swing ile bilinen, destek rolündeki yatay adayla temas ve kapanış koşulları. B, A'nın alt kümesidir; B ile destek bulunmayan A aynı aday havuzundaki ayrı gruplardır.
- **C — B + teyit:** B'den sonra 1–5 barda ilk `close > B.high`. C kendi kapanışında başlar; B zamanına taşınmaz. Teyit bekleyerek giriş geciktiği için C ile A/B farkı eşleştirilmiş etki değildir.
- **Dip etiketi:** yalnız sonradan bilinen 5+5 sağ-eşitlik yerel dip; sinyal pivotun 2 bar öncesi–3 bar sonrasında ve dipten en fazla 1 ATR yukarıda kapanmalıdır. Bu, gerçek/mutlak dibi kanıtlamayan seçilmiş bir vekildir. Dip etiketi tam bilinmeyen sinyal yanlış alarm sayılmadı.
- **20 bar sonucu:** bir sonraki kullanılabilir açılıştan 20. kullanılabilir bar kapanışına ham getiri ve aynı etiketlerden XU100 farkı. Ayrı bir varsayımsal işlemde girişten 1 ATR stop/2 ATR hedef uygulanır; gap açılışından çıkış kullanılır, aynı barda ikisi görülürse iki sıra için alt/üst sonuç saklanır. Aşağıdaki net medyan, **kötümser sıra** ve gidiş-dönüş **%0,25 varsayımsal** maliyet içindir. 10 bar, gecikmeli giriş ve diğer maliyetler CSV'lerdedir.

Tam ufku dönem/veri sınırına sığmayan sonuç `censored` sayılır. Stop önceden vurulmuş olsa bile karşılaştırmanın tüm kolları için tam 20-bar pencere aranır; bu nedenle rapor tamamı gözlenmiş olaylara koşulludur. MFE/MAE tam 20 bar üzerinden ölçülür, gerçekleşmiş stop işlemindeki zarar değildir.

## İç dönem — son tarihsel bölüm

Dönem: 1 Eylül–mevcut verinin sonu, tümü önceden incelenmiş veri. Yüzdeler hisse başına olay ölçüsüdür; olumlu XU100 farkı pozitif işlem getirisi anlamına gelmez.

| Periyot / aday | Sinyal | Dip eşleşmesi / etiketi bilinen | 20 bar sonuç / sansür | Ham medyan | XU100-aşırı medyan | İşlem net medyanı (%0,25) | Net pozitif oranı |
|---|---:|---:|---:|---:|---:|---:|---:|
| 4s A | 412 | 79 / 384 (%20,6) | 360 / 52 | -%4,35 | -%0,27 | -%2,69 | %18,6 |
| 4s B | 227 | 42 / 211 (%19,9) | 197 / 30 | -%4,82 | -%0,89 | -%2,61 | %17,8 |
| 4s C | 112 | 3 / 103 (%2,9) | 94 / 18 | -%4,12 | -%0,87 | -%2,47 | %22,3 |
| Günlük A | 215 | 29 / 204 (%14,2) | 127 / 88 | -%9,23 | +%0,91 | -%4,45 | %14,2 |
| Günlük B | 106 | 15 / 103 (%14,6) | 70 / 36 | -%8,55 | +%1,02 | -%4,31 | %10,0 |
| Günlük C | 64 | 4 / 61 (%6,6) | 42 / 22 | -%7,82 | +%1,10 | -%4,09 | %7,1 |

A'nın 4s son dönemde kapsadığı **benzersiz** referans dip 79/605 (%13,1), günlükte 29/305 (%9,5). Bu sayı sinyal başına eşleşme oranından farklıdır. C'nin geç teyit ve ATR şartıyla dip etiketini daha az yakalaması doğrudan kârlılık veya tek başına yanlış yöntem kanıtı değildir.

4s A'nın 360 sonuçlu olayında 20 barlık medyan MFE +%3,42, medyan MAE -%9,04; MAE'nin %5 yüzdelik dilimi -%26,66'dır. Bu kuyruk riski, gerçek işlemdeki stop zararına eşit değildir. Aynı 4s A örneğinde varsayımsal işlem medyanı maliyet **%0 / %0,10 / %0,25 / %0,50** iken sırasıyla **-%2,44 / -%2,54 / -%2,69 / -%2,94**. 20 barı tamamlanmış sonuçlar sadece 9 farklı haftaya yayılmıştır; 100 hisse 360 bağımsız piyasa rejimi demek değildir.

### Destek filtresinin katkısı ve gecikme

- Son dönem 20-bar XU100 farkında B eksi bölgesiz A medyan farkı 4s'te **-1,39 yüzde puan**, hafta-kümeli keşif %95 bootstrap aralığı **[-2,60; +1,47] puan** (197 B, 163 bölgesiz A; 9 hafta). Günlükte **+1,24 puan**, aralık **[-3,67; +6,73]** (70 B, 57 bölgesiz A; 7 hafta). Aralıklar sıfırı kapsar. Gruplar disjoint, eş zamanlı adaylardır; hisse/rejim/özellikleri dengelenmiş nedensel eşler değildir. Haftalık bootstrap, haftalar arası 20-bar örtüşme ve çoklu denemelerin tüm bağımlılığını çözmez.
- Giriş bir bar daha geciktirilince **aynı 359 tamamlanmış 4s A sinyalinde** ham 20-bar medyan -%4,35'ten -%4,11'e, varsayımsal işlem brüt medyanı -%2,45'ten -%2,41'e değişti. Bu, uygulanabilir avantaj kanıtı değil; aynı olaylarda gecikme hassasiyetidir. Tüm adaylar için eş-sinyal tablosu `internal/paired_delay_summary.csv` içindedir.
- Önceden görülen eğitim/doğrulama/test iç dönemlerinde 4s A varsayımsal net işlem medyanı sırasıyla **-%2,00 / -%1,97 / -%2,69**; günlük A için **-%3,09 / -%3,28 / -%4,45**. Bunlar birbirinden bağımsız ileri testler değildir ve median, ortalamanın yerine geçmez.

## Sabit harici geçmiş — bağımsız ileri test değil

[megecr/bist-pairs-trading](https://github.com/megecr/bist-pairs-trading/tree/f4a353bf9cf1ac3621c294fb397b812c5691e099), MIT lisanslı depo, commit `f4a353bf9cf1ac3621c294fb397b812c5691e099`. Arşiv SHA-256 `1c9cd340ae1b3505ca7c1c5e520b138bd4197294ba16a6a103d410f1be737f90`. Depodaki 92 günlük CSV'den mevcut hisse evreniyle kesişen **68 hisse**, **81.460** ham bar; sinyaller yalnız 1 Ocak 2022–31 Ekim 2025. 34 çok küçük IEEE OHLC yuvarlama sapması, keşif planında belirtilen `1e-9` nispi toleransla sayılarak düzeltildi. Daha büyük geometri hatasında seri reddedilir.

Bu dosyalar yfinance kaynaklıdır; indirme kodu `auto_adjust` politikasını sabitlememiştir ve harici güvenilir XU100 yoktur. Dolayısıyla hem aynı sağlayıcı ailesi/bugünkü evren yanlılığı hem kurumsal işlem ve fiyat ayarı belirsizliği vardır; endeks farkı **unknown**, sıfır değildir. Arşivin yeniden işlenmiş 2026 verileri, 2022'de gerçekten böyle görüldüğünün kanıtı değildir.

| Günlük geçmiş / aday | Sinyal | Dip eşleşmesi / bilinen | 20 bar sonuç / sansür | Ham medyan | %0,25 maliyetle işlem medyanı | Aynı maliyetle işlem **ortalaması** | Net pozitif oranı |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | 2.183 | 754 / 2.180 (%34,6) | 2.137 / 46 | +%0,87 | -%3,27 | **+%0,35** | %39,9 |
| B | 906 | 305 / 905 (%33,7) | 884 / 22 | +%0,78 | -%3,54 | -%0,16 | %36,5 |
| C | 599 | 57 / 595 (%9,6) | 585 / 14 | +%2,09 | -%3,35 | -%0,02 | %37,8 |

Olumlu A ortalaması saklanmamalıdır; fakat ortalama olayları ağırlıklandırır, sonuçlar bağımlıdır, ortalama ile medyan farklı şeylerdir ve endeks/maliyet doğrulaması yoktur. Bu tek geçmiş hücre kârlılık veya bağımsız doğrulama kanıtı değildir. Aynı geçmişte 5+5 diplerin A ile kapsamı 754/3.577 = **%21,1**. B ile bölgesiz A'nın brüt sabit ufuk medyan farkı -0,15 puan, keşif aralığı [-1,65; +1,07] puandır; destek filtresi için tutarlı ek avantaj göstermez.

## Veri ve risk sınırlamaları

- İç evrende güncel 100 hisse; 1 günlük 25.095 ve 4s **49.754 tam** hisse barı kullanıldı. 4s hisse tarafında **24.777**, XU100 tarafında 248 kısmi bar dışlandı. Dolayısıyla “sonraki bar” bazı seans sonu kısmi barları atlar. Bar etiketleri gerçek borsa kapanışı, emir gecikmesi veya gerçekleşmesi olarak doğrulanmadı.
- Yerel günlük fiyatlar `auto_adjust=false` politikasıyla saklanmıştır; split/temettü ve sağlayıcı geçmiş düzeltmeleri ayrı doğrulanmış fiyat getirisi değildir. Son dönem günlük A'nın 127 tam 20-bar penceresinin birinde split, altısında temettü kaydı vardır; bu kayıtlar çıkarıldığında 120 pencerenin ham medyanı -%9,40'tır. Bu **sonradan yapılmış** yalnız pencere içi hassasiyettir; eksik kurumsal işlem kaydı, önceki ATR etkisi veya gerçek fiyat geçerliliğini çözmez. `daily_action_window_summary.csv` ve olay bayrakları ayrıntıyı gösterir.
- Varsayımsal sabit maliyet, spread, kayma, likidite, vergi, finansman ve açığa satış maliyetini ölçmez. Aynı anda çok sayıda pozisyon, sermaye kısıtı, kaldıraç, bileşik getiri veya maksimum portföy düşüşü modellenmedi. Kârlılık ya da işlem kapasitesi çıkarılamaz.
- 4s ve günlük sonuçlar ayrı yorumlanmalıdır. Çoklu aday/ufuk/maliyet incelemesi, kısa dönem ve seçilen hisseler yanlış keşif ve hayatta kalma yanlılığı doğurur. Harici zaman damgası ve yeni veriye dayalı ileri sonuç bulunmadan karar kuralı geçilmiş sayılamaz.

## Dosyalar ve yeniden üretim

`internal/` ve `external/` içinde `signals.csv`, `outcomes.csv`, `reference_pivots.csv`, `confirmation_status.csv`, özetler, `input_manifest.csv`, `run_metadata.json`, eş-sinyal gecikmesi ve işlem duyarlılıkları bulunur. `AUDIT.json`, 202 iç + 68 harici dosya hash'ini, tüm özet/alt-küme ilişkilerini ve her kaynak için 200 örnek olayda fiyat/endeks aritmetiğini denetledi; bu bağımsız fiyat kaynağı doğrulaması değildir. 19 Kasım'da tüm test paketi **174/174 geçti**, `run.py --check` ağ isteği yapmadan başarılı oldu.

Önce Python 3.11+ ve `requirements-dev.txt` kurun; aynı iç fiyat dosyaları mevcut olmalı ve `input_manifest.csv` hash'leri eşleşmelidir. Harici dosyalar Git'e eklenmez. Orijinal sonuçları ezmeden yeniden çalışma örneği:

```bash
python -m tools.fetch_dip_external --output .cache/external-reference
python -m tools.measure_dip_pilot --source internal --output .cache/reproduce/internal
python -m tools.measure_dip_pilot --source external --external-dir .cache/external-reference/data --output .cache/reproduce/external
python -m tools.summarize_dip_sensitivity --research .cache/reproduce
python -m tools.audit_dip_results --research .cache/reproduce
python -m tools.measure_p6_causal --output .cache/reproduce/p6
python -m tools.audit_p6_causal --output .cache/reproduce/p6
python -m pytest -q
```

İleri kilit, keşif çalışmasının tam yerel sürümlerini ayrıca sabitler; `requirements-forward.txt` ve Python **3.11.2** gerektirir. `data/ohlcv` Git dışındadır; kilitli ısınma dosyaları ve her ileri kesit ayrıca kalıcı/haricen zaman damgalı saklanmalıdır. [FORWARD.md](FORWARD.md) tekil kesit, veri öneki ve girişten önce kayıt denetimlerini açıklar.
