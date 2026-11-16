#!/usr/bin/env python3
"""Tüm kaynak sayfalarını bölüm, konu, yorum ve kullanım katmanlarıyla işler."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/knowledge/source-pages"
OUTPUT = ROOT / "research/knowledge/processed"

TOPICS = {
    "market_basics": {"keywords": ["finansal piyasa", "borsa", "broker", "long", "short", "emir tür", "bid", "ask", "kaldıraç", "marjin"], "use": "Referans ve işlem simülasyonu varsayımları"},
    "ohlcv_data": {"keywords": ["ohlc", "veri kaynağı", "grafik verisi", "açılış fiyatı", "kapanış fiyatı", "yüksek fiyat", "düşük fiyat", "bar verisi"], "use": "Veri sözleşmesi ve mum özellikleri"},
    "candle_behavior": {"keywords": ["gövde", "fitil", "mum diz", "kapanış konumu", "örtüşme", "inside bar", "engulf"], "use": "Mum geometrisi ve davranış özellikleri"},
    "chart_transformations": {"keywords": ["heikin ashi", "renko", "kagi", "line break", "grafik tür"], "use": "Standart OHLC ile dönüştürülmüş grafiklerin bilgi ve gecikme ayrımı"},
    "movement_quality": {"keywords": ["rahat ilerliyor", "rahat ilerleme", "temiz ilerleme", "daha az mumla daha fazla mesafe", "mesafe kazanımı", "hareket kalitesi", "ilerleme kalitesi", "az örtüşme"], "use": "Mesafe, süre, örtüşme ve yol verimliliği özellikleri"},
    "pressure_decay": {"keywords": ["momentum kaybı", "ilerleme kaybı", "gövdeler küçülüyor", "yeni uç üretimi", "zayıflayan hareket", "tükenme"], "use": "Mevcut tarafın ilerleme kabiliyetindeki bozulma"},
    "market_structure": {"keywords": ["piyasa yapısı", "swing high", "swing low", "swing geometr", "structure", "bos", "choch", "higher high", "higher low", "lower high", "lower low", "yapı kırılım", "tepe-dip dizisi", "major swing", "minor swing"], "use": "Gelecek sızıntısız yapı ve swing motoru"},
    "swing_geometry": {"keywords": ["swing geometr", "swing mesafe", "swing hız", "hareket bacağı", "iki bacak", "itiş", "major swing", "minor swing"], "use": "Bacak mesafesi, süresi, hızı ve teyit zamanı"},
    "trend_regime": {"keywords": ["trend", "yatay piyasa", "range", "rejim", "kanal", "hareketli ortalama"], "use": "Bağlam ve piyasa rejimi sınıflaması"},
    "support_resistance": {"keywords": ["destek", "direnç", "yatay seviye", "arz", "talep", "supply", "demand", "zone"], "use": "Konum ve seviye yaşam döngüsü"},
    "liquidity_imbalance": {"keywords": ["likidite", "sweep", "fvg", "fair value gap", "order block", "dengesizlik", "gap"], "use": "Kullanıcının OB/FVG sistemi için kaynak ve olay bağlantısı"},
    "patterns": {"keywords": ["formasyon", "üçgen", "bayrak", "flama", "omuz", "çift dip", "çift tepe", "takoz"], "use": "Şekil yerine ölçülebilir davranış dizileri"},
    "breakout_failure": {"keywords": ["kırılım", "breakout", "fakeout", "sahte kırılım", "failure", "retest", "geri test", "takip davranışı"], "use": "Kırılım/kabul/başarısızlık durum makinesi"},
    "follow_through": {"keywords": ["takip davranışı", "follow-through", "alanı koru", "yeni alan", "dışarıda kal", "kabul görd"], "use": "İlk olaydan sonra alanın korunması ve hareketin devamı"},
    "attempt_expectation": {"keywords": ["ikinci deneme", "beklenen yeni uç", "başarısız yeni", "yeni dip üret", "yeni tepe üret", "beklenti testi"], "use": "Beklenen davranış ile gerçekleşen ikinci denemenin farkı"},
    "pullback": {"keywords": ["pullback", "geri çekilme", "ikinci deneme", "iki bacak", "yeni uç"], "use": "Pullback, ikinci deneme ve devam kalitesi"},
    "momentum": {"keywords": ["momentum", "rsi", "stochastic", "macd", "cci", "uyumsuzluk", "divergence"], "use": "Hareket gücü özellik ailesi"},
    "volatility": {"keywords": ["volatilite", "fiyat hareketliliği", "atr", "true range", "bollinger", "sıkışma", "genişleme"], "use": "Risk normalizasyonu ve volatilite rejimi"},
    "volume_flow": {"keywords": ["hacim", "volume", "obv", "vwap", "footprint", "delta", "order flow", "profile"], "use": "Göreceli katılım ve hacim özellikleri"},
    "execution_microstructure": {"keywords": ["bid", "ask", "spread", "order book", "emir defteri", "market order", "limit emir", "slippage", "dolum"], "use": "Replay sonrası gerçekçi emir ve maliyet simülasyonu"},
    "indicator_systems": {"keywords": ["ichimoku", "supertrend", "adx", "dmi", "donchian", "hareketli ortalama", "bollinger", "stochastic", "macd", "rsi"], "use": "Klasik indikatörlerin rol, bilgi ailesi ve tekrar envanteri"},
    "geometry_tools": {"keywords": ["fibonacci", "pitchfork", "gann", "regresyon", "trend çizgi", "pivot point"], "use": "Kuralı önceden tanımlanmış konum/geometri adayları"},
    "wave_cycle_models": {"keywords": ["elliott", "dalga teor", "wyckoff", "birikim", "dağıtım", "spring", "upthrust", "markup", "markdown"], "use": "Dalga ve piyasa döngüsü modellerini test edilebilir varyantlara ayırma"},
    "multi_timeframe": {"keywords": ["çoklu zaman", "üst zaman", "alt zaman", "htf", "mtf", "ltf"], "use": "Kapanmış bar semantiğiyle periyot senkronizasyonu"},
    "relative_cross_market": {"keywords": ["göreceli güç", "korelasyon", "vix", "dolar", "faiz", "makro", "endeks", "emtia"], "use": "Endeks/FX/maden/enerji olay ve lead-lag araştırması"},
    "sessions_timing": {"keywords": ["işlem seansı", "seans", "açılış saati", "kapanış saati", "londra", "new york", "asya seansı", "kill zone"], "use": "Seans, gün içi zaman ve farklı piyasa saatlerinin olay bağlamı"},
    "macro_rates": {"keywords": ["faiz", "enflasyon", "merkez bankası", "tahvil", "duration", "getiri eğrisi", "para politikası", "döviz kuru"], "use": "Makro olayların endeks ve varlık grupları üzerindeki etkisi"},
    "fundamental_valuation": {"keywords": ["bilanço", "gelir tablosu", "nakit akış", "f/k", "pd/dd", "değerleme", "temel analiz", "şirket analizi"], "use": "Teknik olayları temel bağlamla ilişkilendirecek ikinci katman"},
    "strategy_design": {"keywords": ["strateji", "setup", "tetik", "trigger", "invalidation", "işlem yok", "no-trade", "kural tabanlı"], "use": "Deney ve strateji kartı"},
    "risk_management": {"keywords": ["risk", "stop", "pozisyon büyüklüğü", "sermaye", "drawdown", "r:r", "beklenen değer"], "use": "Sonuç ve daha sonraki yürütme simülasyonu"},
    "position_management": {"keywords": ["pozisyon yönet", "kâr al", "trailing stop", "takip eden stop", "kısmi çıkış", "break-even", "pozisyon ekle", "scale"], "use": "Giriş sonrası çıkış, kısmi yönetim ve pozisyon yaşam döngüsü"},
    "portfolio_correlation": {"keywords": ["portföy", "yoğunlaşma", "portföy ısısı", "korelasyon riski", "çeşitlendirme"], "use": "Eşzamanlı sinyallerin portföy ve yoğunlaşma etkisi"},
    "validation_replay": {"keywords": ["backtest", "replay", "forward test", "paper", "aşırı uyum", "overfit", "lookahead", "repaint", "test dönemi"], "use": "Araştırma doğrulama ve future-leak denetimi"},
    "psychology_process": {"keywords": ["psikoloji", "disiplin", "günlük", "fomo", "bilişsel", "duygu"], "use": "İnsan uygulama ve süreç değerlendirmesi"},
    "journal_review": {"keywords": ["işlem günlüğ", "setup kodu", "ekran görüntüsü", "süreç puanı", "hata modelde", "uygulama hatası", "performans günlüğ"], "use": "Model sonucu ile uygulama hatasını ayıran deney günlüğü"},
    "automation_ai": {"keywords": ["yapay zekâ", " ai ", "pine script", "otomasyon", "alarm", "debug", "kod"], "use": "Gereksinim, semantik test ve sürümleme"},
    "fundamental_derivatives": {"keywords": ["temel analiz", "bilanço", "opsiyon", "vadeli", "hedge", "arbitraj", "kripto"], "use": "İkinci seviye referans ve gelecekteki genişleme"},
    "derivatives_options": {"keywords": ["opsiyon", "call", "put", "strike", "delta", "gamma", "theta", "vega", "implied volatility", "vadeli sözleşme"], "use": "Opsiyon ve türev ürünlerin ayrı fiyat/risk semantiği"},
    "hedge_arbitrage": {"keywords": ["hedge", "korunma", "arbitraj", "pairs trading", "spread trade", "baz riski"], "use": "Korunma ve göreceli değer stratejilerinin gelecekteki modülü"},
    "crypto_specific": {"keywords": ["kripto", "blockchain", "cüzdan", "on-chain", "funding", "likidasyon", "token"], "use": "Kriptoya özgü veri, saklama ve piyasa yapısı farkları"}
}

INTERPRETATIONS = {
    "market_basics": "Ürün, piyasa, emir ve veri kaynağı ayrımları daha sonraki replay yürütme varsayımlarının sınırlarını belirler.",
    "ohlcv_data": "OHLCV yalnız giriş verisi değil; barın ne zaman kesinleştiği ve hangi fiyatın kullanılabildiği araştırma semantiğinin temelidir.",
    "candle_behavior": "Mum adlarından önce gövde, fitil, kapanış konumu ve örtüşme gibi gözlenebilir parçalar ayrı özellikler olmalıdır.",
    "chart_transformations": "Dönüştürülmüş grafikler standart OHLC değildir; gecikme ve sentetik fiyat anlamı ayrı tutulmalıdır.",
    "movement_quality": "Yön tek başına yeterli değildir; alınan mesafe, kullanılan süre, toplam yol ve örtüşme hareketin kalitesini açıklar.",
    "pressure_decay": "Dönüş iddiasından önce mevcut tarafın yeni alan üretme kabiliyetindeki düzenli azalma ölçülmelidir.",
    "market_structure": "Yapı olaylarında oluşum barı ile teyit barı ayrılmalı; geçmişe taşınan pivot erken sinyal sayılmamalıdır.",
    "swing_geometry": "Swingler yalnız tepe/dip değil; mesafe, süre, hız ve teyit zamanı taşıyan hareket bacaklarıdır.",
    "trend_regime": "Trend etiketi tek başına tetik değil, diğer olayların anlamını değiştiren bağlam değişkenidir.",
    "support_resistance": "Seviye teması ile seviyenin davranışla tutulması ayrılmalı; seviye bir konum, tepki ise ayrı olaydır.",
    "liquidity_imbalance": "Likidite, OB ve FVG tek başına sonuç değil; konum, olay yaşam döngüsü ve geçersizlik taşıyan modüller olarak ele alınmalıdır.",
    "patterns": "Formasyon adı yerine mesafe, süre, sıkışma, kırılım, kabul ve başarısızlık bileşenleri ölçülebilir.",
    "breakout_failure": "Kırılım fitil, dış kapanış, takip, geri giriş ve kabul/başarısızlık aşamalarına ayrılabilir.",
    "follow_through": "İlk sinyalin değeri, sonraki barların kazanılan alanı koruyup korumadığıyla ayrı ölçülmelidir.",
    "attempt_expectation": "Sağlıklı hareketin üretmesi beklenen yeni uç ile gerçekleşen sonuç arasındaki fark bağımsız bilgi olabilir.",
    "pullback": "Geri çekilme derinlik, süre, hız, örtüşme ve ikinci deneme kalitesiyle ana hareketten ayrı ölçülmelidir.",
    "momentum": "Momentum araçları aynı bilgi ailesinin varyantlarıdır; yön, volatilite veya yapı kanıtı yerine geçirilmemelidir.",
    "volatility": "Volatilite yön söylemez; normalizasyon, rejim, sıkışma/genişleme ve risk ölçeği olarak kullanılabilir.",
    "volume_flow": "Hacim fiyat davranışının yerine değil, göreceli katılım katmanı olarak ve kendi periyodu içinde normalize edilerek kullanılmalıdır.",
    "execution_microstructure": "OHLC barı emir sırasını ve gerçek dolumu tam göstermez; maliyet ve fill varsayımları ayrı simülasyon katmanıdır.",
    "indicator_systems": "Klasik indikatörler adlarından önce ölçtükleri bilgi ailesi ve karar rolüyle envantere alınmalıdır.",
    "geometry_tools": "Geometri araçlarında anchor/pivot seçimi olay anında yapılabilir olmalı; sonradan en iyi oturan seçim lookahead riskidir.",
    "wave_cycle_models": "Dalga ve döngü modellerinin esnek sayımları tek doğru kabul edilmemeli; önceden tanımlı varyantlar halinde sınanmalıdır.",
    "multi_timeframe": "Her periyodun görevi ve kapanış zamanı ayrı tutulmalı; tamamlanmamış üst zaman barı teyit sayılamaz.",
    "relative_cross_market": "Endeks ve dış piyasa etkileri eşzamanlı korelasyonla sınırlanmadan olay, rejim ve lead-lag olarak araştırılabilir.",
    "sessions_timing": "Aynı olay farklı seans ve gün içi konumda farklı katılımcı/likidite koşullarına sahip olabilir.",
    "macro_rates": "Makro değişkenler doğrudan tetik yerine piyasa gruplarını etkileyen olay ve rejim bağlamı olarak modellenebilir.",
    "fundamental_valuation": "Temel veri ilk teknik replay çekirdeğinden ayrı tutulmalı, ileride zaman damgalı bağlam olarak eklenmelidir.",
    "strategy_design": "Strateji; bağlam, konum, setup, tetik, geçersizlik, hedef, no-trade ve kayıt alanlarından oluşan sürümlü sözleşmedir.",
    "risk_management": "Kazanma oranı tek ölçü değildir; MFE/MAE, beklenti, drawdown ve maliyetler sonuç katmanında ayrılmalıdır.",
    "position_management": "Giriş kalitesi ile çıkış/pozisyon yönetimi aynı iddia değildir ve ayrı deneylerde ölçülmelidir.",
    "portfolio_correlation": "Tekil sembol avantajı, eşzamanlı ve korelasyonlu sinyallerde portföy yoğunlaşmasına dönüşebilir.",
    "validation_replay": "Toplu ölçüm, bar replay ve forward gözlem farklı sorular cevaplar; kanıt türleri birbirinin yerine geçmez.",
    "psychology_process": "İnsan uygulama hatası ile model hatası ayrılmalı; süreç kaydı strateji sonucundan bağımsız tutulmalıdır.",
    "journal_review": "Deney, karar ve uygulama kayıtları model hatası ile süreç ihlalini sonradan ayırabilecek kimlikler taşımalıdır.",
    "automation_ai": "Kodun derlenmesi doğruluğu kanıtlamaz; bar zamanı, state, reset, MTF ve future-leak semantiği test edilmelidir.",
    "fundamental_derivatives": "Bu alanlar ilk replay çekirdeğinde referans katmanıdır; ürün ve risk varsayımları genişleme aşamasında ayrı modüller gerektirir.",
    "derivatives_options": "Türevlerin doğrusal olmayan risk ve sözleşme yapısı spot OHLC stratejilerinden ayrı değerlendirilmelidir.",
    "hedge_arbitrage": "Korunma ve arbitraj fikirleri yön tahmininden farklı amaç, maliyet ve yürütme semantiğine sahiptir.",
    "crypto_specific": "Kripto piyasasının kesintisiz seans, funding, saklama ve likidasyon özellikleri ayrı bağlam gerektirir."
}

NOISE = re.compile(r"^(ANA TRADING KİTABI|PROFESYONEL TEKNİK ANALİZ|\d+)$", re.I)
CHAPTER = re.compile(r"(?:^|\n)B[ÖO]L[ÜU]M\s+(\d+)\b", re.I)
SECTION = re.compile(r"(?:^|\n)(\d{1,2}\.\d{1,2})\s*[—-]?\s*([^\n]{3,120})", re.I)


def content_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines and (lines[0].startswith("ANA TRADING KİTABI") or lines[0].startswith("PROFESYONEL TEKNİK ANALİZ")):
        lines = lines[1:]
        if lines and (lines[0].isdigit() or "•" in lines[0]):
            lines = lines[1:]
    return " ".join(lines)


def sentences(text: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", content_text(text)).strip()
    candidates = [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned) if len(s.strip()) >= 35]
    return [s for s in candidates if not s.startswith(("Şekil ", "Tablo ", "İçindekiler"))]


def classify(text: str) -> list[tuple[str, int]]:
    low = text.casefold()
    scores = []
    for topic, spec in TOPICS.items():
        score = 0
        for keyword in spec["keywords"]:
            pattern = rf"(?<!\w){re.escape(keyword.casefold().strip())}(?!\w)"
            score += len(re.findall(pattern, low))
        if score:
            scores.append((topic, score))
    return sorted(scores, key=lambda item: (-item[1], item[0]))[:5]


def relevance(topics: list[tuple[str, int]]) -> str:
    core = {"candle_behavior", "movement_quality", "pressure_decay", "market_structure", "swing_geometry", "trend_regime", "support_resistance", "liquidity_imbalance", "patterns", "breakout_failure", "follow_through", "attempt_expectation", "pullback", "momentum", "volatility", "volume_flow", "indicator_systems", "multi_timeframe", "relative_cross_market", "strategy_design", "validation_replay"}
    if any(topic in core for topic, _ in topics): return "core"
    if topics: return "supporting"
    return "reference"


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((SOURCE / "manifest.json").read_text(encoding="utf-8"))
    coverage = {"schema_version": 1, "sources": [], "topic_counts": Counter(), "total_pages": 0, "processed_pages": 0}
    topic_refs: dict[str, list[dict]] = defaultdict(list)
    card_lookup: dict[str, dict] = {}
    for source in manifest["sources"]:
        source_id = source["source_id"]
        records = [json.loads(line) for line in (ROOT / source["jsonl"]).read_text(encoding="utf-8").splitlines()]
        current_chapter = None
        current_section = None
        out_path = OUTPUT / f"{source_id}-cards.jsonl"
        cards = 0
        with out_path.open("w", encoding="utf-8") as handle:
            for record in records:
                text = record["text"]
                chapter_match = CHAPTER.search(text)
                # Gerçek bölüm açılışı sayfa başlığından hemen sonra gelir. Metin
                # içindeki "Bölüm 2'de gördüğümüz" atıflarını geçiş sayma.
                if chapter_match and chapter_match.start() < 100:
                    number = int(chapter_match.group(1))
                    if current_chapter is None or number == current_chapter + 1 or number == current_chapter:
                        if number != current_chapter:
                            current_section = None
                        current_chapter = number
                section_hits = SECTION.findall(text)
                if section_hits:
                    current_section = f"{section_hits[-1][0]} — {section_hits[-1][1].strip()}"
                topic_scores = classify(text)
                source_summary = sentences(text)[:3]
                top_topics = [topic for topic, _ in topic_scores]
                uses = [TOPICS[t]["use"] for t in top_topics]
                card = {
                    "id": f"{source_id}.p{record['page']:04d}",
                    "source_id": source_id,
                    "page": record["page"],
                    "chapter": current_chapter,
                    "section": current_section,
                    "page_kind": "chapter_content" if current_chapter is not None else "front_matter",
                    "relevance": relevance(topic_scores) if current_chapter is not None else "reference",
                    "topics": [{"id": t, "score": s} for t, s in topic_scores],
                    "source_excerpt": text,
                    "source_extract_summary": source_summary,
                    "inference": "Bu sayfa, kesin uygulama kuralı değil; ilişkili bilgi aileleri ve karar rolleri için kaynak kaydıdır.",
                    "possible_uses": uses,
                    "hypothesis_policy": "Formül ve eşik sonraki kavram incelemesinde tanımlanacak; çelişen tanımlar ayrı varyant kalacak.",
                    "review_status": "systematically_extracted"
                }
                handle.write(json.dumps(card, ensure_ascii=False) + "\n")
                card_lookup[card["id"]] = card
                cards += 1
                for topic, score in topic_scores:
                    coverage["topic_counts"][topic] += 1
                    topic_refs[topic].append({"source_id": source_id, "page": record["page"], "score": score, "card_id": card["id"]})
        coverage["total_pages"] += len(records)
        coverage["processed_pages"] += cards
        coverage["sources"].append({"source_id": source_id, "pages": len(records), "cards": cards, "output": out_path.relative_to(ROOT).as_posix()})
    coverage["topic_counts"] = dict(sorted(coverage["topic_counts"].items()))
    coverage["coverage_percent"] = round(100 * coverage["processed_pages"] / coverage["total_pages"], 2)
    (OUTPUT / "coverage.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    taxonomy = {"schema_version": 1, "topics": [{"id": key, **value} for key, value in TOPICS.items()]}
    (OUTPUT / "topic-taxonomy.json").write_text(json.dumps(taxonomy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    index = {"schema_version": 1, "topics": {topic: sorted(refs, key=lambda r: (-r["score"], r["source_id"], r["page"])) for topic, refs in topic_refs.items()}}
    (OUTPUT / "topic-index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Her konu için üç kaynağı da mümkün olduğunca temsil eden uzun alıntılı dosya üret.
    dossiers = OUTPUT / "themes"
    dossiers.mkdir(exist_ok=True)
    master = ["# Tam Tematik Bilgi Kataloğu", "", f"İşlenen sayfa: **{coverage['processed_pages']}/{coverage['total_pages']} (%{coverage['coverage_percent']})**", "",
              "Bu katalog kaynak alıntısını, proje yorumunu ve kullanım fikrini ayırır. Formül/eşikler sonraki ayrıntılı deney tasarımına bırakılmıştır.", ""]
    for topic, spec in TOPICS.items():
        refs = topic_refs.get(topic, [])
        selected = []
        per_source = Counter()
        for ref in sorted(refs, key=lambda r: (-r["score"], r["source_id"], r["page"])):
            if per_source[ref["source_id"]] >= 4:
                continue
            selected.append(ref)
            per_source[ref["source_id"]] += 1
            if len(selected) >= 10:
                break
        lines = [f"# {topic}", "", f"**Kapsam:** {len(refs)} sayfa eşleşmesi", "", "## Proje yorumu (`inference`)", "", INTERPRETATIONS[topic], "",
                 "## Nasıl kullanılabilir?", "", spec["use"], "",
                 "## Kaynak şeritleri", ""]
        for no, ref in enumerate(selected, 1):
            card = card_lookup[ref["card_id"]]
            excerpt = re.sub(r"\s+", " ", card["source_excerpt"]).strip()
            if len(excerpt) > 1600:
                cut = excerpt.rfind(". ", 900, 1600)
                excerpt = excerpt[:cut + 1 if cut > 0 else 1600] + " …"
            lines.extend([
                f"### {no}. {ref['source_id']} — PDF s. {ref['page']}", "",
                f"> {excerpt}", "",
                f"**Bölüm/alt başlık:** {card.get('chapter') or 'belirlenmedi'} / {card.get('section') or 'belirlenmedi'}", "",
                "**Kaynak özeti (`source`):** " + " ".join(card["source_extract_summary"]), ""
            ])
        lines.extend(["## Test fikri (`hypothesis`)", "", "Bu konuya ait kaynak varyantları korunur. İlk aşamada sabit eşik seçilmez; geniş sembol evreninde aynı tanımların amaçladığı davranışa katkısı karşılaştırılır.", ""])
        target = dossiers / f"{topic}.md"
        target.write_text("\n".join(lines), encoding="utf-8")
        master.append(f"- [{topic}](themes/{topic}.md) — {len(refs)} sayfa — {spec['use']}")
    (OUTPUT / "master-synthesis.md").write_text("\n".join(master) + "\n", encoding="utf-8")

    # Bölüm dosyaları: her bölümün sayfa aralığı, alt başlıkları, baskın
    # konuları ve sayfa sayfa kaynak özetleri. Tam alıntılar kart JSONL'lerinde.
    chapter_root = OUTPUT / "chapters"
    chapter_root.mkdir(exist_ok=True)
    chapter_groups: dict[tuple[str, int], list[dict]] = defaultdict(list)
    for card in card_lookup.values():
        if card["chapter"] is not None:
            chapter_groups[(card["source_id"], card["chapter"])].append(card)
    for (source_id, chapter), cards in sorted(chapter_groups.items()):
        cards.sort(key=lambda c: c["page"])
        topics = Counter(item["id"] for card in cards for item in card["topics"])
        sections = []
        for card in cards:
            if card["section"] and card["section"] not in sections:
                sections.append(card["section"])
        directory = chapter_root / source_id
        directory.mkdir(exist_ok=True)
        lines = [f"# {source_id} — Bölüm {chapter}", "", f"**PDF sayfaları:** {cards[0]['page']}–{cards[-1]['page']}",
                 f"**Sayfa kartları:** {len(cards)}", "", "## Alt başlıklar", ""]
        lines.extend(f"- {section}" for section in sections)
        lines.extend(["", "## Konu dağılımı", ""])
        lines.extend(f"- `{topic}`: {count} sayfa" for topic, count in topics.most_common())
        lines.extend(["", "## Sayfa şeritleri", ""])
        for card in cards:
            summary = " ".join(card["source_extract_summary"]) or "Özet cümlesi otomatik ayrılamadı; tam kaynak şeridi kart JSONL kaydında korunuyor."
            lines.extend([f"### PDF s. {card['page']} — {card['section'] or 'Bölüm girişi/devamı'}", "", summary, "",
                          f"**Konular:** {', '.join(item['id'] for item in card['topics']) or 'referans'}", "",
                          f"**Kart:** `{card['id']}`", ""])
        (directory / f"chapter-{chapter:02d}.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(coverage, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
