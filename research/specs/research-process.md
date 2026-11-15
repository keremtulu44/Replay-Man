# Replay-Man Araştırma Süreci

## 1. Fikir kaydı

Her fikir değişmez bir kimlik ve sürüm alır. Doğal dilde iddia, kaynak referansı ve hangi davranışı açıklamaya çalıştığı yazılır.

## 2. Objektif tanım

- Girdiler
- Yalnız geçmişe dayalı hesap
- Parametreler
- Sinyalin oluştuğu an
- Beklenen hareket
- Ölçüm ufku
- Başarı, başarısızlık ve geçersizlik

belirlenmeden deney çalıştırılmaz.

## 3. Tekil yapı taşı testi

Yeni özellik önce tek başına test edilir. İleri 1/2/4/8/16 bar getirisi, maksimum olumlu hareket, maksimum ters hareket, gerçekleşme süresi ve XU100'e göre göreceli sonuç ölçülür.

## 4. Geniş sembol doğrulaması

BIST fikri mümkün olduğunda 70–100 hissede aynı parametrelerle çalıştırılır. Sembol bazında örnek sayısı, medyan sonuç ve olumlu sembol oranı raporlanır. Birkaç sembolün toplam sonucu taşıması ayrıca gösterilir.

## 5. Rejim ve grup ayrımı

Sonuçlar yükseliş/düşüş/yatay ve yüksek/düşük volatilite koşullarında; ayrıca varlık ve sektör gruplarında ayrıştırılır. Rejim bağımlılığı başarısızlık değil, kullanım koşulu olarak etiketlenebilir.

## 6. Marjinal katkı testi

Bir kombinasyona yeni koşul eklenince temel sistem ile yeni sistem yan yana ölçülür. Yeni koşul beklenen hareketi, ters hareketi veya sembol yaygınlığını iyileştirmiyorsa gereksiz kabul edilir.

## 7. Parametre duyarlılığı

Tek bir mükemmel parametre yerine komşu parametrelerin de benzer sonuç üretip üretmediği kontrol edilir. Keskin tek optimum uyarı oluşturur.

## 8. Replay incelemesi

En iyi, medyan, sınırda ve başarısız örnekler geleceği göstermeyen replay ile incelenir. Görsel inceleme toplu testi geçersiz kılmaz; yalnız tanım hatalarını ve açıklanamayan davranışları bulmak için kullanılır.

## 9. Sürümleme

Kural değişirse eski deney üzerine yazılmaz. Yeni sürüm oluşturulur. Her rapor veri indeksi SHA-256 özeti, kod sürümü ve deney sürümünü taşır.

## 10. Adaylık kararı

Bir fikir ancak yeterli örnek, geniş sembol yaygınlığı, açıklanabilir amaç ve kabul edilebilir veri kalitesi sağladığında strateji/indikatör adayı olur. Aday olmak canlı performans garantisi değildir.

## Ertelenen entegrasyon

Kullanıcının mevcut OB/FVG sistemi acil değildir. Teslim edildiğinde:

1. Tanımları değiştirmeden envanter çıkarılır.
2. Gelecek veri kullanımı denetlenir.
3. Ortak olay şemasına adaptör yazılır.
4. Tekil ve birleşik testleri aynı araştırma sürecinde çalıştırılır.
