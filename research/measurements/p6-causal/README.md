# P6 karşı genişleme — nedensel zamanlama düzeltmesi

**Karar: tarihsel keşif; uygulanabilir avantaj doğrulanmadı.** Eski failure-barından başlayan ve sonradan karşı genişleme olup olmadığına göre ayrılan sonuç, failure anında bilinmeyen geleceği kullanıyordu. [Eski rapor](../cilt2-lifecycle/README.md) ve CSV'ler iz bırakmak için korunmuştur; eski `continue` kararı geri çekilmiştir.

## Ne değişti?

- `enrich_lifecycle`, failure satırına gelecekteki teyit pozisyonunu yazmaz. Failure sonrasında en fazla 10 barda karşı kapanış olursa, teyit **kendi kapanışında** ayrı `counter_expansion` olayı olarak yayımlanır. Teyit yokluğu ve gözlem sonu sansürü ayrı tutulur.
- 4s ve günlük BIST hisselerindeki aynı teyitli failure'lar için üç görünüm hesaplanır: **(1)** geçmişten teyit varlığıyla seçilmiş failure kapanışı (*oracle, alınıp satılabilir değildir*), **(2)** teyit kapanışı (*kapanıştan karar verip aynı kapanışta gerçekleşme varsayımı gerçekçi olmayabilir*), **(3)** teyitten sonraki kullanılabilir barın açılışı (*fiyat vekili*).
- Her satırda üç görünümün **tamamının** ufku gözlenmiş olmalıdır. Endeks farkı için üç görünümün de XU100 giriş ve bitiş etiketleri hisseyle tam eşleşmelidir; eksik eşleşme sıfır değildir. Giriş ile bitiş arası 5 veya 20 kullanılabilir hisse barıdır.
- Yön, failure sonrası tezin yönüdür: hem varsayımsal long hem short gözlemleri içerir. `−%0,25 maliyet` yalnız sabit aritmetik duyarlılıktır; açığa satış erişimi/ödünç faizi, gerçekleşme, portföy veya gerçek komisyon modeli yoktur. Aşağıdaki oranlar portföy getirisi değildir.

## 20 bar: aynı teyitli olay örneği

`Yönlü ham medyan`, fiyata göre yönü terslenen sonuçtur; `XU100-aşırı medyan` aynı etiketlerden hesaplanan yönlü farktır. Yüzdeler yüzde puan cinsindedir.

| Periyot / tarihsel test | Yöntem | Tam çift olay | Yönlü ham medyan | XU100-aşırı medyan | Varsayımsal %0,25 maliyetten sonra ham medyan |
|---|---|---:|---:|---:|---:|
| 4s | Failure kapanışı, **gelecekle seçilmiş** | 851 | -%0,17 | +%0,58 | -%0,42 |
| 4s | Teyit kapanışı | 851 | -%1,62 | +%0,39 | -%1,87 |
| 4s | **Teyit sonrası sonraki açılış** | 851 | **-%1,69** | **+%0,22** | **-%1,94** |
| Günlük | Failure kapanışı, **gelecekle seçilmiş** | 327 | -%0,44 | +%2,74 | -%0,69 |
| Günlük | Teyit kapanışı | 327 | -%3,44 | +%0,53 | -%3,69 |
| Günlük | **Teyit sonrası sonraki açılış** | 327 | **-%3,60** | **+%0,86** | **-%3,85** |

4s testte 5 barlık tam 995 olayın XU100-aşırı medyanı oracle görünümünde +%0,89, teyit sonrası açılışta -%0,06'dır. Yöntemlerin giriş **ve bitiş tarihleri farklıdır**; bu tablo, geleceği bilerek seçimin neyi abartabildiğini gösteren betimsel karşılaştırmadır, izole giriş etkisi veya nedensel kâr farkı değildir. Aynı hisseye ve haftaya ait çoklu örtüşen olaylar bağımsız değildir.

## Kapsam, sansür ve hizalama

- İç arşivde 100 hisse × 2 periyot, toplam **9.101** failure: **7.028** teyitli, **1.792** 10 bar boyunca teyitsiz, **281** veri/dönem sınırında sansürlü. 4s tarihsel testte 1.279 failure'ın 1.025'i teyitli, 212'si teyitsiz, 42'si sansürlüdür; bu 1.025'in 851'i üç yöntemde de 20 bar sonuçludur.
- Günlük tarihsel testte 699 failure'ın 508'i teyitli, 151'i teyitsiz, 40'ı sansürlü; 327 teyit üç yöntemde 20 bar sonuçludur.
- Tarihsel günlük **train** örneğinde, 20 bar için failure kapanışından eski bağımsız endeks `shift(-20)` bitişi karşılaştırılabilen 1.193 olayın **87'sinde** hisse bitiş tarihinden farklıydı. Bu örnek, bütün pencerelerin genel oranı değildir. Yeni sonuç yalnız gerçek başlangıç ve bitiş etiketlerinde eşler.
- Bu çalışma, önceki tablolarla aynı rakamları üretmeyi hedeflemez: sabit takvim bölümleri, sağdaki eşit swing ucu, tam ortak örnek ve düzeltilmiş endeks hizalaması kullanır. Eski rapordaki `%0,07 / %1,51 / %1,91` değerlerine doğrudan eşdeğer değildir.

## Üretim ve denetim

```bash
python -m tools.measure_p6_causal --root data/ohlcv --output research/measurements/p6-causal
python -m tools.audit_p6_causal --root data/ohlcv --output research/measurements/p6-causal
```

Girdi fiyatları Git'te tutulmadığından özgün `data/ohlcv` ve `input_manifest.csv` hash eşleşmeleri gerekir. `failure_status.csv` tüm failure durumlarını; `paired_events.csv` üç yöntemin olay/ufuk kayıtlarını; `status_summary.csv` ve `paired_summary.csv` özetleri; `run_metadata.json` kod ve sürüm hash'lerini içerir. `AUDIT.json`, 202 girdi hash'ini ve örneklenen 200 olay-ufuk satırındaki 560 yöntem/fiyat aritmetiğini doğruladı; bu bağımsız fiyat sağlayıcısı doğrulaması değildir.

Tam eski evrenin yeni biçimli ayrıntı tablosu ayrıca `python -m tools.measure_cilt2_lifecycle` ile üretilebilir; artık `cilt2-lifecycle-causal-full/` klasörüne yazar ve tarihsel arşivi ezmez. Bu ağır tam evren çalışması bu rapordaki dar BIST 4s/günlük karşılaştırmanın yerine çalıştırılmamıştır.
