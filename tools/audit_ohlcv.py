#!/usr/bin/env python3
"""Tüm OHLCV ağacını ve 1h->2h/4h matematiğini yeniden doğrular."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from replayman.catalog import load_catalog
from replayman.config import Settings
from replayman.dataset import build_dataset_index
from replayman.resample import derive_timeframes
from replayman.series import build_series, price_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/settings.json")
    parser.add_argument("--catalog", default="data/universe.csv")
    args = parser.parse_args()
    settings = Settings.load(args.config, base_dir=Path.cwd())
    assets, _ = load_catalog(args.catalog)
    findings = []
    totals = {"assets": len(assets), "files": 0, "rows": 0, "errors": 0, "warnings": 0}
    for asset in assets:
        series = build_series(asset, settings)
        frames = {}
        for interval in ("1h", "2h", "4h", "1d"):
            path = price_path(settings, asset, series, interval)
            errors = []
            if not path.exists():
                errors.append("missing_file")
                frame = pd.DataFrame()
            else:
                frame = pd.read_csv(path)
                totals["files"] += 1; totals["rows"] += len(frame)
                if frame.empty: errors.append("empty")
                if "ts_utc" in frame:
                    ts = pd.to_datetime(frame["ts_utc"], utc=True, errors="coerce")
                    if ts.isna().any(): errors.append("invalid_timestamp")
                    if ts.duplicated().any(): errors.append("duplicate_timestamp")
                    if not ts.is_monotonic_increasing: errors.append("unsorted_timestamp")
                if {"open","high","low","close"}.issubset(frame):
                    invalid = ((frame.high < frame.low) | (frame.high < frame[["open","close"]].max(axis=1)) |
                               (frame.low > frame[["open","close"]].min(axis=1)))
                    if invalid.any(): errors.append(f"invalid_ohlc:{int(invalid.sum())}")
            frames[interval] = frame
            for error in errors:
                findings.append({"severity":"error","asset_id":asset.id,"interval":interval,"finding":error,"path":str(path)})
                totals["errors"] += 1
        if not frames["1h"].empty:
            expected = derive_timeframes(frames["1h"], asset, series_id=series.id)
            for interval in ("2h", "4h"):
                actual = frames[interval]
                target = expected[interval]
                problem = None
                if len(actual) != len(target):
                    problem = f"derived_row_count:{len(actual)}!={len(target)}"
                else:
                    columns = ["open","high","low","close"]
                    numbers_equal = np.allclose(actual[columns], target[columns], rtol=1e-10, atol=1e-10, equal_nan=True)
                    times_equal = actual["ts_utc"].astype(str).equals(target["ts_utc"].astype(str))
                    counts_equal = actual["bar_count"].astype(int).equals(target["bar_count"].astype(int))
                    if not (numbers_equal and times_equal and counts_equal): problem = "derived_math_mismatch"
                if problem:
                    findings.append({"severity":"error","asset_id":asset.id,"interval":interval,"finding":problem,
                                     "path":str(price_path(settings,asset,series,interval))})
                    totals["errors"] += 1
    index_path = build_dataset_index(settings)
    report_dir = Path(settings.output_dir)
    pd.DataFrame(findings, columns=["severity","asset_id","interval","finding","path"]).to_csv(report_dir/"audit_findings.csv", index=False)
    totals["status"] = "passed" if totals["errors"] == 0 else "failed"
    try:
        totals["index"] = index_path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        totals["index"] = str(index_path)
    (report_dir/"audit_summary.json").write_text(json.dumps(totals, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(totals, ensure_ascii=False, indent=2))
    return 0 if totals["errors"] == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
