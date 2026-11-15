# PTA-C1-2026 — Bölüm 10

**PDF sayfaları:** 60–65
**Sayfa kartları:** 6

## Alt başlıklar

- 10.1 — VWAP nasıl hesaplanır? Küçük bir örnek
- 10.3 — Hesabın nereden başladığı neden önemlidir?
- 10.5 — AVWAP için iyi başlangıç noktası nedir?
- 10.6 — AVWAP nasıl kullanılabilir?
- 10.8 — Birden fazla anlamlı AVWAP ve çizginin yeniden aşılması
- 10.10 — VWAP hangi araçlarla birlikte kullanılabilir?

## Konu dağılımı

- `volume_flow`: 5 sayfa
- `trend_regime`: 4 sayfa
- `breakout_failure`: 3 sayfa
- `support_resistance`: 2 sayfa
- `risk_management`: 2 sayfa
- `indicator_systems`: 2 sayfa
- `volatility`: 1 sayfa
- `sessions_timing`: 1 sayfa
- `momentum`: 1 sayfa
- `fundamental_derivatives`: 1 sayfa
- `fundamental_valuation`: 1 sayfa
- `strategy_design`: 1 sayfa

## Sayfa şeritleri

### PDF s. 60 — 10.1 — VWAP nasıl hesaplanır? Küçük bir örnek

BÖLÜM 10 VWAP ve Anchored VWAP: Hacim Ağırlıklı Ortalama Fiyat VWAP’ı “gerçek fiyat” veya sihirli destek/direnç gibi düşünmeyin. VWAP, daha çok işlem yapılan fiyatlara daha fazla ağırlık vererek hesaplanan bir ortalama fiyat çizgisidir. HIZLI ROL — Ana görev: işlemlerin yoğunluğunu da hesaba katan ortalama fiyatı göstermek.

**Konular:** volume_flow, support_resistance, risk_management, volatility

**Kart:** `PTA-C1-2026.p0060`

### PDF s. 61 — 10.3 — Hesabın nereden başladığı neden önemlidir?

10.2 — “VWAP daha gerçek fiyat” cümlesindeki sorun VWAP, hacmi de hesaba katan bir ortalama fiyat çizgisidir; “gerçek fiyat” veya mutlak adil değer değildir. Fiyatın VWAP’a dönmek zorunda olduğuna dair bir kural yoktur. YAYGIN İFADE → DOĞRU ÇERÇEVE “VWAP yüksek hacimli fiyata mıknatıs olur” yerine: “VWAP, yüksek hacimli gözlemlere daha fazla ağırlık verir; bu nedenle çizgi o fiyatların etkisini daha güçlü taşır.” Matematikte fiyatı VWAP’a geri çeken bir kuvvet yoktur.

**Konular:** volume_flow

**Kart:** `PTA-C1-2026.p0061`

### PDF s. 62 — 10.5 — AVWAP için iyi başlangıç noktası nedir?

Araç Başlangıç mantığı En doğal rol Seans / periyodik VWAP Tanımlı dönemlerde sıfırlama Seans/periyot içi hacim ağırlıklı konum Anchored VWAP Kullanıcının seçtiği olay/pivot O olaydan sonraki hacim ağırlıklı maliyet referansı SMA / EMA Sabit kayan geriye bakılan dönem penceresi Trend/yumuşatma; hacim ağırlığı yok 10.4 — Seans VWAP ile AVWAP’ın zaman ufku farklıdır Seans VWAP her yeni seansta sıfırlanır ve ağırlıklı olarak mevcut seansın hacim ağırlıklı ortalama fiyatını temsil eder. Anchored VWAP (AVWAP) ise seçilen olay veya başlangıç noktasından itibaren birikmeye devam eder. Bu nedenle soru “hangisi daha iyi?” değildir.

**Konular:** volume_flow, sessions_timing, breakout_failure, trend_regime

**Kart:** `PTA-C1-2026.p0062`

### PDF s. 63 — 10.6 — AVWAP nasıl kullanılabilir?

B noktası yalnız çizgiyi bugünkü fiyata yaklaştırdığı için seçiliyorsa yöntem geçmişe uydurulmuş olur. BAŞLANGIÇ NOKTASI TESTİ Kendinize şu soruyu sorun: “Grafiğin sağ tarafını kapatsaydım yine bu başlangıç noktasını seçer miydim?” Cevap hayırsa başlangıç noktası seçimi büyük olasılıkla sonuçtan etkilenmiştir. Bağlam AVWAP’ın rolü Giriş işareti / ek bilgi Yükseliş yönlü fiyat yapısı Belirgin dip AVWAP çevresi konum referansı Fiyat yapısının tekrar güçlenmesi Kırılım sonrası Kırılım başlangıcından ortalama maliyet referansı Yeniden test + kabul/reddedilme davranışı Geri çekilmede hareket gücü Konumu tanımlar RSI/MACD hareket gücü yeniden güçlenmesi Risk yönetimi Doğrudan stop değildir ATR + işlem fikrinin bozulduğu seviye ile tamamlanır YANLIŞ KULLANIM Fiyat AVWAP üzerinde = otomatik yükseliş yönlü değildir.

**Konular:** breakout_failure, indicator_systems, momentum, risk_management, trend_regime

**Kart:** `PTA-C1-2026.p0063`

### PDF s. 64 — 10.8 — Birden fazla anlamlı AVWAP ve çizginin yeniden aşılması

10.7 — AVWAP’ın seviyesi kadar eğimi ve başlangıç noktasının yaşı da önemlidir Fiyatın AVWAP’ın üzerinde veya altında olması bir konum bilgisidir. Buna ek olarak AVWAP’ın kendisinin yükselmesi, düşmesi veya yataylaşması da izlenebilir. Yükselen AVWAP, seçilen başlangıç noktasından sonraki hacim ağırlıklı ortalama fiyatın yukarı taşındığını; düşen AVWAP aşağı taşındığını gösterir.

**Konular:** volume_flow, breakout_failure, fundamental_derivatives, fundamental_valuation, trend_regime

**Kart:** `PTA-C1-2026.p0064`

### PDF s. 65 — 10.10 — VWAP hangi araçlarla birlikte kullanılabilir?

10.9 — VWAP + 50 MA kesişimi neden evrensel kural değildir? VWAP ile 50 günlük hareketli ortalama kesişimini işlem sinyali yapmak, VWAP’ın tanımı değil strateji tercihidir. Test edilmeden evrensel kurala dönüştürülemez.

**Konular:** volume_flow, indicator_systems, strategy_design, support_resistance, trend_regime

**Kart:** `PTA-C1-2026.p0065`
