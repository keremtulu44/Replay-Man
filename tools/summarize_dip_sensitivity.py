"""Eş-sinyalde ek giriş gecikmesi ve günlük kurumsal işlem duyarlılığı.

Bu sonradan eklenmiş betimsel duyarlılık analizidir; düzeltilmiş fiyat serisi,
komisyon hesabı veya kurumsal işlem doğrulaması değildir.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from replayman.replay import load_bars
from tools.measure_dip_pilot import discover_internal, sha256


def paired_delay(outcomes: pd.DataFrame) -> pd.DataFrame:
    left = outcomes.loc[outcomes.entry == "next_open"].copy()
    right = outcomes.loc[outcomes.entry == "delayed_open"].copy()
    joined = left.merge(right, on=["signal_id", "horizon"], suffixes=("_next", "_delay"), validate="one_to_one")
    common = joined.loc[(joined.status_next == "observed") & (joined.status_delay == "observed")]
    keys = ["interval_next", "period_next", "variant_next", "horizon"]
    rows = []
    for group, part in common.groupby(keys, sort=True):
        row = dict(zip(("interval", "period", "variant", "horizon"), group))
        row.update({"paired_signals": len(part), "assets": part.asset_id_next.nunique()})
        for metric in ("fixed_return", "excess_return", "trade_lower"):
            a, b = part[f"{metric}_next"], part[f"{metric}_delay"]
            valid = a.notna() & b.notna()
            row[f"{metric}_paired"] = int(valid.sum())
            row[f"{metric}_next_median"] = a[valid].median()
            row[f"{metric}_delay_median"] = b[valid].median()
            row[f"{metric}_median_paired_change"] = (b[valid] - a[valid]).median()
        rows.append(row)
    return pd.DataFrame(rows)


def daily_action_flags(outcomes: pd.DataFrame, root: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    chosen = outcomes.loc[(outcomes.interval == "1d") & (outcomes.entry == "next_open")
                          & (outcomes.horizon == 20) & (outcomes.status == "observed")].copy()
    path_map = {p.parts[-4]: p for p in discover_internal(root) if p.stem == "1d"}
    flags = []
    for asset, part in chosen.groupby("asset_id", sort=True):
        if asset not in path_map:
            raise ValueError(f"Günlük seri yok: {asset}")
        bars = load_bars(path_map[asset])
        columns = ["stock_splits", "dividends"]
        for col in columns:
            if col not in bars:
                bars[col] = np.nan
            bars[col] = pd.to_numeric(bars[col], errors="coerce")
        jump = bars.close.pct_change(fill_method=None).abs().ge(.30)
        for row in part.itertuples():
            start, end = int(row.entry_position), int(row.end_position)
            if start < 0 or end >= len(bars) or start > end:
                raise ValueError(f"Günlük olay penceresi geçersiz: {row.signal_id}")
            window = bars.iloc[start:end + 1]
            flags.append({"signal_id": row.signal_id, "asset_id": asset, "interval": row.interval,
                          "period": row.period, "variant": row.variant,
                          "action_unknown": bool(window[columns].isna().any().any()),
                          "split_recorded": bool(window.stock_splits.fillna(0).ne(0).any()),
                          "dividend_recorded": bool(window.dividends.fillna(0).ne(0).any()),
                          "close_jump_30pct": bool(jump.iloc[start:end + 1].any()),
                          "fixed_return": row.fixed_return, "trade_lower": row.trade_lower})
    data = pd.DataFrame(flags)
    rows = []
    for group, part in data.groupby(["period", "variant"], sort=True):
        known_no_action = part.loc[~part.action_unknown & ~part.split_recorded & ~part.dividend_recorded]
        no_jump = part.loc[~part.close_jump_30pct]
        rows.append({"period": group[0], "variant": group[1], "observed": len(part),
                     "action_unknown": int(part.action_unknown.sum()), "split_recorded": int(part.split_recorded.sum()),
                     "dividend_recorded": int(part.dividend_recorded.sum()), "close_jump_30pct": int(part.close_jump_30pct.sum()),
                     "all_fixed_median": part.fixed_return.median(),
                     "known_no_action_count": len(known_no_action), "known_no_action_fixed_median": known_no_action.fixed_return.median(),
                     "no_jump_count": len(no_jump), "no_jump_fixed_median": no_jump.fixed_return.median()})
    return data, pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("data/ohlcv"))
    parser.add_argument("--research", type=Path, default=Path("research/measurements/dip-research"))
    args = parser.parse_args()
    for source in ("internal", "external"):
        target = args.research / source
        outcomes = pd.read_csv(target / "outcomes.csv")
        outputs = ["paired_delay_summary.csv"]
        paired_delay(outcomes).to_csv(target / outputs[0], index=False)
        if source == "internal":
            detail, summary = daily_action_flags(outcomes, args.root)
            detail.to_csv(target / "daily_action_window_flags.csv", index=False)
            summary.to_csv(target / "daily_action_window_summary.csv", index=False)
            outputs.extend(["daily_action_window_flags.csv", "daily_action_window_summary.csv"])
        meta = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "source": source,
                "method": "post-hoc sensitivity, not a preregistered result",
                "tool_sha256": sha256(Path(__file__)), "outcomes_sha256": sha256(target / "outcomes.csv"),
                "inputs_manifest_sha256": sha256(target / "input_manifest.csv"),
                "output_sha256": {name: sha256(target / name) for name in outputs}}
        (target / "sensitivity_metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print("Aynı-sinyal gecikme ve post-hoc günlük eylem duyarlılığı yazıldı.")


if __name__ == "__main__":
    main()
