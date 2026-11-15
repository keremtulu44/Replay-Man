# PTA-C1-2026 — Bölüm 11

**PDF sayfaları:** 66–73
**Sayfa kartları:** 8

## Alt başlıklar

- 11.1 — POC ve değer alanı: hacim nerede yoğunlaştı?
- 11.3 — Üç farklı profil türü: VRVP, FRVP ve AVP
- 11.4 — Profili yalnız seviyelerle değil, bütün dağılım şekliyle okuyun
- 11.6 — Profil renkleri gerçek alıcı/satıcı emir akışını göstermez
- 11.8 — Değer alanının taşınması, örtüşmesi ve yeni bölgede kalıcılık
- 11.9 — AVWAP ile Anchored Volume Profile arasındaki fark
- 11.10 — Volume Profile için pratik karar akışı

## Konu dağılımı

- `volume_flow`: 8 sayfa
- `risk_management`: 4 sayfa
- `trend_regime`: 4 sayfa
- `breakout_failure`: 3 sayfa
- `support_resistance`: 2 sayfa
- `multi_timeframe`: 2 sayfa
- `volatility`: 2 sayfa
- `validation_replay`: 1 sayfa
- `candle_behavior`: 1 sayfa
- `movement_quality`: 1 sayfa

## Sayfa şeritleri

### PDF s. 66 — 11.1 — POC ve değer alanı: hacim nerede yoğunlaştı?

BÖLÜM 11 Volume Profile: Hacim Hangi Fiyatlarda Yoğunlaştı? Klasik hacim “ne zaman ne kadar aktivite vardı?” diye sorar. Volume Profile ise seçili aralıktaki hacmi fiyat seviyelerine dağıtarak “aktivite hangi fiyatlarda yoğunlaştı?” sorusunu cevaplar.

**Konular:** volume_flow, support_resistance, risk_management

**Kart:** `PTA-C1-2026.p0066`

### PDF s. 67 — 11.3 — Üç farklı profil türü: VRVP, FRVP ve AVP

POC en yüksek hacimli satırdır; VAH/VAL seçilen Value Area’nın sınırlarıdır. HVN/LVN yüksek ve düşük hacimli bölgeler olarak bağlama göre okunabilir. Sık kullanılan %70 Value Area ayarı, seçili profil hacminin yaklaşık %70’ini kapsayan bölgeyi hedefler.

**Konular:** volume_flow, trend_regime, risk_management

**Kart:** `PTA-C1-2026.p0067`

### PDF s. 68 — 11.4 — Profili yalnız seviyelerle değil, bütün dağılım şekliyle okuyun

Araç Analiz edilen aralık Ana risk AVP — Anchored Volume Profile Seçilmiş başlangıç noktasından ileri doğru Başlangıç noktası seçiminde sonradan bakarak seçme Visible Range Volume Profile (VRVP) yalnız ekranda görünen geçmişi hesaplar. Yakınlaştırma veya kaydırma aralığı değiştirirse profil de değişebilir; bu nedenle görünür pencere analiz girdisinin bir parçasıdır. VRVP’de ekran görünümü analiz girdisidir.

**Konular:** volume_flow, trend_regime, risk_management

**Kart:** `PTA-C1-2026.p0068`

### PDF s. 69 — 11.6 — Profil renkleri gerçek alıcı/satıcı emir akışını göstermez

Profil şekli Hacmin ağırlığı Genel yorum Tek başına söylemez b biçimli Alt bölgede Hacim daha düşük fiyatlarda yoğunlaşıyor Otomatik SAT İnce Profil Belirgin bir merkez oluşmamış Yönlü hareket sırasında orta bölgede daha az oyalanma görülebilir Hareketin yönü 11.5 — FRVP aralığını nasıl seçmeli? Fixed Range Volume Profile (FRVP) analiz aralığını kullanıcıya bırakır. Bu esneklik geçmişe uydurma riski yaratır; yatay sıkışma, belirgin hareket veya önemli olay gibi önceden açıklanabilen bir aralık seçme kuralı kullanın.

**Konular:** volume_flow, breakout_failure, multi_timeframe, trend_regime, validation_replay

**Kart:** `PTA-C1-2026.p0069`

### PDF s. 70 — 11.8 — Değer alanının taşınması, örtüşmesi ve yeni bölgede kalıcılık

TEKNİK DÜZELTME Standart profil renk sınıflamasında hacim, alt zaman dilimi barının açılış-kapanış yönüne göre gruplandırılabilir. Bu veri gerçek piyasa emri tarafını göstermez; “alıcılar şu kadar agresifti” sonucu çıkarılamaz. 11.7 — POC bir mıknatıs veya duvar değildir POC, seçilen aralıkta en fazla hacmin toplandığı fiyat satırıdır.

**Konular:** volume_flow, multi_timeframe, support_resistance

**Kart:** `PTA-C1-2026.p0070`

### PDF s. 71 — 11.9 — AVWAP ile Anchored Volume Profile arasındaki fark

Fiyat yönü ile Value Area’nın yönü ayrıca karşılaştırılabilir. Fiyat yeni düşükler üretirken Value Area da aşağı kayıyorsa hacmin yoğunlaştığı bölge de aşağı taşınıyordur. Fiyat hareket ederken Value Area veya POC aynı ölçüde taşınmıyorsa “fiyat nereye gitti?” ile “hacim nerede yoğunlaştı?” soruları farklı cevaplar verebilir.

**Konular:** volume_flow, candle_behavior, movement_quality, trend_regime

**Kart:** `PTA-C1-2026.p0071`

### PDF s. 72 — 11.10 — Volume Profile için pratik karar akışı

Araç Çıktı Soru AVWAP Tek hacim ağırlıklı ortalama çizgisi “Seçtiğim başlangıçtan beri hacim ağırlıklı ortalama fiyat nerede?” AVP Fiyat seviyelerine yatay hacim dağılımı “Seçtiğim başlangıçtan beri hacim hangi fiyatlarda toplandı?” NEDEN İKİSİ BİRLİKTE KULLANILABİLİR? AVWAP, seçilen başlangıçtan sonraki hacim ağırlıklı ortalama fiyatı gösterir. AVP ise hacmin hangi fiyat seviyelerinde toplandığını gösterir.

**Konular:** volume_flow, risk_management, breakout_failure, volatility

**Kart:** `PTA-C1-2026.p0072`

### PDF s. 73 — 11.10 — Volume Profile için pratik karar akışı

ARA ÖZET — Hacim, VWAP ve Volume Profile: aynı veriden üç farklı soru Araç Ana soru Doğal rol En iyi tamamlayıcı Hacim “Ne zaman ne kadar aktivite vardı?” Katılım Fiyat yapısı / kırılım VWAP / AVWAP “Hacim ağırlıklı ortalama fiyat nerede?” Konum / ortalama maliyet Fiyat yapısı / hareket gücü / ATR Volume Profile “Hacim hangi fiyatlarda toplandı?” Konum / kabul haritası Fiyat yapısı / AVWAP / hareket gücü ÖRNEK KARAR ZİNCİRİ Fiyat yapısı yükseliş yönlü → fiyat belirgin bir dipten başlatılmış AVWAP çevresine geri çekiliyor → aynı bölgede anlamlı bir Volume Profile düğümü var → hareket gücü yeniden artıyor → giriş işareti oluşuyor → ATR yapısal stopa gerektiğinde ek pay bırakmaya yardım ediyor. Her araç farklı bir soruya cevap verir; “beş teyit” diye sayılmaz.

**Konular:** volume_flow, volatility, breakout_failure

**Kart:** `PTA-C1-2026.p0073`
