# Replay-Man indirme raporu

- Durum: **completed**
- Varlık: 125
- Bu çalıştırmadaki ağ isteği: 0
- Önbellekten gelen görev: 0
- Seçili kapsamdaki görevler: {'complete': 1250}
- Tüm veritabanındaki görevler: {'complete': 1250}
- Türetilen varlık: 125
- Günlük karşılaştırma uyuşmazlığı: 28884

Dosyalar:
- `tasks.csv`: seçili varlık/seri/periyot görevleri ve yeniden deneme zamanları
- `errors.csv`: seçili kapsamdaki başarısız/hatalı görevler
- `coverage.csv`: seçili kapsamdaki varlık/seri/periyot özeti; task_rows benzersiz CSV satır sayısı değildir

Aynı komutu tekrar çalıştırmak tamamlanan görevleri atlar, bekleyen görevleri sürdürür.
