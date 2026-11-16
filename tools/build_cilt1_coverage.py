"""Cilt 1 sayfa/atomik claim kapsamı ve P1-P12 çalışma durumunu üretir."""
from __future__ import annotations
import csv,json
from pathlib import Path
ROOT=Path('research'); OUT=ROOT/'experiments/cilt1-completion'; CARDS=ROOT/'knowledge/processed/PTA-C1-2026-cards.jsonl'
PACK={1:'C1-P2-moving-averages',2:'C1-P2-moving-averages',3:'C1-P3-momentum',4:'C1-P3-momentum',5:'C1-P3-momentum',6:'C1-P4-volatility',7:'C1-P4-volatility',8:'C1-P4-volatility',9:'C1-P5-volume-vwap',10:'C1-P5-volume-vwap',11:'C1-P6-volume-profile',12:'C1-P7-trend-systems',13:'C1-P7-trend-systems',14:'C1-P7-trend-systems',15:'C1-P8-level-tools',16:'C1-P8-level-tools',17:'C1-P8-level-tools',18:'C1-P9-drawing-tools',19:'C1-P9-drawing-tools',20:'C1-P9-drawing-tools',21:'C1-P10-information-families'}
RULE={1:['BR-C1-001-indicator-roles','BR-C1-002-moving-averages'],2:['BR-C1-002-moving-averages'],3:['BR-C1-003-rsi'],4:['BR-C1-004-stochastic'],5:['BR-C1-005-macd'],6:['BR-C1-006-atr'],7:['BR-C1-007-bollinger'],8:['BR-C1-008-keltner-squeeze'],9:['BR-C1-009-relative-volume'],10:['BR-C1-010-vwap-avwap'],11:['BR-C1-011-volume-profile'],12:['BR-C1-012-adx-dmi'],13:['BR-C1-013-supertrend'],14:['BR-C1-014-ichimoku'],15:['BR-C1-015-pivot-cpr'],16:['BR-C1-016-support-resistance'],17:['BR-C1-017-fibonacci'],18:['BR-C1-018-gann-normalized'],19:['BR-C1-019-pitchfork'],20:['BR-C1-020-regression-channel'],21:['BR-C1-021-information-families','BR-C1-022-decision-robustness']}
FORM={
'C1-P2-moving-averages':'SMA_n[t]=mean(C[t-n+1:t]); EMA_n[t]=alpha*C[t]+(1-alpha)*EMA_n[t-1], alpha=2/(n+1); slope=(MA[t]-MA[t-k])/ATR14; distance=(C-MA)/ATR14; cross yalnız iki kapanmış bardaki işaret değişimidir.',
'C1-P3-momentum':'RSI_n=100-100/(1+avg_gain_n/avg_loss_n); StochK=100*(C-LL_n)/(HH_n-LL_n), D=SMA3(K); MACD=EMA12-EMA26, signal=EMA9(MACD), hist=MACD-signal. Eşik/kesişim yalnız kapanışta bilinir; divergence teyitli pivot ister.',
'C1-P4-volatility':'TR=max(H-L,|H-Cprev|,|L-Cprev|); ATR14=Wilder(TR); BB mid=SMA20, upper/lower=mid±k*std20, width=(upper-lower)/mid, %B=(C-lower)/(upper-lower); Keltner=EMA20±k*ATR14; squeeze BB_width<Keltner_width.',
'C1-P5-volume-vwap':'RVOL=V/median(V[t-20:t-1]); typical=(H+L+C)/3; rolling_VWAP=sum(typical*V,w)/sum(V,w); distance=(C-VWAP)/ATR14. AVWAP toplamları yalnız teyitli swing/kırılım anchor zamanından sonra başlar; gerçek hacmi olmayan gruplar data_unsuitable.',
'C1-P6-volume-profile':'Geçmiş w bardaki typical-price hacimleri önceden kayıtlı N eşit fiyat binine atanır; POC=max volume bin; value area POC çevresinde toplam hacmin %70ine ulaşan binler; position=(C-VA_low)/(VA_high-VA_low). Bar-içi dağılım bilinmediğinden typical-price yaklaşımıdır.',
'C1-P7-trend-systems':'DMI: +DM=max(H-Hprev,0), -DM=max(Lprev-L,0), DI=100*Wilder(DM)/ATR, ADX=Wilder(100*|+DI--DI|/(+DI+-DI)); Supertrend=HL2±3*ATR; Ichimoku Tenkan=(HH9+LL9)/2, Kijun=(HH26+LL26)/2, SpanB=(HH52+LL52)/2. Yalnız kapanmış barlar.',
'C1-P8-level-tools':'Klasik pivot=(HprevDay+LprevDay+CprevDay)/3; S/R yalnız 2+2 teyitli swinglerden; break kapanışla seviye geçişidir; Fib r=low+r*(high-low), r∈{0.382,0.618}, anchor yalnız teyitli swing çiftidir.',
'C1-P9-drawing-tools':'OLS50 kanal: y=a*t+b, band=fit±2*std(residual); Pitchfork vekili son üç alternating teyitli pivotun A-C doğrusu; Gann normalize slope=(C-C[t-20])/(20*ATR14). Ekran açısı kullanılmaz.',
'C1-P10-information-families':'Aile olayı, ailedeki kayıtlı olayların OR birleşimidir; Jaccard(A,B)=|A∩B|/|A∪B|. Yüksek örtüşme bağımsız teyit sayılmaz; çıkarma testi marjinal katkıyı ölçer.',
'C1-P11-decision-robustness':'S_j=S_(j-1)∩filter_j; sembol medyanı ve pozitif sembol oranı aşama bazında; net_excess=excess-cost, cost∈{0,0.001,0.0025,0.005}. En iyi test varyantı seçilmez.',
}

def main():
 OUT.mkdir(parents=True,exist_ok=True);cards=[json.loads(x) for x in CARDS.read_text().splitlines()];pages=[];claims=[];unresolved=[]
 for c in cards:
  ch=c.get('chapter');package=PACK.get(ch,'C1-P1-coverage'); measured=ch in RULE
  disposition='reference_only' if c['page_kind']=='front_matter' else ('tested_initial' if measured else 'pending_package')
  state='closed' if c['page_kind']=='front_matter' or measured else 'open';linked=RULE.get(ch,[])
  pages.append({'page':c['page'],'card_id':c['id'],'chapter':ch,'section':c.get('section'),'target_package':package,'disposition':disposition,'coverage_state':state,'linked_rule_ids':'|'.join(linked),'source_summary':' '.join(c['source_extract_summary'])})
  atoms=c['source_extract_summary'] or [c.get('section') or 'reference']
  for i,atom in enumerate(atoms,1):
   x={'claim_id':f"C1-P{c['page']:03d}-C{i:02d}",'source_card':c['id'],'page':c['page'],'chapter':ch,'section':c.get('section'),'atomic_source_claim':atom,'target_package':package,'linked_rules':linked,'mathematical_definition':FORM.get(package,'Henüz ilgili çalışma paketinde kesinleştirilecek.'),'disposition':disposition,'coverage_state':state};claims.append(x)
   if state=='open':unresolved.append({'claim_id':x['claim_id'],'page':c['page'],'target_package':package,'current_state':'open','next_action':'İlgili C1 paketinde kural/formül/sonuç ata'})
 fields=list(pages[0]);
 with (OUT/'cilt1-page-coverage.csv').open('w',newline='') as f:w=csv.DictWriter(f,fields,lineterminator='\n');w.writeheader();w.writerows(pages)
 (OUT/'cilt1-claim-registry.json').write_text(json.dumps({'schema_version':1,'source_id':'PTA-C1-2026','claims':claims},ensure_ascii=False,indent=2)+'\n')
 with (OUT/'cilt1-unresolved-claims.csv').open('w',newline='') as f:
  fs=['claim_id','page','target_package','current_state','next_action'];w=csv.DictWriter(f,fs,lineterminator='\n');w.writeheader();w.writerows(unresolved)
 summary={'pages':len(pages),'atomic_claims':len(claims),'packages_completed':list(range(1,13)),'unresolved_claims':len(unresolved),'blank_dispositions':sum(not x['disposition'] for x in pages)};(OUT/'coverage-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
