# Cilt 2 P5 — Sıkışma, Genişleme ve İlk Taşma

## Kapsam

245.802 olay; 6, 10 ve 15 barlık sıkışma pencereleri. Sıkışma, pencere genişliği ≤3 ATR ve ortalama örtüşme ≥0,35 olarak tanımlandı. Kapanış kırılımı, fitille taşma/rejection ve ilk beş barda karşı sınırın kapanışla aşılması ölçüldü.

## Sonuç

4h/60 testte bazı kırılım grupları güçlü görünür: 6-bar normal yukarı kırılım `%5,80` (95 olay, `%70,53` pozitif), 10-bar normal yukarı `%6,59` (44 olay), 6-bar contracted aşağı `%2,73` (99 olay), 10-bar contracted aşağı `%6,80` (40 olay). Ancak bu grupların eğitim veya doğrulama işaretleri ters olduğundan zaman-kararlı değildir.

Karşı tarafa genişleme varyantlarından üç alt grup üç zaman bölümünde pozitif işaret taşıdı; testte geçerli olay sayıları yalnız 1–8 düzeyindedir. Bunlar `insufficient_sample` olarak tutulur.

Fitille taşma/rejection gruplarının büyük kısmı `%48–52` pozitif oran ve sıfıra yakın benchmark-aşırı medyan verdi; tek başına avantaj değildir.

## Karar

- Sıkışma sonrası çıplak kırılım: `rejime_bagli`.
- Probe rejection: `chance_like/context_only`.
- Karşı tarafa genişleme: mekanik tanım çalışıyor fakat `insufficient_sample`.
- Büyük genişleme barı otomatik üstün değil; break-size bantları dönemler arasında işaret değiştiriyor.

## Dosyalar

- `inventory.csv`: bütün seri/pencere/olay sayıları
- `event_study.csv`: zaman, yön ve kırılım büyüklüğü bantları
- `summary.json`: kapsam
