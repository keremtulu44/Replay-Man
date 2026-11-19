import json

import pandas as pd
import pytest

from tools.audit_dip_results import verify_hashes
from tools.measure_dip_pilot import sha256


def test_input_hash_tampering_fails_closed(tmp_path):
    code = tmp_path / 'code.py'; code.write_text('ok')
    data = tmp_path / 'bars.csv'; data.write_text('one')
    (tmp_path / 'run_metadata.json').write_text(json.dumps({'code_sha256': {str(code): sha256(code)}}))
    pd.DataFrame([{'path': str(data), 'sha256': sha256(data)}]).to_csv(tmp_path / 'input_manifest.csv', index=False)
    assert verify_hashes(tmp_path) == 1
    data.write_text('different')
    with pytest.raises(ValueError, match='Girdi hash'):
        verify_hashes(tmp_path)
