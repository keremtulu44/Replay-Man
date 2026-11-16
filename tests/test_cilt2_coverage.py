import csv,json
from pathlib import Path

def test_cilt2_coverage_has_every_page_and_no_blank_disposition():
    base=Path('research/experiments/cilt2-completion')
    rows=list(csv.DictReader((base/'cilt2-page-coverage.csv').open(encoding='utf-8')))
    assert len(rows)==109
    assert {int(r['page']) for r in rows}==set(range(1,110))
    assert all(r['card_id'] and r['disposition'] and r['coverage_state'] and r['target_package'] for r in rows)

def test_cilt2_claims_and_summary_match_coverage():
    base=Path('research/experiments/cilt2-completion')
    registry=json.loads((base/'cilt2-claim-registry.json').read_text())
    summary=json.loads((base/'coverage-summary.json').read_text())
    assert summary['pages']==109
    assert len(registry['claims'])==summary['atomic_claims']>=109
    assert summary['blank_dispositions']==0
    assert len({c['claim_id'] for c in registry['claims']})==len(registry['claims'])
