import csv
import gzip
import hashlib
from pathlib import Path

import pytest

from tools.organize_macro_risk import export

FIELDS = ['source_id', 'source_symbol', 'time_split', 'jump_filter', 'target_group', 'n', 'negative_count', 'negative_rate']


def write_input(root, rows):
    with gzip.open(root/'risk-table.csv.gz', 'wt', encoding='utf-8', newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)


def read_csv(path):
    opener=gzip.open if str(path).endswith('.gz') else Path.open
    with opener(path, 'rt', encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def test_export_preserves_all_rows_and_summary_filters_and_hashes(tmp_path):
    def row(asset, split='total', jump='all', group='bist_equities', n='10'):
        return dict(source_id=asset,source_symbol='X',time_split=split,jump_filter=jump,
                    target_group=group,n=n,negative_count='7',negative_rate='0.7')
    rows=[row('METAL_GOLD'), row('METAL_GOLD','test'), row('METAL_GOLD',jump='no_jump10'),
          row('METAL_GOLD',group='bist_indices'), row('OIL_BRENT',n='')]
    write_input(tmp_path,rows)
    counts=export(tmp_path)
    archive=tmp_path/'emtia-arsivi';gold=archive/'madenler/altin'
    assert counts['METAL_GOLD']=={'full':4,'summary':1}
    assert read_csv(gold/'tum-sonuclar.csv.gz')==rows[:4]
    assert read_csv(gold/'ozet-hisseler.csv')==rows[:1]
    assert read_csv(archive/'petrol/brent/tum-sonuclar.csv.gz')==rows[4:]
    for record in read_csv(archive/'dosya-kontrol.csv'):
        path=tmp_path/record['dosya']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256']
        assert int(record['veri_satiri'])==len(read_csv(path))
    # A rerun must not silently leave obsolete, apparently current source files.
    write_input(tmp_path, rows[:4])
    with pytest.raises(ValueError,match='eski kaynaklar'):
        export(tmp_path)


def test_unknown_source_is_not_silently_dropped(tmp_path):
    write_input(tmp_path,[dict(source_id='UNKNOWN',source_symbol='X',time_split='total',jump_filter='all',target_group='bist_equities',n='0',negative_count='0',negative_rate='')])
    with pytest.raises(ValueError,match='Bilinmeyen'):
        export(tmp_path)
    assert not (tmp_path/'emtia-arsivi').exists()
