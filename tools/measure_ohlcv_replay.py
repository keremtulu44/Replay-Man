"""Tüm sürümlü OHLCV dosyalarında ilk replay ölçüm envanterini üretir."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from replayman.replay import causal_features, forward_outcomes, load_bars
from replayman.swings import multi_level_swings, swing_legs


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
    args.output.mkdir(parents=True, exist_ok=True)
    for path in paths:
        bars = load_bars(path)
        if not len(bars):
            continue
        features = causal_features(bars)
        outcomes = forward_outcomes(bars)
        swings = multi_level_swings(bars, features)
        legs = swing_legs(swings, bars)
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
            "zero_volume_ratio": float((bars.volume.fillna(0) == 0).mean()),
        })
    inventory = pd.DataFrame(rows)
    inventory.to_csv(args.output / "series_inventory.csv", index=False)
    summary = {
        "schema_version": 1, "series": len(inventory), "assets": int(inventory.asset_id.nunique()) if len(inventory) else 0,
        "bars": int(inventory.bars.sum()) if len(inventory) else 0,
        "intervals": inventory.groupby("interval").agg(series=("asset_id", "count"), bars=("bars", "sum")).to_dict("index") if len(inventory) else {},
        "swing_events": {column: int(inventory[column].sum()) for column in ("minor_swings", "major_swings", "swing_legs", "higher_highs", "higher_lows", "lower_highs", "lower_lows")} if len(inventory) else {},
        "measurement_families": ["candle_geometry", "overlap", "volatility", "volume_relative", "movement_quality", "pressure_decay", "confirmed_swings", "swing_legs", "forward_return", "mfe_mae"],
        "causality": "features use current/past bars; forward outcomes are isolated research labels",
    }
    (args.output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
