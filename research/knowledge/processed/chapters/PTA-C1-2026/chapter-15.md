# PTA-C1-2026 — Bölüm 15

**PDF sayfaları:** 89–94
**Sayfa kartları:** 6

## Alt başlıklar

- 15.2 — Merkezi Pivot Aralığı (Central Pivot Range, CPR): tek çizgi yerine
- 15.4 — RS Line: RSI değil, karşılaştırma ölçütüne göre performans
- 15.5 — RS Line ile göreli güç sıralaması aynı şey değildir
- 15.6 — Trend Strength Index: trendin ne kadar düzenli ilerlediğini ölçer
- 15.7 — Kısa referans araçları için rol matrisi

## Konu dağılımı

- `trend_regime`: 4 sayfa
- `indicator_systems`: 4 sayfa
- `momentum`: 4 sayfa
- `ohlcv_data`: 2 sayfa
- `volume_flow`: 2 sayfa
- `geometry_tools`: 1 sayfa
- `risk_management`: 1 sayfa
- `psychology_process`: 1 sayfa
- `fundamental_derivatives`: 1 sayfa
- `relative_cross_market`: 1 sayfa
- `volatility`: 1 sayfa

## Sayfa şeritleri

### PDF s. 89 — 15.2 — Merkezi Pivot Aralığı (Central Pivot Range, CPR): tek çizgi yerine

BÖLÜM 15 Kısa Referans Araçları: Pivot Points, RS Line ve Trend Strength Index HIZLI ROL — Pivot Points önemli fiyat bölgelerini, RS Line varlığın karşılaştırma ölçütüne göre güçlü mü zayıf mı olduğunu, Trend Strength Index ise trendin ne kadar düzenli ilerlediğini gösterir. Üçü de yardımcı araçtır; tek başına giriş sistemi değildir. Ana risk: pivotları gelecek tahmini, göreli zayıflığı “ucuz”, TSI’yi de RSI veya ADX ile aynı araç sanmak.

**Konular:** trend_regime, indicator_systems, geometry_tools, momentum, risk_management

**Kart:** `PTA-C1-2026.p0089`

### PDF s. 90 — 15.4 — RS Line: RSI değil, karşılaştırma ölçütüne göre performans

Fiyat CPR’ın üzerinde, içinde veya altında bulunabilir. Bu konum tek başına AL/SAT üretmez; fiyat yapısı ve diğer karar katmanları ayrıca değerlendirilmelidir. Ardışık dönemlerin CPR bölgeleri karşılaştırıldığında merkez referans bölgesinin yukarı, aşağı veya yatay taşındığı görülebilir.

**Konular:** ohlcv_data, psychology_process, fundamental_derivatives, indicator_systems, momentum

**Kart:** `PTA-C1-2026.p0090`

### PDF s. 91 — 15.5 — RS Line ile göreli güç sıralaması aynı şey değildir

“Fiyat yükseliyor” ile “liderlik ediyor” aynı soru değildir. EN ÖNEMLİ TEKNİK HATA “Karşılaştırma ölçütünden düşük performans = göreli olarak ucuz, almak için iyi olabilir” çıkarımı doğru değildir. Göreli zayıflık ucuzluk kanıtı değildir; bir varlık karşılaştırma ölçütünden aylarca daha kötü performans göstermeye devam edebilir.

**Konular:** volume_flow

**Kart:** `PTA-C1-2026.p0091`

### PDF s. 92 — 15.6 — Trend Strength Index: trendin ne kadar düzenli ilerlediğini ölçer

İkisi de göreli güç ailesindedir; ancak hesapları ve çıktıları aynı değildir. Bu nedenle bir RS çizgisi ile “RS 90” gibi bir göreli güç puanını aynı gösterge sanmayın. Göreli liderlik mutlak yükseliş gerektirmez Genel piyasa düşerken bir varlık daha az düşüyor, yatay kalıyor veya pozitif kalabiliyorsa karşılaştırma ölçütüne göre göreli güç gösterebilir.

**Konular:** trend_regime, indicator_systems, momentum, relative_cross_market

**Kart:** `PTA-C1-2026.p0092`

### PDF s. 93 — 15.7 — Kısa referans araçları için rol matrisi

Araç Ana soru Temel çıktı RSI Son kazanç/kayıp hareket gücü dengesi nasıl? 0 … 100 hareket gücü osilatörü NEDEN TSI + ADX AYNI ŞEY DEĞİL? TSI fiyatın zaman içinde ne kadar düzenli ilerlediğine, ADX ise yukarı ve aşağı yönlü hareket arasındaki farkın ne kadar belirgin olduğuna bakar.

**Konular:** indicator_systems, trend_regime, momentum, volatility, ohlcv_data

**Kart:** `PTA-C1-2026.p0093`

### PDF s. 94 — 15.7 — Kısa referans araçları için rol matrisi

Araç Soru Rol RS Line Varlık karşılaştırma ölçütüne göre lider mi? Göreli performans Trend Strength Index Fiyat zamana karşı ne kadar düzenli trend ediyor? Trend tutarlılığı ARA KAVRAM Hesaplanan Araçlardan Çizim Geometrisine Geçiş İlk on beş bölümde çoğunlukla fiyat, hacim veya zaman serisinden hesaplanan araçları inceledik.

**Konular:** trend_regime, volume_flow

**Kart:** `PTA-C1-2026.p0094`
