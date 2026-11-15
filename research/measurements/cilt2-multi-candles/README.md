# Cilt 2 P3 — İki, Üç ve Çok Mumlu Diziler

## Kapsam

343.617 olay; 125 varlık ve dört periyot. Strict engulfing, harami, iki mumluk geri alma, morning/evening star, üç asker/üç karga, üç mumluk devam ve inside-bar kırılımı ölçüldü.

## 4h/60 bar BIST sonucu

Çoğu dizi eğitim ve test arasında işaret değiştirdi. Strict bullish engulfing eğitim `-%3,51`, doğrulama `%0,23`, test `%1,10`; bearish engulfing `%3,51 / %0,11 / -%0,75`. Harami ve iki mumluk geri alma da aynı rejim asimetrisini gösterdi.

### Düzenli aday: three crows

Aşağı hipotezinde XU100-aşırı medyan eğitim `%3,66`, doğrulama `%0,56`, test `%3,76`; testte 84 geçerli olay ve `%61,90` pozitif. İşaret üç bölümde pozitiftir. Örnek sayısı acceptance gibi geniş olaylara göre sınırlıdır; bağlam ve parametre komşuluğu doğrulanacaktır.

### Kararsız: three soldiers

Eğitim `-%4,82`, doğrulama `-%0,75`, test `%3,61`; testte yalnız 32 olay. Kararlı değildir.

### Diğer olumsuz/kararsızlar

Bear continuation eğitim/doğrulamada pozitifken testte `-%2,88`; morning star testte `-%1,70`; inside break up doğrulamada negatif, testte pozitif. Tek başlarına onaylanmadılar.

## Karar

- Three crows: `devam_et_ornek_sinirli`
- Engulfing/harami/two-bar reclaim: `rejime_bagli`
- Three soldiers/morning-evening star/continuation: `kararsiz`
- Mum adı temel geometriden bağımsız avantaj kabul edilmeyecek; P12 örtüşme kontrolü yapılacak.

## Dosyalar

- `inventory.csv`: Bütün seri ve dizi sayıları
- `event_study.csv`: Grup/periyot/zaman/olay/yön için eksiksiz sonuç
- `summary.json`: Kapsam ve olay sayıları
