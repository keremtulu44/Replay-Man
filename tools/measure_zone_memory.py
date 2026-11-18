"""Farklı bölge adayları için açık kapsamlı keşif çalıştırıcısı."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import pandas as pd

from replayman.replay import load_bars
from replayman.zone_memory import ZoneConfig, scan_zones, visit_outcomes
from replayman.sloped_zones import SlopedConfig, scan_sloped_zones
from replayman.behavior_zones import BehaviorConfig, scan_behavior_zones


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("data/ohlcv"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--symbols", required=True, help="Virgülle ayrılmış asset ID, örn. BIST_ASELS,BIST_THYAO")
    parser.add_argument("--intervals", default="4h", help="Virgülle ayrılmış 1h,2h,4h,1d")
    parser.add_argument("--geometry", choices=("horizontal", "sloped", "dwell", "impulse"), default="horizontal")
    parser.add_argument("--method", choices=("atr", "percent"), default="atr")
    parser.add_argument("--tolerance", type=float, default=0.25, help="ATR çarpanı veya ondalık yüzde (0.005 = %%0,5)")
    return parser.parse_args(argv)


def discover(root: Path, symbols: list[str], intervals: list[str]) -> list[Path]:
    paths = []
    for symbol in symbols:
        for interval in intervals:
            matches = sorted((root / "bist_equities" / symbol).glob(f"*/bars/{interval}.csv"))
            if len(matches) != 1:
                raise ValueError(f"{symbol}/{interval}: tam bir seri gerekli, bulunan {len(matches)}")
            paths.append(matches[0])
    return paths


def main(argv=None):
    args = parse_args(argv)
    symbols = list(dict.fromkeys(s.strip() for s in args.symbols.split(",") if s.strip()))
    intervals = list(dict.fromkeys(s.strip() for s in args.intervals.split(",") if s.strip()))
    if not symbols or not intervals or any(x not in {"1h", "2h", "4h", "1d"} for x in intervals):
        raise ValueError("En az bir sembol ve geçerli periyot gerekli")
    config = ZoneConfig(method=args.method, tolerance=args.tolerance)
    paths = discover(args.root, symbols, intervals)
    args.output.mkdir(parents=True, exist_ok=True)
    manifest, all_zones, all_visits, all_events, all_outcomes = [], [], [], [], []
    for path in paths:
        asset, series, interval = path.parts[-4], path.parts[-3], path.stem
        raw = pd.read_csv(path)
        bars = load_bars(path)
        if bars.empty:
            raise ValueError(f"Kullanılabilir bar yok: {path}")
        for column, expected in (("asset_id", asset), ("series_id", series), ("interval", interval)):
            if column not in bars or set(bars[column].astype(str)) != {expected}:
                raise ValueError(f"Seri kimliği uyuşmazlığı: {path}, {column}")
        key = f"{asset}:{series}:{interval}"
        if args.geometry == "sloped":
            zones, visits, events = scan_sloped_zones(bars, config=SlopedConfig(zone=config), series_key=key)
        elif args.geometry in {"dwell", "impulse"}:
            zones, visits, events = scan_behavior_zones(bars, config=BehaviorConfig(kind=args.geometry, zone=config), series_key=key)
        else:
            zones, visits, events = scan_zones(bars, config=config, series_key=key)
        outcomes = visit_outcomes(bars, visits)
        for frame in (zones, visits, events, outcomes):
            frame.insert(0, "interval", interval)
            frame.insert(0, "series_id", series)
            frame.insert(0, "asset_id", asset)
        all_zones.append(zones)
        all_visits.append(visits)
        all_events.append(events)
        all_outcomes.append(outcomes)
        manifest.append({"asset_id": asset, "series_id": series, "interval": interval,
                         "path": path.as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                         "input_rows": len(raw), "usable_rows": len(bars), "excluded_rows": len(raw) - len(bars),
                         "first_bar_label": str(bars.ts_utc.iloc[0]), "last_bar_label": str(bars.ts_utc.iloc[-1])})
        print(f"{asset} {interval}: {len(bars)} bar, {len(zones)} bölge/tepki olayı, {len(visits)} ziyaret", flush=True)
    for name, frames in (("zone-events", all_zones), ("visits", all_visits),
                         ("visit-events", all_events), ("outcomes", all_outcomes)):
        pd.concat(frames, ignore_index=True).to_csv(args.output / f"{name}.csv.gz", index=False, compression="gzip")
    pd.DataFrame(manifest).to_csv(args.output / "input-manifest.csv", index=False)
    v = pd.concat(all_visits, ignore_index=True)
    o = pd.concat(all_outcomes, ignore_index=True)
    findings = []
    if not v.empty:
        paired = v.merge(o.loc[o.horizon == 5, ["visit_id", "status", "return"]], on="visit_id", how="left", validate="one_to_one")
        if args.geometry in {"dwell", "impulse"}:
            paired["reaction_group"] = paired.prior_completed_visits.map(lambda x: "0_completed_visits" if x == 0 else "1+_completed_visits")
        else:
            anchor_count = 2 if args.geometry == "sloped" else 1
            paired["reaction_group"] = paired.reaction_count.map(lambda x: str(anchor_count) if x == anchor_count else f"{anchor_count + 1}+")
        for (interval, group), frame in paired.groupby(["interval", "reaction_group"], sort=True):
            known = frame.loc[frame.status == "observed", "return"].dropna()
            findings.append({"interval": interval, "reaction_group": group, "visits": len(frame),
                             "known_5bar": len(known), "assets": frame.asset_id.nunique(),
                             "median_return_5bar": float(known.median()) if len(known) else None,
                             "positive_fraction_5bar": float((known > 0).mean()) if len(known) else None})
        examples = v.head(30)
    else:
        examples = v
    pd.DataFrame(findings, columns=["interval", "reaction_group", "visits", "known_5bar", "assets", "median_return_5bar", "positive_fraction_5bar"]).to_csv(args.output / "descriptive-5bar.csv", index=False)
    examples.to_csv(args.output / "examples.csv", index=False)
    summary = {"status": "exploratory_pilot", "symbols": symbols, "intervals": intervals,
               "geometry": args.geometry, "zone_method": config.method, "tolerance": config.tolerance, "exit_closes": config.exit_closes,
               "swing": [config.swing_left, config.swing_right], "series": len(paths),
               "zone_events": sum(map(len, all_zones)), "visits": len(v), "visit_events": sum(map(len, all_events)),
               "outcomes": len(o), "notice": "Betimleyici pilot; dönem/baz/bağımlılık kontrolü yapılmamıştır."}
    (args.output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    code_paths = [Path(__file__), Path(__file__).resolve().parents[1] / "replayman" / "zone_memory.py",
                  Path(__file__).resolve().parents[1] / "replayman" / "swings.py",
                  Path(__file__).resolve().parents[1] / "replayman" / "replay.py",
                  Path(__file__).resolve().parents[1] / "replayman" / "sloped_zones.py",
                  Path(__file__).resolve().parents[1] / "replayman" / "behavior_zones.py"]
    experiment = {"geometry": args.geometry, "sloped_anchor_min": 8, "sloped_anchor_max": 80,
                  "sloped_max_anchors_per_kind": 3, "dwell_window": 10, "dwell_width_atr": 2.0,
                  "impulse_bars": 5, "impulse_distance_atr": 2.0,
                  "method": config.method, "tolerance": config.tolerance, "exit_closes": config.exit_closes,
                  "swing_left": config.swing_left, "swing_right": config.swing_right,
                  "horizons": [1, 3, 5, 10, 20], "symbols": symbols, "intervals": intervals,
                  "python": platform.python_version(), "pandas": pd.__version__,
                  "code_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in code_paths}}
    (args.output / "experiment-config.json").write_text(json.dumps(experiment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
