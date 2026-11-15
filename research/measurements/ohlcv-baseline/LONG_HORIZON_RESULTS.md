# Uzun Ufuk ve Zaman-Dışı Doğrulama Sonuçları

## Yönetici özeti

Mevcut arşiv yaklaşık bir yıllık veri içerdiği için çok yıllı “uzun dönem” sonucu üretmek dürüstçe mümkün değildir. Bu turda yapılabilecek en sağlam kontrol uygulanmıştır:

- Her sembol/periyot olayları kronolojik olarak ilk `%60` eğitim, sonraki `%20` doğrulama, son `%20` test olarak ayrıldı.
- BIST hisselerinin getirisi aynı zaman ve ufuktaki XU100 getirisinden arındırıldı.
- Ham yönlü getiri yerine **yön düzeltilmiş endeks-aşırı getiri** esas alındı.
- Eksik ileri ufuklar kazanma oranında kayıp sayılmadı; yalnız sonucu gerçekten mevcut olaylar kullanıldı.
- 20, 40 ve 60 bar ufukları ölçüldü.

En düzenli aday, **4 saatlik seride aşağı yönlü kırılımın kabul/takip davranışı ve 60 barlık sonuç** oldu. Ancak bu hâlâ işlem maliyeti ve kurumsal işlem temizliği uygulanmamış bir olay çalışmasıdır.

## Neden önceki ham sonuç yeterli değildi?

Son test bölümünde piyasa genel olarak aşağı yönlüydü. Bu nedenle aşağı hipotezlerinin ham kazanma oranı çok yüksek, yukarı hipotezlerinin çok düşük görünüyordu. XU100 etkisi çıkarılınca farkların büyük bölümü kayboldu. Bu, çıplak getiri ile strateji avantajının aynı şey olmadığını gösterir.

Örnek — BIST hisseleri 4h, test bölümü, 20 bar:

| Olay | Hipotez | Ham medyan | Ham pozitif | XU100-aşırı medyan | Aşırı pozitif |
|---|---|---:|---:|---:|---:|
| Close break | aşağı | %3,12 | %64,16 | **-%0,87** | %44,87 |
| Acceptance | aşağı | %2,81 | %63,82 | **-%0,77** | %44,52 |
| Retest hold | aşağı | %3,83 | %69,22 | **-%0,25** | %47,83 |
| Failure | yukarı | -%4,05 | %25,94 | **%0,67** | %54,84 |

Ham sonuç “aşağı kırılım güçlü” derken benchmark sonrası 20 bar avantajı kalmamaktadır. Dolayısıyla önceki ham tablo tek başına strateji seçmek için kullanılmamalıdır.

## En düzenli aday — 4h aşağı acceptance, 60 bar

60 adet tamamlanmış 4h bar BIST seans yapısında yaklaşık birkaç hafta ile bir ay arası piyasa süresine karşılık gelir; kesin takvim süresi tatil ve eksik barlara göre değişir.

| Zaman bölümü | Geçerli olay | XU100-aşırı medyan | Aşırı pozitif oran |
|---|---:|---:|---:|
| Eğitim `%60` | 2.264 | **%2,83** | **%59,72** |
| Doğrulama `%20` | 853 | **%0,63** | **%50,88** |
| Test `%20` | 582 | **%1,40** | **%54,64** |

Üç bölümde de medyan pozitif kalmıştır. Eğitimden doğrulamaya düşüş büyüktür; bu nedenle beklenen avantaj eğitim sonucu olan `%2,83` değil, doğrulama/testte görülen yaklaşık `%0,6–1,4` brüt aralığı olarak ele alınmalıdır.

### Yakın kopya: follow-through

4h aşağı follow-through, acceptance ile neredeyse aynı olayları taşımaktadır:

| Zaman bölümü | Geçerli olay | XU100-aşırı medyan | Aşırı pozitif oran |
|---|---:|---:|---:|
| Eğitim | 2.270 | %2,82 | %59,65 |
| Doğrulama | 852 | %0,63 | %50,94 |
| Test | 574 | %1,40 | %54,70 |

Bu iki satır iki bağımsız avantaj sayılmamalıdır. Mevcut tanımla follow-through ve acceptance güçlü biçimde bilgi tekrarı yapmaktadır.

## Daha zayıf ama izlenebilir aday — 4h aşağı close break, 60 bar

| Zaman bölümü | Geçerli olay | XU100-aşırı medyan | Aşırı pozitif oran |
|---|---:|---:|---:|
| Eğitim | 2.912 | %3,01 | %61,64 |
| Doğrulama | 1.074 | -%0,03 | %50,00 |
| Test | 677 | %0,80 | %53,91 |

Doğrulama medyanı sıfırdır. Test pozitif olsa da acceptance kadar düzenli değildir.

## Failure sonuçları

### 4h aşağı kırılım başarısız → yukarı hipotezi, 60 bar

| Zaman bölümü | Geçerli olay | XU100-aşırı medyan | Aşırı pozitif oran |
|---|---:|---:|---:|
| Eğitim | 1.770 | -%3,48 | %37,40 |
| Doğrulama | 607 | %0,69 | %51,57 |
| Test | 392 | %1,25 | %58,42 |

Son iki bölüm olumlu fakat eğitim negatiftir. Bu davranış rejim bağımlılığı veya tanım değişkenliği gösterir; sağlam genel kural olarak kabul edilmemelidir.

## Günlük 20 bar sonuçları

Günlük 20 bar yaklaşık bir işlem ayıdır.

### Aşağı acceptance

| Zaman bölümü | Geçerli olay | XU100-aşırı medyan | Aşırı pozitif oran |
|---|---:|---:|---:|
| Eğitim | 1.000 | %2,08 | %58,60 |
| Doğrulama | 451 | -%0,12 | %48,56 |
| Test | 320 | %0,68 | %51,88 |

Doğrulama negatiftir; üç dönemde düzenli avantaj yoktur.

### Aşağı close break

| Zaman bölümü | Geçerli olay | XU100-aşırı medyan | Aşırı pozitif oran |
|---|---:|---:|---:|
| Eğitim | 1.403 | %1,47 | %56,45 |
| Doğrulama | 543 | -%0,66 | %46,41 |
| Test | 401 | %0,12 | %50,62 |

Test sonucu yaklaşık sıfırdır. Günlük çıplak kırılım için sağlam avantaj tespit edilmemiştir.

### Yukarı seviye probe rejection → aşağı hipotezi

| Zaman bölümü | Geçerli olay | XU100-aşırı medyan | Aşırı pozitif oran |
|---|---:|---:|---:|
| Eğitim | 1.363 | %2,91 | %63,32 |
| Doğrulama | 479 | -%1,03 | %45,30 |
| Test | 184 | %3,20 | %58,70 |

Eğitim ve test olumlu, doğrulama negatiftir. Sonuç kararsızdır ve güvenilir genel avantaj sayılmaz.

## Günlük 60 bar neden rapor kararı için kullanılmadı?

Test bölümündeki olayların çoğunun önünde 60 günlük tamamlanmış veri yoktur. Örneğin bazı olay türlerinde yalnız 1–13 geçerli test sonucu kalmaktadır. Medyanlar büyük görünse bile örnek yetersizdir. Bu değerleri “üç aylık sağlam sonuç” diye sunmak yanıltıcı olur.

Gerçek 60 günlük out-of-sample değerlendirme için veri bitişinden sonra en az 60 yeni işlem günü veya daha uzun tarihsel veri gereklidir.

## Şu anki finansal karar

### Araştırmaya devam edilecek aday

```text
4h teyitli swing seviyesi
→ aşağı kapanış kırılımı
→ yeni alanda iki kapanış / erken follow-through
→ 60 tamamlanmış 4h bar sonuç ufku
```

Benchmark sonrası test medyanı yaklaşık `%1,40`, pozitif oranı `%54,6` civarındadır. Bu **brüt ve maliyetsiz** olay avantajıdır.

### Şimdilik reddedilmeyen ama onaylanmayanlar

- 4h aşağı close break
- 4h aşağı failure sonrası yukarı dönüş
- Günlük yukarı seviye rejection sonrası aşağı hareket

### Şimdilik avantaj göstermeyenler

- Günlük çıplak close break
- Günlük acceptance'ın bütün dönemlerde düzenli olduğu iddiası
- 4h kısa 20-bar aşağı kırılım avantajı; benchmark sonrası negatife dönmüştür
- Çıplak yukarı kırılım devamı

## Kalan riskler

1. Yaklaşık bir yıllık tarih çok yıllı piyasa döngüsünü kapsamaz.
2. Kurumsal işlem sıçramaları henüz olay penceresinden mekanik olarak çıkarılmadı.
3. İşlem maliyeti, spread ve slippage yoktur.
4. Aynı anda oluşan korelasyonlu hisseler portföyde tek piyasa yönü riski yaratabilir.
5. Acceptance ve follow-through büyük ölçüde aynı olay kümesidir.
6. Parametre hassasiyeti henüz ayrı doğrulanmadı.
7. Sonuçlar sabit ufuk getirileridir; yürütülebilir giriş/çıkış stratejisi değildir.

## Sonraki zorunlu çalışma

- Kurumsal işlem/anormal fiyat sıçraması filtresi
- Acceptance olaylarının tekilleştirilmesi
- Olay anı trend, volatilite, hareket kalitesi ve baskı kaybı snapshot'ı
- 4h 60-bar adayında sembol bazlı tutarlılık
- İşlem maliyeti stres testi
- Parametre komşuluğu: tolerans, kabul kapanışı ve seviye ömrü
- Yeni veri geldikçe sabitlenmiş test kuralının ileri doğrulaması
