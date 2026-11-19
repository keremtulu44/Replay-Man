"""Oyalanma bölgesi adayını, kontrollerini ve tolerans duyarlılığını özetle.

Keşiften sonra seçilmiş bu karşılaştırma bağımsız doğrulama değildir.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import pandas as pd


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('research/measurements/zone-memory'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    variants = ['universe-dwell', 'sensitivity-dwell-atr010', 'sensitivity-dwell-atr050', 'sensitivity-dwell-pct050']
    rows = []
    baseline_rows = []
    for variant in variants:
        root = args.root / variant
        grouped = pd.read_csv(root / 'group-results.csv', dtype={'memory_group': str})
        assets = pd.read_csv(root / 'asset-results.csv', dtype={'memory_group': str})
        metadata = json.loads((root / 'summary.json').read_text(encoding='utf-8'))
        events = pd.read_csv(root / 'events.csv.gz', dtype={'memory_group': str})
        for split in ('train', 'validation', 'test'):
            for memory in ('0', '1+'):
                sample = events[(events.interval == '1d') & (events.split == split) &
                                (events.memory_group == memory) & events.one_per_bar & events.eligible]
                excess = sample.directional_excess.dropna()
                baseline_rows.append({'variant': variant, 'split': split, 'memory_group': memory,
                                      'eligible': len(sample), 'benchmark_eligible': len(excess),
                                      'median_directional_excess': float(excess.median()) if len(excess) else None})
        for split in ('train', 'validation', 'test'):
            for memory in ('0', '1+'):
                for progress in ('falling', 'rising'):
                    query = ((grouped['mode'] == 'one_visit_per_bar') & (grouped.interval == '1d') &
                             (grouped.split == split) & (grouped.memory_group == memory) & (grouped.progress_group == progress))
                    matches = grouped.loc[query]
                    if len(matches) != 1:
                        raise ValueError(f'Beklenen grup yok/çoklu: {variant}/{split}/{memory}/{progress}')
                    item = matches.iloc[0]
                    aq = ((assets['mode'] == 'one_visit_per_bar') & (assets.interval == '1d') &
                          (assets.split == split) & (assets.memory_group == memory) & (assets.progress_group == progress) &
                          (assets.benchmark_eligible >= 3))
                    stock = assets.loc[aq]
                    rows.append({'variant': variant, 'method': metadata['zone_method'], 'tolerance': metadata['tolerance'],
                                 'split': split, 'memory_group': memory, 'progress_group': progress,
                                 'eligible': int(item.eligible), 'benchmark_eligible': int(item.benchmark_eligible),
                                 'assets': int(item.assets), 'median_directional_excess': item.median_directional_excess,
                                 'assets_with_3_or_more': len(stock), 'asset_medians_negative': int((stock.median_directional_excess < 0).sum()),
                                 'asset_medians_positive': int((stock.median_directional_excess > 0).sum())})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(args.output, index=False)
    pd.DataFrame(baseline_rows).to_csv(args.output.with_name('candidate-baseline.csv'), index=False)
    print(f'{len(rows)} satır yazıldı: {args.output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
