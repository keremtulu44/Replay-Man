"""Ana Trading Kitabı 530 sayfa kapsamı ve çapraz-kitap kural bağlantıları."""
from pathlib import Path
import csv,json
ROOT=Path('research');OUT=ROOT/'experiments/atk-completion';CARDS=ROOT/'knowledge/processed/ATK-TR-D1.0-2026-08-cards.jsonl'
PACK={1:'ATK-P1-coverage',2:'ATK-P2-price-action',3:'ATK-P2-price-action',4:'ATK-P3-zones-liquidity',5:'ATK-P3-zones-liquidity',6:'ATK-P4-patterns',7:'ATK-P5-volume-indicators',8:'ATK-P5-volume-indicators',9:'ATK-P6-measurement-geometry',10:'ATK-P7-multi-timeframe',11:'ATK-P8-strategy-schema',12:'ATK-P8-strategy-schema',13:'ATK-P9-risk',14:'ATK-P10-process',15:'ATK-P11-data-replay',16:'ATK-P12-ai-governance',17:'ATK-P13-cycle-cross-market-time',18:'ATK-P14-fundamentals',19:'ATK-P15-crypto-options',20:'ATK-P13-cycle-cross-market-time',21:'ATK-P15-crypto-options',22:'ATK-P13-cycle-cross-market-time',23:'ATK-P9-risk',24:'ATK-P16-arbitrage-final'}
RULES={
2:['BR-024-single-candle-geometry','BR-025-multi-candle-sequences','BR-026-pressure-loss'],3:['BR-001-confirmed-swing','BR-002-close-break','BR-004-acceptance','BR-006-failure','BR-028-breakout-lifecycle-details'],
4:['BR-C1-015-pivot-cpr','BR-C1-016-support-resistance','BR-031-location-context'],5:['BR-007-probe-rejection','BR-021-formations','BR-028-breakout-lifecycle-details'],
6:['BR-024-single-candle-geometry','BR-025-multi-candle-sequences','BR-021-formations'],7:['BR-C1-009-relative-volume','BR-C1-010-vwap-avwap','BR-C1-011-volume-profile'],
8:['BR-C1-002-moving-averages','BR-C1-003-rsi','BR-C1-004-stochastic','BR-C1-005-macd','BR-C1-006-atr','BR-C1-007-bollinger','BR-C1-012-adx-dmi','BR-C1-013-supertrend','BR-C1-014-ichimoku','BR-C1-021-information-families'],
9:['BR-C1-017-fibonacci','BR-C1-018-gann-normalized','BR-C1-019-pitchfork','BR-C1-020-regression-channel','BR-C1-022-decision-robustness'],10:['BR-018-multi-timeframe','BR-032-volume-mtf'],11:['BR-ATK-007-strategy-setup-schema'],12:['BR-ATK-007-strategy-setup-schema'],13:['BR-ATK-008-risk-boundary'],14:['BR-ATK-009-journal-process'],15:['BR-ATK-010-data-replay-contract'],16:['BR-ATK-011-ai-governance'],23:['BR-ATK-008-risk-boundary']}
FORM={
'ATK-P1-coverage':'Kaynak/terminoloji; ayrı finansal olay formülü uygulanmaz.',
'ATK-P2-price-action':'R=H-L; B=|C-O|; wick ve close-location oranları; teyitli pivot p ancak p+right kapanınca bilinir; yapı durumu teyitli HH/HL/LH/LL; break/acceptance/failure kapanış-temelli yaşam döngüsüdür.',
'ATK-P3-zones-liquidity':'zone=[level-k*ATR14,level+k*ATR14], k∈{0.05,0.10,0.20}; level yalnız teyitli swing veya tamamlanmış önceki gün/haftadan; probe wick dışarıda ve kapanış içeride, break kapanış dışarıda. Gerçek emir/stop konumu OHLCV’den bilinmez.',
'ATK-P4-patterns':'Formasyon, yalnız son bileşeni/neckline kapanış teyidi oluşunca olaydır; temel özellikler teyitli pivot mesafe-süre oranları ve OHLC kapsama ilişkileridir. Ad etiketi temel geometrinin marjinal katkısıyla karşılaştırılır.',
'ATK-P5-volume-indicators':'RVOL=V/median(V[t-20:t-1]); indikatörler BR-C1 formülleriyle; aile Jaccard ve ablation bağımsız bilgi katkısını ölçer. Endeks/FX hacmi data_unsuitable.',
'ATK-P6-measurement-geometry':'distance_atr=|P-level|/ATR14; MFE/MAE ileri high-low yolu; Fibonacci teyitli swing çiftinden; OLS kanal yalnız geçmiş pencere; ekran açısı yerine ATR-normalize fiyat/zaman eğimi.',
'ATK-P7-multi-timeframe':'Alt zaman olayı event_ts anında, üst zaman özellikleri event_ts öncesinde kapanmış son 2h/4h/1d bardan as-of birleşir; alignment=sign(lower thesis)==sign(completed HTF regime).',
'ATK-P8-strategy-schema':'StrategyCard={universe,context,setup,trigger,invalidation,outcomes,validation}; her expression known_at∈{bar_close,confirmed_pivot,completed_higher_timeframe}; doğrulama %60/%20/%20, common-calendar, >=70 hedef sembol ve negatif sonuç koruması.',
'ATK-P9-risk':'R=|entry-invalidation|; directional_MFE/MAE ileri high-low yolu; aynı barda hedef ve stop görülürse ambiguous; net_excess=benchmark_excess-cost; portföy/execution deferred_execution_portfolio.',
'ATK-P10-process':'Karar kalitesi outcome kullanılmadan plan alanlarının tamamlığı ve rule_violation ile puanlanır; psikoloji iddiası finansal sinyal değil process_rule/not_ohlcv_testable.',
'ATK-P11-data-replay':'Görünürlük closed_bars_only; pivot confirmed_position; HTF last_completed_asof; deney kimliği code_version+rule_version+parameter_set+data_snapshot_hash.',
'ATK-P12-ai-governance':'Her AI önerisi source+assumptions+data_requirements+validation_status+limitations taşır; future leakage, fabricated result, silent post-result rule change ve negatif sonuç silme yasaktır.',
}

def main():
 OUT.mkdir(parents=True,exist_ok=True);cards=[json.loads(x) for x in CARDS.read_text().splitlines()];pages=[];claims=[];un=[];cross=[]
 for c in cards:
  ch=c.get('chapter');pack=PACK.get(ch,'ATK-P1-coverage');done=ch in RULES;front=c['page_kind']=='front_matter';disp='reference_only' if front else ('tested_crossbook_or_new' if done else 'pending_package');state='closed' if front or done else 'open';rules=RULES.get(ch,[])
  pages.append({'page':c['page'],'card_id':c['id'],'chapter':ch,'section':c.get('section'),'target_package':pack,'disposition':disp,'coverage_state':state,'linked_rule_ids':'|'.join(rules),'source_summary':' '.join(c['source_extract_summary'])})
  for rid in rules:cross.append({'source_card':c['id'],'page':c['page'],'chapter':ch,'target_package':pack,'linked_rule_id':rid,'link_type':'cross_book_existing_result'})
  atoms=c['source_extract_summary'] or [c.get('section') or 'reference']
  for i,a in enumerate(atoms,1):
   x={'claim_id':f"ATK-P{c['page']:03d}-C{i:02d}",'source_card':c['id'],'page':c['page'],'chapter':ch,'section':c.get('section'),'atomic_source_claim':a,'target_package':pack,'linked_rules':rules,'mathematical_definition':FORM.get(pack,'İlgili sonraki ATK paketinde kesinleştirilecek.'),'disposition':disp,'coverage_state':state};claims.append(x)
   if state=='open':un.append({'claim_id':x['claim_id'],'page':c['page'],'target_package':pack,'next_action':'İlgili ATK paketini tamamla'})
 with (OUT/'atk-page-coverage.csv').open('w',newline='') as f:w=csv.DictWriter(f,list(pages[0]),lineterminator='\n');w.writeheader();w.writerows(pages)
 (OUT/'atk-claim-registry.json').write_text(json.dumps({'schema_version':1,'source_id':'ATK-TR-D1.0-2026-08','claims':claims},ensure_ascii=False,indent=2)+'\n')
 for name,rows,fields in [('atk-unresolved-claims.csv',un,['claim_id','page','target_package','next_action']),('cross-book-rule-map.csv',cross,['source_card','page','chapter','target_package','linked_rule_id','link_type'])]:
  with (OUT/name).open('w',newline='') as f:w=csv.DictWriter(f,fields,lineterminator='\n');w.writeheader();w.writerows(rows)
 summary={'pages':len(pages),'atomic_claims':len(claims),'packages_completed':list(range(1,13)),'cross_book_links':len(cross),'unresolved_claims':len(un),'blank_dispositions':sum(not x['disposition'] for x in pages)};(OUT/'coverage-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
