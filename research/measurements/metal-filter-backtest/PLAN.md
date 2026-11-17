# Test öncesi sözleşme — metal uyarısı ve sanal işlemler

Kullanıcı seçimi: 100 hisse, 1h ve 4h ayrı; üç farklı uzun giriş fikri; USD altın ve gümüşün 10 ortak BIST mumunda kesinlikle %2'yi aşan pozitif/negatif hareketi; 10/20 mum azami elde tutma; ATR(14) ile 1/2 ve 1,5/3 zarar/kâr uzaklıkları; %60/%70/%80 geçmiş düşüş oranı ve en az 10 tamamlanmış olay; metal ayrı ayrı ve herhangi biri; işlem maliyeti duyarlılığı; aynı mumda hem hedef hem stop için iki olasılık. Eşikler keyfi, araştırma amaçlıdır.

## Başlangıç kuralları (keşifsel vekiller, yatırım tavsiyesi değil)

- `breakout20`: kapanış kendisinden önceki 20 mumun en yüksek değerini aşar.
- `failed_low5`: mumun en düşüğü önceki beş mumun en düşüğünün altına iner, kapanış aynı seviyenin ve açılışın üstündedir. Bu ikinci deneme/pullback fikri için basit fiyat vekilidir, tam kitap yorumu değildir.
- `trend_cross`: 20 mumluk basit kapanış ortalaması 50 mumluk ortalamayı yukarı keser.

Sadece ortak XU100/hisse barları; göstergede gerekli geçmiş tam olmalı. Sinyal tamamlanmış mum sonunda bilinir. Nominal kapanışından **kesinlikle sonra** başlayan ilk ortak bar açılışı giriş vekili. Ayrı adaylar çakışabilir; eşit ağırlıklı olay çalışmasıdır, portföy/sermaye veya işlem kârı iddiası değildir. Sinyal ve gerçekleşen çıkış aynı UTC split içinde olmalı: 1 Temmuz / 1 Eylül 2026. Bu bölümler önceden görüldüğü için bağımsız OOS değildir.

ATR 14 kapanış itibarıyla son 14 gerçek aralık basit ortalamasıdır. Giriş fiyatından −1 veya −1,5 ATR stop ve +2 veya +3 ATR hedef belirlenir. Pozisyon sonraki açılış stop/hedefini geçtiyse açılıştan, aksi halde seviyeden çıkılmış varsayılır; aynı mumda iki seviye dokunursa zarar önce ve hedef önce senaryoları ayrı raporlanır. Aksi halde 10/20. bar kapanışı, geçersiz veya eksik bar ve bölümler arası sonuç hesaplanmaz. İşlem maliyeti toplam gidiş-dönüş %0 / %0,10 / %0,25 / %0,50 getiri puanı olarak iki sınırdan çıkarılır; gerçek kotasyon değildir. Eksik sonuç gizlenmez.

## Makro bilgi sözleşmesi

XU100 10-bar penceresi boyunca metal USD değişimi aynı as-of/90 dakika kuralı. Kaynak olayı hedefe bakmadan dönem içinde çakışmasız seçilir; `<−%2` ve `>+%2` için ayrı. Seçilen olayların hisseye ait **post_open 10 mum <0** sonucu ve bitiş anı kullanılır. Her adayda sadece o ana kadar kapanmış hedef sonuçları sayılır; `same` ve bugünkü toplam tablo kullanılmaz. Her metal/yön için olay sayısı ve düşen sayısı kayıtlıdır. Bu oran stratejinin kâr/zarar oranı değil, önceki 10 mumluk yön riski vekilidir; 20 mum veya ATR sonucu için kalibre edilmemiştir. İlk olaylar veya yetersiz veri kayıp/sıfır risk olarak sayılmaz.

Her metal için hareket koşulu yoksa `no_signal`, koşul varsa n<10 `unknown`, aksi halde her eşikte `warning` veya `clear`. Kaynak eksikse `unknown`. İki metalin herhangi biri için: en az bir warning → warning; ikisi de biliniyor ve warning yok → clear; aksi → unknown. Eşleştirilmiş karşılaştırmada unknown dışlanır ve ayrıca sayılır; warning varsa filtre işlemi pas geçer; aynı bilinen adaylardaki filtresiz baz ile karşılaştırılır. Kapsam yalnız aday-tabanlıdır; farklı filtrelerin farklı sonuçlarının sermaye/pozisyon etkileşimi modellenmez.

Çıktılar kaynak/strateji bazında özet, işlem seviyesinde açıklanabilir sonuç, kaynak sayısı ve girdi hash manifesti. Belirsiz sonuçların alt ve üst sınırları, eksik aday sayıları, uyarılı işlemler, maliyet ve hisse grupları korunur. Veri dönemleri gözlenmiş, yaklaşık bir yıl; çoklu sınama, üst üste gelen adaylar ve hisseler arası korelasyon nedeniyle yüksek sonuçlar keşifseldir. Ham OHLC, seans/nominal bar, vadeli roll, kurumsal işlem, maliyet ve emir gerçekleşmesi belirsizlikleri kaydedilir; küçük veri oynamaları çalışmayı durduran önşart yapılmaz.
