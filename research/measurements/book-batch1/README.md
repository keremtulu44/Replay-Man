# Pullback, Mum, Rejim ve Çoklu Zaman Ölçümü

## Kapsam

- 309.467 toplam olay
- 85.475 teyitli pullback
- 223.992 güçlü kapanış/engulfing mum olayı
- 125 varlık, 495 yeterli seri
- Rejim: trend_up, trend_down, range, transition
- 1h/2h olaylarında yalnız tamamlanmış 4h bar bağlamı

## Pullback sonucu

4h/60 bar testte yükseliş yönlü pullback devamı 297 olayda `%1,57` XU100-aşırı medyan ve `%55,22` pozitif; aşağı yönlü devam 285 olayda `-%2,11` ve `%41,40`. Eğitim döneminde işaretler ters olduğu için çıplak pullback rejime bağlıdır.

Derinlikte sığ pullback testte güçlü görünür: yukarı hipotez 18 olayda `%8,18`, aşağı hipotez 21 olayda `%3,39`. Örnekler çok küçük olduğu için onaylanmaz. Orta derinlik yukarı 58 olayda `%2,10`; aşağı -%1,76.

## Mum sonucu

4h/60 bar test:

- Güçlü boğa kapanışı: 450 olay, `%1,30`, `%53,78` pozitif.
- Güçlü ayı kapanışı: 590 olay, `-%0,76`, `%47,29`.
- Bullish engulfing: 239 olay, `%1,15`, `%51,88`.
- Bearish engulfing: 174 olay, `-%0,78`, `%46,55`.

Bu olayların eğitim dönemindeki işaretleri ters olduğundan tek mum veya isimlendirilmiş dizi bağımsız ve kararlı avantaj değildir.

## Rejim ve çoklu zaman

1h güçlü aşağı kapanış, tamamlanmış 4h düşüş rejimiyle hizalı olduğunda 20 bar XU100-aşırı medyan:

- Eğitim `%0,18`, pozitif `%53,1`
- Doğrulama `%0,07`, pozitif `%51,4`
- Test `%0,45`, pozitif `%55,3`

İşaret üç bölümde pozitiftir fakat büyüklük küçüktür; maliyet testi gerekir. 1h güçlü yukarı kapanış + 4h yükseliş hizası üç bölümde kararlı değildir.

## Dosyalar

- `events.csv.gz`: Azaltılmamış olay tablosu
- `inventory.csv`: Mum ve rejim sayımları
- `time_regime_mtf_study.csv`: Zaman/rejim/üst-zaman sonuçları
- `pullback_depth_study.csv`: Pullback derinlik sonuçları
- `summary.json`: Kapsam
