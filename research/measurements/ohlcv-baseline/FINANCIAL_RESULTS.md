# Yapı Olayları — İlk Finansal Sonuç Raporu

## Raporun niteliği

Bu rapor BIST 100 hisselerinin 1 saatlik serilerine odaklanan **keşifsel olay çalışmasıdır**. Getiriler olay kapanışından sonraki sabit bar ufkudur; emir girişi, spread, komisyon, slippage veya portföy çakışması içermez. Bu nedenle backtest kârı veya işlem tavsiyesi değildir.

## BIST hisseleri 1h — olay sonrası sonuç

| Olay | Hipotez | Gözlem | Varlık | 5 bar medyan | 5 bar pozitif | 20 bar medyan | 20 bar pozitif | 20 bar MFE | 20 bar MAE | MFE/|MAE| | ≥20 gözlemli sembol | Pozitif sembol (20) | Sembol medyanı (20) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `close_break` | down | 23,636 | 100 | 0.17% | 53.36% | 0.27% | 52.58% | 2.46% | -2.10% | 1.17 | 100 | 69.00% | 0.23% |
| `retest_hold` | down | 12,668 | 100 | 0.17% | 53.28% | 0.25% | 52.49% | 2.30% | -2.06% | 1.12 | 100 | 62.00% | 0.26% |
| `acceptance` | down | 19,123 | 100 | 0.14% | 52.76% | 0.21% | 52.14% | 2.44% | -2.14% | 1.14 | 100 | 58.00% | 0.15% |
| `follow_through` | down | 19,071 | 100 | 0.15% | 52.79% | 0.21% | 52.10% | 2.44% | -2.15% | 1.14 | 100 | 59.00% | 0.15% |
| `probe_rejection` | down | 25,066 | 100 | 0.09% | 51.13% | 0.10% | 50.90% | 2.08% | -2.27% | 0.92 | 100 | 60.00% | 0.11% |
| `failure` | down | 13,420 | 100 | 0.09% | 51.72% | 0.07% | 50.33% | 2.05% | -2.20% | 0.93 | 100 | 52.00% | 0.07% |
| `retest_hold` | up | 12,176 | 100 | -0.06% | 46.27% | 0.00% | 49.33% | 2.30% | -2.07% | 1.11 | 100 | 50.00% | -0.01% |
| `acceptance` | up | 17,667 | 100 | 0.00% | 47.29% | 0.00% | 49.97% | 2.44% | -2.13% | 1.15 | 100 | 48.00% | 0.00% |
| `follow_through` | up | 17,629 | 100 | 0.00% | 47.29% | 0.00% | 49.99% | 2.44% | -2.13% | 1.15 | 100 | 48.00% | 0.00% |
| `close_break` | up | 23,026 | 100 | -0.10% | 45.27% | -0.05% | 48.66% | 2.39% | -2.17% | 1.10 | 100 | 46.00% | -0.03% |
| `failure` | up | 13,233 | 100 | -0.09% | 45.25% | -0.09% | 48.32% | 2.17% | -2.10% | 1.03 | 100 | 43.00% | -0.05% |
| `probe_rejection` | up | 23,773 | 100 | -0.20% | 41.61% | -0.28% | 45.99% | 2.00% | -2.27% | 0.88 | 100 | 32.00% | -0.27% |

## Okuma

- Aşağı kırılım devamı (`close_break`, `follow_through`, `acceptance`, `retest_hold`, hipotez `down`) mevcut ham örneklemde yukarı kırılım devamından daha güçlü görünmektedir.
- Yukarı kırılım devamının 5 ve 20 bar medyanı çoğu varyantta sıfır çevresindedir; bu haliyle tek başına güçlü avantaj göstermez.
- Failure ve probe rejection satırlarında hipotez yönü ilk denemenin tersidir. Böylece sonuç, başarısız kırılım yönünde değil geri dönüş yönünde okunur.
- MFE ve MAE birbirine yakın olduğunda çıplak olayın hedef/stop ayrıştırması zayıftır. Bağlam, hareket kalitesi ve rejim filtresi gereklidir.
- Sembol tutarlılığı, en az 20 gözlemi olan her sembolün medyan sonucunun pozitif olup olmadığıyla hesaplanmıştır; olay sayısı çok olan sembollerin sonucu tek başına ezmesine izin vermez.

## Finansal olarak henüz hesaplanmayanlar

- Komisyon, spread ve slippage
- Aynı anda açılan korelasyonlu pozisyonlar
- Sermaye ve pozisyon büyüklüğü
- Stop/target sırası ve bar içi belirsizlik
- Portföy drawdown'u
- Kurumsal işlem ayıklamasından sonra yeniden ölçüm
- Eğitim/doğrulama/out-of-sample ayrımı

## Risk ve veri uyarıları

1. Ham fiyatlarda bölünme ve diğer kurumsal işlemler aşağı yönlü olayları yapay biçimde güçlendirebilir.
2. Aynı sembolde yakın zamanlı olaylar bağımsız değildir; gözlem sayısı istatistiksel bağımsız örnek sayısı değildir.
3. Olaylar aynı anda birden fazla geçmiş swing seviyesinde üretilebilir.
4. İlk parametreler seçilmiştir ama optimize edilmemiştir: 0,10 ATR tolerans, iki kapanış kabul, üç bar takip, on bar failure, yüz bar seviye ömrü.
5. Sonuç seçimi bu veriye bakılarak değiştirilirse çoklu deneme yanlılığı doğar. Bundan sonraki parametreler eğitim döneminde seçilip ayrı doğrulama döneminde sınanmalıdır.

## Sonraki zorunlu ölçüm

Olay anındaki trend/range, volatilite, yol verimliliği, örtüşme, gövde gücü ve baskı kaybı dondurulacak; sonuçlar bu bağlamlara ayrılacaktır. Ardından kurumsal işlem filtresi ve zaman bazlı out-of-sample doğrulama uygulanacaktır.
