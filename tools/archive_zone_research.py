"""Bölge araştırmasının dosya manifestini ve kaynak bütünlüğü kaydını üretir.

Kopya veya Git işlemi yapmaz; mevcut sonuçları değiştirmez. Manifestteki
SHA-256 değerleri içerik kimliğidir, bilimsel doğrulama veya yedek değildir.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT=Path('research/measurements/zone-memory')
MANIFEST='KAYIT-DOSYA-MANIFEST.sha256'
STATUS='KAYIT-DURUMU.json'
TOOLS=['analyze_lifecycle_filters.py','analyze_lifecycle_ten_filters.py','analyze_zone_philosophy.py',
       'archive_zone_research.py','compact_lifecycle.py','compare_zone_movement.py','describe_zone_paths.py',
       'evaluate_f01_matching.py','investigate_f01_reasons.py','measure_f01_censoring.py','measure_movement_character.py','measure_zone_lifecycle.py','measure_zone_memory.py',
       'measure_zone_universe.py','report_zone_evidence.py','summarize_behavior_pilot.py','summarize_lifecycle.py']
MODULES=['behavior_zones.py','movement_character.py','sloped_zones.py','zone_lifecycle.py','zone_memory.py',
         'replay.py','swings.py']
TESTS=['test_archive_zone_research.py','test_behavior_zones.py','test_compare_zone_movement.py','test_describe_zone_paths.py',
       'test_f01_research.py','test_f01_reasons.py','test_lifecycle_filters.py','test_lifecycle_ten_filters.py','test_movement_character.py',
       'test_sloped_zones.py','test_summarize_lifecycle.py','test_zone_lifecycle.py','test_zone_memory.py',
       'test_zone_philosophy.py','test_zone_research.py']


def digest(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def verify_references(references, cache=None):
    """Liste hâlindeki (path, beklenen hash) kaynaklarını kontrol et."""
    cache={} if cache is None else cache
    issues=[]
    for path, expected in references:
        p=Path(path)
        if not p.is_file():
            issues.append({'path':str(p),'error':'missing'});continue
        actual=cache.setdefault(str(p),None)
        if actual is None:
            actual=digest(p);cache[str(p)]=actual
        if actual != expected:
            issues.append({'path':str(p),'error':'sha256_mismatch','expected':expected,'actual':actual})
    return issues


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);args=p.parse_args(argv)
    root=args.root
    refs=[]; csv_manifests=[]
    for pattern in ('*/input-manifest.csv','*/benchmark-manifest.csv'):
        for manifest in sorted(root.glob(pattern)):
            csv_manifests.append(str(manifest))
            with manifest.open(newline='',encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    if row.get('path') and row.get('sha256'):
                        refs.append((row['path'],row['sha256']))
    json_count=0
    for path in sorted(root.glob('*/summary.json')):
        data=json.loads(path.read_text(encoding='utf-8'))
        json_count+=1
        # F01 analizleri tekil giriş ve manifestlerini liste yerine alanlarda tutar.
        if data.get('input_path') and data.get('input_sha256'):
            refs.append((data['input_path'],data['input_sha256']))
        if path.parent.name in {'f01-matched','f01-censoring','f01-reasons'}:
            if data.get('input_manifest_sha256'):
                refs.append((str(root/'lifecycle-horizontal/input-manifest.csv'),data['input_manifest_sha256']))
            if data.get('reference_events_sha256'):
                refs.append((str(root/'lifecycle-horizontal/events.csv.xz'),data['reference_events_sha256']))
            script={'f01-matched':'evaluate_f01_matching.py','f01-censoring':'measure_f01_censoring.py',
                    'f01-reasons':'investigate_f01_reasons.py'}[path.parent.name]
            if data.get('code_sha256'):
                refs.append((str(Path('tools')/script),data['code_sha256']))
            for field, filename in [('loader_sha256','replay.py'),('lifecycle_sha256','zone_lifecycle.py'),('scanner_sha256','zone_memory.py')]:
                if data.get(field):refs.append((str(Path('replayman')/filename),data[field]))
            for field, filename in [('comparison_sha256','summarize_lifecycle.py'),('censor_logic_sha256','measure_f01_censoring.py')]:
                if data.get(field):refs.append((str(Path('tools')/filename),data[field]))
        for field in ('inputs','benchmark_inputs'):
            items=data.get(field,[])
            if not isinstance(items,list):continue
            for item in items:
                if isinstance(item,dict) and item.get('path') and item.get('sha256'):
                    refs.append((item['path'],item['sha256']))
                    if item.get('manifest_sha256'):
                        refs.append((str(Path(item['path']).parent/'input-manifest.csv'),item['manifest_sha256']))
    # Kaydedilen yaşam döngüsü koşularının gerçek motor sürümü ayrıca saklıdır.
    for folder in sorted(root.glob('lifecycle-*')):
        summary=folder/'summary.json'
        if not summary.exists():continue
        code=json.loads(summary.read_text(encoding='utf-8')).get('code_sha256')
        if isinstance(code,dict) and 'zone_lifecycle.py' in code:
            refs.append((str(root/'sources/zone_lifecycle-recorded.py'),code['zone_lifecycle.py']))
    if not refs:raise ValueError('Kontrol edilecek kaynak manifesti yok')
    cache={};issues=verify_references(refs,cache)
    if issues:
        print(json.dumps({'status':'failed','issues':issues},ensure_ascii=False,indent=2))
        return 1
    research=[x for x in root.rglob('*') if x.is_file() and x.name not in (MANIFEST,STATUS)]
    code=[Path('tools')/x for x in TOOLS]+[Path('replayman')/x for x in MODULES]+[Path('tests')/x for x in TESTS]
    code.append(Path('research/plans/bolge-hafizasi-hareket-karakteri.md'))
    missing=[str(x) for x in code if not x.is_file()]
    if missing:raise FileNotFoundError(', '.join(missing))
    # Fiyat ve XU100 kaynaklarının tamamı diğer dosyalardan ayrı da listelenir.
    price=[Path(x) for x in cache if x.startswith('data/ohlcv/')]
    files=sorted(set(research+code+price),key=lambda x:x.as_posix())
    status={'status':'passed','csv_manifest_files':len(csv_manifests),'json_summaries_scanned':json_count,
            'recorded_hash_references_checked':len(refs),'unique_referenced_files':len(cache),
            'price_and_benchmark_files':len(price),'research_files':len(research),'code_plan_test_files':len(code),
            'manifest_files_including_status':len(files)+1,'issues':[],
            'scope':'Kaynak manifestlerinde belirtilen dosya hashleri ve araştırma kayıtlarının envanteri; veri doğruluğu, tüm tarihsel kod sürümleri veya GitHub yedeği değildir.'}
    status_path=root/STATUS
    status_path.write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    files=sorted(files+[status_path],key=lambda x:x.as_posix())
    lines=[]
    for file in files:
        val=cache.get(str(file)) or digest(file)
        lines.append(f'{val}  {file.as_posix()}\n')
    (root/MANIFEST).write_text(''.join(lines),encoding='utf-8')
    print(json.dumps(status,ensure_ascii=False,indent=2))
    return 0


if __name__=='__main__':raise SystemExit(main())
