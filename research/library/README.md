# Replay-Man Araştırma Kütüphanesi

Bu dizin, Replay-Man araştırma/replay motorunun kavramsal kaynaklarını sürümlü ve doğrulanabilir biçimde saklar.

## Düzen

- `books/`: Değiştirilmeden saklanan kaynak PDF'ler.
- `catalog.json`: Kimlik, sürüm, sayfa sayısı, proje rolü ve SHA-256 özeti.
- `../specs/concept-map.md`: Kitap kavramlarının yazılım modüllerine dönüşüm haritası.
- `../specs/research-process.md`: Bir fikrin hipotezden geniş sembol doğrulamasına giden süreci.

## Kaynakların rolleri

1. **Ana Trading Kitabı:** Genel süreç ve karar mimarisi. Özellikle strateji kartı, backtest/replay, fikirden objektif kurala geçiş ve performans iddialarının denetimi.
2. **Cilt 1:** İndikatörleri bilgi ailelerine ayırma; aynı bilgiyi tekrar eden araçları bağımsız teyit saymama; bağlam, konum, tetik ve risk görevlerini ayırma.
3. **Cilt 2:** OHLC'den ölçülebilir fiyat davranışı özellikleri üretme; mum gücü, örtüşme, hareket verimliliği, swing hızı, ikinci deneme, kırılım kabulü ve pullback kalitesi.

## Değişiklik politikası

- Kaynak PDF dosyaları yerinde düzenlenmez.
- Yeni baskı/sürüm ayrı dosya ve ayrı katalog kaydı olarak eklenir.
- Yazılım gereksinimleri PDF içine yazılmaz; `research/specs/` altında sürümlenir.
- Bir kavramın kitaptaki anlatımı ile uygulamadaki matematiksel tanımı ayrı tutulur.
- Her uygulama tanımı kaynak kitap/bölüm referansı, sürüm ve test amacı taşımalıdır.

## OB/FVG notu

Kullanıcının mevcut OB/FVG sistematiği daha sonra teslim edilecektir. Şimdilik yeniden yazılmaz veya tahmin edilmez. Geldiğinde mevcut tanımlar korunarak ortak olay/deney arayüzüne adaptörle bağlanacaktır.
