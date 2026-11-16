# Cilt 2 P6 — Kırılım Yaşam Döngüsü Ayrıntıları

## Kapsam

556.255 yaşam döngüsü olayı, 125 varlık ve dört periyot. 50.566 failure sonrası karşı genişleme tespit edildi. Olaylara seviye kimliği, deneme sayısı, dışarıda kalma süresi, retest yaklaşma hızı, geri alma oranı, eski alana giriş derinliği ve karşı genişleme zamanı eklendi.

## Parametre dayanıklılığı

BIST 4h üzerinde baseline yanında tolerans 0,05/0,20 ATR, acceptance 1/3 kapanış, follow-through 1/5 bar, failure 5/20 bar ve seviye ömrü 50/150 test edildi. Bütün çıplak olayları/yönleri havuzlayan 60-bar benchmark-aşırı medyanlar çoğunlukla -%0,6 ile +%0,2 arasında ve pozitif oranlar %48–51 çevresindedir. Tek parametre değişimi genel bir avantaj yaratmadı.

## Failure sonrası karşı genişleme

4h BIST failure olaylarında karşı genişleme olan grup üç zaman bölümünde pozitif medyan taşıdı: eğitim yaklaşık `%0,07`, doğrulama `%1,51`, test `%1,91`. Testte 573 hazır alt-grup gözlemi; karşı genişleme olmayan grup testte `-%3,88` ve belirgin zayıf. Çok boyutlu tablodaki alt gruplar nedeniyle bu sayılar doğrudan bağımsız işlem sayısı değildir, ancak işaret ayrımı güçlüdür.

## Karar

- Çıplak close-break/acceptance/retest/failure: parametre komşuluğunda `chance_like/context_required`.
- Failure sonrası karşı genişleme: `continue`, tam olay tekilleştirmesi ve maliyet testi gerekli.
- Deneme sayısı, dışarıda kalma ve retest kalitesi: ayrıntılı tabloda korunur; tek bir evrensel eşik henüz seçilmez.

## Dosyalar

- `detailed_event_study.csv`: bütün ayrıntı bantları ve zaman sonuçları
- `parameter_study.csv`: önceden kayıtlı 11 tek-faktör varyant
- `summary.json`: kapsam
