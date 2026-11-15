# Kavram → Yazılım Haritası

Bu belge kaynak kitaplardaki fikirleri doğrudan işlem kuralı kabul etmez. Kavramların hangi ölçülebilir modüle dönüştürülebileceğini ve nasıl doğrulanacağını kaydeder.

| Kavram | Kaynak rolü | Planlanan matematik/özellik | Motor |
|---|---|---|---|
| Mum gücü | Cilt 2, Bölüm 1–2 | Gövde/aralık, fitil/aralık, kapanış konumu, yakın dönem yüzdeliği | Feature engine |
| Temiz ilerleme | Cilt 2, Bölüm 2/5 | Net mesafe / toplam yol, yönlü kapanış oranı | Movement quality |
| Örtüşme | Cilt 2, Bölüm 2/5/6 | Ardışık bar kesişimi / küçük bar aralığı | Compression/quality |
| Momentum kaybı | Cilt 2, Bölüm 3–4 | Mesafe küçülmesi, süre uzaması, yeni uç azalması | Pressure decay |
| Swing geometrisi | Cilt 2, Bölüm 8 | Onaylı pivot, bacak mesafesi, süre, ATR-normalize hız | Swing engine |
| İkinci deneme | Cilt 2, Bölüm 9 | İlk/ikinci bacak oranı, yeni uç, geri alınma süresi | Attempt lifecycle |
| Kırılım kabulü | Cilt 2, Bölüm 7 | Sınır dışı kapanış, takip, yeniden giriş derinliği | Breakout lifecycle |
| Pullback kalitesi | Cilt 2, Bölüm 10 | Derinlik, süre, verimlilik, örtüşme, yapısal koruma | Pullback engine |
| Bilgi ailesi | Cilt 1, Bölüm 1/21 | Yön, momentum, volatilite, konum, katılım, yapı etiketi | Feature registry |
| Rol çakışması | Cilt 1, Bölüm 21 | Aynı aile/karar rolü, çıkarma testi, marjinal katkı | Combination validator |
| Strateji kartı | Ana Kitap, 12.14 | Bağlam, setup, tetik, geçersizlik, amaç, ufuk | Experiment registry |
| Replay doğrulama | Ana Kitap, 12.15 | Gelecek sızıntısız bar akışı ve örnek inceleme | Replay engine |
| Objektif kural | Ana Kitap, 16.6 | Doğal fikirden ölçülebilir şart/amaç dönüşümü | Hypothesis schema |
| İddia denetimi | Ana Kitap, 16.10 | Örnek, sembol yaygınlığı, rejim, duyarlılık uyarıları | Report/audit |

## İlk özellik ailesi

1. Candle Geometry
2. Movement Quality
3. Pressure Decay
4. Swing Geometry
5. Breakout Acceptance
6. Failed Attempt
7. Pullback Quality
8. Follow-Through
9. Relative Strength
10. Cross-Market Event/Lead-Lag

## Değişmez tasarım ilkeleri

- Gelecekte oluşan bar, mevcut bardaki özelliği hesaplamak için kullanılamaz.
- Swing gibi sonradan teyit edilen olaylarda `observed_at` ile `confirmed_at` ayrı tutulur.
- Sabit TL/yüzde yerine mümkün olduğunda ATR, yüzdelik veya varlığın kendi dağılımı kullanılır.
- Aynı tanım aynı varlık grubunda sembole özel ayar değiştirmeden uygulanır.
- Sonuçlar ortalama kadar medyan, sembol yaygınlığı ve örnek sayısıyla raporlanır.
- Native 1d ana günlük kaynaktır; `1d_from_1h` yalnız kalite kontrolüdür.
- Hacim kendi periyodu içinde göreceli ölçülür; native günlük hacimle saatlik toplamın eşitliği varsayılmaz.
- OB/FVG, mevcut kullanıcı sistematiği gelmeden yeniden tanımlanmaz.
