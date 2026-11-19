import json
import tarfile
from pathlib import Path

import pytest

from tools import archive_forward_research as archive


def fixture_workspace(tmp_path: Path):
    root = tmp_path / 'data' / 'ohlcv'
    relative = 'bist_equities/BIST_X/id/bars/1d.csv'
    data = root / relative
    data.parent.mkdir(parents=True)
    data.write_bytes(b'ts_utc,close\n2026-01-01,1\n')
    policy = data.parent.parent / 'series.json'
    policy.write_bytes(b'{"policy":"raw"}\n')
    code = tmp_path / 'replayman' / 'sample.py'
    code.parent.mkdir(parents=True)
    code.write_text('x = 1\n')
    freeze = tmp_path / archive.FREEZE_NAME
    freeze.parent.mkdir(parents=True)
    m = {'schema_version': 1, 'frozen_at_utc': '2026-11-19T14:00:00Z',
         'forward_start_utc': '2026-11-19T21:00:00Z', 'runtime': {'python': '3.11.2'},
         'code_sha256': {'replayman/sample.py': archive.digest(code.read_bytes())},
         'baseline_files': [{'asset_id': 'BIST_X', 'series_id': 'id', 'interval': '1d',
                             'relative_path': relative, 'sha256': archive.digest(data.read_bytes()),
                             'series_manifest_sha256': archive.digest(policy.read_bytes())}]}
    freeze.write_text(json.dumps(m))
    snap = tmp_path / archive.SNAPSHOT_NAME
    snap.mkdir(parents=True)
    (snap / 'signals.csv').write_text('signal_id\n')
    initial = {'status': 'blocked_data', 'freeze_sha256': archive.digest(freeze.read_bytes()),
               'files_sha256': {'signals.csv': archive.digest((snap / 'signals.csv').read_bytes())}}
    (snap / 'manifest.json').write_text(json.dumps(initial))
    return root, data, freeze, snap


def test_archive_verifies_freeze_sources_and_refuses_overwrite(tmp_path):
    root, data, freeze, snap = fixture_workspace(tmp_path)
    target = tmp_path / 'out' / 'snapshot.tar.gz'
    result = archive.create_archive(target, tmp_path, root, freeze, snap, extras=())
    assert result['status'] == 'verified' and result['baseline_series'] == 1
    assert result['initial_status'] == 'blocked_data'
    assert not result['external_timestamp_attestation']
    assert archive.verify_archive(target, expected_sha256=result['sha256'])['freeze_sha256'] == archive.digest(freeze.read_bytes())
    assert Path(str(target) + '.sha256').exists()
    with pytest.raises(FileExistsError):
        archive.create_archive(target, tmp_path, root, freeze, snap, extras=())
    with pytest.raises(ValueError, match='SHA-256'):
        archive.verify_archive(target, expected_sha256='0' * 64)
    data.write_bytes(b'changed')
    with pytest.raises(ValueError, match='hash'):
        archive.create_archive(tmp_path / 'other.tar.gz', tmp_path, root, freeze, snap, extras=())
    assert not (tmp_path / 'other.tar.gz').exists()


def test_matching_rewritten_internal_index_does_not_override_frozen_hash(tmp_path):
    root, _, freeze, snap = fixture_workspace(tmp_path)
    good = tmp_path / 'good.tar.gz'
    archive.create_archive(good, tmp_path, root, freeze, snap, extras=())
    with tarfile.open(good, 'r:gz') as tar:
        content = {m.name: tar.extractfile(m).read() for m in tar.getmembers()}
    data_name = next(n for n in content if n.endswith('/bars/1d.csv'))
    content[data_name] = b'changed but index rehashed'
    index = json.loads(content[archive.INDEX_NAME])
    for row in index['files']:
        if row['path'] == data_name:
            row['sha256'] = archive.digest(content[data_name])
            row['bytes'] = len(content[data_name])
    content[archive.INDEX_NAME] = json.dumps(index).encode()
    bad = tmp_path / 'bad.tar.gz'
    with tarfile.open(bad, 'w:gz') as tar:
        for name, value in content.items():
            archive._tar_entry(tar, name, value)
    with pytest.raises(ValueError, match='ısınma girdisi'):
        archive.verify_archive(bad)


def test_snapshot_tampering_and_unsafe_paths_are_rejected(tmp_path):
    root, _, freeze, snap = fixture_workspace(tmp_path)
    (snap / 'signals.csv').write_text('tampered')
    with pytest.raises(ValueError, match='hash'):
        archive.create_archive(tmp_path / 'bad.tar.gz', tmp_path, root, freeze, snap, extras=())
    for name in ('../escape', '/absolute', 'a/../b', 'a\\b', 'a//b'):
        with pytest.raises(ValueError, match='Güvensiz'):
            archive.safe_name(name)
