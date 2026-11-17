import csv
import hashlib
import pytest
from tools.organize_market_context import export

FIELDS=['source_id','source_group','source_symbol','time_split','jump_filter','target_group','target_symbol','n','negative_count','negative_rate']


def write_input(root,rows):
    with (root/'hisse-ozet.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)


def read(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))


def test_split_preserves_rows_hash_and_no_stale_outputs(tmp_path):
    def row(src,group,symbol,target,n):
        return {'source_id':src,'source_group':group,'source_symbol':symbol,'time_split':'total','jump_filter':'all','target_group':'bist_equities','target_symbol':target,'n':n,'negative_count':'7','negative_rate':'0.7'}
    rows=[row('IDX_XU100','bist_indices','XU100.IS','A.IS','10'),row('FX_USDTRY','fx','TRY=X','A.IS','10'),row('IDX_XU100','bist_indices','XU100.IS','B.IS','')]
    write_input(tmp_path,rows);count=export(tmp_path);archive=tmp_path/'kaynak-arsivi'
    assert count=={'IDX_XU100':2,'FX_USDTRY':1}
    assert read(archive/'bist-endeksleri/IDX_XU100.csv')==[rows[0],rows[2]]
    assert read(archive/'doviz-kurlari/FX_USDTRY.csv')==[rows[1]]
    for record in read(archive/'dosya-kontrol.csv'):
        p=tmp_path/record['dosya'];assert hashlib.sha256(p.read_bytes()).hexdigest()==record['sha256']
        assert int(record['veri_satiri'])==len(read(p))
    write_input(tmp_path,[rows[0],rows[2]])
    with pytest.raises(ValueError,match='eski dosyalar'):export(tmp_path)


def test_bad_group_and_invalid_source_id_do_not_write(tmp_path):
    row=dict(source_id='../bad',source_group='fx',source_symbol='X',time_split='total',jump_filter='all',target_group='bist_equities',target_symbol='A',n='1',negative_count='0',negative_rate='0')
    write_input(tmp_path,[row])
    with pytest.raises(ValueError,match='Geçersiz kaynak'):export(tmp_path)
    assert not (tmp_path/'kaynak-arsivi').exists()
