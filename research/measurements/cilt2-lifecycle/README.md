# Cilt 2 P6 — Kırılım Yaşam Döngüsü Ayrıntıları

> **Tarihsel arşiv — işlem sinyali olarak geçersiz:** Aşağıdaki karşı genişleme grubu, failure kapanışında henüz bilinmeyen sonraki 10 bardaki olaya göre seçilmiştir. Ayrıca günlük XU100 bazı olaylarda hisseyle farklı bitiş etiketine hizalanmıştır. Bu nedenle aşağıdaki `%0,07 / %1,51 / %1,91` ve `continue` kararı uygulanabilir veya bağımsız performans kanıtı **değildir**. Eski sayılar denetim izi olarak korunmuştur. Düzeltilmiş ölçüm: [`../p6-causal/`](../p6-causal/). Kod artık karşı genişlemeyi ayrı ve teyit kapanışında yayımlar; `tools.measure_cilt2_lifecycle` tarihsel CSV'leri ezmez.

## Kapsam

556.255 yaşam döngüsü olayı, 125 varlık ve dört periyot. 50.566 failure sonrası karşı genişleme tespit edildi. Olaylara seviye kimliği, deneme sayısı, dışarıda kalma süresi, retest yaklaşma hızı, geri alma oranı, eski alana giriş derinliği ve karşı genişleme zamanı eklendi.

## Parametre dayanıklılığı

BIST 4h üzerinde baseline yanında tolerans 0,05/0,20 ATR, acceptance 1/3 kapanış, follow-through 1/5 bar, failure 5/20 bar ve seviye ömrü 50/150 test edildi. Bütün çıplak olayları/yönleri havuzlayan 60-bar benchmark-aşırı medyanlar çoğunlukla -%0,6 ile +%0,2 arasında ve pozitif oranlar %48–51 çevresindedir. Tek parametre değişimi genel bir avantaj yaratmadı.

## Failure sonrası karşı genişleme

Eski, **gelecekle seçilmiş** 4h BIST failure alt grubunun medyanları eğitim/doğrulama/test için yaklaşık `%0,07 / %1,51 / %1,91`; testte 573 hazır alt-grup gözlemi ve seçilmeyenlerde `-%3,88` idi. Bu sayılar denetim izi olarak bırakılmıştır; failure anında bilinebilir bir ayrım veya bağımsız işlem sonucu değildir.

## Karar

- Çıplak close-break/acceptance/retest/failure: parametre komşuluğunda `chance_like/context_required`.
- Failure sonrası karşı genişleme: eski `continue` kararı **geri çekildi**; yalnız teyit sonrası, nedensel ve maliyetli yeni ölçüm değerlendirilebilir.
- Deneme sayısı, dışarıda kalma ve retest kalitesi: ayrıntılı tabloda korunur; tek bir evrensel eşik henüz seçilmez.

## Dosyalar

- `detailed_event_study.csv`: bütün ayrıntı bantları ve zaman sonuçları
- `parameter_study.csv`: önceden kayıtlı 11 tek-faktör varyant
- `summary.json`: kapsam
