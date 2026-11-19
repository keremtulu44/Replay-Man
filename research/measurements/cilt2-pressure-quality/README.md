# Cilt 2 P4 — Baskı Kaybı ve Hareket Kalitesi

> **Tarihsel arşiv uyarısı (19.11.2026):** Olay-sıralı bölümler sonuç ufkunu bölüm içinde zorunlu tutmaz ve XU100 bağımsız satır kaydırmasıyla eşlenir; özellikle günlük bitiş etiketleri farklı olabilir. Sonuçlar kapanış başlangıçlı/maliyetsiz keşiftir, bağımsız ileri test veya gerçek işlem değildir. [Genel denetim](../general-review/README.md).

## Kapsam

1.350.145 örtüşebilen olay; 125 varlık ve dört periyot. Gövde küçülmesi, ilerleme küçülmesi, örtüşme artışı, ikili/üçlü birleşimler ve güçlü karşı mum teyidi; 0,60 ve 0,80 oran eşikleriyle ölçüldü.

## Ana soru

Mevcut yön zayıfladığında ters yön avantajı oluşuyor mu? Hipotez önceki 5 bar yönünün tersidir. Sonuçlar, zayıflamanın otomatik dönüş olmadığını açıkça gösterdi.

## 4h/60 bar BIST testi

Testte bütün çıplak ters-yön varyantlarının XU100-aşırı medyanı negatiftir. Önceki yükseliş sonrası gövde küçülmesi `-%3,48`, ilerleme küçülmesi `-%3,11`, ikili küçülme `-%3,38`, üçlü küçülme `-%5,43`; güçlü karşı mum teyidi bile `-%4,76`. Pozitif oranlar çoğunlukla `%34–41`.

Önceki düşüş sonrası yukarı dönüş hipotezi de testte negatiftir: 0,80 ilerleme küçülmesi `-%0,84`, gövde küçülmesi `-%1,33`, üçlü küçülme `-%2,33`; güçlü karşı mum `-%5,98`.

Eğitim/doğrulama işaretleri bazı yönlerde değiştiği için olaylar ayrıca rejime bağlıdır. Ancak testte “zayıflama=dönüş” iddiasının bütün varyantları başarısızdır.

## Mantıksal karar

- Gövde veya ilerleme küçülmesi: `context_only`, doğrudan dönüş sinyali değil.
- Örtüşme artışı: `context_only`.
- Gövde+ilerleme+örtüşme: ters yön sinyali olarak `negative`.
- Güçlü karşı mum eklense bile örnek küçülüyor ve avantaj oluşmuyor.
- Baskı kaybı, acceptance gibi başka bir olayın bağlamında ayrıştırma üretebilir; bağımsız giriş olarak kullanılmayacak.

Bu sonuç kitabın “zayıflama tek mumda oluşmaz ve dönüş anlamına gelmez” uyarısını destekler.

## Dosyalar

- `inventory.csv`: Bütün seri/varyant olay sayıları
- `event_overall_study.csv`: Olay/yön/zaman sonuçları
- `event_study.csv`: Hareket kalitesi bantları eklenmiş sonuçlar
- `summary.json`: Kapsam
