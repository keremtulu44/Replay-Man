from tools.audit_research_completion import audit

def test_all_books_and_rules_pass_final_audit():
 report=audit()
 assert report['status']=='passed',report['errors']
 assert set(report['books'])=={'CILT1','CILT2','ATK'}
 assert sum(x['pages'] for x in report['books'].values())==778
 assert report['rules_total']==report['unique_rules']==71
