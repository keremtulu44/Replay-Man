# Cilt 1 Genel Kontrolü

Kontrol tarihi: 2026-11-14

## Üretilmiş çalışma

- 139/139 sayfa kapsamda.
- 403 atomik claim ve 403 benzersiz claim kimliği.
- 22 `BR-C1` kuralı; bütün rule ID'leri registry'de mevcut.
- Sonuç klasörü eksik kural yok.
- C1-P2–P9 arasında toplam **3.140.304** olay ölçülmüş.
- 5/20/40/60 bar ham yönlü medyan, pozitif oran ve BIST için XU100-aşırı medyan mevcut.
- Eğitim/doğrulama/test, varlık grubu, zaman dilimi ve sembol sonuçları mevcut.
- Altı bilgi ailesi için Jaccard örtüşme matrisi mevcut.
- %0/%0,10/%0,25/%0,50 maliyet stres tablosu mevcut.
- Hacim uygunluk kapısı var; Volume Profile yaklaşımı gerçek bar-içi dağılım değil typical-price yaklaşımı olarak etiketli.
- Pivot/swing/AVWAP/Pitchfork tarafında teyit zamanı kullanılıyor.

## Başarılı teknik kontroller

- Yazılım: **66 passed**.
- Bilgi tabanı: **passed** — 778 sayfa/kart, 58 bölüm, 40 tema.
- OHLCV: **passed** — 125 varlık, 500 dosya, 620.094 satır, 0 hata, 0 uyarı.
- Sayfa numaraları 1–139 tam.
- Unresolved satırı 0; boş disposition 0.
- Test edilebilir claim'de eksik rule ID 0; registry'de bulunmayan rule ID 0.
- 13 formül placeholder'ı yalnız ön madde/içindekiler `reference_only` kayıtlarında.

## Katı tamamlama planına göre bulunan açıklar

### 1. Parametre komşuluğu eksik

P12 planında zorunlu olmasına rağmen `parameter_study.csv` yok. MA, RSI/Stochastic, Bollinger/Keltner, ADX, Supertrend, Ichimoku, profil pencere/bin, regresyon penceresi ve eşik komşulukları çalıştırılmamış. Mevcut sonuçlar çoğunlukla tek varsayılan parametreye aittir.

### 2. MFE/MAE eksik

Cilt 1 event study dosyaları 5/20/40/60 bar kapanış getirilerini taşıyor; ileri maksimum olumlu/olumsuz hareket (`MFE/MAE`) taşımıyor. Planın risk ve hareket yolu denetimi bu nedenle eksik.

### 3. Ortak takvim doğrulaması eksik

Sembol içi kronolojik %60/%20/%20 var; fakat bütün sembollerde aynı takvim sınırlarını kullanan ayrı common-calendar sonuç tablosu yok.

### 4. Karar zincirinde benchmark-aşırı marjinal katkı eksik

`decision_chain.csv`, `median_symbol_return` kullanıyor. Her aşamada XU100-aşırı marjinal katkı ve bir önceki aşamaya göre net fark kaydedilmemiş. Bu nedenle P11'in “her aşamanın benchmark sonrası marjinal katkısı” şartı tam karşılanmıyor.

### 5. Bilgi ailesi denetimi yalnız olay Jaccard'ı

Aile örtüşmesi mevcut; ancak plandaki getiri korelasyonu, koşullu bilgi vekili ve tek-aracı çıkarma/ablation testi ayrı tablolar olarak yok.

### 6. Hacim kapısı P10 aile örtüşmesinde yeniden uygulanmıyor

P5/P6 ölçüm çıktılarında hacim kapısı uygulanmış olsa da P10 aile boolean'ları bütün gruplarda yeniden üretiliyor. Endeks/FX volume/profile olaylarının aile-overlap hesabından dışlanması gerekir.

### 7. Volume Profile komşuluğu eksik

Yalnız 60 bar ve 20 fiyat-bin yaklaşımı ölçülmüş. Planda belirtilen pencere/bin hassasiyeti ve komşuluk sonuçları yok.

## Sonuç

Cilt 1 için geniş ve yeniden üretilebilir bir ilk deney katmanı kurulmuş; sayfa/claim/kural kapsamı, 3,14 milyon olay, zaman ayrımı, sembol tabloları ve temel maliyet/örtüşme kontrolleri mevcut. Ancak C1-P10–P12'nin katı kabul ölçütleri tam karşılanmadığı için mevcut `passed/completed` etiketi erken verilmiştir.

Nihai kapanıştan önce parametre komşuluğu, MFE/MAE, ortak takvim, benchmark-aşırı karar zinciri, ablation/korelasyon ve hacim-kapılı overlap tamamlanmalıdır. Bu açıklar giderilene kadar denetim durumu `conditional_gap_found` olarak değerlendirilir.
