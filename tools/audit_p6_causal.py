"""P6 eş-olay dosyalarında zaman, XU100 ve fiyat aritmetiği denetimi."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from replayman.replay import load_bars
from tools.audit_dip_results import require, verify_hashes
from tools.measure_dip_pilot import load_benchmarks
from tools.measure_p6_causal import METHODS, summarize_pairs, summarize_status


def audit(directory: Path, root: Path) -> dict:
    input_count = verify_hashes(directory)
    statuses = pd.read_csv(directory / "failure_status.csv")
    pairs = pd.read_csv(directory / "paired_events.csv")
    pd.testing.assert_frame_equal(summarize_status(statuses), pd.read_csv(directory / "status_summary.csv"),
                                  check_dtype=False, check_exact=False, rtol=1e-9, atol=1e-12)
    pd.testing.assert_frame_equal(summarize_pairs(pairs), pd.read_csv(directory / "paired_summary.csv"),
                                  check_dtype=False, check_exact=False, rtol=1e-9, atol=1e-12)
    confirmed = statuses.loc[statuses.status == "confirmed"]
    require(len(pairs) == len(confirmed) * 2, "Her teyit için iki ufuk yok")
    require((confirmed.confirmation_position > confirmed.failure_position).all(), "Teyit failure'dan önce")
    require(((confirmed.confirmation_position - confirmed.failure_position) == confirmed.confirmation_delay).all(),
            "Teyit gecikmesi uyuşmuyor")
    keys = ["asset_id", "interval", "level_id", "failure_position"]
    require(not confirmed.duplicated(keys).any(), "Teyitli failure tekil değil")
    linked = pairs.merge(confirmed[keys], on=keys, how="left", indicator=True, validate="many_to_one")
    require(linked._merge.eq("both").all(), "Çiftin teyitli failure kaydı yok")
    inputs = pd.read_csv(directory / "input_manifest.csv")
    paths = {(r.asset_id, r.interval): Path(r.path) for r in inputs.itertuples() if r.kind == "internal_equity"}
    markets, _ = load_benchmarks(root)
    cache = {}
    sample = pairs.sample(min(200, len(pairs)), random_state=44)
    comparisons = 0
    for row in sample.to_dict("records"):
        key = (row["asset_id"], row["interval"])
        if key not in cache:
            cache[key] = load_bars(paths[key])
        bars, market = cache[key], markets.get(row["interval"])
        for method in METHODS:
            if row[f"{method}__status"] != "observed":
                continue
            event_pos = int(row["failure_position"] if method == "failure_close_oracle" else row["confirmation_position"])
            first = event_pos + int(method == "confirmation_next_open")
            end = event_pos + int(row["horizon"])
            field = "open" if method == "confirmation_next_open" else "close"
            start_ts, end_ts = bars.ts_utc.iloc[first], bars.ts_utc.iloc[end]
            require(pd.Timestamp(row[f"{method}__start_ts"]) == start_ts and pd.Timestamp(row[f"{method}__end_ts"]) == end_ts,
                    "P6 hisse tarih etiketleri uyuşmuyor")
            price = float(bars[field].iloc[first])
            actual = int(row["thesis_sign"]) * (float(bars.close.iloc[end]) / price - 1)
            require(np.isclose(row[f"{method}__directional_return"], actual, atol=1e-10), "P6 yönlü getiri uyuşmuyor")
            if market is not None and start_ts in market.index and end_ts in market.index:
                market_ret = float(market.at[end_ts, "close"]) / float(market.at[start_ts, field]) - 1
                require(np.isclose(row[f"{method}__benchmark_return"], market_ret, atol=1e-10), "P6 XU100 eşleşmesi hatalı")
                excess = actual - int(row["thesis_sign"]) * market_ret
                require(np.isclose(row[f"{method}__directional_excess"], excess, atol=1e-10), "P6 XU100 farkı hatalı")
            else:
                require(pd.isna(row[f"{method}__benchmark_return"]), "Eksik P6 benchmark sıfır sayılmış")
            comparisons += 1
    return {"audited_at_utc": datetime.now(timezone.utc).isoformat(), "status": "passed",
            "input_files_verified": input_count, "failures": len(statuses), "confirmed": len(confirmed),
            "paired_horizon_rows": len(pairs), "sampled_rows": len(sample), "sampled_method_arithmetic_checks": comparisons,
            "scope": "artifact arithmetic and timing; not independent market validation or causal efficacy"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("data/ohlcv"))
    parser.add_argument("--output", type=Path, default=Path("research/measurements/p6-causal"))
    args = parser.parse_args()
    result = audit(args.output, args.root)
    (args.output / "AUDIT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
