"""P6 eski ileri-bilgili seçim ile teyit-sonrası girişi aynı olaylarda karşılaştır.

Bu tarihsel bir olay çalışmasıdır. İlk sütun future-conditioned oracle olup
hiçbir zaman failure barında uygulanabilir sinyal olarak yorumlanmamalıdır.
"""
from __future__ import annotations

import argparse
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from replayman.dip_research import period_at
from replayman.lifecycle import enrich_lifecycle
from replayman.p6_causal import classify_failure, event_result
from replayman.replay import causal_features
from replayman.structure import structure_events
from replayman.swings import multi_level_swings
from tools.measure_dip_pilot import (INTERNAL_PERIODS, discover_internal, load_benchmarks,
                                    load_internal, sha256, week_key)

HORIZONS = (5, 20)
METHODS = ("failure_close_oracle", "confirmation_close", "confirmation_next_open")
CODE_FILES = ("research/measurements/dip-research/PLAN.md", "replayman/dip_research.py", "replayman/p6_causal.py",
              "replayman/lifecycle.py", "replayman/structure.py", "replayman/swings.py", "replayman/replay.py",
              "tools/measure_dip_pilot.py", "tools/measure_p6_causal.py")


def collect(bars: pd.DataFrame, asset: str, interval: str, market: pd.DataFrame | None) -> tuple[list[dict], list[dict]]:
    features = causal_features(bars)
    swings = multi_level_swings(bars, features)
    events = enrich_lifecycle(structure_events(bars, features, swings), bars, features)
    failures = events.loc[events.event == "failure"]
    confirmations = events.loc[events.event == "counter_expansion"]
    mapping: dict[tuple[str, int], dict] = {}
    for row in confirmations.to_dict("records"):
        key = (str(row["level_id"]), int(row["origin_failure_position"]))
        if key in mapping:
            raise ValueError(f"Aynı failure için birden fazla karşı genişleme: {key}")
        mapping[key] = row
    statuses, pairs = [], []
    for failure in failures.to_dict("records"):
        fpos = int(failure["event_position"])
        period = period_at(bars.ts_utc.iloc[fpos], INTERNAL_PERIODS)
        if period is None:
            continue
        confirm = mapping.get((str(failure["level_id"]), fpos))
        cpos = int(confirm["event_position"]) if confirm else None
        status = classify_failure(bars, fpos, cpos, period)
        base = {"asset_id": asset, "interval": interval, "period": period.name,
                "level_id": failure["level_id"], "direction": failure["direction"],
                "failure_position": fpos, "failure_ts": bars.ts_utc.iloc[fpos],
                "confirmation_position": cpos if status == "confirmed" else None,
                "confirmation_ts": bars.ts_utc.iloc[cpos] if status == "confirmed" else None,
                "confirmation_delay": cpos - fpos if status == "confirmed" else None}
        statuses.append({**base, "status": status})
        if status != "confirmed":
            continue
        sign = -1 if failure["direction"] == "up" else 1
        for horizon in HORIZONS:
            evaluations = {
                "failure_close_oracle": event_result(bars, fpos, entry="close", sign=sign, horizon=horizon, period=period, benchmark=market),
                "confirmation_close": event_result(bars, cpos, entry="close", sign=sign, horizon=horizon, period=period, benchmark=market),
                "confirmation_next_open": event_result(bars, cpos, entry="next_open", sign=sign, horizon=horizon, period=period, benchmark=market),
            }
            pair = {**base, "horizon": horizon, "thesis_sign": sign}
            for method, result in evaluations.items():
                pair.update({f"{method}__{key}": value for key, value in result.items()})
            pairs.append(pair)
    return statuses, pairs


def summarize_status(status: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for group, part in status.groupby(["interval", "period"], sort=True):
        rows.append({"interval": group[0], "period": group[1], "failures": len(part),
                     "assets": part.asset_id.nunique(),
                     "confirmed": int((part.status == "confirmed").sum()),
                     "not_confirmed": int((part.status == "not_confirmed").sum()),
                     "censored": int((part.status == "censored").sum()),
                     "median_delay": part.confirmation_delay.median()})
    return pd.DataFrame(rows)


def summarize_pairs(pairs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    keys = ["interval", "period", "horizon"]
    for group, part in pairs.groupby(keys, sort=True):
        both = part.loc[np.logical_and.reduce([part[f"{m}__status"].eq("observed") for m in METHODS])]
        shared_market = both.dropna(subset=[f"{m}__directional_excess" for m in METHODS])
        for method in METHODS:
            returns = both[f"{method}__directional_return"]
            excess = shared_market[f"{method}__directional_excess"]
            net = returns - .0025
            mismatch = both[f"{method}__old_end_mismatch"].dropna()
            rows.append({**dict(zip(keys, group)), "method": method, "confirmed_events": len(part),
                         "paired_observed": len(both), "paired_market": len(shared_market),
                         "assets": both.asset_id.nunique(), "weeks": week_key(both.failure_ts).nunique(),
                         "return_mean": returns.mean(), "return_median": returns.median(),
                         "positive_rate": (returns > 0).mean() if len(returns) else np.nan,
                         "return_p05": returns.quantile(.05),
                         "net_median_cost_025": net.median(), "net_positive_cost_025": (net > 0).mean() if len(net) else np.nan,
                         "excess_median": excess.median(), "excess_positive_rate": (excess > 0).mean() if len(excess) else np.nan,
                         "mfe_median": both[f"{method}__mfe"].median(), "mae_median": both[f"{method}__mae"].median(),
                         "old_end_comparable": len(mismatch), "old_end_mismatches": int(mismatch.astype(bool).sum())})
    return pd.DataFrame(rows)


def run(root: Path, output: Path) -> dict:
    paths = discover_internal(root)
    if not paths:
        raise ValueError("İç BIST hisse verisi bulunamadı")
    markets, records = load_benchmarks(root)
    statuses, pairs = [], []
    for i, path in enumerate(paths, 1):
        bars, rec = load_internal(path, kind="internal_equity")
        records.append(rec)
        a, b = collect(bars, rec["asset_id"], rec["interval"], markets.get(rec["interval"]))
        statuses.extend(a); pairs.extend(b)
        if i % 25 == 0 or i == len(paths):
            print(f"P6 {i}/{len(paths)} seri; {len(statuses)} failure; {len(pairs)} çift/ufuk", flush=True)
    sf, pf, mf = map(pd.DataFrame, (statuses, pairs, records))
    if sf.empty or pf.empty:
        raise ValueError("P6 failure veya teyit örneği yok")
    output.mkdir(parents=True, exist_ok=True)
    sf.to_csv(output / "failure_status.csv", index=False)
    pf.to_csv(output / "paired_events.csv", index=False)
    mf.to_csv(output / "input_manifest.csv", index=False)
    summarize_status(sf).to_csv(output / "status_summary.csv", index=False)
    summarize_pairs(pf).to_csv(output / "paired_summary.csv", index=False)
    metadata = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "input_series": len(paths),
                "failures": len(sf), "confirmed": int((sf.status == "confirmed").sum()),
                "not_confirmed": int((sf.status == "not_confirmed").sum()), "censored": int((sf.status == "censored").sum()),
                "paired_horizon_rows": len(pf), "python": platform.python_version(), "pandas": pd.__version__,
                "numpy": np.__version__, "code_sha256": {x: sha256(Path(x)) for x in CODE_FILES},
                "warning": "Failure-close group selection uses future confirmation; not a signal. Historical only."}
    (output / "run_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("data/ohlcv"))
    parser.add_argument("--output", type=Path, default=Path("research/measurements/p6-causal"))
    args = parser.parse_args()
    print(json.dumps(run(args.root, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
