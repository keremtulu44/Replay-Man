"""Tüm sürümlü OHLCV dosyalarında ilk replay ölçüm envanterini üretir."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from replayman.replay import causal_features, forward_outcomes, load_bars
from replayman.swings import multi_level_swings, swing_legs
from replayman.structure import attach_event_outcomes, structure_events


def positive_rate(series: pd.Series) -> float:
    valid = series.dropna()
    return float((valid > 0).mean()) if len(valid) else float("nan")


def discover(root: Path, intervals: set[str]) -> list[Path]:
    return sorted(path for path in root.glob("*/*/*/bars/*.csv") if path.stem in intervals)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("data/ohlcv"))
    parser.add_argument("--output", type=Path, default=Path("research/measurements/ohlcv-baseline"))
    parser.add_argument("--intervals", default="1h,2h,4h,1d")
    args = parser.parse_args()
    paths = discover(args.root, set(args.intervals.split(",")))
    rows: list[dict] = []
    event_samples: list[pd.DataFrame] = []
    args.output.mkdir(parents=True, exist_ok=True)
    for path in paths:
        bars = load_bars(path)
        if not len(bars):
            continue
        features = causal_features(bars)
        outcomes = forward_outcomes(bars)
        swings = multi_level_swings(bars, features)
        legs = swing_legs(swings, bars)
        events = structure_events(bars, features, swings)
        event_results = attach_event_outcomes(events, bars, (5, 20, 40, 60))
        if len(event_results):
            event_results.insert(0, "group", path.parts[-5]); event_results.insert(1, "asset_id", str(bars.get("asset_id", pd.Series([path.parts[-4]])).iloc[0])); event_results.insert(2, "interval", path.stem)
            result_columns = ["group", "asset_id", "interval", "event_ts", "direction", "thesis_direction", "event"]
            for horizon in (5, 20, 40, 60):
                result_columns += [f"directional_return_{horizon}", f"directional_mfe_{horizon}", f"directional_mae_{horizon}"]
            event_samples.append(event_results[result_columns])
        event_counts = events.event.value_counts()
        finite = features.select_dtypes("number").notna().sum()
        rows.append({
            "group": path.parts[-5], "asset_id": str(bars.get("asset_id", pd.Series([path.parts[-4]])).iloc[0]),
            "symbol": str(bars.get("symbol", pd.Series([""])).iloc[0]), "interval": path.stem,
            "bars": len(bars), "start": bars.ts_utc.iloc[0].isoformat(), "end": bars.ts_utc.iloc[-1].isoformat(),
            "feature_columns": len(features.columns) - len(set(features.columns) & {"ts_utc", "open", "high", "low", "close", "volume", "asset_id", "symbol", "interval", "session_date"}),
            "atr_ready": int(finite.get("atr", 0)), "quality_ready": int(finite.get("path_efficiency", 0)),
            "outcome_20_ready": int(outcomes["return_fwd_20"].notna().sum()),
            "minor_swings": int((swings.level == "minor").sum()), "major_swings": int((swings.level == "major").sum()),
            "swing_legs": len(legs), "higher_highs": int((swings.relation == "higher_high").sum()),
            "higher_lows": int((swings.relation == "higher_low").sum()), "lower_highs": int((swings.relation == "lower_high").sum()),
            "lower_lows": int((swings.relation == "lower_low").sum()),
            "probe_rejections": int(event_counts.get("probe_rejection", 0)), "close_breaks": int(event_counts.get("close_break", 0)),
            "follow_throughs": int(event_counts.get("follow_through", 0)), "acceptances": int(event_counts.get("acceptance", 0)),
            "retest_holds": int(event_counts.get("retest_hold", 0)), "failures": int(event_counts.get("failure", 0)),
            "zero_volume_ratio": float((bars.volume.fillna(0) == 0).mean()),
        })
    inventory = pd.DataFrame(rows)
    inventory.to_csv(args.output / "series_inventory.csv", index=False)
    all_events = pd.concat(event_samples, ignore_index=True) if event_samples else pd.DataFrame()
    if len(all_events):
        all_events["event_ts"] = pd.to_datetime(all_events["event_ts"], utc=True)
        # BIST hisselerinde piyasa rejimini olay avantajından ayırmak için XU100 ileri getirisi.
        benchmark_parts = []
        for benchmark_path in discover(args.root, set(args.intervals.split(","))):
            if benchmark_path.parts[-4] != "IDX_XU100":
                continue
            benchmark = load_bars(benchmark_path)
            part = pd.DataFrame({"interval": benchmark_path.stem, "event_ts": benchmark.ts_utc})
            for horizon in (5, 20, 40, 60):
                part[f"benchmark_return_{horizon}"] = benchmark.close.shift(-horizon).div(benchmark.close).sub(1)
            benchmark_parts.append(part)
        if benchmark_parts:
            benchmarks = pd.concat(benchmark_parts, ignore_index=True)
            all_events = all_events.merge(benchmarks, on=["interval", "event_ts"], how="left")
            thesis_sign = all_events.thesis_direction.map({"up": 1, "down": -1})
            for horizon in (5, 20, 40, 60):
                all_events[f"directional_excess_{horizon}"] = all_events[f"directional_return_{horizon}"] - thesis_sign * all_events[f"benchmark_return_{horizon}"]
        order_fraction = all_events.groupby(["asset_id", "interval"])["event_ts"].rank(method="first", pct=True)
        all_events["time_split"] = pd.cut(order_fraction, bins=[0, .6, .8, 1.0], labels=["train", "validation", "test"], include_lowest=True)
        grouped = all_events.groupby(["group", "interval", "event", "direction", "thesis_direction"], dropna=False)
        event_study = grouped.agg(
            observations=("asset_id", "size"), assets=("asset_id", "nunique"),
            median_return_5=("directional_return_5", "median"), win_rate_5=("directional_return_5", positive_rate),
            median_mfe_5=("directional_mfe_5", "median"), median_mae_5=("directional_mae_5", "median"),
            ready_20=("directional_return_20", "count"), median_return_20=("directional_return_20", "median"), win_rate_20=("directional_return_20", positive_rate),
            median_mfe_20=("directional_mfe_20", "median"), median_mae_20=("directional_mae_20", "median"),
            ready_40=("directional_return_40", "count"), median_return_40=("directional_return_40", "median"), win_rate_40=("directional_return_40", positive_rate),
            ready_60=("directional_return_60", "count"), median_return_60=("directional_return_60", "median"), win_rate_60=("directional_return_60", positive_rate),
            ready_excess_20=("directional_excess_20", "count"), median_excess_20=("directional_excess_20", "median"), excess_win_rate_20=("directional_excess_20", positive_rate),
            ready_excess_60=("directional_excess_60", "count"), median_excess_60=("directional_excess_60", "median"), excess_win_rate_60=("directional_excess_60", positive_rate),
            median_mfe_60=("directional_mfe_60", "median"), median_mae_60=("directional_mae_60", "median"),
        ).reset_index()
        event_study.to_csv(args.output / "structure_event_study.csv", index=False)
        split_grouped = all_events.groupby(["group", "interval", "time_split", "event", "thesis_direction"], observed=True)
        split_study = split_grouped.agg(
            observations=("asset_id", "size"), assets=("asset_id", "nunique"),
            ready_20=("directional_return_20", "count"), median_return_20=("directional_return_20", "median"), win_rate_20=("directional_return_20", positive_rate),
            ready_40=("directional_return_40", "count"), median_return_40=("directional_return_40", "median"), win_rate_40=("directional_return_40", positive_rate),
            ready_60=("directional_return_60", "count"), median_return_60=("directional_return_60", "median"), win_rate_60=("directional_return_60", positive_rate),
            ready_excess_20=("directional_excess_20", "count"), median_excess_20=("directional_excess_20", "median"), excess_win_rate_20=("directional_excess_20", positive_rate),
            ready_excess_60=("directional_excess_60", "count"), median_excess_60=("directional_excess_60", "median"), excess_win_rate_60=("directional_excess_60", positive_rate),
            median_mfe_60=("directional_mfe_60", "median"), median_mae_60=("directional_mae_60", "median"),
        ).reset_index()
        split_study.to_csv(args.output / "structure_time_split_study.csv", index=False)
        symbol_grouped = all_events.groupby(["group", "asset_id", "interval", "event", "thesis_direction"], dropna=False)
        symbol_results = symbol_grouped.agg(
            observations=("event_ts", "size"), first_event=("event_ts", "min"), last_event=("event_ts", "max"),
            median_return_5=("directional_return_5", "median"), win_rate_5=("directional_return_5", positive_rate),
            ready_20=("directional_return_20", "count"), median_return_20=("directional_return_20", "median"), win_rate_20=("directional_return_20", positive_rate),
            median_mfe_20=("directional_mfe_20", "median"), median_mae_20=("directional_mae_20", "median"),
            ready_40=("directional_return_40", "count"), median_return_40=("directional_return_40", "median"), win_rate_40=("directional_return_40", positive_rate),
            ready_60=("directional_return_60", "count"), median_return_60=("directional_return_60", "median"), win_rate_60=("directional_return_60", positive_rate),
            ready_excess_20=("directional_excess_20", "count"), median_excess_20=("directional_excess_20", "median"), excess_win_rate_20=("directional_excess_20", positive_rate),
            ready_excess_60=("directional_excess_60", "count"), median_excess_60=("directional_excess_60", "median"), excess_win_rate_60=("directional_excess_60", positive_rate),
        ).reset_index()
        symbol_results.to_csv(args.output / "structure_symbol_results.csv", index=False)
    event_columns = ("probe_rejections", "close_breaks", "follow_throughs", "acceptances", "retest_holds", "failures")
    summary = {
        "schema_version": 1, "series": len(inventory), "assets": int(inventory.asset_id.nunique()) if len(inventory) else 0,
        "bars": int(inventory.bars.sum()) if len(inventory) else 0,
        "intervals": inventory.groupby("interval").agg(series=("asset_id", "count"), bars=("bars", "sum")).to_dict("index") if len(inventory) else {},
        "swing_events": {column: int(inventory[column].sum()) for column in ("minor_swings", "major_swings", "swing_legs", "higher_highs", "higher_lows", "lower_highs", "lower_lows")} if len(inventory) else {},
        "structure_events": {column: int(inventory[column].sum()) for column in event_columns} if len(inventory) else {},
        "measurement_families": ["candle_geometry", "overlap", "volatility", "volume_relative", "movement_quality", "pressure_decay", "confirmed_swings", "swing_legs", "breakout_acceptance_failure", "forward_return", "mfe_mae"],
        "causality": "features use current/past bars; forward outcomes are isolated research labels",
    }
    (args.output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
