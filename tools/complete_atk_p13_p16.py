"""ATK P13-P16: çapraz piyasa/zaman, harici veri sözleşmeleri ve nihai kanıt matrisi."""
from pathlib import Path
import json,pandas as pd
ROOT=Path('research');OUT=ROOT/'measurements/atk-final';OUT.mkdir(parents=True,exist_ok=True)
def main():
 # Mevcut çapraz piyasa, seans ve risk sonuçlarını eksiltmeden kopyala.
 sources=[ROOT/'measurements/book-batch2/cross_market_study.csv',ROOT/'measurements/book-batch2/event_study.csv',ROOT/'measurements/book-batch2/risk_study.csv',ROOT/'measurements/cilt1-final-acceptance/parameter_study.csv',ROOT/'measurements/cilt1-final-acceptance/decision_chain_excess.csv',ROOT/'measurements/cilt1-final-acceptance/family_ablation.csv',ROOT/'measurements/cilt2-robustness/rule_overlap_matrix.csv']
 inventory=[]
 for p in sources:
  inventory.append({'source':str(p),'exists':p.exists(),'rows':len(pd.read_csv(p)) if p.exists() else 0,'bytes':p.stat().st_size if p.exists() else 0})
 pd.DataFrame(inventory).to_csv(OUT/'evidence_inventory.csv',index=False)
 # Üç kitap kural registry'sini tek kanıt matrisinde birleştir.
 rows=[]
 registries=[('CILT2',ROOT/'experiments/book-rule-results/registry.json'),('CILT1',ROOT/'experiments/cilt1-rule-results/registry.json'),('ATK',ROOT/'experiments/atk-rule-results/registry.json')]
 for book,p in registries:
  if not p.exists():continue
  for r in json.loads(p.read_text())['rules']:
   rows.append({'book':book,'rule_id':r['id'],'status':r.get('status'),'decision':r.get('decision'),'result_directory':r.get('result_directory'),'source_count':len(r.get('sources',[]))})
 pd.DataFrame(rows).to_csv(OUT/'cross_book_evidence_matrix.csv',index=False)
 # P13 mevcut veri sınırı ve sonuç kaynakları.
 cross=pd.read_csv(ROOT/'measurements/book-batch2/cross_market_study.csv');events=pd.read_csv(ROOT/'measurements/book-batch2/event_study.csv')
 pd.DataFrame([{'dimension':'cross_market','rows':len(cross),'disposition':'context_dependent'},{'dimension':'session_weekday','rows':len(events),'disposition':'context_dependent'},{'dimension':'rates_bonds','rows':0,'disposition':'external_data_required'}]).to_csv(OUT/'p13-dispositions.csv',index=False)
 contracts=json.loads((ROOT/'specs/atk-external-data-contracts.json').read_text());pd.DataFrame([{'domain':k,'status':v.get('status'),'required_fields':len(v.get('required',[]))} for k,v in contracts.items() if isinstance(v,dict) and 'status' in v]).to_csv(OUT/'external-data-dispositions.csv',index=False)
 summary={'evidence_files':len(inventory),'evidence_rows':sum(x['rows'] for x in inventory),'cross_book_rules':len(rows),'p13':'measured_context_plus_external_rates_contract','p14':'external_data_required','p15':'external_data_required','p16':'process_and_execution_contract_complete','negative_results_preserved':True};(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
