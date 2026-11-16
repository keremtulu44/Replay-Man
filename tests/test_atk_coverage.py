import csv,json
from pathlib import Path

def test_atk_p1_p7_coverage():
 b=Path('research/experiments/atk-completion');pages=list(csv.DictReader((b/'atk-page-coverage.csv').open()));reg=json.loads((b/'atk-claim-registry.json').read_text());s=json.loads((b/'coverage-summary.json').read_text())
 assert len(pages)==530 and {int(x['page']) for x in pages}==set(range(1,531))
 assert len(reg['claims'])==s['atomic_claims']>=530 and s['blank_dispositions']==0
 assert s['packages_completed']==list(range(1,17)) and s['cross_book_links']>0
 measured=[x for x in reg['claims'] if x['disposition']!='reference_only']
 assert measured and all(x['linked_rules'] and not x['mathematical_definition'].startswith('İlgili') for x in measured)

def test_atk_p2_p7_results_exist():
 m=Path('research/measurements/atk-p2-p7');r=Path('research/experiments/atk-rule-results')
 assert {'zone_event_study.csv','zone_symbol_results.csv','cross_book_measurement_inventory.csv','summary.json'} <= {x.name for x in m.iterdir()}
 registry=json.loads((r/'registry.json').read_text())['rules'];assert len(registry)==15 and all(Path(x['result_directory']).exists() for x in registry)
 assert len(list(csv.DictReader(Path('research/experiments/atk-completion/atk-unresolved-claims.csv').open())))==0
