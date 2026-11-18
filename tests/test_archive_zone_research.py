from tools.archive_zone_research import digest, verify_references


def test_recorded_hash_references_detect_missing_and_corrupt(tmp_path):
    path = tmp_path/'source.csv'
    path.write_text('bar,close\n1,20\n',encoding='utf-8')
    wanted = digest(path)
    assert verify_references([(str(path), wanted)]) == []
    path.write_text('bar,close\n1,21\n',encoding='utf-8')
    failures = verify_references([(str(path), wanted), (str(tmp_path/'missing.csv'), wanted)])
    assert [x['error'] for x in failures] == ['sha256_mismatch', 'missing']
