"""Yapı olaylarını finansal ve sembol-tutarlılık odaklı Markdown rapora dönüştürür."""
from pathlib import Path
import pandas as pd

BASE = Path("research/measurements/ohlcv-baseline")


def pct(value):
    return "—" if pd.isna(value) else f"{100*value:.2f}%"


def main():
    pooled = pd.read_csv(BASE / "structure_event_study.csv")
    symbols = pd.read_csv(BASE / "structure_symbol_results.csv")
    focus = pooled[(pooled.group == "bist_equities") & (pooled.interval == "1h")].copy()
    robust = symbols[(symbols.group == "bist_equities") & (symbols.interval == "1h") & (symbols.observations >= 20)].copy()
    consistency = robust.groupby(["event", "thesis_direction"]).agg(
        eligible_symbols=("asset_id", "nunique"),
        positive_symbols_5=("median_return_5", lambda x: float((x > 0).mean())),
        median_symbol_return_5=("median_return_5", "median"),
        positive_symbols_20=("median_return_20", lambda x: float((x > 0).mean())),
        median_symbol_return_20=("median_return_20", "median"),
    ).reset_index()
    table = focus.merge(consistency, on=["event", "thesis_direction"], how="left")
    table["payoff20"] = table.median_mfe_20 / table.median_mae_20.abs()
    table = table.sort_values("median_return_20", ascending=False)
    lines = [
        "# Yapı Olayları — İlk Finansal Sonuç Raporu", "",
        "## Raporun niteliği", "",
        "Bu rapor BIST 100 hisselerinin 1 saatlik serilerine odaklanan **keşifsel olay çalışmasıdır**. Getiriler olay kapanışından sonraki sabit bar ufkudur; emir girişi, spread, komisyon, slippage veya portföy çakışması içermez. Bu nedenle backtest kârı veya işlem tavsiyesi değildir.", "",
        "## BIST hisseleri 1h — olay sonrası sonuç", "",
        "| Olay | Hipotez | Gözlem | Varlık | 5 bar medyan | 5 bar pozitif | 20 bar medyan | 20 bar pozitif | 20 bar MFE | 20 bar MAE | MFE/|MAE| | ≥20 gözlemli sembol | Pozitif sembol (20) | Sembol medyanı (20) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in table.itertuples():
        lines.append(f"| `{r.event}` | {r.thesis_direction} | {r.observations:,} | {r.assets} | {pct(r.median_return_5)} | {pct(r.win_rate_5)} | {pct(r.median_return_20)} | {pct(r.win_rate_20)} | {pct(r.median_mfe_20)} | {pct(r.median_mae_20)} | {r.payoff20:.2f} | {int(r.eligible_symbols) if pd.notna(r.eligible_symbols) else 0} | {pct(r.positive_symbols_20)} | {pct(r.median_symbol_return_20)} |")
    lines += [
        "", "## Okuma", "",
        "- Aşağı kırılım devamı (`close_break`, `follow_through`, `acceptance`, `retest_hold`, hipotez `down`) mevcut ham örneklemde yukarı kırılım devamından daha güçlü görünmektedir.",
        "- Yukarı kırılım devamının 5 ve 20 bar medyanı çoğu varyantta sıfır çevresindedir; bu haliyle tek başına güçlü avantaj göstermez.",
        "- Failure ve probe rejection satırlarında hipotez yönü ilk denemenin tersidir. Böylece sonuç, başarısız kırılım yönünde değil geri dönüş yönünde okunur.",
        "- MFE ve MAE birbirine yakın olduğunda çıplak olayın hedef/stop ayrıştırması zayıftır. Bağlam, hareket kalitesi ve rejim filtresi gereklidir.",
        "- Sembol tutarlılığı, en az 20 gözlemi olan her sembolün medyan sonucunun pozitif olup olmadığıyla hesaplanmıştır; olay sayısı çok olan sembollerin sonucu tek başına ezmesine izin vermez.",
        "", "## Finansal olarak henüz hesaplanmayanlar", "",
        "- Komisyon, spread ve slippage", "- Aynı anda açılan korelasyonlu pozisyonlar", "- Sermaye ve pozisyon büyüklüğü", "- Stop/target sırası ve bar içi belirsizlik", "- Portföy drawdown'u", "- Kurumsal işlem ayıklamasından sonra yeniden ölçüm", "- Eğitim/doğrulama/out-of-sample ayrımı", "",
        "## Risk ve veri uyarıları", "",
        "1. Ham fiyatlarda bölünme ve diğer kurumsal işlemler aşağı yönlü olayları yapay biçimde güçlendirebilir.",
        "2. Aynı sembolde yakın zamanlı olaylar bağımsız değildir; gözlem sayısı istatistiksel bağımsız örnek sayısı değildir.",
        "3. Olaylar aynı anda birden fazla geçmiş swing seviyesinde üretilebilir.",
        "4. İlk parametreler seçilmiştir ama optimize edilmemiştir: 0,10 ATR tolerans, iki kapanış kabul, üç bar takip, on bar failure, yüz bar seviye ömrü.",
        "5. Sonuç seçimi bu veriye bakılarak değiştirilirse çoklu deneme yanlılığı doğar. Bundan sonraki parametreler eğitim döneminde seçilip ayrı doğrulama döneminde sınanmalıdır.",
        "", "## Sonraki zorunlu ölçüm", "",
        "Olay anındaki trend/range, volatilite, yol verimliliği, örtüşme, gövde gücü ve baskı kaybı dondurulacak; sonuçlar bu bağlamlara ayrılacaktır. Ardından kurumsal işlem filtresi ve zaman bazlı out-of-sample doğrulama uygulanacaktır.", "",
    ]
    (BASE / "FINANCIAL_RESULTS.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
