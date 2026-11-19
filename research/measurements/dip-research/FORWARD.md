# İleri gözlem protokolü

`PLAN.md` geçmiş veriler görüldükten sonra hazırlanmış keşif planıdır. İleri gözlem ancak kurallar ve ısınma verisi sabitlendikten **sonra** kullanılabilir olan barlarla başlar; tarihsel harici arşiv bu amaçla kullanılamaz.

## Kilit ve korumalar

- `python -m tools.forward_dip_research freeze` 20 Kasım 2026 İstanbul günü başlamadan önce mevcut plan, sinyal/ölçüm kodları, Python/pandas/numpy sürümleri, hisse/endeks girişleri ve fiyat-politikası manifestlerinin SHA-256 değerlerini kaydeder. Dosyaya ikinci kez yazılmaz. Kilit dosyası yerel saat ve hash kaydıdır; üçüncü tarafça zaman damgalanmış ön kayıt **değildir**. Bağımsız kanıt için veri gelmeden önce kilidi değiştirilemez, haricen zaman damgalı bir yerde yayımlamak gerekir.
- Başlangıç 20 Kasım 2026 saat 00:00 İstanbul bar etiketidir. Gözlem kesiti için 4s bar etiketine dört saat, günlük bar etiketine bir takvim günü eklenir; ancak bu muhafazakâr kural gerçek seans/kapanış saatini veya emir gerçekleşmesini doğrulamaz. Kesit saatinden sonra kapanmış gibi görünen satırlar kullanılmaz. 4s `complete=false` çıkarılır.
- Yeni Yahoo verisi ayrı bir ağaçtan alınır; varlık, periyot, seri kimliği ve `series.json` hash'i eski fiyat politikasıyla eşleşmelidir. Isınma dosyalarının hash'i değişirse çalışma durur. Yeni dosyanın eski tarihlerdeki olası düzeltmeleri yok sayılır; yalnız sabit ısınma sonrasına yeni satırlar eklenir. İşlem gören günlerdeki eksikler, kurumsal işlemler ve kaynak doğruluğu yine ayrıca incelenmelidir.
- Her kesit benzersiz yeni bir klasöre yazılır; üzerine yazılamaz. Önceki kesit `--previous` ile bağlandığında önceki çıktı hash'leri ve her veri serisinin eski öneki denetlenir. Kesit, ilk gözlenme saatini gerçek kayıt saatinden alır; geçmişe ait `--as-of` argümanıyla kayıt zamanı geri alınamaz. Gerçek ilk kayıt giriş barının etiketinden sonraysa o sonuç `registered_before_entry_label=false` işaretlenir; geçmişten doldurulmuş sinyal zamanında izlenmiş sayılmaz. Etiket zamanından önce kaydedilmiş olmak da bir emrin gerçekleştiğinin kanıtı değildir.
- Kesit arşivleri/hash zinciri yerelde değiştirilebilir; bağımsız delil için her dosya ve manifesti harici, zaman damgalı, değiştirilemez bir yere koyun. `review_required` yalnız örnek sayısı eşiklerinin incelenebileceği anlamındadır; başarı kararı değildir. `blocked_data` sonuç yok demektir, sıfır başarı demek değildir.

## Kullanım

Depo kökünden, veriler güncellenmeden önce (mevcut kilit varsa yeniden üretmeyin):

```bash
python -m tools.forward_dip_research freeze \
  --root data/ohlcv \
  --output research/measurements/dip-research/forward-freeze.json
```

Sabit ısınma ağacını ayrıca güvenli ve kalıcı biçimde saklayın; `data/ohlcv/` Git'e dahil değildir. Yeni veriyi **ayrı** `.cache/forward-ohlcv/` gibi bir dizine aynı `bist_equities/BIST_<sembol>/<series_id>/bars/{1d,4h}.csv` ve `series.json` düzeniyle koyun. Sonra:

```bash
python -m tools.forward_dip_research observe \
  --freeze research/measurements/dip-research/forward-freeze.json \
  --warmup-root data/ohlcv --new-root .cache/forward-ohlcv \
  --output .cache/forward-observations/2026-11-20-a

# Sonraki kayıt; eski çıktı klasörünü koruyun.
python -m tools.forward_dip_research observe \
  --freeze research/measurements/dip-research/forward-freeze.json \
  --warmup-root data/ohlcv --new-root .cache/forward-ohlcv \
  --previous .cache/forward-observations/2026-11-20-a \
  --output .cache/forward-observations/2026-11-21-a
```

İstenirse `--as-of 2026-11-20T21:00:00Z` kullanılır; gelecekteki bir kesite izin verilmez, dosyada daha sonraki barlar varsa bunlar kullanılmaz. Varsayılan kesit gerçek çalışma zamanıdır. Tam sonuçlar için ileri fiyatların uygun ufku kapsaması gerekir; yoksa sansürlüdür. `.cache/` Git/snapshot dışındadır: kalıcı delili ayrıca saklayın.

İleri karar yalnız önceden kaydedilmiş sinyaller ve tamamlanmış ufuklar için, en az 100 sonuç, 20 hisse, 20 hafta, maliyet/gecikme duyarlılığı, dip kapsaması ve bölgesiz A kontrolü bir arada incelenerek verilebilir. Yine de tedarikçi bağımsızlığı, tarihsel evren yanlılığı ve gerçek işlem gerçekleşmesi ayrıca doğrulanmadan kanıt veya yatırım önerisi sayılmaz.
