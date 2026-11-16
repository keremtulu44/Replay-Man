"""Cilt 2'nin 109 sayfasını deney kuralı ve tamamlama paketlerine bağlar."""
from __future__ import annotations
import csv,json
from pathlib import Path

ROOT=Path('research');OUT=ROOT/'experiments/cilt2-completion';CARDS=ROOT/'knowledge/processed/PTA-C2-2026-cards.jsonl';REG=ROOT/'experiments/book-rule-results/registry.json'
PACKAGES={1:'C2-P2-single-candle',2:'C2-P2-single-candle',3:'C2-P4-pressure-quality',4:'C2-P3-multi-candle',5:'C2-P3-multi-candle',6:'C2-P5-compression-expansion',7:'C2-P6-breakout-lifecycle',8:'C2-P7-swing-geometry',9:'C2-P8-attempt-pullback',10:'C2-P8-attempt-pullback',11:'C2-P9-location-context',12:'C2-P10-volume-mtf',13:'C2-P11-decision-chain'}
CHAPTER_RULES={
 1:['BR-024-single-candle-geometry'],2:['BR-024-single-candle-geometry','BR-026-pressure-loss'],
 3:['BR-024-single-candle-geometry','BR-026-pressure-loss'],4:['BR-025-multi-candle-sequences'],5:['BR-025-multi-candle-sequences'],
 6:['BR-027-compression-expansion'],7:['BR-028-breakout-lifecycle-details'],8:['BR-029-swing-geometry'],
 9:['BR-030-second-attempt-pullback'],10:['BR-030-second-attempt-pullback'],11:['BR-031-location-context'],
 12:['BR-032-volume-mtf'],13:['BR-033-decision-chain','BR-034-robustness-cost-overlap'],
}
DEFINITIONS={
 'C2-P2-single-candle':'R=H-L; B=|C-O|; body_ratio=B/R; upper_wick=(H-max(O,C))/R; lower_wick=(min(O,C)-L)/R; close_location=(C-L)/R; size_atr=R/ATR14. Olay yalnız mum kapanınca bilinir; adlandırılmış eşikler önceden kayıtlı varyantlardır.',
 'C2-P3-multi-candle':'Ardışık kapanmış mumlarda engulfing/inside/harami/star/devam koşulları O,H,L,C kapsama ve yön ilişkileriyle kurulur; olay zamanı dizinin son kapanışıdır. İleri yönlü sonuç sign*(C[t+h]/C[t]-1).',
 'C2-P4-pressure-quality':'body_decay=B[t]/median(B[t-k:t]); progress=direction*(extreme[t]-extreme[t-1])/ATR14; overlap=intersection(range[t],range[t-1])/min(R[t],R[t-1]); efficiency=|C[t]-C[t-k]|/sum(|ΔC|). Bileşen varyantları ayrı tutulur.',
 'C2-P5-compression-expansion':'width=(max(H,w)-min(L,w))/ATR14; overlap_density=mean(pairwise_overlap); compression: width<=3 ve overlap_density>=0.35, w∈{6,10,15}; close-break C sınır dışında, probe wick dışarıda fakat C içeride; karşı genişleme ilk kırılımın karşı sınırında kapanıştır.',
 'C2-P6-breakout-lifecycle':'distance_atr=|C-level|/ATR14; acceptance n∈{1,2,3} ardışık dış kapanış; outside_duration=t_event-t_break; failure_depth=eski_alana_giriş/ATR14; retest_speed=max_excursion/(ATR14*bar_sayısı); counter_expansion karşı kırılım sınırının kapanışla aşılmasıdır.',
 'C2-P7-swing-geometry':'Pivot high: H[p]>max(H[p-L:p]) ve H[p]>=max(H[p+1:p+R]); low simetriği; known_at=p+R. L=R∈{1,2,3,4,5,7}; equal extreme: |P-Pprev|<=k*ATR14, k∈{0.10,0.25,0.50}; leg speed=|ΔP|/bars; efficiency=|ΔP|/sum(|ΔC|).',
 'C2-P8-attempt-pullback':'distance_ratio=D2/D1; duration_ratio=T2/T1; speed_ratio=(D2/T2)/(D1/T1); new_extreme direction*Δextreme>k*ATR14; pullback_depth=counter_move/impulse_distance; çok bacak ardışık teyitli karşıt swinglerden sayılır. Olay ikinci bacağın bitiş teyidinde bilinir.',
 'C2-P9-location-context':'range_position=(C-rolling_min)/(rolling_max-rolling_min); level_distance=|C-confirmed_level|/ATR14; extension=move_range/ATR14; regime yalnız t anına kadar ADX/eğim/örtüşmeden; aynı olay location/regime bantlarında ayrı raporlanır.',
 'C2-P10-volume-mtf':'relative_volume=V/median(V[t-20:t-1]); volume usable yalnız gerçek pozitif hacimli gruplarda. Alt-zaman olayı için HTF özellikleri yalnız event_ts öncesinde kapanmış son 2h/4h/1d bardan as-of birleşir; eksik/temsili hacim data_unsuitable.',
 'C2-P11-decision-chain':'Aşama j için S_j=S_(j-1)∩filter_j; marginal_edge_j=median(excess_h|S_j)-median(excess_h|S_(j-1)); marginal_loss=1-|S_j|/|S_(j-1)|. Edge artmıyorsa aşama redundant_filter; maliyetli sonuç excess_net=excess-cost.',
 'C2-P1-coverage':'Ölçülebilir deney yok; ön/arka madde veya kaynak referansı. disposition=reference_only ve matematiksel tanım uygulanamaz.',
}
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
  package=PACKAGES.get(c.get('chapter'),'C2-P1-coverage')
  linked=sorted(by_card.get(c['id'],[])); text=(c.get('section') or '')+' '+c.get('source_excerpt','')
  is_ob_fvg=any(k in text.casefold() for k in ['order block','fvg','fair value gap'])
  if c['page_kind']=='front_matter': disposition='reference_only';state='closed'
  elif is_ob_fvg: disposition='deferred_ob_fvg';state='closed_deferred'
  elif c.get('chapter')==12: disposition='tested_or_data_unsuitable';state='closed'
  elif c.get('chapter') in PACKAGES: disposition='tested_or_context_classified';state='closed'
  else: disposition='reference_only';state='closed'
  # Kaynak sayfası doğrudan BR kaydında yoksa, test edilebilir claim'i o
  # bölüm için ölçümü yapan nihai BR kaydına bağla. Reference/deferred kayıtlar
  # deney kuralı değildir ve yapay BR kimliği almaz.
  if not linked and disposition not in {'reference_only','deferred_ob_fvg'}:
   linked=CHAPTER_RULES.get(c.get('chapter'),[])
  row={'page':c['page'],'card_id':c['id'],'chapter':c.get('chapter'),'section':c.get('section'),'page_kind':c['page_kind'],'relevance':c['relevance'],'topic_ids':'|'.join(t['id'] for t in c['topics']),'linked_rule_ids':'|'.join(linked),'target_package':package,'disposition':disposition,'coverage_state':state,'source_summary':' '.join(c['source_extract_summary']),'inference':c['inference'],'possible_uses':'|'.join(c['possible_uses'])}
  rows.append(row)
  atoms=c['source_extract_summary'] or [c.get('inference') or c.get('section') or 'reference']
  for atom_no,atom in enumerate(atoms,1):
   claim={'claim_id':f"C2-P{c['page']:03d}-C{atom_no:02d}",'source_card':c['id'],'page':c['page'],'chapter':c.get('chapter'),'section':c.get('section'),'atomic_source_claim':atom,'mathematical_definition':('Uygulanamaz: OB/FVG tanımı kullanıcının sistemi teslim edilene kadar deferred_ob_fvg.' if disposition=='deferred_ob_fvg' else DEFINITIONS[package]),'inference':c['inference'],'possible_uses':c['possible_uses'],'topics':[t['id'] for t in c['topics']],'linked_rules':linked,'target_package':package,'disposition':disposition,'coverage_state':state}
   claims.append(claim)
   if state in {'open','linked_needs_exhaustive_review'}:unresolved.append({'claim_id':claim['claim_id'],'page':c['page'],'section':c.get('section'),'target_package':package,'current_state':state,'linked_rules':'|'.join(linked),'next_action':'Atomik iddiaya sonuç disposition ata'})
 with (OUT/'cilt2-page-coverage.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerows(rows)
 (OUT/'cilt2-claim-registry.json').write_text(json.dumps({'schema_version':1,'source_id':'PTA-C2-2026','claims':claims},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 with (OUT/'cilt2-unresolved-claims.csv').open('w',encoding='utf-8',newline='') as f:
  fields=['claim_id','page','section','target_package','current_state','linked_rules','next_action'];w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(unresolved)
 counts={}
 for r in rows:counts[r['disposition']]=counts.get(r['disposition'],0)+1
 summary={'schema_version':1,'pages':len(rows),'atomic_claims':len(claims),'pages_with_rule_links':sum(bool(r['linked_rule_ids']) for r in rows),'unique_linked_rules':len({x for r in rows for x in r['linked_rule_ids'].split('|') if x}),'disposition_counts':counts,'unresolved_claim_rows':len(unresolved),'blank_dispositions':sum(not r['disposition'] for r in rows),'completion_rule':'Cilt 2 tamamlanması için unresolved_claim_rows sıfır olmalı'}
 (OUT/'coverage-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
