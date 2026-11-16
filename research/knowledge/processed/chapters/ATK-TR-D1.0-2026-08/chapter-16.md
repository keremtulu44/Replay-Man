# ATK-TR-D1.0-2026-08 — Bölüm 16

**PDF sayfaları:** 329–351
**Sayfa kartları:** 23

## Alt başlıklar

- 16.1 — AI’yı Oracle Değil Yardımcı Olarak
- 16.2 — İnsan–AI Yetki Seviyeleri ve Sorumluluk
- 16.3 — Prompt Anatomisi: Amaçtan Doğrulamaya
- 16.5 — AI ile Grafik Analizi ve Çapraz Kontrol
- 16.6 — Fikirden Objektif Strateji Kuralına
- 16.7 — Pine Script Gereksinim Sözleşmesi
- 16.8 — AI Üretimli Kodu Semantik Olarak
- 16.9 — Debug, Trace, Regresyon ve Sürüm
- 16.10 — Backtest ve Performans İddialarını
- 16.12 — AI ile Screening ve Aday Liste Üretimi
- 16.13 — Ünlü Yatırımcı ve Kurumsal Portföy
- 16.14 — Fair Value, Hazır AI Stratejileri ve Model
- 16.15 — Tam AI–Pine–Araştırma İş Akışı

## Konu dağılımı

- `automation_ai`: 23 sayfa
- `strategy_design`: 11 sayfa
- `validation_replay`: 10 sayfa
- `risk_management`: 7 sayfa
- `liquidity_imbalance`: 7 sayfa
- `trend_regime`: 6 sayfa
- `multi_timeframe`: 5 sayfa
- `fundamental_valuation`: 4 sayfa
- `market_structure`: 4 sayfa
- `portfolio_correlation`: 3 sayfa
- `pullback`: 3 sayfa
- `volume_flow`: 3 sayfa
- `geometry_tools`: 3 sayfa
- `psychology_process`: 2 sayfa
- `fundamental_derivatives`: 2 sayfa
- `momentum`: 1 sayfa
- `support_resistance`: 1 sayfa
- `execution_microstructure`: 1 sayfa
- `crypto_specific`: 1 sayfa
- `ohlcv_data`: 1 sayfa
- `hedge_arbitrage`: 1 sayfa
- `relative_cross_market`: 1 sayfa

## Sayfa şeritleri

### PDF s. 329 — Bölüm girişi/devamı

BÖLÜM 16 Yapay Zekâ, Pine Script ve Araştırma Araçları AI önerisini doğrulanabilir kurala, kod ve araştırma kanıtına dönüştürmek

**Konular:** automation_ai

**Kart:** `ATK-TR-D1.0-2026-08.p0329`

### PDF s. 330 — Bölüm girişi/devamı

Bu Bölümün Amacı Bölüm 15’te grafik çalışma ortamını kurduk. Şimdi bu ortamda yapay zekâyı analiz yardımcısı, Pine Script’i kuralları görünür ve test edilebilir hâle getiren araç, araştırma platformlarını ise aday ve kaynak bulma katmanı olarak kullanacağız. Amacımız karar sorumluluğunu teknolojiye devretmek değil; tekrar eden işleri hızlandırırken hata kanıtını daha görünür hâle getirmektir.

**Konular:** automation_ai, validation_replay, fundamental_valuation, multi_timeframe, portfolio_correlation

**Kart:** `ATK-TR-D1.0-2026-08.p0330`

### PDF s. 331 — 16.1 — AI’yı Oracle Değil Yardımcı Olarak

16.1 AI’yı Oracle Değil Yardımcı Olarak Konumlandırmak Artificial intelligence — AI (verilen veri ve talimatlardan analiz, metin, kod veya aday fikir üretme aracı), geleceği bilen bağımsız bir piyasa aktörü değildir. Ona hangi grafiği, hangi dönemi, hangi tanımı ve hangi hedefi verdiğim; aldığı cevabın sınırını belirler. AI’nın hızı, girdi kalitesinin yerine geçmez.

**Konular:** automation_ai

**Kart:** `ATK-TR-D1.0-2026-08.p0331`

### PDF s. 332 — 16.2 — İnsan–AI Yetki Seviyeleri ve Sorumluluk

AI’nın uygun görevi İnsan denetimi Doğrudan verilmeyecek yetki Notları özetlemek ve karşılaştırmak Önemli ayrıntı atlandı mı? Kaynak görmeden gerçek kabul etmek Grafik için aday senaryo üretmek Swing, timeframe ve invalidation doğru mu? Tek cevaptan emir vermek Kural taslağı veya Pine kodu yazmak Tanım ve bar semantiği eşleşiyor mu?

**Konular:** automation_ai, strategy_design, portfolio_correlation, risk_management, validation_replay

**Kart:** `ATK-TR-D1.0-2026-08.p0332`

### PDF s. 333 — 16.3 — Prompt Anatomisi: Amaçtan Doğrulamaya

“Grafiği analiz et” ile “emir gönder” arasına veri, kural, test, risk ve onay kapıları koyarım. Hangi kapının otomatik, hangisinin manuel olduğunu süreç kartına yazarım. VAKA ANALİZİ — XAGTRYG AI YARDIMCISI AI, XAGTRYG 2S grafikte bullish pullback adayı gördüğünü söylüyor.

**Konular:** automation_ai, pullback, strategy_design, trend_regime, psychology_process

**Kart:** `ATK-TR-D1.0-2026-08.p0333`

### PDF s. 334 — 16.3 — Prompt Anatomisi: Amaçtan Doğrulamaya

Prompt parçası Yazılacak bilgi Örnek aksiyon Kural Eşik, swing tanımı, invalidation ve no- trade. “Protected low altı kapanışta aday iptal.” Çıktı Tablo, Pine spec, soru listesi veya hata raporu. “Kanıt–karşı kanıt–eksik veri tablosu.” Doğrulama Kaynak, hesap, test ve belirsizlik talebi.

**Konular:** automation_ai, strategy_design, pullback, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0334`

### PDF s. 335 — 16.5 — AI ile Grafik Analizi ve Çapraz Kontrol

16.4 Bağlam Paketi, Veri Kaynağı ve Zaman Damgası Context pack (AI’nın görevi doğru yorumlaması için birlikte verilen sembol, veri, timeframe, kural, sürüm ve örnekler paketi), konuşmanın geçmişine güvenmekten daha denetlenebilirdir. Özellikle grafik ve kod çalışmalarında hangi barların görünür olduğu, verinin kapanmış mı canlı mı olduğu ve kullanılan script sürümü kaydedilmelidir. Kayıt örneği Sembol kimliği Yanlış feed veya ürün analizini önlemek.

**Konular:** automation_ai, strategy_design, volume_flow, liquidity_imbalance, market_structure

**Kart:** `ATK-TR-D1.0-2026-08.p0335`

### PDF s. 336 — 16.6 — Fikirden Objektif Strateji Kuralına

Analiz sorusu AI’dan istenecek Kullanıcının kontrolü Momentum / hacim Impulse–pullback karşılaştırması. Zaman dilimleri aynı anda mı ve doğru mı? Senaryo Birincil, alternatif ve no-trade.

**Konular:** automation_ai, strategy_design, psychology_process, pullback, market_structure

**Kart:** `ATK-TR-D1.0-2026-08.p0336`

### PDF s. 337 — 16.7 — Pine Script Gereksinim Sözleşmesi

Son iki confirmed swing HH–HL ve close EMA üstünde. Pullback sağlıklı Derinlik, süre ve momentum ölçüsü? Depth ≤ 1.5 ATR; red body share sınırı.

**Konular:** automation_ai, strategy_design, volume_flow, risk_management, momentum

**Kart:** `ATK-TR-D1.0-2026-08.p0337`

### PDF s. 338 — 16.7 — Pine Script Gereksinim Sözleşmesi

Gereksinim alanı Sorulacak soru Örnek Artifact türü Indicator mı strategy mi? Adayları çiz + alert; emir simülasyonu ayrı strategy. Girdiler Kullanıcı hangi ayarları değiştirebilir?

**Konular:** multi_timeframe, automation_ai, trend_regime, volume_flow, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0338`

### PDF s. 339 — 16.8 — AI Üretimli Kodu Semantik Olarak

16.8 AI Üretimli Kodu Semantik Olarak Denetlemek Compile (kodun dil kurallarına uygun olup olmadığını denetleyip çalıştırılabilir hâle getirme), ilk kapıdır. Semantic test (kodun yazılı strateji kuralını doğru zaman ve doğru veriyle uygulayıp uygulamadığını sınama), asıl doğrulama kapısıdır. Sentaks hatasız kod; yanlış swing, erken sinyal veya future leak üretebilir.

**Konular:** automation_ai, multi_timeframe, strategy_design, validation_replay

**Kart:** `ATK-TR-D1.0-2026-08.p0339`

### PDF s. 340 — 16.9 — Debug, Trace, Regresyon ve Sürüm

VAKA ANALİZİ — GEÇMİŞTE KUSURSUZ DİP AI’nın yazdığı script her swing dibine “AL” etiketi yerleştiriyor. Replay’i etiketin öncesinden başlatırım. Etiket pivot için sağ tarafta üç bar bekledikten sonra geçmişteki dibe taşınıyorsa bu olay “pivot üç bar sonra onaylandı” diye kaydedilmelidir; dip anında erken sinyal gibi sunulamaz.

**Konular:** automation_ai, strategy_design, liquidity_imbalance, geometry_tools, market_structure

**Kart:** `ATK-TR-D1.0-2026-08.p0340`

### PDF s. 341 — 16.10 — Backtest ve Performans İddialarını

Kanıtlanmamış kod değişikliği yapma. En küçük tanılayıcı plot/trace öner. Seçilen neden doğrulandıktan sonra yalnız ilgili bloğa minimal patch üret ve korunması gereken davranışları listele.” DOĞRU BİLİNEN YANLIŞ Mit: AI’ya tüm kodu verip “düzelt” demek en hızlı yoldur.

**Konular:** automation_ai, validation_replay, support_resistance

**Kart:** `ATK-TR-D1.0-2026-08.p0341`

### PDF s. 342 — 16.10 — Backtest ve Performans İddialarını

Sonradan hayatta kalan/başarılı varlıklar mı seçildi? Lookahead, repaint veya gelecekteki endeks üyeliği var mı? Aynı bar close, gap, limit ve likidite gerçekçi mi?

**Konular:** validation_replay, automation_ai, risk_management, trend_regime, execution_microstructure

**Kart:** `ATK-TR-D1.0-2026-08.p0342`

### PDF s. 343 — 16.12 — AI ile Screening ve Aday Liste Üretimi

16.11 Alarm, Otomasyon, Entegrasyon ve Güvenlik Integration (iki uygulama arasında veri veya komut akışı kurma), kolaylık sağlarken yeni güven ve hata yüzeyi oluşturur. Örneğin üçüncü taraf bir köprü, AI’nın grafik ve Pine araçlarına erişmesini sağlayabilir. Kitapta araç adı yerine şu soru korunur: Bu entegrasyon hangi veriyi okuyabilir, hangi komutu çalıştırabilir ve hangi yetkiye gerçekten ihtiyaç duyar?

**Konular:** automation_ai, liquidity_imbalance, risk_management, validation_replay, crypto_specific

**Kart:** `ATK-TR-D1.0-2026-08.p0343`

### PDF s. 344 — 16.12 — AI ile Screening ve Aday Liste Üretimi

Screening adımı Aksiyon Kriter Büyüme, sağlık, değerleme ve risk ölçütlerini tanımla. Eksik veri Null değerlerin elenme veya işaretlenme kuralını yaz. Sıralama Tek skor yerine kriter katkılarını ayrı göster.

**Konular:** automation_ai, risk_management, fundamental_valuation, liquidity_imbalance, ohlcv_data

**Kart:** `ATK-TR-D1.0-2026-08.p0344`

### PDF s. 345 — 16.13 — Ünlü Yatırımcı ve Kurumsal Portföy

16.13 Ünlü Yatırımcı ve Kurumsal Portföy Araştırması Public holding / filing research (kurum veya yatırımcının açıklanmış raporlarından belirli tarihteki pozisyonları inceleme), canlı emir akışı değildir. Bir aracın “şu anda tutuyor” etiketi; çoğu zaman son açıklanmış rapor dönemini veya veri sağlayıcının işlediği kaydı temsil eder. Rapor tarihi ile bugünkü pozisyon aynı şey değildir.

**Konular:** fundamental_derivatives, hedge_arbitrage, portfolio_correlation, automation_ai, liquidity_imbalance

**Kart:** `ATK-TR-D1.0-2026-08.p0345`

### PDF s. 346 — 16.14 — Fair Value, Hazır AI Stratejileri ve Model

16.14 Fair Value, Hazır AI Stratejileri ve Model Riski Fair value estimate (belirli finansal veri, model ve varsayımlarla hesaplanan tahmini değer), gözlemlenen piyasa fiyatından farklı bir model çıktısıdır. Hazır AI stratejisi de seçtiği evren, yeniden dengeleme, veri ve hedef fonksiyonuna bağlı bir model ürünüdür. İkisi de yöntem açıklaması olmadan karar kanıtı sayılamaz.

**Konular:** automation_ai, relative_cross_market, risk_management, fundamental_derivatives, fundamental_valuation

**Kart:** `ATK-TR-D1.0-2026-08.p0346`

### PDF s. 347 — 16.15 — Tam AI–Pine–Araştırma İş Akışı

DOĞRU BİLİNEN YANLIŞ Mit: Birden fazla modelin ortalaması “gerçek fair value”yu verir. Gerçeklik: Model çeşitliliği yararlı olabilir; fakat ortak yanlış varsayım, veri hatası ve rejim değişimi ortalamada kaybolmaz. Uygulama Görseli 16.6 – Bir fair value ekranında model isimleri, tahmin aralığı, rapor dönemi, varsayımlar ve piyasa fiyatının ayrı gösterimi.

**Konular:** automation_ai, trend_regime

**Kart:** `ATK-TR-D1.0-2026-08.p0347`

### PDF s. 348 — 16.15 — Tam AI–Pine–Araştırma İş Akışı

Aşama Eylem Çıktı 7 Pine spec Artifact, inputs, state, event, output ve tests yaz. 8 Kod / debug Minimal modül, trace, compile ve semantic test. 9 Doğrulama Replay, backtest, maliyet, benchmark ve paper test.

**Konular:** automation_ai, validation_replay, strategy_design, liquidity_imbalance, market_structure

**Kart:** `ATK-TR-D1.0-2026-08.p0348`

### PDF s. 349 — 16.15 — Tam AI–Pine–Araştırma İş Akışı

Uygulama Görseli 16.7 – Bölüm 16 tam ekran serisi: araştırma sorusu kaynak tablosu prompt Pine→ → → spec kod diff replay/backtest paper karar günlüğü. Temsilî eğitim şeması.→ → → → Hızlı Başvuru Sorun İlk kontrol Varsayılan eylem AI kesin sinyal veriyor Veri, TF, karşı senaryo Koşullu rapor iste; emir verme. Kod derleniyor ama sinyal erken Bar close, MTF, pivot/lookahead Replay + debug trace.

**Konular:** automation_ai, validation_replay, multi_timeframe, geometry_tools, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0349`

### PDF s. 350 — 16.15 — Tam AI–Pine–Araştırma İş Akışı

 Backtestte maliyet, benchmark, drawdown, örneklem, rejim ve out-of-sample kontrol edildi.  Screening ve değerleme çıktısında kaynak, timestamp, rapor dönemi ve model açık.  Kurumsal holding verisi canlı portföy gibi yorumlanmadı.

**Konular:** automation_ai, risk_management, validation_replay, trend_regime, fundamental_valuation

**Kart:** `ATK-TR-D1.0-2026-08.p0350`

### PDF s. 351 — 16.15 — Tam AI–Pine–Araştırma İş Akışı

Yetki arttıkça hangi güvenlik katmanları artmalıdır? Prompt görev sözleşmesinin altı parçası nedir? Context pack hangi bilgileri içermelidir?

**Konular:** automation_ai, multi_timeframe, validation_replay, geometry_tools, strategy_design

**Kart:** `ATK-TR-D1.0-2026-08.p0351`
