# OHLCV Replay Ölçüm Arşivi

125 varlık, 500 seri ve 558.121 tamamlanmış barda çalışan nedensel replay ölçümleri.

## Dosyalar

- `summary.json`: Kapsam ve olay sayıları
- `series_inventory.csv`: Seri bazında ölçüm envanteri
- `structure_event_study.csv`: Havuzlanmış 5/20/40/60 bar sonuçları
- `structure_symbol_results.csv`: Sembol bazlı tutarlılık sonuçları
- `structure_time_split_study.csv`: Kronolojik `%60/%20/%20` eğitim/doğrulama/test sonuçları ve XU100-aşırı getiriler
- `FINANCIAL_RESULTS.md`: İlk kısa ufuk finansal raporu
- `LONG_HORIZON_RESULTS.md`: Uzun ufuk, benchmark ve zaman-dışı doğrulama raporu

## Kritik sözleşme

Pivot ancak teyit barında bilinir; seviye teyitten sonraki barda aktiftir. İleri sonuç özellik girdisi değildir. BIST hisse avantajı değerlendirilirken aynı ufuktaki XU100 getirisi çıkarılır. Eksik ileri ufuklar kazanma oranında başarısız sayılmaz, hesaplamadan çıkarılır.

Yaklaşık bir yıllık veri çok yıllı uzun dönem kanıtı değildir. En uzun günlük test ufuklarında yeterli gelecek barı olmayan olaylar ayrıca sayılır ve karar için kullanılmaz.
