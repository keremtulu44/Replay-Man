# Yapılandırılmış Trading Bilgi Tabanı

Bu dizin PDF arşivinden farklıdır. Amaç, kaynak bilgisini kaybetmeden kitapları bölüm/alt başlık/kavram katmanlarında işlemek; kaynağın söylediği ile proje yorumunu ve kullanım fikrini açıkça ayırmaktır.

## Katmanlar

1. `source-pages/`: PDF'lerin SHA-256 ile doğrulanmış, sayfa bazlı tam metin arşivi. Bilgi kaybını ve bağlamdan kopmayı önleyen kanonik arama katmanıdır.
2. `reading-ledger.json`: Her kitabın/kısmın işlenme durumu ve kapsam seviyesi.
3. `themes/`: Benzer konuları, kaynakları silmeden bir araya getiren başlangıç temaları.
4. `processed/*-cards.jsonl`: 778 sayfanın tamamı için bölüm, alt başlık, uzun kaynak şeridi, konu, ayrı yorum ve kullanım kayıtları.
5. `processed/chapters/`: 24 + 21 + 13 olmak üzere 58 bölümün ayrı dosyaları; sayfa aralığı, alt başlık, konu dağılımı ve sayfa şeritleri.
6. `processed/themes/`: 22 konu ailesinin kaynakları birleştirmeden yan yana getiren uzun dosyaları.
7. `processed/topic-index.json`: Konudan kaynak sayfa/kartına çift yönlü erişim indeksi.
8. `processed/master-synthesis.md`: Bütün temaların ana kataloğu.
9. `QUALITY_REVIEW.md`: Bulunan/düzeltilen sorunlar, bilinçli sınırlamalar ve “%100 kapsam” tanımı.
10. `experiments/` (sonraki aşama): Araştırmaya değer bulunan bilgiler için test fikirleri; ilk okumada kesin formül/eşik dayatılmaz.

## Her tematik kaydın sırası

- **Kaynak:** Kitabın fikrini yeterli bağlamla taşıyan, kısa slogan yerine birkaç cümlelik temiz alıntı.
- **Kaynak özeti:** Alıntının kendi içinde ne söylediği ve ne söylemediği.
- **Yorum (`inference`):** Replay-Man açısından yapılan ayrı çıkarım.
- **Nasıl kullanılabilir (`hypothesis/use`):** Özellik, olay, bağlam, replay veya araştırma fikri.
- **Varyantlar/çelişkiler:** Bir görüş silinmez; ayrı varyant olarak korunur ve ileride ölçülür.
- **Referans:** Kaynak kimliği ve PDF sayfası.

## Bilgi türleri

- `source`: Kaynakta açıkça bulunan bilgi.
- `inference`: Kaynaktan türetilen proje yorumu.
- `hypothesis`: Veri/replay ile sınanması gereken fikir.

## Birleştirme kuralı

Benzer başlıklar tek temada toplanabilir; fakat kaynak kayıtları ve sayfa referansları ayrı kalır. Birleştirme, farklı nüansları tek cümleye indirgeme veya çelişkili görüşlerden birini silme anlamına gelmez.
