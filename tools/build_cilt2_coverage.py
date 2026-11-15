"""Cilt 2'nin 109 sayfasını deney kuralı ve tamamlama paketlerine bağlar."""
from __future__ import annotations
import csv,json
from pathlib import Path

ROOT=Path('research');OUT=ROOT/'experiments/cilt2-completion';CARDS=ROOT/'knowledge/processed/PTA-C2-2026-cards.jsonl';REG=ROOT/'experiments/book-rule-results/registry.json'
PACKAGES={1:'C2-P2-single-candle',2:'C2-P2-single-candle',3:'C2-P4-pressure-quality',4:'C2-P3-multi-candle',5:'C2-P3-multi-candle',6:'C2-P5-compression-expansion',7:'C2-P6-breakout-lifecycle',8:'C2-P7-swing-geometry',9:'C2-P8-attempt-pullback',10:'C2-P8-attempt-pullback',11:'C2-P9-location-context',12:'C2-P10-volume-mtf',13:'C2-P11-decision-chain'}
FIELDS=['page','card_id','chapter','section','page_kind','relevance','topic_ids','linked_rule_ids','target_package','disposition','coverage_state','source_summary','inference','possible_uses']

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 cards=[json.loads(x) for x in CARDS.read_text(encoding='utf-8').splitlines()]
 rules=json.loads(REG.read_text(encoding='utf-8'))['rules']; by_card={}
 for rule in rules:
  for card in rule['sources']:
   if card.startswith('PTA-C2-2026.') : by_card.setdefault(card,[]).append(rule['id'])
 rows=[];claims=[];unresolved=[]
 for c in cards:
  linked=sorted(by_card.get(c['id'],[])); text=(c.get('section') or '')+' '+c.get('source_excerpt','')
  is_ob_fvg=any(k in text.casefold() for k in ['order block','fvg','fair value gap'])
  if c['page_kind']=='front_matter': disposition='reference_only';state='closed'
  elif is_ob_fvg: disposition='deferred_ob_fvg';state='closed_deferred'
  elif linked: disposition='tested_initial';state='linked_needs_exhaustive_review'
  else: disposition='pending_package';state='open'
  package=PACKAGES.get(c.get('chapter'),'C2-P1-coverage')
  row={'page':c['page'],'card_id':c['id'],'chapter':c.get('chapter'),'section':c.get('section'),'page_kind':c['page_kind'],'relevance':c['relevance'],'topic_ids':'|'.join(t['id'] for t in c['topics']),'linked_rule_ids':'|'.join(linked),'target_package':package,'disposition':disposition,'coverage_state':state,'source_summary':' '.join(c['source_extract_summary']),'inference':c['inference'],'possible_uses':'|'.join(c['possible_uses'])}
  rows.append(row)
  claim={'claim_id':f"C2-P{c['page']:03d}-C01",'source_card':c['id'],'page':c['page'],'chapter':c.get('chapter'),'section':c.get('section'),'source_summary':c['source_extract_summary'],'inference':c['inference'],'possible_uses':c['possible_uses'],'topics':[t['id'] for t in c['topics']],'linked_rules':linked,'target_package':package,'disposition':disposition,'coverage_state':state}
  claims.append(claim)
  if state in {'open','linked_needs_exhaustive_review'}:unresolved.append({'claim_id':claim['claim_id'],'page':c['page'],'section':c.get('section'),'target_package':package,'current_state':state,'linked_rules':'|'.join(linked),'next_action':'Sayfadaki bütün ayrı iddiaları atomik kurallara ayır ve sonuç disposition ata'})
 with (OUT/'cilt2-page-coverage.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
 (OUT/'cilt2-claim-registry.json').write_text(json.dumps({'schema_version':1,'source_id':'PTA-C2-2026','claims':claims},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 with (OUT/'cilt2-unresolved-claims.csv').open('w',encoding='utf-8',newline='') as f:
  fields=['claim_id','page','section','target_package','current_state','linked_rules','next_action'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(unresolved)
 counts={}
 for r in rows:counts[r['disposition']]=counts.get(r['disposition'],0)+1
 summary={'schema_version':1,'pages':len(rows),'pages_with_rule_links':sum(bool(r['linked_rule_ids']) for r in rows),'unique_linked_rules':len({x for r in rows for x in r['linked_rule_ids'].split('|') if x}),'disposition_counts':counts,'unresolved_claim_rows':len(unresolved),'blank_dispositions':sum(not r['disposition'] for r in rows),'completion_rule':'Cilt 2 tamamlanması için unresolved_claim_rows sıfır olmalı'}
 (OUT/'coverage-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
