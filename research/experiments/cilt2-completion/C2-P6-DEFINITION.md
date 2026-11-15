# C2-P6 — Kırılım Yaşam Döngüsü Ayrıntı Sözleşmesi

Bu paket mevcut probe→close-break→follow-through→acceptance→retest→failure motorunu genişletir. Ölçüm başlamadan önce aşağıdaki alanlar sabitlenmiştir.

## Olay anında dondurulacak alanlar

- Seviye kaynağı, pivot zamanı ve teyit zamanı
- Seviye yaşı ve önceki deneme sayısı
- Kırılım kapanış mesafesi/ATR
- Kırılım gövde/aralık oranı
- Yönsel kapanış konumu
- Kırılım range/ATR
- Kırılım öncesi 6/10/15 bar sıkışma durumu
- Dışarıda kalan kapanış sayısı ve bar süresi
- En fazla dışarı taşma/ATR

## Retest alanları

- Kırılımdan reteste bar sayısı
- Seviyeye yaklaşma hızı
- Kırılım hareketinin geri alınma oranı
- Retest mum gövdesi, fitili ve kapanış konumu
- Retestte seviye toleransı: 0,05 / 0,10 / 0,20 ATR
- Retest sonrası 1/2/3 bar takip

## Failure alanları

- Eski alana kapanış derinliği/ATR
- Dışarıda kalınan süre
- Failure öncesi takip oluşup oluşmadığı
- Failure sonrası karşı sınır/yapı kırılımı
- Karşı tarafa genişleme süresi ve mesafesi

## Önceden kayıtlı varyantlar

- Acceptance: 1 / 2 / 3 dış kapanış
- Follow-through penceresi: 1 / 3 / 5 bar
- Failure penceresi: 5 / 10 / 20 bar
- Seviye ömrü: 50 / 100 / 150 bar
- Tolerans: 0,05 / 0,10 / 0,20 ATR

## Kontroller

- Pivot teyidinden önce olay yok.
- Aynı seviye ve bar için yinelenen olay kimliği yok.
- Acceptance/follow-through olay örtüşmesi ayrıca raporlanır.
- Parametre varyantları bağımsız avantaj sayılmaz.
- Ham, XU100-aşırı, MFE/MAE, sembol ve zaman ayrımı korunur.
- Failure sonrası karşı genişleme az örnekliyse sonuç `insufficient_sample` kalır.

## Kaynak

Cilt 2 sayfa 45–53, 57, 70, 73, 76, 91 ve 96. Sonuçlar BR-002–BR-007 ile karşılaştırılacak; mevcut sonuçların üzerine sessizce yazılmayacaktır.
