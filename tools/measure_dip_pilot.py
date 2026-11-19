"""Dondurulmuş A/B/C dip pilotunu çalıştır; emir veya portföy simülasyonu değildir.

Örnekler:
  python -m tools.measure_dip_pilot --source internal --output research/measurements/dip-research/internal
  python -m tools.measure_dip_pilot --source external --external-dir .cache/external-reference/data --output research/measurements/dip-research/external
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from replayman.dip_research import (Period, confirmation_events, evaluate_trade, label_signal,
                                    local_boundary, period_at, reference_lows, scan_candidates)
from replayman.replay import load_bars

INTERNAL_PERIODS = [
    Period("train", local_boundary("1900-01-01"), local_boundary("2026-07-01")),
    Period("validation", local_boundary("2026-07-01"), local_boundary("2026-09-01")),
    Period("historical_test", local_boundary("2026-09-01"), local_boundary("2027-01-01")),
]
EXTERNAL_PERIODS = [Period("external_history", local_boundary("2022-01-01"), local_boundary("2025-11-01"))]
EXTERNAL_COMMIT = "f4a353bf9cf1ac3621c294fb397b812c5691e099"
HORIZONS = (10, 20)
ENTRY_LAGS = {"next_open": 1, "delayed_open": 2}
COSTS = {"000": 0., "010": .001, "025": .0025, "050": .005}
CODE_FILES = (
    "research/measurements/dip-research/PLAN.md", "replayman/dip_research.py", "replayman/swings.py",
    "replayman/zone_memory.py", "replayman/replay.py", "tools/measure_dip_pilot.py",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def week_key(values: pd.Series) -> pd.Series:
    return pd.to_datetime(values, utc=True).dt.tz_convert("Europe/Istanbul").dt.strftime("%G-W%V")


def input_record(path: Path, bars: pd.DataFrame, *, kind: str, asset_id: str, interval: str,
                 raw_rows: int, partial_rows: int = 0, rounding_repairs: int = 0) -> dict:
    return {"kind": kind, "asset_id": asset_id, "interval": interval, "path": str(path), "sha256": sha256(path),
            "raw_rows": raw_rows, "partial_rows": partial_rows, "usable_rows": len(bars),
            "rounding_repairs": rounding_repairs,
            "start_ts": bars.ts_utc.iloc[0] if len(bars) else None,
            "end_ts": bars.ts_utc.iloc[-1] if len(bars) else None}


def load_internal(path: Path, *, kind: str) -> tuple[pd.DataFrame, dict]:
    raw = pd.read_csv(path)
    partial = 0
    if "complete" in raw:
        partial = int((~raw.complete.astype(str).str.lower().isin({"true", "1"})).sum())
    bars = load_bars(path)
    asset = path.parts[-4]
    return bars, input_record(path, bars, kind=kind, asset_id=asset, interval=path.stem,
                              raw_rows=len(raw), partial_rows=partial)


def load_external(path: Path) -> tuple[pd.DataFrame, dict]:
    """Günlük MIT arşivini yükle; büyük geometri kusurunda sessizce onarma."""
    raw = pd.read_csv(path)
    required = {"Price", "Open", "High", "Low", "Close", "Volume"}
    if required - set(raw):
        raise ValueError(f"Harici CSV kolonları eksik: {path}")
    data = raw.rename(columns={"Price": "date", "Open": "open", "High": "high", "Low": "low",
                               "Close": "close", "Volume": "volume"}).copy()
    for column in ("open", "high", "low", "close", "volume"):
        data[column] = pd.to_numeric(data[column], errors="raise")
    dates = pd.to_datetime(data.date, format="%Y-%m-%d", errors="raise")
    data["ts_utc"] = dates.dt.tz_localize("Europe/Istanbul").dt.tz_convert("UTC")
    if data.ts_utc.duplicated().any() or not data.ts_utc.is_monotonic_increasing:
        raise ValueError(f"Harici tarih sırası/tekilliği bozuk: {path}")
    ohlc = data[["open", "high", "low", "close"]]
    if not np.isfinite(ohlc.to_numpy()).all() or (ohlc.to_numpy() <= 0).any():
        raise ValueError(f"Harici seri eksik veya pozitif olmayan OHLC: {path}")
    required_high, required_low = ohlc.max(axis=1), ohlc.min(axis=1)
    high_gap = (required_high - data.high).clip(lower=0)
    low_gap = (data.low - required_low).clip(lower=0)
    bad = (high_gap > data.close.abs() * 1e-9) | (low_gap > data.close.abs() * 1e-9)
    if bad.any():
        raise ValueError(f"Harici seride ciddi OHLC hatası ({int(bad.sum())}): {path}")
    repairs = int(((high_gap > 0) | (low_gap > 0)).sum())
    data["high"] = data.high.clip(lower=required_high)
    data["low"] = data.low.clip(upper=required_low)
    data = data[["ts_utc", "open", "high", "low", "close", "volume"]].reset_index(drop=True)
    return data, input_record(path, data, kind="external_yfinance_archive", asset_id="BIST_" + path.stem,
                              interval="1d", raw_rows=len(raw), rounding_repairs=repairs)


def discover_internal(root: Path) -> list[Path]:
    paths = sorted(p for p in root.glob("bist_equities/BIST_*/*/bars/*.csv") if p.stem in {"4h", "1d"})
    keys = [(p.parts[-4], p.stem) for p in paths]
    if len(keys) != len(set(keys)):
        raise ValueError("Aynı hisse/periyot için birden fazla seri var; önce açık seçim yapılmalı")
    return paths


def load_benchmarks(root: Path) -> tuple[dict[str, pd.DataFrame], list[dict]]:
    paths = sorted(p for p in root.glob("bist_indices/IDX_XU100/*/bars/*.csv") if p.stem in {"4h", "1d"})
    if len({p.stem for p in paths}) != len(paths):
        raise ValueError("Birden fazla XU100 serisi; açık seçim gerekli")
    series, manifest = {}, []
    for path in paths:
        bars, record = load_internal(path, kind="benchmark")
        series[path.stem] = bars.set_index("ts_utc")
        manifest.append(record)
    return series, manifest


def collect_series(bars: pd.DataFrame, asset: str, interval: str, periods: list[Period],
                   benchmark: pd.DataFrame | None) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    series_key = f"{asset}:{interval}"
    base = scan_candidates(bars, series_key=series_key)
    confirmed, status = confirmation_events(bars, base, periods)
    pivots = reference_lows(bars, periods)
    meta = {"asset_id": asset, "interval": interval}
    pivot_rows = [{**meta, **row} for row in pivots.to_dict("records")]
    status_rows = [{**meta, **row} for row in status.to_dict("records")]
    signal_rows: list[dict] = []
    outcome_rows: list[dict] = []
    sets = [("A_all", base), ("A_no_support", base.loc[~base.support]),
            ("B_support", base.loc[base.support]), ("C_confirmed", confirmed)]
    for variant, frame in sets:
        for signal in frame.to_dict("records"):
            p = period_at(signal["signal_ts"], periods)
            if p is None:
                continue
            uid = f"{series_key}:{int(signal['signal_position'])}:{variant}"
            signal_row = {**meta, "period": p.name, "variant": variant, "signal_id": uid, **signal,
                          **label_signal(signal, bars, pivots, p)}
            signal_rows.append(signal_row)
            for entry_name, lag in ENTRY_LAGS.items():
                for horizon in HORIZONS:
                    outcome = evaluate_trade(bars, signal, p, horizon=horizon, entry_lag=lag, benchmark=benchmark)
                    outcome_rows.append({**meta, "period": p.name, "variant": variant, "signal_id": uid,
                                         "signal_ts": signal["signal_ts"], "entry": entry_name,
                                         "horizon": horizon, **outcome})
    return signal_rows, outcome_rows, pivot_rows, status_rows


def summarize_signals(signals: pd.DataFrame, pivots: pd.DataFrame) -> pd.DataFrame:
    keys = ["interval", "period", "variant"]
    rows = []
    for group, part in signals.groupby(keys, sort=True):
        interval, period, variant = group
        refs = pivots[(pivots.interval == interval) & (pivots.period == period)]
        known = part[part.label_status != "censored"]
        matched = part[part.label_status == "matched"]
        covered = matched[["asset_id", "matched_pivot_position"]].drop_duplicates().shape[0]
        rows.append({**dict(zip(keys, group)), "signals": len(part), "assets": part.asset_id.nunique(),
                     "weeks": week_key(part.signal_ts).nunique(), "label_known": len(known),
                     "label_censored": int((part.label_status == "censored").sum()), "matched_signals": len(matched),
                     "precision": len(matched) / len(known) if len(known) else np.nan,
                     "reference_pivots": len(refs), "covered_pivots": covered,
                     "pivot_coverage": covered / len(refs) if len(refs) else np.nan,
                     "median_delay_bars": matched.pivot_delay.median() if len(matched) else np.nan})
    return pd.DataFrame(rows)


def summarize_outcomes(outcomes: pd.DataFrame) -> pd.DataFrame:
    keys = ["interval", "period", "variant", "entry", "horizon"]
    rows = []
    for group, part in outcomes.groupby(keys, sort=True):
        ready = part.loc[part.status == "observed"]
        excess = ready.excess_return.dropna()
        lower = ready.trade_lower.dropna()
        row = {**dict(zip(keys, group)), "signals": len(part), "observed": len(ready),
               "censored": int((part.status == "censored").sum()), "unknown": int((part.status == "unknown").sum()),
               "assets": ready.asset_id.nunique(), "weeks": week_key(ready.signal_ts).nunique(),
               "benchmark_paired": len(excess),
               "fixed_mean": ready.fixed_return.mean(), "fixed_median": ready.fixed_return.median(),
               "fixed_positive_rate": (ready.fixed_return > 0).mean() if len(ready) else np.nan,
               "fixed_p05": ready.fixed_return.quantile(.05), "excess_median": excess.median(),
               "mfe_median": ready.mfe.median(), "mae_median": ready.mae.median(),
               "mae_p05": ready.mae.quantile(.05),
               "ambiguous": int((ready.exit_reason == "ambiguous").sum()),
               "stop_exits": int(ready.exit_reason.isin(["stop", "gap_stop"]).sum()),
               "target_exits": int(ready.exit_reason.isin(["target", "gap_target"]).sum()),
               "time_exits": int((ready.exit_reason == "time").sum()),
               "trade_upper_median_gross": ready.trade_upper.median(),
               "trade_lower_p05_gross": lower.quantile(.05),
               "median_bars_held": ready.bars_held.median()}
        for label, cost in COSTS.items():
            net = lower - cost
            row[f"net_median_{label}"] = net.median()
            row[f"net_mean_{label}"] = net.mean()
            row[f"net_win_rate_{label}"] = (net > 0).mean() if len(net) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def bootstrap_weekly_difference(part: pd.DataFrame, column: str, *, draws: int = 2000, seed: int = 418) -> dict:
    """B − bölgesiz A medyanı; hafta küme bootstrap, nedensel eşleştirme değil."""
    sample = part.loc[part.variant.isin(["B_support", "A_no_support"]) & part[column].notna()].copy()
    sample["week"] = week_key(sample.signal_ts)
    a = sample.loc[sample.variant == "A_no_support", column].to_numpy(float)
    b = sample.loc[sample.variant == "B_support", column].to_numpy(float)
    weeks = sorted(sample.week.unique())
    result = {"n_no_support": len(a), "n_support": len(b), "weeks": len(weeks),
              "median_difference": np.median(b) - np.median(a) if len(a) and len(b) else np.nan,
              "ci_low": np.nan, "ci_high": np.nan, "valid_draws": 0}
    if len(a) < 2 or len(b) < 2 or len(weeks) < 5:
        return result
    grouped = {week: (sample.loc[(sample.week == week) & (sample.variant == "A_no_support"), column].to_numpy(float),
                      sample.loc[(sample.week == week) & (sample.variant == "B_support"), column].to_numpy(float))
               for week in weeks}
    rng = np.random.default_rng(seed)
    differences = []
    for _ in range(draws):
        chosen = rng.integers(0, len(weeks), len(weeks))
        a_chunks = [grouped[weeks[i]][0] for i in chosen if len(grouped[weeks[i]][0])]
        b_chunks = [grouped[weeks[i]][1] for i in chosen if len(grouped[weeks[i]][1])]
        if a_chunks and b_chunks:
            differences.append(float(np.median(np.concatenate(b_chunks)) - np.median(np.concatenate(a_chunks))))
    if differences:
        result.update({"ci_low": float(np.quantile(differences, .025)), "ci_high": float(np.quantile(differences, .975)),
                       "valid_draws": len(differences)})
    return result


def summarize_comparison(outcomes: pd.DataFrame) -> pd.DataFrame:
    keys = ["interval", "period", "entry", "horizon"]
    rows = []
    for group, part in outcomes.loc[outcomes.status == "observed"].groupby(keys, sort=True):
        for metric in ("fixed_return", "excess_return", "trade_lower"):
            row = {**dict(zip(keys, group)), "metric": metric}
            row.update(bootstrap_weekly_difference(part, metric))
            rows.append(row)
    return pd.DataFrame(rows)


def run(source: str, root: Path, external_dir: Path, output: Path) -> dict:
    local_paths = discover_internal(root)
    if not local_paths:
        raise ValueError(f"İç BIST hisse verisi bulunamadı: {root}")
    markets, records = load_benchmarks(root) if source == "internal" else ({}, [])
    if source == "internal":
        paths = local_paths
        periods = INTERNAL_PERIODS
    else:
        available = {p.parts[-4].removeprefix("BIST_") for p in local_paths}
        paths = sorted(p for p in external_dir.glob("*.csv") if p.stem in available)
        periods = EXTERNAL_PERIODS
    if not paths:
        raise ValueError(f"İncelenecek {source} CSV yok")
    signals: list[dict] = []
    outcomes: list[dict] = []
    pivots: list[dict] = []
    statuses: list[dict] = []
    for number, path in enumerate(paths, 1):
        if source == "internal":
            bars, record = load_internal(path, kind="internal_equity")
        else:
            bars, record = load_external(path)
        records.append(record)
        if len(bars) < 30:
            continue
        asset, interval = record["asset_id"], record["interval"]
        a, b, c, d = collect_series(bars, asset, interval, periods, markets.get(interval))
        signals.extend(a); outcomes.extend(b); pivots.extend(c); statuses.extend(d)
        if number % 25 == 0 or number == len(paths):
            print(f"{source}: {number}/{len(paths)} seri; {len(signals)} varyant-sinyali", flush=True)
    sf, of, pf, cf, mf = map(pd.DataFrame, (signals, outcomes, pivots, statuses, records))
    if sf.empty or pf.empty:
        raise ValueError("Sinyal veya referans dip yok; boş analiz başarı olarak yazılmaz")
    output.mkdir(parents=True, exist_ok=True)
    sf.to_csv(output / "signals.csv", index=False)
    of.to_csv(output / "outcomes.csv", index=False)
    pf.to_csv(output / "reference_pivots.csv", index=False)
    cf.to_csv(output / "confirmation_status.csv", index=False)
    mf.to_csv(output / "input_manifest.csv", index=False)
    summarize_signals(sf, pf).to_csv(output / "signal_summary.csv", index=False)
    summarize_outcomes(of).to_csv(output / "outcome_summary.csv", index=False)
    summarize_comparison(of).to_csv(output / "support_comparison.csv", index=False)
    metadata = {"source": source, "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                "external_commit": EXTERNAL_COMMIT if source == "external" else None,
                "python": platform.python_version(), "pandas": pd.__version__, "numpy": np.__version__,
                "code_sha256": {name: sha256(Path(name)) for name in CODE_FILES},
                "input_series": len(paths), "input_assets": len(set(x["asset_id"] for x in records if x["kind"] != "benchmark")),
                "variant_signal_rows": len(sf), "outcome_rows": len(of), "reference_pivots": len(pf),
                "incomplete_rows_dropped": int(mf.partial_rows.sum()), "floating_point_repairs": int(mf.rounding_repairs.sum()),
                "periods": [{"name": p.name, "start": p.start.isoformat(), "end_exclusive": p.end.isoformat()} for p in periods],
                "forward_claim": False,
                "warning": "Exploratory history; no portfolio or independent prospective validation."}
    (output / "run_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, choices=("internal", "external"))
    parser.add_argument("--root", type=Path, default=Path("data/ohlcv"))
    parser.add_argument("--external-dir", type=Path, default=Path(".cache/external-reference/data"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.root, args.external_dir, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
