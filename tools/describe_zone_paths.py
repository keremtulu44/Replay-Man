"""Dört bölge türünde ziyaret içi kapanış yolları: sınırlı, betimleyici pilot.

Girdi kaynak pilotlarıdır. Bu çalışma kapanış vekillerini sınıflar; bar içi
sıralama, al/sat sonucu veya bölgeler arası geometrik ilişki iddia etmez.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

FOLDERS = {'yatay':'pilot-4h-atr025', 'oyalanma':'pilot-multiframe-dwell-atr025',
           'hizli_cikis':'pilot-multiframe-impulse-atr025', 'egimli':'pilot-4h-sloped-atr025'}
ASSETS = ['BIST_ASELS','BIST_THYAO','BIST_TUPRS']


def summarize_visit(visit: dict, events: pd.DataFrame, next_start, last_pos: int, horizon: int = 10):
    """Yalnız gözlenen mum olayları; 2 dış kapanış aynı tarafta değilse belirsiz."""
    if horizon < 1:
        raise ValueError('Ufuk pozitif olmalı')
    e = events.sort_values('position', kind='stable')
    touches = e.loc[e.event == 'touch_bar', 'position'].drop_duplicates()
    ends = e[e.event == 'visit_end']
    if len(ends) > 1:
        raise ValueError('Bir ziyaretin birden fazla bitişi var')
    end_pos = int(ends.iloc[0].position) if len(ends) else None
    end_ts = ends.iloc[0].bar_ts if len(ends) else None
    close_events = e[e.event.isin(['close_above', 'close_below'])]
    outside_positions = set(close_events.position.astype(int))
    first_outside = min(outside_positions) if outside_positions else None
    # İçeride kapanan bir bar zorunlu olarak temas barıdır. Aynı barda
    # yüksek/düşük sırası bilinmez; burada yalnız kapanış zamanı sırası kullanılır.
    inside_after_outside = first_outside is not None and any(int(p) > first_outside and int(p) not in outside_positions for p in touches)
    if end_pos is None:
        exit_class = 'censored'
    else:
        last = close_events.tail(2)
        approach = visit['approach_side']
        if (len(last) < 2 or int(last.iloc[-1].position) != end_pos or
                int(last.iloc[-2].position) != end_pos-1 or last.iloc[-1].event != last.iloc[-2].event or
                approach not in ('above', 'below')):
            exit_class = 'unknown'
        else:
            exit_side = last.iloc[-1].event.removeprefix('close_')
            exit_class = 'same_side' if exit_side == approach else 'opposite_side'
    if end_pos is None:
        revisit = 'unknown'
    elif pd.notna(next_start) and int(next_start) <= end_pos + horizon:
        if int(next_start) <= end_pos:
            raise ValueError('Sonraki ziyaret bitişten önce başlayamaz')
        revisit = 'yes'
    elif end_pos + horizon <= last_pos:
        revisit = 'no'
    else:
        revisit = 'censored'
    flags = set(e.event)
    return {'end_position':end_pos, 'end_bar_ts':end_ts, 'exit_class':exit_class,
            'touch_bars':len(touches), 'duration_bars':end_pos - int(visit['position']) + 1 if end_pos is not None else None,
            'upper_wick': 'upper_wick_outside' in flags, 'lower_wick':'lower_wick_outside' in flags,
            'both_boundaries_ambiguous':'both_boundaries_ambiguous' in flags,
            'outside_then_inside_close':bool(inside_after_outside), 'revisit_within_10':revisit}


def build(root: Path):
    outputs, inputs = [], []
    for kind, folder in FOLDERS.items():
        path = root / folder
        inputs.extend({'path':str(path / f), 'sha256':hashlib.sha256((path / f).read_bytes()).hexdigest()}
                      for f in ['visits.csv.gz', 'visit-events.csv.gz', 'input-manifest.csv'])
        visits = pd.read_csv(path/'visits.csv.gz')
        events = pd.read_csv(path/'visit-events.csv.gz')
        manifest = pd.read_csv(path/'input-manifest.csv')
        visits = visits[(visits.asset_id.isin(ASSETS)) & (visits.interval == '4h')].copy()
        if visits.visit_id.duplicated().any():
            raise ValueError('Ziyaret kimliği yinelendi')
        ev_map = {key: g for key,g in events[events.visit_id.isin(visits.visit_id)].groupby('visit_id', sort=False)}
        last_by_asset = manifest[manifest.interval == '4h'].set_index('asset_id').usable_rows.sub(1).to_dict()
        visits = visits.sort_values(['asset_id','zone_id','position','visit_id']).reset_index(drop=True)
        visits['next_start'] = visits.groupby(['asset_id','zone_id']).position.shift(-1)
        visits['representative'] = ~visits.sort_values(['asset_id','position','zone_id','visit_id']).duplicated(['asset_id','position'])
        records = []
        for v in visits.to_dict('records'):
            if v['visit_id'] not in ev_map:
                raise ValueError('Ziyaret olayları eksik')
            record = {k: v.get(k) for k in ['asset_id','interval','zone_id','visit_id','position','bar_ts',
                       'center','lower','upper','approach_side','prior_visits','source_direction','line_kind','slope_per_bar','representative']}
            record['kind'] = kind
            record.update(summarize_visit(v, ev_map[v['visit_id']], v['next_start'], last_by_asset[v['asset_id']]))
            records.append(record)
        outputs.extend(records)
    return pd.DataFrame(outputs), inputs


def table(paths: pd.DataFrame):
    rows=[]
    for mode in ('all', 'one_per_bar'):
        source = paths if mode == 'all' else paths[paths.representative]
        for kind, g in source.groupby('kind', sort=True):
            rows.append({'mode':mode, 'kind':kind, 'visits':len(g), 'assets':g.asset_id.nunique(),
                         'same_side':(g.exit_class=='same_side').sum(), 'opposite_side':(g.exit_class=='opposite_side').sum(),
                         'unknown':(g.exit_class=='unknown').sum(), 'censored':(g.exit_class=='censored').sum(),
                         'touch_3plus':(g.touch_bars>=3).sum(), 'both_boundaries_ambiguous':g.both_boundaries_ambiguous.sum(),
                         'outside_then_inside_close':g.outside_then_inside_close.sum(),
                         'revisit_yes':(g.revisit_within_10=='yes').sum(), 'revisit_no':(g.revisit_within_10=='no').sum(),
                         'revisit_censored_or_unknown':g.revisit_within_10.isin(['censored','unknown']).sum()})
    return pd.DataFrame(rows)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path('research/measurements/zone-memory'))
    p.add_argument('--output', type=Path, required=True)
    args=p.parse_args(argv)
    paths, inputs = build(args.root)
    args.output.mkdir(parents=True, exist_ok=True)
    paths.to_csv(args.output/'paths.csv.gz', index=False, compression='gzip')
    table(paths).to_csv(args.output/'summary.csv', index=False)
    meta={'status':'descriptive_pilot', 'assets':ASSETS, 'interval':'4h', 'inputs':inputs,
          'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'notice':'Kapanış yönü vekildir. Türler ve ziyaretler bağımsız değil; yüzde genellemesi yapılamaz.'}
    (args.output/'summary.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(table(paths).to_string(index=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
