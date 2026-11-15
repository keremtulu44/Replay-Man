"""Kitap kartlarını ölçülen replay kuralları ve eksiksiz sonuç tablolarıyla bağlar."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

ROOT = Path("research")
MEASURE = ROOT / "measurements/ohlcv-baseline"
OUT = ROOT / "experiments/book-rule-results"

RULES = {
 "BR-001-confirmed-swing": {"title":"Swing ancak sağ taraf oluştuktan sonra kesinleşir", "sources":["PTA-C2-2026.p0054","PTA-C2-2026.p0055","PTA-C2-2026.p0058","PTA-C2-2026.p0059"], "events":[], "status":"altyapi_kurali", "decision":"Replay motorunda pivot zamanı ve teyit zamanı ayrı tutuldu."},
 "BR-002-close-break": {"title":"Seviyeyi geçmek yetmez; kapanış konumu gerekir", "sources":["PTA-C2-2026.p0045","PTA-C2-2026.p0047","PTA-C2-2026.p0052"], "events":["close_break"], "status":"baglam_filtresi_gerekli", "decision":"Çıplak kırılım kısa ufukta benchmark sonrası zayıf; 4h 60 barda test pozitif ama doğrulama yaklaşık sıfır."},
 "BR-003-follow-through": {"title":"İlk kapanıştan sonra takip davranışı", "sources":["PTA-C2-2026.p0048","PTA-C2-2026.p0050","PTA-C2-2026.p0051","PTA-C2-2026.p0052"], "events":["follow_through"], "status":"bilgi_tekrari", "decision":"4h aşağı sonuç olumlu; mevcut tanım acceptance ile neredeyse aynı olayları üretiyor."},
 "BR-004-acceptance": {"title":"Kırılımın yeni alanda kabul görmesi", "sources":["PTA-C2-2026.p0045","PTA-C2-2026.p0048","PTA-C2-2026.p0052","PTA-C2-2026.p0096"], "events":["acceptance"], "status":"devam_et", "decision":"4h aşağı acceptance 60 barda eğitim/doğrulama/test bölümlerinin üçünde de pozitif XU100-aşırı medyan verdi."},
 "BR-005-retest-hold": {"title":"Kırılım bölgesine dönüş ve seviyenin tutulması", "sources":["PTA-C2-2026.p0057","PTA-C2-2026.p0076","PTA-C2-2026.p0091","PTA-C2-2026.p0096"], "events":["retest_hold"], "status":"yazi_turaya_yakin", "decision":"Benchmark sonrası çoğu bölümde sıfır çevresi; tek başına belirgin ayrıştırma sağlamadı."},
 "BR-006-failure": {"title":"Başarısız kırılım ve eski alana dönüş", "sources":["PTA-C2-2026.p0041","PTA-C2-2026.p0043","PTA-C2-2026.p0046","PTA-C2-2026.p0049","PTA-C2-2026.p0070"], "events":["failure"], "status":"rejime_bagli", "decision":"4h aşağı kırılım failure sonrası yukarı hipotezi doğrulama/testte olumlu, eğitimde belirgin olumsuz."},
 "BR-007-probe-rejection": {"title":"Fitille taşma tek başına dönüş değildir", "sources":["PTA-C2-2026.p0017","PTA-C2-2026.p0043","PTA-C2-2026.p0073"], "events":["probe_rejection"], "status":"kararsiz", "decision":"Yön ve zaman bölümüne göre işaret değiştiriyor; bağlamsız kullanım güvenilir değil."},
 "BR-008-movement-quality": {"title":"Temiz hareket, örtüşme ve ilerleme verimliliği", "sources":["PTA-C2-2026.p0013","PTA-C2-2026.p0015","PTA-C2-2026.p0016","PTA-C2-2026.p0094"], "events":["acceptance"], "context":"movement_quality_band", "status":"olumlu_baglam", "decision":"4h aşağı acceptance içinde düşük ve yüksek verim bantları üç zaman bölümünde pozitif; orta bant doğrulamada negatif."},
 "BR-009-overlap": {"title":"Örtüşme arttıkça hareketin sıkışması", "sources":["PTA-C2-2026.p0015","PTA-C2-2026.p0038","PTA-C2-2026.p0044"], "events":["acceptance"], "context":"overlap_band", "status":"ornek_yetersiz_bant_var", "decision":"Düşük örtüşme testte güçlü; yüksek örtüşme testinde 60 bar hazır gözlem yok."},
 "BR-010-volatility-context": {"title":"Sıkışma, genişleme ve kırılım bağlamı", "sources":["PTA-C2-2026.p0038","PTA-C2-2026.p0041","PTA-C2-2026.p0044"], "events":["acceptance"], "context":"volatility_band", "status":"devam_et", "decision":"4h aşağı acceptance öncesi contracted bant üç zaman bölümünde pozitif ve testte belirgin; normal/expanded testte negatif."},
 "BR-011-pressure-decay": {"title":"Gövde ve ilerleme küçülmesiyle baskı kaybı", "sources":["PTA-C2-2026.p0018","PTA-C2-2026.p0022","PTA-C2-2026.p0033"], "events":["acceptance"], "context":"body_pressure_band", "status":"olumlu_baglam", "decision":"Decaying gövde baskısı 4h aşağı acceptance içinde üç bölümde pozitif ve testte expanding gruptan daha güçlü."},
 "BR-012-second-attempt": {"title":"İkinci denemeyi ilk bacakla mesafe, süre ve hız açısından karşılaştır", "sources":["PTA-C2-2026.p0063","PTA-C2-2026.p0064","PTA-C2-2026.p0065","PTA-C2-2026.p0071","PTA-C2-2026.p0097"], "events":[], "attempt_events":["new_extreme_success","new_extreme_failure"], "status":"altyapi_tamam", "decision":"112.790 ikinci deneme olayı üretildi; çıplak sonuçlar dönem/yön bağımlı, oran bağlamları ayrıca korunuyor."},
 "BR-013-new-extreme-success": {"title":"İkinci denemenin beklenen yeni ucu üretmesi", "sources":["PTA-C2-2026.p0064","PTA-C2-2026.p0067","PTA-C2-2026.p0097"], "events":[], "attempt_events":["new_extreme_success"], "status":"rejime_bagli", "decision":"Başarı etiketi tek başına devam avantajı değil; yön ve zaman bölümü arasında işaret değişiyor."},
 "BR-014-new-extreme-failure": {"title":"İkinci denemenin yeni uç üretememesi", "sources":["PTA-C2-2026.p0065","PTA-C2-2026.p0070","PTA-C2-2026.p0071","PTA-C2-2026.p0097"], "events":[], "attempt_events":["new_extreme_failure"], "status":"baglam_gerekli", "decision":"4h yukarı deneme failure sonrası aşağı hipotezinde daha zayıf mesafe, uzun süre veya benzer hız alt grupları üç zaman bölümünde pozitif; çıplak olay kararlı değil."},
}

def cards():
 result={}
 for path in (ROOT/"knowledge/processed").glob("*-cards.jsonl"):
  for line in path.read_text(encoding="utf-8").splitlines():
   card=json.loads(line); result[card["id"]]=card
 return result

def main():
 OUT.mkdir(parents=True,exist_ok=True); card_map=cards()
 tables={name:pd.read_csv(MEASURE/name) for name in ["structure_event_study.csv","structure_time_split_study.csv","structure_symbol_results.csv","book_context_rule_study.csv"]}
 attempt_base=ROOT/"measurements/attempts"
 attempt_tables={name:pd.read_csv(attempt_base/name) for name in ["attempt_time_split_study.csv","attempt_symbol_results.csv","attempt_context_study.csv"]} if attempt_base.exists() else {}
 registry=[]
 for slug,rule in RULES.items():
  folder=OUT/slug; folder.mkdir(parents=True,exist_ok=True)
  source_records=[]
  for card_id in rule["sources"]:
   c=card_map[card_id]
   source_records.append({k:c.get(k) for k in ["id","source_id","page","chapter","section","source_excerpt","source_extract_summary","inference","possible_uses"]})
  (folder/"source-links.json").write_text(json.dumps(source_records,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  if rule["events"]:
   for filename,table in tables.items():
    subset=table[table.event.isin(rule["events"])] if "event" in table else table.iloc[0:0]
    if filename=="book_context_rule_study.csv" and rule.get("context"):
     subset=subset[subset.context_dimension==rule["context"]]
    elif filename=="book_context_rule_study.csv":
     continue
    subset.to_csv(folder/filename,index=False)
  if rule.get("attempt_events"):
   for filename,table in attempt_tables.items():
    table[table.event.isin(rule["attempt_events"])].to_csv(folder/filename,index=False)
  record={"id":slug,**rule,"source_link":str(folder/"source-links.json"),"result_directory":str(folder)}
  registry.append(record)
 (OUT/"registry.json").write_text(json.dumps({"schema_version":1,"rules":registry},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": main()
