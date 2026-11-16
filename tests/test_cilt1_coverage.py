import csv,json
from pathlib import Path

def test_cilt1_p1_p6_coverage_and_claims():
 b=Path('research/experiments/cilt1-completion');pages=list(csv.DictReader((b/'cilt1-page-coverage.csv').open()));reg=json.loads((b/'cilt1-claim-registry.json').read_text());summary=json.loads((b/'coverage-summary.json').read_text())
 assert len(pages)==139 and {int(x['page']) for x in pages}==set(range(1,140))
 assert summary['atomic_claims']==len(reg['claims'])>=139 and summary['blank_dispositions']==0
 measured=[x for x in reg['claims'] if x['disposition']!='reference_only']
 assert measured and all(x['linked_rules'] and x['mathematical_definition']!='Henüz ilgili çalışma paketinde kesinleştirilecek.' for x in measured)
 assert summary['packages_completed']==list(range(1,13))


def test_cilt1_final_unresolved_is_empty():
 b=Path('research/experiments/cilt1-completion'); assert len(list(csv.DictReader((b/'cilt1-unresolved-claims.csv').open())))==0
