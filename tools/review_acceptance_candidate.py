"""Eski 4s aşağı acceptance adayını sıkı bölüm/etiket ve açılışla yeniden ölç."""
from __future__ import annotations

import argparse
import json
import platform
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from replayman.acceptance_review import down_acceptance_representatives, open_result
from replayman.dip_research import period_at
from replayman.general_review import block_bootstrap_mean
from replayman.replay import causal_features, load_bars
from replayman.structure import structure_events
from replayman.swings import SwingConfig, confirmed_swings
from tools.audit_dip_results import verify_hashes
from tools.measure_dip_pilot import INTERNAL_PERIODS, discover_internal, load_benchmarks, sha256

ROOT = Path("research/measurements")
OUT = ROOT / "general-review"
COST = .0025
HORIZON = 60
CODE_FILES = ("research/measurements/general-review/PLAN.md", "replayman/acceptance_review.py",
              "replayman/general_review.py", "replayman/p6_causal.py", "replayman/dip_research.py",
              "replayman/structure.py", "replayman/swings.py", "replayman/replay.py",
              "tools/measure_dip_pilot.py", "tools/review_acceptance_candidate.py")


def collect(root: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    paths = [p for p in discover_internal(root) if p.stem == "4h"]
    if not paths:
        raise ValueError("4s hisse serileri bulunamadı")
    market = load_benchmarks(root)[0].get("4h")
    rows, inventory = [], []
    for number, path in enumerate(paths, 1):
        bars = load_bars(path)
        features = causal_features(bars)
        asset = path.parts[-4]
        for tie in ("leftmost", "rightmost"):
            swings = confirmed_swings(bars, features, config=SwingConfig(2, 2, tie_break=tie), level="minor")
            events = structure_events(bars, features, swings)
            raw, unique = down_acceptance_representatives(events)
            raw_counts: Counter[str] = Counter()
            unique_counts: Counter[str] = Counter()
            for e in raw.itertuples():
                p = period_at(bars.ts_utc.iloc[int(e.event_position)], INTERNAL_PERIODS)
                if p is not None:
                    raw_counts[p.name] += 1
            for event in unique.to_dict("records"):
                pos = int(event["event_position"])
                p = period_at(bars.ts_utc.iloc[pos], INTERNAL_PERIODS)
                if p is None:
                    continue
                unique_counts[p.name] += 1
                row = {"asset_id": asset, "interval": "4h", "period": p.name, "tie_break": tie,
                       "signal_position": pos, "signal_ts": bars.ts_utc.iloc[pos],
                       "source_pivot_position": int(event["source_pivot_position"]),
                       "source_confirmed_position": int(event["source_confirmed_position"])}
                for entry, lag in (("next_open", 1), ("delayed_open", 2)):
                    result = open_result(bars, pos, entry_lag=lag, horizon=HORIZON, period=p, benchmark=market)
                    for field in ("status", "start_ts", "end_ts", "directional_return", "directional_excess", "mfe", "mae"):
                        row[f"{entry}__{field}"] = result.get(field)
                rows.append(row)
            for p in INTERNAL_PERIODS:
                inventory.append({"asset_id": asset, "interval": "4h", "period": p.name, "tie_break": tie,
                                  "raw_level_events": raw_counts[p.name], "unique_bar_events": unique_counts[p.name]})
        if number % 25 == 0 or number == len(paths):
            print(f"acceptance {number}/{len(paths)} hisse; {len(rows)} tekil olay", flush=True)
    return pd.DataFrame(rows), pd.DataFrame(inventory)


def summarize(events: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    keys = ["tie_break", "period"]
    counts = inventory.groupby(keys).agg(raw_level_events=("raw_level_events", "sum"),
                                          unique_bar_events=("unique_bar_events", "sum")).reset_index()
    rows = []
    for count in counts.to_dict("records"):
        part = events.loc[(events.tie_break == count["tie_break"]) & (events.period == count["period"])]
        common = part.loc[(part.next_open__status == "observed") & (part.delayed_open__status == "observed")].copy()
        markets = common.dropna(subset=["next_open__directional_excess", "delayed_open__directional_excess"])
        for entry in ("next_open", "delayed_open"):
            ret = common[f"{entry}__directional_return"]
            excess = markets[f"{entry}__directional_excess"]
            bootstrap = block_bootstrap_mean(excess, markets.signal_ts, draws=2000, block_weeks=5)
            net = ret - COST
            rows.append({**count, "entry": entry, "next_observed": int((part.next_open__status == "observed").sum()),
                         "next_censored": int((part.next_open__status == "censored").sum()),
                         "next_unknown": int((part.next_open__status == "unknown").sum()),
                         "delayed_observed": int((part.delayed_open__status == "observed").sum()),
                         "delayed_censored": int((part.delayed_open__status == "censored").sum()),
                         "delayed_unknown": int((part.delayed_open__status == "unknown").sum()),
                         "common_observed": len(common), "common_market": len(markets),
                         "assets": markets.asset_id.nunique(), "observed_weeks": bootstrap["observed_weeks"],
                         "raw_mean": ret.mean(), "raw_median": ret.median(),
                         "net_mean_cost_025": net.mean(), "net_median_cost_025": net.median(),
                         "net_positive_rate": (net > 0).mean() if len(net) else np.nan,
                         "directional_excess_mean": excess.mean(), "directional_excess_median": excess.median(),
                         "directional_excess_positive_rate": (excess > 0).mean() if len(excess) else np.nan,
                         "excess_mean_ci_low": bootstrap["ci_low"], "excess_mean_ci_high": bootstrap["ci_high"],
                         "bootstrap_draws": bootstrap["valid_draws"]})
    return pd.DataFrame(rows)


def run(root: Path, research: Path, output: Path) -> dict:
    original = research / "dip-research" / "internal"
    input_count = verify_hashes(original)
    manifest = pd.read_csv(original / "input_manifest.csv")
    expected = {(r.asset_id, r.interval): r.sha256 for r in manifest.itertuples()}
    actual = [p for p in discover_internal(root) if p.stem == "4h"] + list(root.glob("bist_indices/IDX_XU100/*/bars/4h.csv"))
    expected_4h = {key for key in expected if key[1] == "4h"}
    actual_keys = {(p.parts[-4], p.stem) for p in actual}
    if len(actual) != len(actual_keys) or actual_keys != expected_4h:
        raise ValueError("Kullanılan 4s seri evreni kilitli manifestle uyuşmuyor")
    for path in actual:
        if sha256(path) != expected[(path.parts[-4], path.stem)]:
            raise ValueError(f"Kullanılan 4s seri hash'i uyuşmuyor: {path}")
    events, inventory = collect(root)
    if events.empty:
        raise ValueError("Aşağı acceptance adayı yok")
    output.mkdir(parents=True, exist_ok=True)
    tables = {"acceptance_events.csv": events, "acceptance_inventory.csv": inventory,
              "acceptance_summary.csv": summarize(events, inventory)}
    for name, frame in tables.items():
        frame.to_csv(output / name, index=False)
    meta = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "input_files_verified": input_count,
            "python": platform.python_version(), "pandas": pd.__version__, "numpy": np.__version__,
            "horizon": HORIZON, "assumed_round_trip_cost": COST,
            "code_sha256": {name: sha256(Path(name)) for name in CODE_FILES},
            "source_file_sha256": {str(original / "input_manifest.csv"): sha256(original / "input_manifest.csv")},
            "output_file_sha256": {name: sha256(output / name) for name in tables},
            "warning": "Post-hoc, historic, deduplicated directional event proxy; short access and execution unverified."}
    (output / "acceptance_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"unique_event_rows_both_tie_rules": len(events), "inventory_rows": len(inventory)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("data/ohlcv"))
    parser.add_argument("--research", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    print(json.dumps(run(args.root, args.research, args.output), indent=2))


if __name__ == "__main__":
    main()
