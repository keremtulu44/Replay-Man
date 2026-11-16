# Cilt 1 Nihai Genel Kabul Denetimi

Kontrol tarihi: 2026-11-14

Nihai durum: **PASSED**

## Kapsam

- 139/139 sayfa.
- 403 benzersiz atomik claim.
- 22 kaynak bağlantılı BR-C1 kuralı.
- Test edilebilir claim'de eksik veya geçersiz rule ID: 0.
- Unresolved: 0; boş disposition: 0.
- P2–P9 temel olayları: 3.140.304.

## Önceki yedi açığın kapanışı

1. **Parametre komşuluğu:** 106 varyant; EMA, RSI, Bollinger, ADX, Supertrend, Ichimoku, Gann ve profil komşulukları kaydedildi.
2. **MFE/MAE:** 5/20/40/60 bar için ortak takvimli sonuçlar üretildi.
3. **Ortak takvim:** bütün sembollerde aynı UTC sınırları 2026-06-24 ve 2026-09-03.
4. **Benchmark karar zinciri:** BIST için XU100-aşırı medyan ve aşama bazlı `marginal_excess` kaydedildi.
5. **Ablation/korelasyon:** altı aile için çıkarma testi ve phi sinyal korelasyonu üretildi.
6. **Hacim kapısı:** endeks/FX volume ailesi overlap, zincir ve ablation hesabında false yapıldı.
7. **Volume Profile hassasiyeti:** 40/60/120 bar, 12/20/30 bin, %68/%70/%75 value area varyantları ölçüldü.

## Sağlamlık bulguları

4h BIST'te eksiksiz 98 parametre komşuluğunun yalnız 7'si üç zaman bölümünde aynı işareti korudu. Birden fazla aşağı Gann eğim komşusu pozitif; RSI21 düşük bölge yukarı dönüş komşusu negatiftir. Bu sonuçlar aile düzeyi aday/negatif kararları destekler, tek en iyi parametre seçimine izin vermez.

Benchmark-aşırı karar zincirinde momentum test medyanını düşürürken yapı son aşamada artırdı; eğitim ve doğrulama zinciri yine negatiftir. Tam aile kesişimi ablation sonucunda 4h BIST genel medyanı negatiftir. Çoklu teyit otomatik avantaj değildir.

## Teknik denetimler

- Yazılım testleri: başarılı.
- Bilgi tabanı: 3 kaynak, 778 kart, 58 bölüm, 40 tema, hata yok.
- OHLCV: 125 varlık, 500 dosya, 620.094 satır, hata/uyarı yok.
- `git diff --check`: başarılı.

Cilt 1, kaynak–claim–formül–kural izlenebilirliği, nedensel ölçüm, parametre komşuluğu, ortak takvim, MFE/MAE, sembol/benchmark, bilgi tekrarı, ablation ve maliyet koşullarına göre tamamlanmıştır.
