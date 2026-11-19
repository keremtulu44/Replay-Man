"""A dip adayını aynı bar etiketindeki gözlemsel başka-hisse kontrolüyle karşılaştır."""
from __future__ import annotations

import argparse
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from replayman.contemporaneous_control import bar_context, match_at_same_bar
from replayman.dip_research import evaluate_trade, label_signal, period_at
from tools.audit_dip_results import verify_hashes
from tools.measure_dip_pilot import (EXTERNAL_PERIODS, INTERNAL_PERIODS, load_external, sha256)
from tools.review_general_results import COST, _statistics, verified_markets
from replayman.replay import load_bars

ROOT = Path("research/measurements")
OUT = ROOT / "general-review"
CODE_FILES = ("research/measurements/general-review/PLAN.md", "replayman/contemporaneous_control.py",
              "replayman/general_review.py", "replayman/dip_research.py", "replayman/swings.py",
              "replayman/zone_memory.py", "replayman/replay.py", "tools/measure_dip_pilot.py",
              "tools/review_general_results.py", "tools/compare_dip_contemporaneous.py")


def collect(dip: Path, source: str, markets: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    directory = dip / source
    verify_hashes(directory)
    external = source == "external"
    periods = EXTERNAL_PERIODS if external else INTERNAL_PERIODS
    signals = pd.read_csv(directory / "signals.csv")
    signals = signals.loc[signals.variant == "A_all"].copy()
    signals["signal_ts"] = pd.to_datetime(signals.signal_ts, utc=True)
    outcomes = pd.read_csv(directory / "outcomes.csv")
    outcomes = outcomes.loc[(outcomes.variant == "A_all") & (outcomes.horizon == 20)].set_index(["signal_id", "entry"])
    if not outcomes.index.is_unique:
        raise ValueError("A sonuç anahtarları yineleniyor")
    pivots = pd.read_csv(directory / "reference_pivots.csv")
    manifest = pd.read_csv(directory / "input_manifest.csv")
    paths = {(r.asset_id, r.interval): Path(r.path) for r in manifest.itertuples() if r.kind != "benchmark"}
    data, contexts = {}, []
    for (asset, interval), path in sorted(paths.items()):
        bars = load_external(path)[0] if external else load_bars(path)
        data[(asset, interval)] = bars
        contexts.append(bar_context(bars, asset, interval))
    selected = match_at_same_bar(signals, pd.concat(contexts, ignore_index=True))
    merged = signals.merge(selected, on=["signal_id", "asset_id", "interval", "period", "signal_position", "signal_ts"], validate="one_to_one")
    merged.insert(0, "source", source)
    pairs = []
    for item in merged.loc[merged.control_status == "matched"].to_dict("records"):
        signal_bars = data[(item["asset_id"], item["interval"])]
        ctrl_bars = data[(item["control_asset_id"], item["interval"])]
        ctrl_pos, signal_pos = int(item["control_position"]), int(item["signal_position"])
        if signal_bars.ts_utc.iloc[signal_pos] != ctrl_bars.ts_utc.iloc[ctrl_pos]:
            raise ValueError("Kontrol/sinyal etiketleri eşzamanlı değil")
        period = period_at(signal_bars.ts_utc.iloc[signal_pos], periods)
        if period is None or period.name != item["period"]:
            raise ValueError("Sinyal dönemi uyuşmuyor")
        ctrl_signal = {"signal_position": ctrl_pos, "signal_close": float(ctrl_bars.close.iloc[ctrl_pos]), "atr": float(item["control_atr"])}
        ref = pivots.loc[(pivots.asset_id == item["control_asset_id"]) & (pivots.interval == item["interval"])]
        c_label = label_signal(ctrl_signal, ctrl_bars, ref, period)
        for entry, lag in (("next_open", 1), ("delayed_open", 2)):
            original = outcomes.loc[(item["signal_id"], entry)]
            comp = evaluate_trade(ctrl_bars, ctrl_signal, period, horizon=20, entry_lag=lag, benchmark=markets.get(item["interval"]))
            if original.status == "observed" and comp["status"] == "observed":
                same = (pd.Timestamp(original.entry_ts) == comp["entry_ts"] and pd.Timestamp(original.end_ts) == comp["end_ts"])
                timing = "same" if same else "different"
            else:
                timing = "censored_or_unknown"
            row = {"source": source, "asset_id": item["asset_id"], "control_asset_id": item["control_asset_id"],
                   "interval": item["interval"], "period": item["period"], "signal_id": item["signal_id"],
                   "signal_ts": item["signal_ts"], "signal_position": signal_pos, "control_position": ctrl_pos,
                   "entry": entry, "horizon": 20, "a_label": item["label_status"],
                   "control_label": c_label["label_status"], "a_status": original.status,
                   "control_outcome_status": comp["status"], "timing": timing}
            for field in ("fixed_return", "excess_return", "trade_lower", "trade_upper", "entry_ts", "end_ts"):
                row[f"a_{field}"] = original[field]
                row[f"control_{field}"] = comp[field]
            pairs.append(row)
    print(f"{source} eşzamanlı kontrol: {len(merged)} A, {int(merged.control_status.eq('matched').sum())} eş", flush=True)
    return merged, pd.DataFrame(pairs)


def summarize(matches: pd.DataFrame, pairs: pd.DataFrame) -> pd.DataFrame:
    keys = ["source", "interval", "period"]
    counts = matches.groupby(keys).agg(total_a=("signal_id", "size"), matched_controls=("control_status", lambda x: int((x == "matched").sum())),
                                       no_control=("control_status", lambda x: int((x == "no_control").sum())),
                                       unknown_context=("control_status", lambda x: int((x == "unknown_context").sum()))).reset_index()
    rows = []
    for count in counts.to_dict("records"):
        mask = np.logical_and.reduce([pairs[k].eq(count[k]) for k in keys])
        group = pairs.loc[mask].copy()
        label_pairs = group.loc[group.entry == "next_open"]
        known = label_pairs.loc[label_pairs.a_label.isin(["matched", "not_matched"])
                                & label_pairs.control_label.isin(["matched", "not_matched"])].copy()
        known["a_value"] = known.a_label.eq("matched").astype(float)
        known["control_value"] = known.control_label.eq("matched").astype(float)
        rows.append({**count, "entry": "signal_close", "metric": "dip_match", "timing_mismatch": 0,
                     "censored_or_unknown": len(label_pairs) - len(known),
                     **_statistics(known, "a_value", "control_value")})
        for entry in ("next_open", "delayed_open"):
            a = group.loc[group.entry == entry]
            ready = a.loc[a.timing == "same"].copy()
            mismatched = int((a.timing == "different").sum())
            censored = int((a.timing == "censored_or_unknown").sum())
            for metric in ("fixed_return", "excess_return", "trade_net"):
                if metric == "trade_net":
                    ready["a_value"] = ready.a_trade_lower - COST
                    ready["control_value"] = ready.control_trade_lower - COST
                else:
                    ready["a_value"] = ready[f"a_{metric}"]
                    ready["control_value"] = ready[f"control_{metric}"]
                rows.append({**count, "entry": entry, "metric": metric, "timing_mismatch": mismatched,
                             "censored_or_unknown": censored, **_statistics(ready, "a_value", "control_value")})
    return pd.DataFrame(rows)


def run(root: Path, research: Path, output: Path) -> dict:
    markets = verified_markets(root, research / "dip-research" / "internal")
    match_parts, pair_parts = [], []
    for source in ("internal", "external"):
        a, b = collect(research / "dip-research", source, markets if source == "internal" else {})
        match_parts.append(a); pair_parts.append(b)
    matches, pairs = pd.concat(match_parts, ignore_index=True), pd.concat(pair_parts, ignore_index=True)
    output.mkdir(parents=True, exist_ok=True)
    tables = {"contemporaneous_matches.csv": matches, "contemporaneous_pairs.csv": pairs,
              "contemporaneous_summary.csv": summarize(matches, pairs)}
    for name, frame in tables.items():
        frame.to_csv(output / name, index=False)
    meta = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
            "pandas": pd.__version__, "numpy": np.__version__,
            "code_sha256": {name: sha256(Path(name)) for name in CODE_FILES},
            "source_file_sha256": {str(p): sha256(p) for source in ("internal", "external") for p in (
                research / "dip-research" / source / "signals.csv", research / "dip-research" / source / "outcomes.csv",
                research / "dip-research" / source / "reference_pivots.csv", research / "dip-research" / source / "input_manifest.csv")},
            "output_file_sha256": {name: sha256(output / name) for name in tables},
            "warning": "Post-hoc observational cross-asset matching, not independent forward or causal efficacy."}
    (output / "contemporaneous_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"signals": len(matches), "matched": int((matches.control_status == "matched").sum()), "entry_pair_rows": len(pairs)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("data/ohlcv"))
    parser.add_argument("--research", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    print(json.dumps(run(args.root, args.research, args.output), indent=2))


if __name__ == "__main__":
    main()
