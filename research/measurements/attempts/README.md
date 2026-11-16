# İlk/İkinci Deneme ve Yeni Uç Ölçümü

## Kaynak fikri

Cilt 2 Bölüm 9–10: ikinci deneme, beklenen yeni uç, başarısız yeni dip/tepe ve iki hareket bacağının kalitesini karşılaştırma.

## Nedensel tanım

Ardışık aynı yönlü minor swing bacakları karşılaştırılır. İkinci bacak ancak bitiş swing'i teyit edildiğinde olay olur. Mesafe, süre, hız ve yol verimliliği oranları ilk bacağa göre hesaplanır. Yeni uç için 0,10 ATR tolerans kullanılır.

- `new_extreme_success`: İkinci bacak beklenen yönde önceki ucu toleransın ötesinde geçti; hipotez devam yönü.
- `new_extreme_failure`: Yeni uç üretilemedi; hipotez denemenin ters yönü.

## Kapsam

- 112.790 olay
- 60.400 yeni uç başarısızlığı
- 52.390 yeni uç başarısı
- 125 varlık, 494 yeterli uzunluktaki seri

## Ana sonuç

Çıplak “yeni uç başarısı devam eder” veya “yeni uç başarısızlığı tersine döner” kuralları yön ve zaman bölümü arasında kararlı değildir. Eğitim dönemindeki güçlü yön asimetrileri doğrulama/testte büyük ölçüde kaybolur.

4h/60 bar testte:

- Aşağı deneme başarısız → yukarı: 203 olay, `%1,46` XU100-aşırı medyan, `%57,64` pozitif.
- Yukarı deneme başarısız → aşağı: 259 olay, `-%0,70`, `%47,10` pozitif.
- Aşağı yeni uç başarısı → aşağı devam: 217 olay, `-%0,92`, `%48,85` pozitif.
- Yukarı yeni uç başarısı → yukarı devam: 172 olay, `%1,97`, `%58,14` pozitif.

Fakat bu işaretler eğitim dönemiyle aynı değildir; çıplak olay genel kural olarak onaylanmaz.

## Daha düzenli alt bağlamlar

4h yukarı ikinci denemenin yeni tepe üretememesi sonrası aşağı hipotezinde:

- Mesafe oranı `0,70–1,00` (weaker): eğitim `%4,02`, doğrulama `%0,04`, test `%1,68`; test 42 olay.
- Süre oranı `1,00–1,50` (longer): `%2,99 / %0,69 / %1,17`; test 18 olay.
- Hız oranı `1,00–1,30` (similar): `%3,24 / %3,98 / %0,73`; test 29 olay.

Üçü de işaret olarak üç zaman bölümünde pozitiftir; fakat test örnekleri küçüktür ve birbirinden bağımsız kombinasyonlar değildir. `devam_et` yerine `baglam_gerekli/ornek_sinirli` olarak tutulur.

## Dosyalar

- `attempt_events.csv`: 112.790 olayın azaltılmamış olay tablosu
- `attempt_time_split_study.csv`: Grup/periyot/yön/olay bazında zaman ayrımı
- `attempt_context_study.csv`: Mesafe, hız ve süre bantları
- `attempt_symbol_results.csv`: Sembol bazlı sonuçlar
- `summary.json`: Kapsam özeti
