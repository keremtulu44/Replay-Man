"""Dip pilotu için hash kilidi ve append-only kesitli ileri gözlem altyapısı.

Yerel hash ve sistem saati harici zaman damgası/gerçek emir kanıtı değildir.
"""
from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd

from replayman.dip_research import Period, local_boundary
from replayman.replay import load_bars
from tools.measure_dip_pilot import (CODE_FILES, ENTRY_LAGS, collect_series, discover_internal,
                                    sha256, summarize_outcomes, summarize_signals)

FORWARD_START = local_boundary("2026-11-20")
FORWARD_END = local_boundary("2100-01-01")
FROZEN_FILES = (*CODE_FILES, "research/measurements/dip-research/FORWARD.md", "tools/forward_dip_research.py")


def now_utc() -> pd.Timestamp:
    return pd.Timestamp.now(tz="UTC")


def stamp(value) -> pd.Timestamp:
    result = pd.Timestamp(value)
    if result.tzinfo is None:
        raise ValueError("Saat UTC ofseti/zaman dilimi içermeli")
    return result.tz_convert("UTC")


def safe_relative(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("Manifestte güvensiz dosya yolu")
    path = root / rel
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("Dosya kök dışına çıkıyor")
    return path


def code_hashes() -> dict[str, str]:
    return {name: sha256(Path(name)) for name in FROZEN_FILES}


def runtime() -> dict[str, str]:
    return {"python": platform.python_version(), "pandas": pd.__version__, "numpy": np.__version__}


def prefix_hash(bars: pd.DataFrame) -> str:
    """Kullanılan OHLC önekini sürüm-sabit CSV ile hash'le (hacim kullanılmaz)."""
    import hashlib
    part = bars[["ts_utc", "open", "high", "low", "close"]].copy()
    part["ts_utc"] = pd.to_datetime(part.ts_utc, utc=True).dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    text = part.to_csv(index=False, float_format="%.17g", lineterminator="\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def create_freeze(root: Path, output: Path, *, now: pd.Timestamp | None = None) -> dict:
    recorded = stamp(now if now is not None else now_utc())
    if recorded >= FORWARD_START:
        raise ValueError("İleri dönem başladı; bu dönem için sonradan kilit oluşturulamaz")
    equities = discover_internal(root)
    market = sorted(p for p in root.glob("bist_indices/IDX_XU100/*/bars/*.csv") if p.stem in {"4h", "1d"})
    if not equities or not market or len({p.stem for p in market}) != len(market):
        raise ValueError("Sabit hisse ve tekil XU100 ısınma serileri gerekli")
    files = []
    for path in equities + market:
        raw = pd.read_csv(path)
        raw_ts = pd.to_datetime(raw.ts_utc, utc=True, errors="raise")
        if raw_ts.duplicated().any() or not raw_ts.is_monotonic_increasing or (raw_ts >= FORWARD_START).any():
            raise ValueError(f"Isınma serisi yineleniyor, sırasız veya ileri dönemi içeriyor: {path}")
        bars = load_bars(path)
        if bars.empty:
            raise ValueError(f"Boş ısınma serisi: {path}")
        series_manifest = path.parents[1] / "series.json"
        if not series_manifest.is_file():
            raise ValueError(f"Fiyat politikası manifesti yok: {series_manifest}")
        files.append({"relative_path": str(path.relative_to(root)), "sha256": sha256(path),
                      "series_manifest_sha256": sha256(series_manifest), "asset_id": path.parts[-4],
                      "series_id": path.parts[-3], "interval": path.stem,
                      "kind": "benchmark" if path.parts[-4] == "IDX_XU100" else "equity",
                      "rows": len(bars), "last_ts": bars.ts_utc.iloc[-1].isoformat() if len(bars) else None})
    manifest = {"schema_version": 1, "frozen_at_utc": recorded.isoformat(),
                "forward_start_utc": FORWARD_START.isoformat(), "forward_end_utc": FORWARD_END.isoformat(),
                "runtime": runtime(), "code_sha256": code_hashes(), "baseline_files": files,
                "external_timestamp_attestation": False,
                "warning": "Local hash/time only; archive externally before observing forward bars."}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return manifest


def verify_freeze(path: Path, warmup_root: Path) -> dict:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1 or stamp(manifest["forward_start_utc"]) != FORWARD_START:
        raise ValueError("İleri kilit sözleşmesi uyuşmuyor")
    if stamp(manifest["frozen_at_utc"]) >= FORWARD_START:
        raise ValueError("Kilit ileri dönemden önce oluşturulmamış")
    if manifest["runtime"] != runtime() or manifest["code_sha256"] != code_hashes():
        raise ValueError("Kilit sonrası kod/plan veya çalışma ortamı değişmiş")
    keys = set()
    for row in manifest["baseline_files"]:
        key = (row["asset_id"], row["interval"])
        if key in keys:
            raise ValueError("Kilit içinde yinelenen hisse/periyot")
        keys.add(key)
        source = safe_relative(warmup_root, row["relative_path"])
        series = source.parents[1] / "series.json"
        if not source.is_file() or sha256(source) != row["sha256"]:
            raise ValueError(f"Sabit ısınma CSV'si eksik/değişmiş: {source}")
        if not series.is_file() or sha256(series) != row["series_manifest_sha256"]:
            raise ValueError(f"Sabit fiyat politikası eksik/değişmiş: {series}")
    return manifest


def validate_new_file(path: Path, entry: dict) -> pd.DataFrame:
    series = path.parents[1] / "series.json"
    if not series.is_file() or sha256(series) != entry["series_manifest_sha256"]:
        raise ValueError(f"Yeni serinin fiyat politikası eşleşmiyor: {path}")
    raw = pd.read_csv(path)
    expected = {"asset_id": entry["asset_id"], "series_id": entry["series_id"], "interval": entry["interval"]}
    for column, value in expected.items():
        if column not in raw or not raw[column].astype(str).eq(value).all():
            raise ValueError(f"Yeni seri kimliği uyuşmuyor ({column}): {path}")
    if entry["interval"] == "4h" and "complete" not in raw:
        raise ValueError("4s satırlar tamamlanma bayrağı içermeli")
    times = pd.to_datetime(raw.ts_utc, utc=True, errors="raise")
    if times.duplicated().any() or not times.is_monotonic_increasing:
        raise ValueError(f"Yeni veri zamanları yineleniyor veya sırasız: {path}")
    return load_bars(path)


def verify_previous(path: Path, freeze_sha: str, as_of: pd.Timestamp, now: pd.Timestamp) -> tuple[dict, pd.DataFrame]:
    manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
    if manifest["freeze_sha256"] != freeze_sha or stamp(manifest["as_of_utc"]) > as_of or stamp(manifest["recorded_at_utc"]) > now:
        raise ValueError("Önceki kesit kilit veya zaman sırasıyla uyuşmuyor")
    for name, digest in manifest["files_sha256"].items():
        output = safe_relative(path, name)
        if not output.is_file() or sha256(output) != digest:
            raise ValueError(f"Önceki kesit çıktısı değişmiş: {output}")
    signals = pd.read_csv(path / "signals.csv")
    if signals.signal_id.duplicated().any():
        raise ValueError("Önceki kesitte yinelenen sinyal kimliği")
    return manifest, signals


def observe(freeze: Path, warmup_root: Path, new_root: Path, output: Path, *, as_of: pd.Timestamp | None = None,
            previous: Path | None = None, now: pd.Timestamp | None = None) -> dict:
    recorded = stamp(now if now is not None else now_utc())
    cutoff = stamp(as_of if as_of is not None else recorded)
    frozen = verify_freeze(freeze, warmup_root)
    if cutoff > recorded or cutoff < stamp(frozen["frozen_at_utc"]) or recorded < stamp(frozen["frozen_at_utc"]):
        raise ValueError("Kesit gelecekte veya kilitten önce olamaz")
    freeze_digest = sha256(freeze)
    prior, prior_signals = (verify_previous(previous, freeze_digest, cutoff, recorded) if previous else (None, None))
    if output.exists():
        raise FileExistsError(f"Yeni kesit klasörü zaten var: {output}")
    data: dict[tuple[str, str], pd.DataFrame] = {}
    prefix: dict[str, dict] = {}
    coverage, input_records = [], []
    forward_bar_count = 0
    for entry in frozen["baseline_files"]:
        source = safe_relative(warmup_root, entry["relative_path"])
        old = load_bars(source)
        candidate_path = safe_relative(new_root, entry["relative_path"])
        appended = old.iloc[0:0].copy()
        if candidate_path.is_file():
            fresh = validate_new_file(candidate_path, entry)
            maturity = pd.Timedelta(hours=4) if entry["interval"] == "4h" else pd.Timedelta(days=1)
            appended = fresh.loc[(fresh.ts_utc > old.ts_utc.iloc[-1]) & (fresh.ts_utc + maturity <= cutoff)].copy()
            input_records.append({"asset_id": entry["asset_id"], "interval": entry["interval"],
                                  "relative_path": entry["relative_path"], "sha256": sha256(candidate_path),
                                  "new_eligible_rows": len(appended)})
        combined = pd.concat([old, appended], ignore_index=True)
        key = (entry["asset_id"], entry["interval"])
        key_text = "|".join(key)
        if combined.ts_utc.duplicated().any() or not combined.ts_utc.is_monotonic_increasing:
            raise ValueError(f"Birleşik veride sırasız veya tekrarlı bar: {key_text}")
        if prior:
            old_prefix = prior["series_prefixes"].get(key_text)
            if old_prefix is None or len(combined) < old_prefix["rows"] or prefix_hash(combined.iloc[:old_prefix["rows"]]) != old_prefix["sha256"]:
                raise ValueError(f"Önceki kesitin veri öneki değişmiş: {key_text}")
        data[key] = combined
        prefix[key_text] = {"rows": len(combined), "sha256": prefix_hash(combined)}
        forward_rows = int((appended.ts_utc >= FORWARD_START).sum())
        if entry["kind"] == "equity":
            forward_bar_count += forward_rows
        coverage.append({"asset_id": key[0], "interval": key[1], "kind": entry["kind"],
                         "baseline_rows": len(old), "appended_rows": len(appended), "forward_rows": forward_rows,
                         "last_eligible_ts": combined.ts_utc.iloc[-1] if len(combined) else None})
    signals, outcomes, pivots, statuses = [], [], [], []
    if forward_bar_count:
        for entry in frozen["baseline_files"]:
            if entry["kind"] != "equity":
                continue
            key = (entry["asset_id"], entry["interval"])
            bars = data[key]
            if not (bars.ts_utc >= FORWARD_START).any():
                continue
            benchmark = data.get(("IDX_XU100", entry["interval"]))
            market = benchmark.set_index("ts_utc") if benchmark is not None else None
            a, b, c, d = collect_series(bars, key[0], key[1], [Period("forward", FORWARD_START, FORWARD_END)], market)
            signals.extend(a); outcomes.extend(b); pivots.extend(c); statuses.extend(d)
    signal_cols = ["signal_id", "asset_id", "interval", "period", "variant", "signal_position", "signal_ts", "first_observed_at_utc"]
    sf = pd.DataFrame(signals) if signals else pd.DataFrame(columns=signal_cols[:-1])
    prior_first = dict(zip(prior_signals.signal_id, prior_signals.first_observed_at_utc)) if prior is not None else {}
    if set(prior_first) - set(sf.signal_id):
        raise ValueError("Önceki kesitteki bir sinyal yeni kesitte yok; veri öneki veya kod incelenmeli")
    sf["first_observed_at_utc"] = [prior_first.get(uid, recorded.isoformat()) for uid in sf.signal_id]
    first_map = dict(zip(sf.signal_id, sf.first_observed_at_utc))
    position_map = {row.signal_id: (row.asset_id, row.interval, int(row.signal_position)) for row in sf.itertuples()}
    of = pd.DataFrame(outcomes)
    if of.empty:
        of = pd.DataFrame(columns=["signal_id", "asset_id", "interval", "period", "variant", "signal_ts", "entry",
                                   "horizon", "status", "entry_ts", "first_observed_at_utc", "entry_label_ts",
                                   "registered_before_entry_label"])
    else:
        of["first_observed_at_utc"] = of.signal_id.map(first_map)
        labels = []
        flags = []
        for row in of.itertuples():
            asset, interval, pos = position_map[row.signal_id]
            entry_pos = pos + ENTRY_LAGS[row.entry]
            bars = data[(asset, interval)]
            label = bars.ts_utc.iloc[entry_pos] if entry_pos < len(bars) else None
            labels.append(label)
            flags.append(bool(stamp(row.first_observed_at_utc) <= label) if label is not None else None)
        of["entry_label_ts"] = labels
        of["registered_before_entry_label"] = flags
    pf = pd.DataFrame(pivots) if pivots else pd.DataFrame(columns=["asset_id", "interval", "period", "pivot_position"])
    cf = pd.DataFrame(statuses) if statuses else pd.DataFrame(columns=["asset_id", "interval", "period", "origin_position", "status"])
    eligible = of.loc[(of.status == "observed") & of.registered_before_entry_label.eq(True)]
    timely_summary = summarize_outcomes(eligible) if len(eligible) else pd.DataFrame()
    ready = (not timely_summary.empty and bool(((timely_summary.observed >= 100) & (timely_summary.assets >= 20)
                                                 & (timely_summary.weeks >= 20)).any()))
    status = "blocked_data" if not forward_bar_count else ("review_required" if ready else "collecting")
    output.mkdir(parents=True, exist_ok=False)
    tables = {"signals.csv": sf, "outcomes.csv": of, "reference_pivots.csv": pf, "confirmation_status.csv": cf,
              "series_coverage.csv": pd.DataFrame(coverage),
              "new_input_manifest.csv": pd.DataFrame(input_records, columns=["asset_id", "interval", "relative_path", "sha256", "new_eligible_rows"])}
    if len(sf) and len(pf):
        tables["signal_summary.csv"] = summarize_signals(sf, pf)
    if len(of):
        tables["outcome_summary_all.csv"] = summarize_outcomes(of)
    if len(timely_summary):
        tables["outcome_summary_timely.csv"] = timely_summary
    for name, frame in tables.items():
        frame.to_csv(output / name, index=False)
    result = {"schema_version": 1, "status": status, "freeze_sha256": freeze_digest,
              "previous_manifest_sha256": sha256(previous / "manifest.json") if previous else None,
              "recorded_at_utc": recorded.isoformat(), "as_of_utc": cutoff.isoformat(),
              "forward_start_utc": FORWARD_START.isoformat(), "forward_equity_bars": forward_bar_count,
              "signal_rows": len(sf), "timely_observed_outcome_rows": len(eligible),
              "series_prefixes": prefix, "files_sha256": {name: sha256(output / name) for name in tables},
              "external_timestamp_attestation": False,
              "warning": "No automatic success or execution claim. Local time/hash and timestamps require independent verification."}
    (output / "manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    lock = commands.add_parser("freeze")
    lock.add_argument("--root", type=Path, default=Path("data/ohlcv"))
    lock.add_argument("--output", type=Path, required=True)
    snap = commands.add_parser("observe")
    snap.add_argument("--freeze", type=Path, required=True)
    snap.add_argument("--warmup-root", type=Path, default=Path("data/ohlcv"))
    snap.add_argument("--new-root", type=Path, default=Path(".cache/forward-ohlcv"))
    snap.add_argument("--output", type=Path, required=True)
    snap.add_argument("--previous", type=Path)
    snap.add_argument("--as-of", type=stamp)
    args = parser.parse_args()
    if args.command == "freeze":
        result = create_freeze(args.root, args.output)
        print(json.dumps({"frozen_at_utc": result["frozen_at_utc"], "forward_start_utc": result["forward_start_utc"],
                          "baseline_files": len(result["baseline_files"]), "externally_attested": False}, indent=2))
    else:
        result = observe(args.freeze, args.warmup_root, args.new_root, args.output, as_of=args.as_of, previous=args.previous)
        print(json.dumps({k: result[k] for k in ("status", "recorded_at_utc", "as_of_utc", "forward_equity_bars",
                                                  "signal_rows", "timely_observed_outcome_rows")}, indent=2))


if __name__ == "__main__":
    main()
