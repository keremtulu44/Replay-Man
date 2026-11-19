"""Dip/P6 sonuçları için sonradan tanımlanmış kontrollü keşif analizleri.

Bu çalışma ileri test veya nedensel etki değildir. Sözleşme: general-review/PLAN.md.
"""
from __future__ import annotations

import argparse
import json
import math
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from replayman.dip_research import evaluate_trade, label_signal, period_at
from replayman.general_review import block_bootstrap_mean, prior_bull_controls, week_starts
from replayman.replay import load_bars
from tools.audit_dip_results import verify_hashes
from tools.measure_dip_pilot import (EXTERNAL_PERIODS, INTERNAL_PERIODS, load_benchmarks,
                                    load_external, sha256)

ROOT = Path("research/measurements")
OUT = ROOT / "general-review"
COST = .0025
DRAWS = 2000
CODE_FILES = ("research/measurements/general-review/PLAN.md", "replayman/general_review.py",
              "replayman/dip_research.py", "replayman/swings.py", "replayman/zone_memory.py",
              "replayman/replay.py", "tools/measure_dip_pilot.py", "tools/review_general_results.py")


def series_data(path: Path, *, external: bool) -> pd.DataFrame:
    return load_external(path)[0] if external else load_bars(path)


def verified_markets(root: Path, internal_directory: Path) -> dict[str, pd.DataFrame]:
    """Verilen kökteki XU100, orijinal çalışmanın gerçek hash'leriyle aynı olmalı."""
    markets, records = load_benchmarks(root)
    manifest = pd.read_csv(internal_directory / "input_manifest.csv")
    expected = {r.interval: r.sha256 for r in manifest.itertuples() if r.kind == "benchmark"}
    actual = {r["interval"]: r["sha256"] for r in records}
    if not expected or actual != expected:
        raise ValueError("XU100 serileri özgün çalışmanın girdi hash'leriyle uyuşmuyor")
    return markets


def pair_controls(dip: Path, source: str, market: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    directory = dip / source
    verify_hashes(directory)
    is_external = source == "external"
    periods = EXTERNAL_PERIODS if is_external else INTERNAL_PERIODS
    signals = pd.read_csv(directory / "signals.csv")
    signals = signals.loc[signals.variant == "A_all"].copy()
    outcomes = pd.read_csv(directory / "outcomes.csv")
    outcomes = outcomes.loc[(outcomes.variant == "A_all") & (outcomes.horizon == 20)].set_index(["signal_id", "entry"])
    if not outcomes.index.is_unique:
        raise ValueError("A sonuç anahtarları tekil olmalı")
    pivots = pd.read_csv(directory / "reference_pivots.csv")
    manifest = pd.read_csv(directory / "input_manifest.csv")
    paths = {(r.asset_id, r.interval): Path(r.path) for r in manifest.itertuples() if r.kind != "benchmark"}
    matches, pairs = [], []
    groups = list(signals.groupby(["asset_id", "interval"], sort=True))
    for index, ((asset, interval), sig) in enumerate(groups, 1):
        data = series_data(paths[(asset, interval)], external=is_external)
        selected = prior_bull_controls(data, sig, periods)
        merged = sig.merge(selected, on=["signal_id", "signal_position", "period"], suffixes=("", "_matched"), validate="one_to_one")
        reference = pivots.loc[(pivots.asset_id == asset) & (pivots.interval == interval)]
        for item in merged.to_dict("records"):
            match = {"source": source, "asset_id": asset, "interval": interval, "period": item["period"],
                     "signal_id": item["signal_id"], "signal_position": int(item["signal_position"]),
                     "signal_ts": item["signal_ts"], "support": bool(item["support"]),
                     "control_position": item["control_position"], "control_ts": item["control_ts"],
                     "bar_gap": item["bar_gap"], "control_status": item["control_status"]}
            matches.append(match)
            if item["control_status"] != "matched":
                continue
            period = period_at(data.ts_utc.iloc[int(item["signal_position"])], periods)
            if period is None:
                raise ValueError("Sinyal dönemi yok")
            a_signal = {"signal_position": int(item["signal_position"]), "atr": float(item["atr"]),
                        "signal_close": float(item["signal_close"])}
            a_label = label_signal(a_signal, data, reference, period)
            if a_label["label_status"] != item["label_status"]:
                raise ValueError(f"Özgün A dip etiketi uyuşmuyor: {item['signal_id']}")
            cpos = int(item["control_position"])
            control = {"signal_position": cpos, "atr": float(item["control_atr"]),
                       "signal_close": float(data.close.iloc[cpos])}
            control_label = label_signal(control, data, reference, period)
            for entry, lag in (("next_open", 1), ("delayed_open", 2)):
                original = outcomes.loc[(item["signal_id"], entry)]
                ctrl_result = evaluate_trade(data, control, period, horizon=20, entry_lag=lag, benchmark=market.get(interval))
                row = {**match, "entry": entry, "horizon": 20,
                       "a_label": a_label["label_status"], "control_label": control_label["label_status"],
                       "a_pivot": a_label["matched_pivot_position"], "control_pivot": control_label["matched_pivot_position"],
                       "a_status": original["status"], "control_outcome_status": ctrl_result["status"]}
                for field in ("fixed_return", "excess_return", "trade_lower", "trade_upper", "entry_ts", "end_ts"):
                    row[f"a_{field}"] = original[field]
                    row[f"control_{field}"] = ctrl_result[field]
                pairs.append(row)
        if index % 25 == 0 or index == len(groups):
            print(f"{source} önceki-bar kontrolü: {index}/{len(groups)} seri", flush=True)
    return pd.DataFrame(matches), pd.DataFrame(pairs)


def _statistics(frame: pd.DataFrame, a: str, control: str) -> dict:
    part = frame.loc[frame[a].notna() & frame[control].notna()].copy()
    diff = part[a].astype(float) - part[control].astype(float)
    boot = block_bootstrap_mean(diff, part.signal_ts, draws=DRAWS)
    asset_means = pd.DataFrame({"asset": part.asset_id.to_numpy(), "diff": diff.to_numpy()}).groupby("asset")["diff"].mean()
    return {"n": len(part), "assets": part.asset_id.nunique(), "observed_weeks": boot["observed_weeks"],
            "calendar_weeks": boot["calendar_weeks"], "a_mean": part[a].mean(), "control_mean": part[control].mean(),
            "a_median": part[a].median(), "control_median": part[control].median(),
            "paired_difference_mean": boot["mean"], "paired_difference_median": diff.median(),
            "paired_difference_positive_rate": (diff > 0).mean() if len(diff) else np.nan,
            "asset_equal_weight_difference": asset_means.mean(),
            "asset_positive_fraction": (asset_means > 0).mean() if len(asset_means) else np.nan,
            "ci_low": boot["ci_low"], "ci_high": boot["ci_high"], "valid_draws": boot["valid_draws"]}


def summarize_controls(matches: pd.DataFrame, pairs: pd.DataFrame) -> pd.DataFrame:
    keys = ["source", "interval", "period"]
    counts = matches.groupby(keys).agg(total_a=("signal_id", "size"), matched_controls=("control_status", lambda x: int((x == "matched").sum())),
                                       no_control=("control_status", lambda x: int((x != "matched").sum()))).reset_index()
    rows = []
    for count in counts.to_dict("records"):
        mask = np.logical_and.reduce([pairs[key].eq(count[key]) for key in keys])
        group = pairs.loc[mask].copy()
        known = group.loc[(group.entry == "next_open") & group.a_label.isin(["matched", "not_matched"])
                          & group.control_label.isin(["matched", "not_matched"])].copy()
        known["a_value"] = known.a_label.eq("matched").astype(float)
        known["control_value"] = known.control_label.eq("matched").astype(float)
        rows.append({**count, "entry": "signal_close", "metric": "dip_match", **_statistics(known, "a_value", "control_value")})
        for entry in ("next_open", "delayed_open"):
            ready = group.loc[(group.entry == entry) & (group.a_status == "observed") & (group.control_outcome_status == "observed")].copy()
            for metric in ("fixed_return", "excess_return", "trade_net"):
                if metric == "trade_net":
                    ready["a_value"] = ready.a_trade_lower - COST
                    ready["control_value"] = ready.control_trade_lower - COST
                else:
                    ready["a_value"] = ready[f"a_{metric}"]
                    ready["control_value"] = ready[f"control_{metric}"]
                rows.append({**count, "entry": entry, "metric": metric, **_statistics(ready, "a_value", "control_value")})
    return pd.DataFrame(rows)


def p6_same_end(p6: Path, root: Path) -> pd.DataFrame:
    verify_hashes(p6)
    data = pd.read_csv(p6 / "paired_events.csv")
    data = data.loc[(data.horizon == 20) & data.failure_close_oracle__status.eq("observed")
                    & data.confirmation_close__status.eq("observed") & data.confirmation_next_open__status.eq("observed")]
    manifest = pd.read_csv(p6 / "input_manifest.csv")
    paths = {(r.asset_id, r.interval): Path(r.path) for r in manifest.itertuples() if r.kind == "internal_equity"}
    markets, _ = load_benchmarks(root)
    rows = []
    for (asset, interval), group in data.groupby(["asset_id", "interval"], sort=True):
        bars = load_bars(paths[(asset, interval)])
        benchmark = markets.get(interval)
        for event in group.to_dict("records"):
            f, c, sign = int(event["failure_position"]), int(event["confirmation_position"]), int(event["thesis_sign"])
            end, later = f + 20, c + 1
            if later > end or end >= len(bars) or pd.Timestamp(event["failure_close_oracle__end_ts"]) != bars.ts_utc.iloc[end]:
                raise ValueError("P6 ortak bitiş konumu/zamanı geçersiz")
            failure_price, later_price, exit_price = float(bars.close.iloc[f]), float(bars.open.iloc[later]), float(bars.close.iloc[end])
            if min(failure_price, later_price, exit_price) <= 0:
                raise ValueError("P6 fiyatları pozitif olmalı")
            oracle = sign * (exit_price / failure_price - 1)
            confirm = sign * (exit_price / later_price - 1)
            row = {"asset_id": asset, "interval": interval, "period": event["period"], "level_id": event["level_id"],
                   "failure_position": f, "confirmation_position": c, "failure_ts": bars.ts_utc.iloc[f],
                   "confirmation_entry_ts": bars.ts_utc.iloc[later], "common_end_ts": bars.ts_utc.iloc[end],
                   "direction": event["direction"], "thesis_sign": sign, "confirmation_delay": c - f,
                   "remaining_bars": end - later + 1, "failure_to_entry_move": sign * (later_price / failure_price - 1),
                   "oracle_return": oracle, "confirmation_return": confirm, "oracle_excess": np.nan, "confirmation_excess": np.nan}
            if benchmark is not None:
                fts, lts, ets = (bars.ts_utc.iloc[x] for x in (f, later, end))
                if all(t in benchmark.index for t in (fts, lts, ets)):
                    f_market, l_market, e_market = float(benchmark.at[fts, "close"]), float(benchmark.at[lts, "open"]), float(benchmark.at[ets, "close"])
                    if min(f_market, l_market, e_market) > 0 and all(np.isfinite(v) for v in (f_market, l_market, e_market)):
                        row["oracle_excess"] = oracle - sign * (e_market / f_market - 1)
                        row["confirmation_excess"] = confirm - sign * (e_market / l_market - 1)
            rows.append(row)
    return pd.DataFrame(rows)


def summarize_p6(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (interval, period), part in data.groupby(["interval", "period"], sort=True):
        tmp = part.rename(columns={"failure_ts": "signal_ts"}).copy()
        for metric, a, b in (("directional_return", "confirmation_return", "oracle_return"),
                             ("directional_excess", "confirmation_excess", "oracle_excess")):
            row = {"interval": interval, "period": period, "metric": metric,
                   "median_remaining_bars": part.remaining_bars.median(),
                   "median_failure_to_entry_move": part.failure_to_entry_move.median()}
            row.update(_statistics(tmp, a, b))
            rows.append(row)
    return pd.DataFrame(rows)


def external_stability(dip: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    directory = dip / "external"
    outcomes = pd.read_csv(directory / "outcomes.csv")
    data = outcomes.loc[(outcomes.variant == "A_all") & (outcomes.entry == "next_open")
                        & (outcomes.horizon == 20) & (outcomes.status == "observed")].copy()
    data["net"] = data.trade_lower - COST
    ts = pd.to_datetime(data.signal_ts, utc=True).dt.tz_convert("Europe/Istanbul")
    data["year"] = ts.dt.year
    data["week"] = week_starts(data.signal_ts)
    annual_rows = []
    for year, group in data.groupby("year", sort=True):
        b = block_bootstrap_mean(group.net, group.signal_ts, draws=DRAWS)
        per_asset = group.groupby("asset_id").net.mean()
        annual_rows.append({"year": int(year), "events": len(group), "assets": group.asset_id.nunique(),
                            "observed_weeks": b["observed_weeks"], "net_mean": group.net.mean(),
                            "net_median": group.net.median(), "net_positive_rate": (group.net > 0).mean(),
                            "asset_equal_weight_mean": per_asset.mean(), "asset_positive_fraction": (per_asset > 0).mean(),
                            "net_p05": group.net.quantile(.05), "net_p95": group.net.quantile(.95),
                            "mean_ci_low": b["ci_low"], "mean_ci_high": b["ci_high"], "valid_draws": b["valid_draws"]})
    assets = data.groupby("asset_id").agg(events=("net", "size"), net_mean=("net", "mean"), net_median=("net", "median"),
                                          net_win_rate=("net", lambda x: (x > 0).mean())).reset_index()
    weeks = data.groupby("week").agg(events=("net", "size"), assets=("asset_id", "nunique"), net_mean=("net", "mean"),
                                     net_median=("net", "median")).reset_index()
    bootstrap = block_bootstrap_mean(data.net, data.signal_ts, draws=DRAWS)
    n_top = max(1, math.ceil(len(data) * .01))
    sorted_returns = data.net.sort_values(ascending=False)
    positive_sum = float(data.net.clip(lower=0).sum())
    overall = {"events": len(data), "assets": data.asset_id.nunique(), "weeks": weeks.shape[0],
               "event_weighted_net_mean": float(data.net.mean()), "net_median": float(data.net.median()),
               "net_positive_rate": float((data.net > 0).mean()),
               "asset_equal_weight_net_mean": float(assets.net_mean.mean()),
               "asset_positive_fraction": float((assets.net_mean > 0).mean()),
               "week_equal_weight_net_mean": float(weeks.net_mean.mean()),
               "week_positive_fraction": float((weeks.net_mean > 0).mean()),
               "top_one_percent_events": n_top,
               "top_one_percent_share_of_positive_sum": float(sorted_returns.iloc[:n_top].sum() / positive_sum) if positive_sum > 0 else None,
               "net_mean_after_removing_top_one_percent": float(sorted_returns.iloc[n_top:].mean()),
               "bootstrap_mean_ci_low": bootstrap["ci_low"], "bootstrap_mean_ci_high": bootstrap["ci_high"],
               "bootstrap_valid_draws": bootstrap["valid_draws"],
               "leave_one_year_out": {str(int(y)): float(data.loc[data.year != y, "net"].mean()) for y in sorted(data.year.unique())},
               "warning": "Post-hoc concentration diagnostics; neither a portfolio nor an independently validated result."}
    return pd.DataFrame(annual_rows), assets, weeks, overall


def run(root: Path, research: Path, output: Path) -> dict:
    dip, p6 = research / "dip-research", research / "p6-causal"
    markets = verified_markets(root, dip / "internal")
    match_parts, pair_parts = [], []
    for source in ("internal", "external"):
        a, b = pair_controls(dip, source, markets if source == "internal" else {})
        match_parts.append(a); pair_parts.append(b)
    matches, pairs = pd.concat(match_parts, ignore_index=True), pd.concat(pair_parts, ignore_index=True)
    same_end = p6_same_end(p6, root)
    annual, asset, weeks, stability = external_stability(dip)
    output.mkdir(parents=True, exist_ok=True)
    tables = {"control_matches.csv": matches, "control_pairs.csv": pairs, "control_summary.csv": summarize_controls(matches, pairs),
              "p6_same_end_pairs.csv": same_end, "p6_same_end_summary.csv": summarize_p6(same_end),
              "external_annual.csv": annual, "external_assets.csv": asset, "external_weeks.csv": weeks}
    for name, frame in tables.items():
        frame.to_csv(output / name, index=False)
    (output / "external_stability.json").write_text(json.dumps(stability, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    files = [*tables, "external_stability.json"]
    meta = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
            "pandas": pd.__version__, "numpy": np.__version__, "draws": DRAWS, "block_calendar_weeks": 5,
            "cost_per_trade": COST, "code_sha256": {name: sha256(Path(name)) for name in CODE_FILES},
            "source_file_sha256": {str(p): sha256(p) for p in (
                dip / "internal/signals.csv", dip / "internal/outcomes.csv", dip / "internal/reference_pivots.csv",
                dip / "internal/input_manifest.csv", dip / "external/signals.csv", dip / "external/outcomes.csv",
                dip / "external/reference_pivots.csv", dip / "external/input_manifest.csv",
                p6 / "paired_events.csv", p6 / "input_manifest.csv")},
            "output_file_sha256": {name: sha256(output / name) for name in files},
            "warning": "Post-hoc exploration only; same provider, no portfolio or independent forward claim."}
    (output / "run_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"signals": len(matches), "matched": int(matches.control_status.eq("matched").sum()),
            "pair_entry_rows": len(pairs), "p6_same_end_events": len(same_end), "external_events": stability["events"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("data/ohlcv"))
    parser.add_argument("--research", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    print(json.dumps(run(args.root, args.research, args.output), indent=2))


if __name__ == "__main__":
    main()
