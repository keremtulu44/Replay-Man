# PTA-C1-2026 — Bölüm 6

**PDF sayfaları:** 37–42
**Sayfa kartları:** 6

## Alt başlıklar

- 6.1 — Gerçek hareket aralığı (True Range): neden yalnız mum boyu
- 6.4 — Ham ATR neden iki farklı varlık arasında doğrudan karşılaştırılmaz?
- 6.5 — ATR stop için nasıl kullanılır?
- 6.7 — Düşük ATR ve kırılım beklentisi
- 6.10 — ATR penceresi ve zaman dilimi “normal” tanımını değiştirir
- 6.11 — ATR hangi araçlarla tamamlanır?

## Konu dağılımı

- `volatility`: 6 sayfa
- `risk_management`: 5 sayfa
- `trend_regime`: 4 sayfa
- `breakout_failure`: 4 sayfa
- `ohlcv_data`: 2 sayfa
- `strategy_design`: 1 sayfa
- `multi_timeframe`: 1 sayfa
- `psychology_process`: 1 sayfa
- `fundamental_derivatives`: 1 sayfa
- `momentum`: 1 sayfa

## Sayfa şeritleri

### PDF s. 37 — 6.1 — Gerçek hareket aralığı (True Range): neden yalnız mum boyu

BÖLÜM 6 ATR: Yön Değil, Hareket Genişliği ATR’yi “fiyat nereye gidecek?” sorusu için kullanmayın. ATR’nin işi daha basittir: fiyatın son dönemde ne kadar geniş hareket ettiğini ölçer ve stop mesafesi gibi risk kararlarına yardımcı olur. HIZLI ROL — Ana görev: fiyatın ne kadar geniş hareket ettiğini görmek ve stop mesafesini ayarlamaya yardım etmek.

**Konular:** volatility, risk_management, trend_regime, breakout_failure

**Kart:** `PTA-C1-2026.p0037`

### PDF s. 38 — 6.4 — Ham ATR neden iki farklı varlık arasında doğrudan karşılaştırılmaz?

SAYISAL ÖRNEK Önceki kapanış 100, en yüksek 108, en düşük 104. En yüksek−en düşük=4; |108−100|=8; |104−100|=4. Yalnız mum boyuna bakılsaydı hareketin yarısı görünmezdi.

**Konular:** volatility, trend_regime, ohlcv_data, breakout_failure, risk_management

**Kart:** `PTA-C1-2026.p0038`

### PDF s. 39 — 6.5 — ATR stop için nasıl kullanılır?

KÜÇÜK HESAP ATR% ≈ ATR / Fiyat × 100. Ham sayı aynı, göreli risk aynı değil. 6.5 — ATR stop için nasıl kullanılır?

**Konular:** volatility, risk_management

**Kart:** `PTA-C1-2026.p0039`

### PDF s. 40 — 6.7 — Düşük ATR ve kırılım beklentisi

Yaklaşım Avantaj Risk Sadece 1×ATR Otomatik ve kolay İşlem fikrinin bozulduğu seviyeyle ilişkili olmayabilir Yapı + ATR ek payı Yapı ve fiyat hareketliliğini birleştirir Katsayı yine test/strateji gerektirir “1 ATR” VE “2 ATR” SİHİRLİ SAYI DEĞİLDİR Katsayı büyüdükçe stop genişler, pozisyon büyüklüğü aynı tutulursa parasal risk de artar. Profesyonel kullanımda stop mesafesi ile pozisyon büyüklüğü birlikte ele alınmalıdır. 6.6 — Başlangıç stopu ile takip eden stop aynı görev değildir Başlangıç stopunun yeri 6.5’teki gibi önce işlem fikrinin bozulduğu seviyeye göre belirlenir.

**Konular:** risk_management, volatility, breakout_failure, strategy_design, trend_regime

**Kart:** `PTA-C1-2026.p0040`

### PDF s. 41 — 6.10 — ATR penceresi ve zaman dilimi “normal” tanımını değiştirir

DOĞRU ÇEVİRİ Düşük ATR = sakin piyasa. Donchian/fiyat yapısı kırılımı = yönlü giriş işareti. İlki yön vermez; ikincisi kırılımı gösterir.

**Konular:** volatility, multi_timeframe, psychology_process, fundamental_derivatives, ohlcv_data

**Kart:** `PTA-C1-2026.p0041`

### PDF s. 42 — 6.11 — ATR hangi araçlarla tamamlanır?

6.11 — ATR hangi araçlarla tamamlanır? Kombinasyon Rol dağılımı Değerlendirme ATR + Fiyat yapısı Fiyat hareketliliği/risk + yapısal seviye Çok güçlü ATR + Donchian Fiyat hareketliliği koşulu + kırılım tetiği Çok güçlü ATR + RSI/Stoch Risk/koşul + hareket gücü zamanlama Tamamlayıcı ATR + MACD Fiyat hareketliliği + hareket gücü Tamamlayıcı ATR + Supertrend ATR + ATR-tabanlı trend çizgisi Bağımsız iki teyit değildir ATR + Bollinger İki farklı fiyat hareketliliği ölçümü Görev ayrımı yoksa tekrar BÖLÜM SONUCU ATR yön değil hareket genişliği aracıdır. En doğal rolleri fiyat hareketliliğini ölçmek, yapısal stopa gerektiğinde ek pay bırakmak ve kırılım öncesi sıkışma/genişlemeyi izlemektir.

**Konular:** volatility, breakout_failure, momentum, risk_management, trend_regime

**Kart:** `PTA-C1-2026.p0042`
