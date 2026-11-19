"""Eski bağımsız benchmark shift'lerinin olası hisse pencereleriyle uyumunu say."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from replayman.replay import load_bars
from tools.audit_dip_results import verify_hashes
from tools.measure_dip_pilot import discover_internal, load_benchmarks, sha256


def window_alignment(stock: pd.DataFrame, market: pd.DataFrame, horizon: int) -> dict:
    if horizon < 1:
        raise ValueError("Ufuk pozitif olmalı")
    if not stock.ts_utc.is_unique or not stock.ts_utc.is_monotonic_increasing or not market.index.is_unique or not market.index.is_monotonic_increasing:
        raise ValueError("Hisse ve endeks etiketleri tekil ve sıralı olmalı")
    if len(stock) <= horizon:
        return {"stock_windows": 0, "old_comparable": 0, "old_end_mismatches": 0,
                "start_missing": 0, "old_end_unavailable": 0, "exact_end_missing": 0}
    start = pd.DatetimeIndex(stock.ts_utc.iloc[:-horizon])
    end = pd.DatetimeIndex(stock.ts_utc.iloc[horizon:])
    start_pos = market.index.get_indexer(start)
    has_start = start_pos >= 0
    has_old_end = has_start & (start_pos + horizon < len(market))
    exact_end = market.index.get_indexer(end) >= 0
    mismatch = np.zeros(len(start), dtype=bool)
    mismatch[has_old_end] = market.index.take(start_pos[has_old_end] + horizon) != end[has_old_end]
    return {"stock_windows": len(start), "old_comparable": int(has_old_end.sum()),
            "old_end_mismatches": int(mismatch.sum()), "start_missing": int((~has_start).sum()),
            "old_end_unavailable": int((has_start & ~has_old_end).sum()),
            "exact_end_missing": int((has_start & ~exact_end).sum())}


def run(root: Path, research: Path, output: Path) -> dict:
    original = research / "dip-research" / "internal"
    verify_hashes(original)
    reference = pd.read_csv(original / "input_manifest.csv")
    expected = {(x.asset_id, x.interval): x.sha256 for x in reference.itertuples()}
    paths = discover_internal(root)
    market, records = load_benchmarks(root)
    for rec in records:
        if expected.get((rec["asset_id"], rec["interval"])) != rec["sha256"]:
            raise ValueError("Endeks kaynağı özgün manifestle uyuşmuyor")
    rows = []
    for path in paths:
        asset, interval = path.parts[-4], path.stem
        if expected.get((asset, interval)) != sha256(path):
            raise ValueError(f"Hisse verisi manifestle uyuşmuyor: {path}")
        if interval not in market:
            raise ValueError(f"Endeks serisi yok: {interval}")
        bars = load_bars(path)
        for horizon in (5, 20, 60):
            rows.append({"asset_id": asset, "interval": interval, "horizon": horizon,
                         **window_alignment(bars, market[interval], horizon)})
    data = pd.DataFrame(rows)
    summary = data.groupby(["interval", "horizon"], as_index=False).agg(
        assets=("asset_id", "nunique"), stock_windows=("stock_windows", "sum"), old_comparable=("old_comparable", "sum"),
        old_end_mismatches=("old_end_mismatches", "sum"), start_missing=("start_missing", "sum"),
        old_end_unavailable=("old_end_unavailable", "sum"), exact_end_missing=("exact_end_missing", "sum"))
    summary["mismatch_fraction"] = summary.old_end_mismatches / summary.old_comparable.replace(0, np.nan)
    output.mkdir(parents=True, exist_ok=True)
    data.to_csv(output / "legacy_alignment_assets.csv", index=False)
    summary.to_csv(output / "legacy_alignment_summary.csv", index=False)
    meta = {"generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "plan_sha256": sha256(Path("research/measurements/general-review/PLAN.md")),
            "tool_sha256": sha256(Path(__file__)), "replay_sha256": sha256(Path("replayman/replay.py")),
            "input_manifest_sha256": sha256(original / "input_manifest.csv"),
            "output_sha256": {x: sha256(output / x) for x in ("legacy_alignment_assets.csv", "legacy_alignment_summary.csv")},
            "warning": "These are all possible complete stock windows, not realized event counts."}
    (output / "legacy_alignment_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"series": len(paths), "windows": int(summary.stock_windows.sum()), "mismatches": int(summary.old_end_mismatches.sum())}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path("data/ohlcv"))
    p.add_argument("--research", type=Path, default=Path("research/measurements"))
    p.add_argument("--output", type=Path, default=Path("research/measurements/general-review"))
    args = p.parse_args()
    print(json.dumps(run(args.root, args.research, args.output), indent=2))


if __name__ == "__main__":
    main()
