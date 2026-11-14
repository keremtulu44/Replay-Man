# Replay-Man — İlk Sembol Havuzu

**Durum:** Veri çekme sistemi eklendi (`run.py`); canlı Yahoo indirme testi henüz yapılmadı. Bu dosya sembol/varlık kataloğudur.
**Hazırlanma tarihi:** 14 Kasım 2026
**BIST 100 üyelik tarihi:** 13 Kasım 2026 ikincil kaynak listesi; resmî dönemsel üyelik doğrulaması değildir. [2](https://yatirimci.ai/endeksler/xu100)

## Kapsam

| Grup | Adet | Not |
|---|---:|---|
| BIST 100 hisseleri | 100 | Yahoo eşlemeleri `.IS` adayı; canlı API testi yapılmadı |
| BIST endeksleri | 10 | XU100, XU030, XUTUM, XBANK, XUSIN, XUMAL, XUHIZ, XHOLD, XULAS, XUTEK |
| Küresel endeks / gösterge | 6 | S&P 500, Nasdaq, Dow, VIX, DAX, DXY |
| Döviz | 2 | USD/TRY, EUR/TRY |
| Maden vadeli | 5 | Altın, gümüş, bakır, platin, paladyum |
| Petrol vadeli | 2 | Brent, WTI |
| **Toplam** | **125** | |

Makine-okunur liste: `data/universe.csv`
BIST 100 kaynak anlık listesi: `data/reference/bist100_snapshot_2026-11-13.csv`

## Yahoo ekleri: hepsine aynı ek takılmayacak

| Tür | Örnek | Kural / istisna |
|---|---|---|
| BIST hisse | `THYAO → THYAO.IS` | Genellikle `.IS`; canlı veri uygunluğu ayrıca test edilecek. [1](https://finance.yahoo.com/quote/THYAO?p=THYAO) |
| BIST endeks | `XU100 → XU100.IS` | BIST endekslerinde de `.IS` görülür; `^XU100` varsayılmadı. [2](https://sg.finance.yahoo.com/quote/XU100.IS/options/?p=XU100.IS) |
| Döviz | `USD/TRY → TRY=X` | `USDTRY=X` diye otomatik üretilmedi. [1](https://finance.yahoo.com/quote/TRY=X/) |
| Vadeli emtia | `Altın → GC=F`, `Brent → BZ=F` | `=F` vadeli seri; spot/gram ile karıştırılmayacak. [1](https://finance.yahoo.com/quote/GC=F/news/) [1](https://finance.yahoo.com/quote/BZ=F/news/) |
| Küresel endeks | `S&P 500 → ^GSPC` | Bazı endekslerde `^` öne gelir. [1](https://finance.yahoo.com/quote/%5EDJUSSC/chart/) |
| Dolar endeksi | `DXY → DX-Y.NYB` | Ne `DXY=X` ne `^DXY`; ayrı sembol. [1](https://nz.finance.yahoo.com/quote/DX-Y.NYB/) |

## BIST 100 hisseleri

Aşağıdaki kodlar `data/universe.csv` içinde adları ve kaynak tarihiyle birlikte yer alır. Yahoo karşılıkları şimdilik `KOD.IS` adayıdır.

```text
ASELS, TUPRS, BIMAS, THYAO, AKBNK, YKBNK, KCHOL, EREGL, ISCTR, SAHOL,
GARAN, TCELL, ASTOR, ENKAI, CCOLA, TAVHL, SISE, FROTO, MGROS, MPARK,
SASA, EKGYO, TRALT, PGSUS, AEFES, TOASO, ENERY, ENJSA, HALKB, KRDMD,
TTKOM, GLYHO, MAVI, GUBRF, PETKM, VAKBN, AGHOL, TRMET, AKSEN, OYAKC,
BRSAN, AHGAZ, DOHOL, ANSGR, TURSG, ALARK, TABGD, RGYAS, TKFEN, AYGAZ,
CIMSA, RYSAS, AKSA, SOKM, CVKMD, ULKER, ISMEN, TSKB, TRGYO, DOAS,
OTKAR, GLRMK, TTRAK, ARCLK, ALBRK, ISDMR, HEKTS, TRENJ, CANTE, CWENE,
TCKRC, ANHYT, ECILC, BTCIM, SNGYO, GRSEL, EGEEN, AKFYE, ODAS, TUKAS,
KCAER, BRYAT, BERA, FENER, ALTNY, ENTRA, LMKDC, EGGUB, PAHOL, GWIND,
ECZYT, OBAMS, KARSN, ZOREN, KORDS, EUREN, AKCNS, VESTL, BINHO, KATMR
```

## Endeksler, döviz, maden ve petrol

| Grup | Yerel ad | Yahoo sembolü | Not |
|---|---|---|---|
| BIST endeks | BIST 100 | `XU100.IS` | Ana kıyas endeksi |
| BIST endeks | BIST 30 | `XU030.IS` | |
| BIST endeks | BIST Tüm | `XUTUM.IS` | |
| BIST endeks | BIST Banka | `XBANK.IS` | |
| BIST endeks | BIST Sınai | `XUSIN.IS` | |
| BIST endeks | BIST Mali | `XUMAL.IS` | |
| BIST endeks | BIST Hizmetler | `XUHIZ.IS` | |
| BIST endeks | BIST Holding ve Yatırım | `XHOLD.IS` | |
| BIST endeks | BIST Ulaştırma | `XULAS.IS` | |
| BIST endeks | BIST Teknoloji | `XUTEK.IS` | |
| Küresel endeks | S&P 500 | `^GSPC` | |
| Küresel endeks | Nasdaq Composite | `^IXIC` | |
| Küresel endeks | Dow Jones | `^DJI` | |
| Küresel gösterge | VIX | `^VIX` | Volatilite endeksi |
| Küresel endeks | DAX | `^GDAXI` | |
| Küresel gösterge | Dolar Endeksi | `DX-Y.NYB` | DXY |
| Döviz | USD/TRY | `TRY=X` | 1 USD kaç TRY |
| Döviz | EUR/TRY | `EURTRY=X` | 1 EUR kaç TRY |
| Maden vadeli | Altın | `GC=F` | Spot/gram altın değil |
| Maden vadeli | Gümüş | `SI=F` | |
| Maden vadeli | Bakır | `HG=F` | |
| Maden vadeli | Platin | `PL=F` | |
| Maden vadeli | Paladyum | `PA=F` | |
| Petrol vadeli | Brent | `BZ=F` | |
| Petrol vadeli | WTI | `CL=F` | |

## Doğrulama durumu

- `symbol_evidence=candidate_suffix`: BIST 100 hisseleri için `.IS` eşlemesi adaydır; Yahoo geçmiş veri testi henüz yapılmadı.
- `symbol_evidence=quote_page_seen`: Endeks/döviz/emtia sembolleri Yahoo sayfalarında görüldü; bu, bir yıllık saatlik verinin hazır olduğu anlamına gelmez.
- `history_check=not_tested`: Hiçbir sembol için saatlik/günlük indirme testi yapılmadı.
- Vadeli emtialarda sürekli kontrat/rollover etkisi ayrı not edildi.
- Spot altın `XAUUSD=X` için eski Yahoo sayfaları görülse de güncel seri doğrulanmadığı için aktif listeye alınmadı; gram altın da şimdilik yok.

## Sonraki adım

Önce bu katalogdan küçük bir doğrulama koşusu yapılacak: birkaç BIST hissesi, XU100, USD/TRY, altın ve Brent için saatlik + günlük veri uygunluğu, tarih aralığı, eksik mum ve para birimi kontrol edilecek. Sonra 125 varlığın tamamı bekleme süreli kuyruğa alınacak.
