# Çapraz Piyasa, Cilt 1, Formasyon, Seans ve Risk Sonuçları

## Kapsam

156.386 olay: RSI çıkışları, MACD kesişimleri, Bollinger geri girişleri, ikili tepe ve ikili dip. 125 varlık ve dört periyot işlendi.

## Cilt 1 indikatörleri

4h/60 bar BIST testinde MACD bull cross `%2,60` XU100-aşırı medyan ve `%56,2` pozitif verdi; fakat eğitimde `-%4,01` ve `%36,3` olduğundan kararlı değildir. RSI oversold exit testte `-%0,36`, RSI overbought exit `-%3,97`; Bollinger alt geri giriş `-%0,79`, üst geri giriş `-%2,62`. Çıplak indikatör olayı genel avantaj değildir.

ADX zayıf/güçlü bağlamı tüm olaylarda tek yönlü üstünlük üretmedi. İndikatörler rejim ve yön filtresi olmadan kullanılmamalıdır.

## Formasyonlar

23.136 ikili tepe ve 22.435 ikili dip adayı üretildi. 4h/60 testte ikili tepe aşağı hipotezi `-%2,21`, `%41,7` pozitif; ikili dip yukarı hipotezi `%0,22`, `%50,7`. Her ikisi de eğitim/test arasında işaret değiştiriyor. Yalnız eşit iki uç, formasyon avantajı değildir; aradaki geri çekilme, boyun kırılımı ve bağlam gerekir.

## Göreceli ve çapraz piyasa

XU100, S&P 500, USDTRY, altın ve Brent'in yalnız tamamlanmış geçmiş 5-bar getirileri olaylara backward-asof ile bağlandı. Farklı sinyaller birlikte havuzlandığında tek bir çapraz piyasa yönü evrensel üstünlük vermedi. Özellikle tüm olayları/yönleri toplamak ekonomik olarak anlamsızdır; sonuçlar `cross_market_study.csv` içinde olay ve hipotez yönü ayrımında korunur.

## Seans

UTC saat, hafta günü ve overnight/morning/midday/afternoon/evening grupları kaydedildi. Tek seans bütün olaylarda üstün çıkmadı; seans yalnız olay × piyasa grubu etkileşimi olarak kullanılmalıdır.

## Risk ve pozisyon sonucu

20 bar, 1 ATR hedef ve 1 ATR stop ilk erişim testi:

- Target: 75.054
- Stop: 74.662
- Aynı barda hedef ve stop: 2.037 — sıra bilinmediği için `ambiguous`
- Süre sonu: 2.024
- Yetersiz gelecek: 2.609

Target/stop toplamı neredeyse yazı-turadır. Sabit 1:1 ATR yönetimi çıplak olay havuzunda avantaj üretmiyor. Aynı bar belirsizliği başarıya çevrilmedi. Portföy simülasyonu yapılmadı; korelasyonlu eşzamanlı olaylar sonraki katmandır.

## Dosyalar

- `events.csv.gz`: azaltılmamış olaylar
- `event_study.csv`: indikatör/formasyon × ADX × seans × zaman bölümü
- `cross_market_study.csv`: olay/yön ayrımlı çapraz piyasa bağlamı
- `risk_study.csv`: hedef/stop/ambiguous/timeout
- `summary.json`: kapsam
