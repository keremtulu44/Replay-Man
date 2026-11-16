# PTA-C1-2026 — Bölüm 21

**PDF sayfaları:** 126–139
**Sayfa kartları:** 14

## Alt başlıklar

- 21.1 — Beş soruluk rol çakışması testi
- 21.2 — Üç çizgi aynı şeyi söylüyorsa üç teyit yoktur
- 21.3 — Örnek sistem 1: trend içi geri çekilme
- 21.4 — Örnek sistem 2: düşük fiyat hareketliliğinden kırılım
- 21.6 — Örnek sistem 4: geometrik işlem düzeni
- 21.8 — Kendi minimal sistemini kurma şablonu
- 21.9 — Sistemi kurduktan sonra: beklenen değer ve sermaye
- 21.10 — Geçmişe aşırı uyumu kontrol edin: tek “mükemmel” ayardan
- 21.11 — Geliştirme dönemi, test dönemi ve zaman içinde ileri test
- 21.12 — Kötü koşullarda dayanıklılık ve işlem sırası testi
- 21.14 — Hayatta kalma yanlılığı: yalnız başarılı örneklere bakmayın

## Konu dağılımı

- `risk_management`: 9 sayfa
- `trend_regime`: 6 sayfa
- `indicator_systems`: 5 sayfa
- `validation_replay`: 5 sayfa
- `volatility`: 4 sayfa
- `momentum`: 3 sayfa
- `breakout_failure`: 2 sayfa
- `volume_flow`: 2 sayfa
- `geometry_tools`: 2 sayfa
- `position_management`: 2 sayfa
- `strategy_design`: 1 sayfa
- `pullback`: 1 sayfa
- `candle_behavior`: 1 sayfa
- `execution_microstructure`: 1 sayfa

## Sayfa şeritleri

### PDF s. 126 — 21.1 — Beş soruluk rol çakışması testi

BÖLÜM 21 Profesyonel Kombinasyon Sistemi: Araçlardan Karar Sistemine İyi bir sistem çok sayıda gösterge kullanan sistem değildir. Her aracın ayrı bir soruya cevap verdiği, aynı bilgiyi tekrar eden araçların çıkarıldığı ve gerektiğinde “işlem yok” diyebilen sade bir karar sistemidir. HIZLI ÇERÇEVE — Önce piyasa ortamını ve yönü belirleyin.

**Konular:** strategy_design, trend_regime

**Kart:** `PTA-C1-2026.p0126`

### PDF s. 127 — 21.2 — Üç çizgi aynı şeyi söylüyorsa üç teyit yoktur

ÇIKARMA TESTİ Bir indikatörü eklemeden önce “ne katıyor?” diye sormak yeterli değildir. Daha güçlü soru şudur: “Bu indikatörü çıkarırsam hangi karar aşamasını artık veremiyorum?” Cevap yoksa araç yalnız görsel güven hissi üretiyor olabilir. 21.2 — Üç çizgi aynı şeyi söylüyorsa üç teyit yoktur RSI, Stochastic ve Stoch RSI aynı yönde hareket ettiğinde üç ayrı teyit varmış gibi görünebilir; ancak aynı hareket gücü ailesinden bilgi taşırlar ve Stoch RSI doğrudan RSI’dan türetilir.

**Konular:** indicator_systems, momentum, trend_regime

**Kart:** `PTA-C1-2026.p0127`

### PDF s. 128 — 21.3 — Örnek sistem 1: trend içi geri çekilme

Zayıf yığın Sorun Daha temiz alternatif RSI + Stochastic + Stoch RSI Benzer hareket gücü bilgisi Tek hareket gücü aracı + Fiyat yapısı + ATR 20/50/200 EMA + MACD + Supertrend Aynı trend bilgisinin yoğun tekrarı Tek piyasa ortamı filtresi + konum + risk ATR + Bollinger bant genişliği + Bollinger Fiyat hareketliliğini üç biçimde saymak Bollinger sıkışması + fiyat yapısı/hacim; ATR yalnız riskte VRVP + FRVP aynı aralık Aynı profil ailesi Tek profil + Fiyat yapısı / AVWAP 21.3 — Örnek sistem 1: trend içi geri çekilme Trend içi geri çekilmede amaç fiyatı “ucuz” diye otomatik almak değildir. Önce yön ve korunması gereken yapı belirlenir; ardından uygun konumda hareket gücünün yeniden trend yönüne dönmesi beklenir. Stop, sinyalden değil işlem fikrinin bozulduğu yapısal seviyeden belirlenir; ATR yalnız gerektiğinde hareket genişliğine göre ek pay bırakmaya yardım eder.

**Konular:** indicator_systems, volatility, trend_regime, momentum, pullback

**Kart:** `PTA-C1-2026.p0128`

### PDF s. 129 — 21.4 — Örnek sistem 2: düşük fiyat hareketliliğinden kırılım

Aşama Örnek araç Sorduğu soru Bağlam / yön Fiyat yapısı veya tek MA Ana trend hâlâ yukarı mı? Konum Önceki destek/direnç, AVWAP veya anlamlı geri çekilme bölgesi İşlem aramak için mantıklı yerde miyiz? Giriş işareti RSI veya Stochastic Hareket gücü trend yönüne yeniden dönüyor mu?

**Konular:** volatility, breakout_failure, indicator_systems, momentum, risk_management

**Kart:** `PTA-C1-2026.p0129`

### PDF s. 130 — 21.4 — Örnek sistem 2: düşük fiyat hareketliliğinden kırılım

Katman Örnek gözlem Yanlış çıkarım Donchian Son N mumun en yüksek seviyesinin üzerinde kapanış “Kesin trend başladı” ATR Sıkışma sonrası genişleme “Yön yukarı olmak zorunda” Hacim Göreli hacim belirgin arttı “Fiyat kesin devam eder” Fiyat yapısı / stop Kırılan aralığın içine geri kapanış “İndikatörler olumlu; stopa gerek yok”

**Konular:** volatility, volume_flow, indicator_systems, risk_management, trend_regime

**Kart:** `PTA-C1-2026.p0130`

### PDF s. 131 — 21.6 — Örnek sistem 4: geometrik işlem düzeni

21.5 — Örnek sistem 3: konum / değer odaklı geri çekilme Volume Profile ve AVWAP aynı hacim verisini kullansa da farklı sorular sorar: biri hacmin fiyat seviyelerine dağılımını, diğeri seçilen başlangıçtan sonraki hacim ağırlıklı ortalama maliyeti gösterir. İkisi de fiyat davranışının yerine geçmez; yapı desteklemiyorsa POC, HVN veya AVWAP teması tek başına alış gerekçesi değildir. Rol Araç Doğru okuma Yapı Fiyat yapısı Yükseliş yönlü tepe-dip dizisi / korunması gereken dip Konum 1 Volume Profile VAH/VAL/POC/HVN/LVN çevresindeki kabul veya reddi izle Konum 2 AVWAP Önemli başlangıç noktasından ortalama maliyet referansı Giriş işareti RSI / fiyat davranışı Konumda hareket gücü veya fiyat yapısı dönüşü Risk ATR + işlem fikrinin bozulduğu seviye Konum seviyesi ile stop seviyesini karıştırma ÖRTÜŞME ≠ BAĞIMSIZLIK İki farklı araç aynı fiyat bölgesini işaret edebilir ve bu bölgeyi daha dikkat çekici hale getirebilir.

**Konular:** volume_flow, geometry_tools, risk_management, volatility, candle_behavior

**Kart:** `PTA-C1-2026.p0131`

### PDF s. 132 — 21.8 — Kendi minimal sistemini kurma şablonu

GEÇMİŞE AŞIRI UYUM ALARMI Fibonacci başlangıç noktasını, Pitchfork dönüş noktalarını ve varyantını fiyatın geçmişine en iyi oturacak şekilde art arda değiştiriyorsanız sonradan çok sayıda “kesişim” bulmak kolaylaşır. Bu durum öngörü gücünü değil, model esnekliğini gösterir. 21.7 — “İşlem yok” sonucunu sistemin içine yaz Her grafikte işlem bulmak zorunda değilsiniz.

**Konular:** geometry_tools, indicator_systems, risk_management, trend_regime, breakout_failure

**Kart:** `PTA-C1-2026.p0132`

### PDF s. 133 — 21.9 — Sistemi kurduktan sonra: beklenen değer ve sermaye

Alan Yazılması gereken kural Bağlam Trend veya yatay piyasa nasıl tanımlanıyor? Yön Alış veya satış yönü hangi açık koşulla belirleniyor? Konum İşlem yalnız nerede aranacak?

**Konular:** risk_management, execution_microstructure, trend_regime, position_management, validation_replay

**Kart:** `PTA-C1-2026.p0133`

### PDF s. 134 — 21.10 — Geçmişe aşırı uyumu kontrol edin: tek “mükemmel” ayardan

Başa baş kazanma oranı = 1 / (1 + Ortalama Kazanç R) Örneğin 1R ortalama kazançta yaklaşık %50, 2R’de %33,3, 3R’de %25 ve 4R’de %20 kazanma oranı başa baş noktasıdır. Gerçek sistemde komisyon, emir kayması, kısmi çıkış ve değişken sonuçlar bu hesabı değiştirir. Kısa dönem sonuçların dalgalanması (variance): iyi bir sistem bile bir süre kötü görünebilir Pozitif beklenen değer, işlemlerin düzenli sırayla kazanacağı anlamına gelmez.

**Konular:** risk_management, position_management, validation_replay

**Kart:** `PTA-C1-2026.p0134`

### PDF s. 135 — 21.11 — Geliştirme dönemi, test dönemi ve zaman içinde ileri test

Bu ilke kitabın çizim araçlarında kullandığı “sağ tarafı görmeden aynı başlangıç noktasını seçebilir miydim?” disiplininin sistem optimizasyonundaki karşılığıdır: çok fazla indikatör, filtre ve parametre denenirse geçmişte iyi görünen bir kombinasyon bulmak kolaylaşır; bu, gerçek avantajın arttığını göstermez. 21.11 — Geliştirme dönemi, test dönemi ve zaman içinde ileri test Sistemi kurarken kullanılan dönem ile onu sınamak için ayrılan dönem aynı görevi taşımaz. Bir modelin geliştirildiği geçmişte iyi görünmesi, daha önce kullanılmamış bir dönemde de aynı davranışı göstereceği anlamına gelmez.

**Konular:** validation_replay

**Kart:** `PTA-C1-2026.p0135`

### PDF s. 136 — 21.12 — Kötü koşullarda dayanıklılık ve işlem sırası testi

21.12 — Kötü koşullarda dayanıklılık ve işlem sırası testi Geçmiş veri testi (backtest) yalnız ideal koşullarda değerlendirilmemelidir. Komisyonun artması, emir kaymasının büyümesi veya işlemin biraz gecikmesi gibi daha kötü koşullarda sistemin nasıl değiştiği de incelenebilir. Dayanıklılık kontrolü Ne değiştirilir?

**Konular:** risk_management, validation_replay

**Kart:** `PTA-C1-2026.p0136`

### PDF s. 137 — 21.14 — Hayatta kalma yanlılığı: yalnız başarılı örneklere bakmayın

Bu testin ana sorusu şudur: Aynı matematiksel avantaj daha kötü bir işlem sırasıyla karşıma çıksaydı sermaye ne kadar zorlanırdı? Bu nedenle bu test özellikle kötü bir işlem sırasının sermayeyi ne kadar zorlayabileceğini ve pozisyon büyüklüğünün buna uygun olup olmadığını anlamaya yardım eder. 21.13 — Veri uzunluğu ile güncellik arasında denge vardır Daha uzun tarih daha fazla işlem örneği sağlar; ancak çok eski veriler güncel piyasa davranışını daha az temsil edebilir.

**Konular:** risk_management, validation_replay

**Kart:** `PTA-C1-2026.p0137`

### PDF s. 138 — 21.14 — Hayatta kalma yanlılığı: yalnız başarılı örneklere bakmayın

değerlendirmesinde yalnız kazanan örnekleri değil, başarısız örnekleri, sermaye düşüşünü ve alınan riski de görünür tutun. BÖLÜM SONUCU İyi bir sistem, yalnız geçmişte güzel görünen sistem değildir. Her aracın görevi açık olmalı; işlem yapılmayacak koşullar, risk sınırı ve yönetim kuralı önceden tanımlanmalıdır.

**Konular:** risk_management

**Kart:** `PTA-C1-2026.p0138`

### PDF s. 139 — 21.14 — Hayatta kalma yanlılığı: yalnız başarılı örneklere bakmayın

SON SÖZ Teknik analizde profesyonellik, daha fazla çizgi görmek değil; hangi çizginin hangi soruya cevap verdiğini, hangi koşulda başarısız olabileceğini ve hangi bilgi eksikse işlem yapmamak gerektiğini bilmektir. Bu kitapta kullanılan bütün araçların ortak amacı da budur: belirsizliği yok etmek değil, belirsizlik içinde daha tutarlı karar kurmak.

**Konular:** referans

**Kart:** `PTA-C1-2026.p0139`
