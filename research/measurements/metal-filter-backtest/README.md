# Altın ve gümüş uyarısı: sanal işlem karşılaştırması

## Kısa sonuç

Seçtiğin üç uzun işlem fikri, **100 mevcut hisse**, 1 saatlik ve 4 saatlik mumlar için altın ve gümüş uyarısıyla sınandı. Bu çalışma **canlı işlem değil, geçmiş veri üzerinde olay bazlı bir simülasyondur**. Aşağıdaki örnekte filtre bazı işlemleri eledi, ancak **zararı güvenilir biçimde azalttığı gösterilemedi**. Diğer ayarlarda sonuç değişebilir; çok sayıda varyant denendiğinden bu sonuçlar keşifseldir.

### Somut örnek: 4 saatlik, test dönemi

Aşağıdaki tek görünüm: USD altın **veya** gümüş 10 mumda %2'den fazla yükselmiş ya da düşmüş, geçmişte ilgili hisse en az 10 tamamlanmış olayın ≥%70'inde düşmüşse uyarı; stop 1 ATR, hedef 2 ATR; en fazla 10 mum; varsayımsal toplam gidiş-dönüş maliyet %0,10. Test dönemi 1 Eylül 2026 ve sonrası; **bu dönem daha önce de incelendi**, el değmemiş bağımsız test değildir.

| Uzun işlem fikri | Sonucu bilinen tüm aday | Makro bilgisi yetersiz | Karşılaştırılabilir aday | Uyarıyla elenen | Filtre yok: ortalama işlem getirisi | Filtreli: ortalama işlem getirisi |
|---|---:|---:|---:|---:|---:|---:|
| 20 mum tepesi kırılımı | 229 | 16 | 213 | 5 | −%1,58 ile −%1,48 | −%1,57 ile −%1,48 |
| Başarısız dip vekili | 583 | 12 | 571 | 45 | −%1,424 | −%1,427 |
| Ortalama kesişimi | 55 | 2 | 53 | 2 | −%1,607 | −%1,921 |

Aralıklar, aynı mumda hedef ve stop görülürse hangisinin önce olduğunun bilinmemesinden kaynaklanır. İlk satırda 5 elenen işlemin 4'ü zarar, 1'i kâr; ikinci satırda 45 işlemin 36'sı zarar, 9'u kârdır. Ancak ikinci satırda kalanların ortalaması çok az daha kötüydü: **zarar eden bazı işlemleri elemek, toplam ortalamanın mutlaka iyileşeceği anlamına gelmez**. Üçüncü satırda sadece 2 aday elendi; bu sayıdan güçlü çıkarım yapılamaz. Yüzdeler eşit ağırlıklı **işlem adayı ortalamasıdır**, portföy getirisi değildir.

Aynı 4 saatlik görünümün eldeki üç dönemin toplamında, başarısız dip vekilinde 1.309 karşılaştırılabilir işlemden 83'ü elendi; ortalama alt sınır filtresiz −%0,691, filtreli −%0,667 idi. Test dönemi yukarıdaki gibi farklı sonuç verdi. Farkların küçüklüğü, birbirine bağlı adaylar ve örnek seçimi nedeniyle bunlar bir avantaj ispatı değildir. Altın ve gümüş ayrı ayrı ve eşikler/diğer maliyetler için sonuçların tamamı tablolardadır.

## Dosyalar

- [ornek-gorunum.csv](ornek-gorunum.csv): doğrudan açılabilir, **%70 eşik ve %0,10 maliyet** için tüm strateji/periyot/hedef/dönem/metal görünümü. Tam sonuçların yalnız bir kesitidir.
- [karsilastirma.csv.gz](karsilastirma.csv.gz): bütün eşikler, dönemler, maliyetler ve alt/üst sonuçlar; 3.456 özet satırı. Gzip açılarak CSV filtrelenebilir.
- [hisse-karsilastirma.csv.gz](hisse-karsilastirma.csv.gz): aynı sonuçların hisse bazında ayrıntıları; az örnekli hisseler de korunur.
- [islem-adaylari.csv.gz](islem-adaylari.csv.gz): her aday için sinyal zamanı, hisse, iki metal hareketi, o anda bilinen düşen/olay sayısı, giriş/çıkış ve brüt alt/üst getiriler. Her sinyal dört hedef/süre varyantında ayrı satırdır.
- [kapsam.csv](kapsam.csv): hisse ve periyot başına sinyal ve geçmişte hesaplanabilen makro sonuç sayısı. [girdi-manifest.csv](girdi-manifest.csv): 204 girdi dosyası ve SHA-256. [summary.json](summary.json): genel sayılar. [PLAN.md](PLAN.md): test öncesi kurallar.

26.174 giriş sinyali ve bunların 104.696 süre/ATR varyantı incelendi. Bu varyant satırları birbirinden bağımsız işlemler değildir. 1.549 varyantta sonuç hesaplanamadı; 294 varyantta aynı mumda stop ve hedef sıralaması belirsizdi. Bunlar sırasıyla `missing` ve `ambiguous` olarak ham dosyada saklandı.

## Test süreci

1. **Aday:** `breakout20` kapanışı önceki 20 mumun tepesini aşar; `failed_low5` önceki beş mumun dibini kırıp aynı seviyenin ve açılışın üzerinde kapanır; `trend_cross` 20 mumluk basit ortalama 50 mumluğu yukarı keser. Bunlar araştırma için açık başlangıç kurallarıdır. Özellikle `failed_low5`, kitapta anlatılan ikinci denemenin tam karşılığı değil, basit bir vekildir.
2. **Giriş:** Sinyal barı kapanınca bilinir; nominal kapanışından **kesinlikle sonra** başlayan ilk XU100 barının aynı zamanlı hisse açılışı kullanılır. Tam kapanış anında başlayan bar atlanır. Eksik ortak bar/sonuç veya dönem sınırı aşımı varsa hesaplanmayan aday gösterilir.
3. **Çıkış:** Sinyaldeki 14 mumluk ATR sabitlenir. İki ayrı ayar: 1 ATR zarar kes / 2 ATR hedef ve 1,5 ATR zarar kes / 3 ATR hedef. Hedef veya stop gerçekleşmezse 10. veya 20. mum sonunda ayrı varyantlarda çıkış. Sonraki açılış bir seviyeyi aşmışsa o açılış kullanılır. Aynı mumda ikisine de dokunulduğunda zarar önce ve kâr önce varsayımları ayrı sonuçtur; sıra bilinmez.
4. **Makro geçmiş:** Her kaynak için son 10 ortak BIST mumunda USD altın veya gümüş kesinlikle **+%2'den büyük** ya da **−%2'den küçük** değişirse ilgili yön ayrı değerlendirilir. Kaynak şok pencereleri hedeften bağımsız seçilir ve dönem içinde çakışmaz. Tarihsel düşüş oranı, geçmişte bu şoklardan sonra başlayan **10 mumluk hisse getirisinin negatif olduğu** olay sayısı / sonucu bilinen olay sayısıdır. Sadece sinyal anında sonucu kapanmış olaylar kullanılır. Bu oran, ATR hedefli veya 20 mumluk işlemin kâr oranı değildir.
5. **Uyarı:** En az 10 tamamlanmış olay ve ilgili geçmiş düşüş oranı ≥%60, ≥%70 veya ≥%80; eşikler ayrı raporlanır. `gold` ve `silver` ayrı, `either` ise herhangi birinin uyarısıdır. Örnek yetersizse ya da gerekli kaynak yoksa `unknown`; eşik koşulu yoksa `no_signal`. `either` için tek bir kesin uyarı yeterlidir; aksi halde metallerden biri bilinmiyorsa birleşik durum bilinmez.
6. **Eşleştirme:** Aynı bilinen aday kümesindeki **filtresiz** (`paired`) ve **uyarıda işlem açmayan** (`kept`) sonuçlar karşılaştırılır; `blocked` elenenlerdir. Bilinmeyenler eşleştirilmiş karşılaştırmadan çıkarılır ve `unknown` olarak ayrıca sayılır. Bu, bilinmeyenleri güvenli veya zararlı saymak değildir. `all` tüm adayları gösterir.
7. **Maliyet:** Gidiş-dönüş toplam %0 / %0,10 / %0,25 / %0,50 varsayımsal getiri puanı, her işlem sonucundan çıkarılır. Gerçek komisyon, spread ve kayma ölçülmüş değildir.

## Tablodaki alanlar

- `all_candidates` bütün aday varyantları, `all_n` sonucu hesaplanabilenleri; `unknown_candidates` ve `unknown_n` makro durumu bilinmeyen toplam ve sonucu bilinenleri gösterir.
- `paired_n = kept_n + blocked_n`: sonucu ve makro durumu bilinen aynı aday havuzu. `*_lower_mean` ve `*_upper_mean` maliyet sonrası işlem başına ortalamalardır; ondalık biçimde `-0.01` = −%1. Aynı mum belirsiz değilse alt/üst eşittir.
- `*_lower_wins`, `*_lower_losses`, `*_lower_win_rate` ve üst sınır eşleri maliyet sonrası işaretleri; `*_ambiguous` belirsiz sıralama sayısını verir. `*_sum` eşit ağırlıklı işlem getirilerinin toplamıdır, **portföy getirisi değildir**. `difference_lower/upper` filtreli ortalama − aynı adayların filtresiz ortalamasıdır; nedensel etki değildir.
- Ham satırda `gold_return`, `silver_return` metal değişimleri; `*_condition` up/down/no_signal/unknown; `*_n` ve `*_down` sadece koşul etkinse o anda bilinen geçmiş sayılarıdır. `gross_lower` ve `gross_upper` maliyet öncesidir.

Sorgu örnekleri:

```bash
# Rapor örneği
.venv/bin/python -m tools.query_metal_filter --interval 4h --strategy failed_low5 --mode either --split test
# 1h kırılımda yalnız altın, %60 uyarı ve 20 mum
.venv/bin/python -m tools.query_metal_filter --interval 1h --strategy breakout20 --mode gold --threshold 0.6 --horizon 20
# Tek hisse (büyük tabloyu okur)
.venv/bin/python -m tools.query_metal_filter --table research/measurements/metal-filter-backtest/hisse-karsilastirma.csv.gz --target TUPRS
```

Yeniden üretim: `.venv/bin/python -m tools.measure_metal_filter`. `--root` ve `--output` değiştirilebilir. Orijinal veri dosyaları manifestteki hash'lerle eşleşmiyorsa sonuçlar değişebilir.

## Sınırlamalar

Aynı hissede ve farklı hisselerde adaylar/pozisyonlar üst üste gelebilir. Sermaye sınırı, portföy dağılımı, gerçek emir sırası, piyasa derinliği ve portföy maksimum düşüşü hesaplanmadı. Açılış ve stop/limit seviyelerinde gerçekleşme yalnızca model varsayımıdır; aynı mumdaki gerçek sıra bilinmez. Bölünme/temettü, ham fiyatlar, sağlayıcı seans saatleri ve eksik tamamlanmış mumlar sonuçları etkileyebilir; küçük veri oynamaları çalışma önkoşulu yapılmadı.

Bir yıllık veri ve az sayıdaki özellikle uyarılı işlem sonucu sınırlıdır. Kapsamdaki 100 hisse tarihsel üyelik açısından ayrı doğrulanmadı; hayatta kalma/evren seçimi yanlılığı olabilir. Bu veriler daha önce incelendi; eğitim/doğrulama/test etiketleri temiz ileri test kanıtı değildir. Çok sayıda strateji, eşik ve varyant karşılaştırılması tesadüfi iyi sonuçlar üretebilir; yalnız en iyi satır seçilmemelidir. Gerçek kullanımdan önce daha fazla tarih ve ileriye dönük gözlem gerekir. **Yatırım tavsiyesi değildir.**
