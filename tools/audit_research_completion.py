"""Üç kitabın nihai kapsam, kural, kaynak ve sonuç bütünlüğünü denetler."""
from __future__ import annotations
import csv,hashlib,json
from pathlib import Path
ROOT=Path('research')
BOOKS=[
 ('CILT2',109,ROOT/'experiments/cilt2-completion','cilt2-page-coverage.csv','cilt2-claim-registry.json','cilt2-unresolved-claims.csv','final-summary.json'),
 ('CILT1',139,ROOT/'experiments/cilt1-completion','cilt1-page-coverage.csv','cilt1-claim-registry.json','cilt1-unresolved-claims.csv','final-summary.json'),
 ('ATK',530,ROOT/'experiments/atk-completion','atk-page-coverage.csv','atk-claim-registry.json','atk-unresolved-claims.csv','final-summary.json')]
REGISTRIES=[ROOT/'experiments/book-rule-results/registry.json',ROOT/'experiments/cilt1-rule-results/registry.json',ROOT/'experiments/atk-rule-results/registry.json']
def audit()->dict:
 errors=[];rules=[]
 for p in REGISTRIES:
  if not p.exists():errors.append(f'eksik registry: {p}');continue
  rules.extend(json.loads(p.read_text())['rules'])
 ids=[r['id'] for r in rules];known=set(ids)
 if len(ids)!=len(known):errors.append('yinelenen rule id')
 books={}
 for name,count,base,pagef,claimf,unf,finalf in BOOKS:
  missing=[x for x in (pagef,claimf,unf,finalf) if not (base/x).exists()]
  if missing:errors.append(f'{name} eksik dosya: {missing}');continue
  pages=list(csv.DictReader((base/pagef).open()));claims=json.loads((base/claimf).read_text())['claims'];un=list(csv.DictReader((base/unf).open()));final=json.loads((base/finalf).read_text())
  if len(pages)!=count or {int(x['page']) for x in pages}!=set(range(1,count+1)):errors.append(f'{name} sayfa kapsamı bozuk')
  claim_ids=[x['claim_id'] for x in claims]
  if len(claim_ids)!=len(set(claim_ids)):errors.append(f'{name} claim id tekrarı')
  if un:errors.append(f'{name} unresolved={len(un)}')
  if any(not x.get('disposition') for x in claims):errors.append(f'{name} boş disposition')
  testable=[x for x in claims if x.get('disposition')!='reference_only']
  if any(not x.get('linked_rules') for x in testable):errors.append(f'{name} kuralsız test edilebilir claim')
  missing_rules=sorted({rid for x in claims for rid in x.get('linked_rules',[]) if rid not in known})
  if missing_rules:errors.append(f'{name} bulunmayan kurallar: {missing_rules}')
  if any(not x.get('mathematical_definition') or x['mathematical_definition'].startswith(('C1-P','C2-P','İlgili','Henüz')) for x in testable):errors.append(f'{name} geçersiz matematiksel tanım')
  if final.get('status')!='passed':errors.append(f'{name} final status={final.get("status")}')
  books[name]={'pages':len(pages),'atomic_claims':len(claims),'unresolved':len(un),'status':final.get('status')}
 for r in rules:
  d=r.get('result_directory')
  if d and not Path(d).exists():errors.append(f"eksik sonuç dizini: {r['id']}")
 catalog=json.loads((ROOT/'library/catalog.json').read_text())
 for b in catalog['books']:
  p=Path(b['path'])
  if not p.exists():errors.append(f"eksik PDF: {p}")
  elif hashlib.sha256(p.read_bytes()).hexdigest()!=b['sha256']:errors.append(f"PDF hash uyuşmazlığı: {b['id']}")
 evidence=ROOT/'measurements/atk-final/cross_book_evidence_matrix.csv'
 if not evidence.exists() or len(list(csv.DictReader(evidence.open())))!=len(rules):errors.append('çapraz kitap kanıt matrisi rule sayısıyla eşleşmiyor')
 external=json.loads((ROOT/'specs/atk-external-data-contracts.json').read_text())
 required={'rates_bonds','fundamentals','crypto_derivatives','options','arbitrage_execution'}
 if not required<=set(external):errors.append('harici veri sözleşmesi alanı eksik')
 return {'status':'passed' if not errors else 'failed','books':books,'rules_total':len(rules),'unique_rules':len(known),'external_contracts':sorted(required),'errors':errors}
def main():
 report=audit();out=ROOT/'experiments/FINAL_RESEARCH_AUDIT.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(0 if report['status']=='passed' else 1)
if __name__=='__main__':main()
