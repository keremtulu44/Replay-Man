"""İleri gözlemden önce kilit, seri, etiket ve veri boşluğu kontrolü.

Bu bağımsız araç dondurulmuş motoru değiştirmez veya gözlem başlatmaz. Kullanıcı
sağladığı beklenen bar etiketleri resmî takvim olarak doğrulanmış sayılmaz.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

from replayman.replay import load_bars
from tools.forward_dip_research import (FORWARD_START, now_utc, prefix_hash, safe_relative, stamp,
                                        validate_new_file, verify_freeze, verify_previous)
from tools.measure_dip_pilot import sha256

DEFAULT_FREEZE = Path("research/measurements/dip-research/forward-freeze.json")
DEFAULT_PREVIOUS = Path("research/measurements/dip-research/forward-initial")
MATURITY = {"1d": pd.Timedelta(days=1), "4h": pd.Timedelta(hours=4)}


def parse_calendar(path: Path, *, intervals: set[str], first_baseline: pd.Timestamp,
                   cutoff: pd.Timestamp) -> dict:
    """Kullanıcıdan beklenen tam bar etiketlerini oku; doğruluğunu varsayma."""
    record = json.loads(path.read_text(encoding="utf-8"))
    if record.get("schema_version") != 1 or not isinstance(record.get("source"), str) or not record["source"].strip():
        raise ValueError("Takvim için schema_version=1 ve kaynak açıklaması gerekli")
    first, last = stamp(record["coverage_start_utc"]), stamp(record["coverage_end_utc"])
    if first > first_baseline or last <= cutoff or first >= last:
        raise ValueError("Takvim kapsamı başlangıçtan kesit sonrasına kadar olmalı")
    labels = record.get("labels")
    if not isinstance(labels, dict) or set(labels) != intervals:
        raise ValueError("Takvimde kilitli her periyodun etiket listesi gerekli")
    parsed = {}
    for interval in sorted(intervals):
        raw = labels[interval]
        if not isinstance(raw, list):
            raise ValueError(f"Takvim listesi geçersiz: {interval}")
        times = pd.DatetimeIndex([stamp(value) for value in raw], tz="UTC")
        if not times.is_unique or not times.is_monotonic_increasing:
            raise ValueError(f"Takvim etiketleri yinelenmiş veya sırasız: {interval}")
        if ((times < first) | (times >= last)).any():
            raise ValueError(f"Takvim etiketi kapsam dışında: {interval}")
        parsed[interval] = times
    return {"source": record["source"], "coverage_start_utc": first, "coverage_end_utc": last,
            "labels": parsed, "file_sha256": sha256(path)}


def timing_windows(bars: pd.DataFrame, interval: str, lag: int) -> dict:
    """Tarihsel etiketlerden kayıt için kalan pencere; fiilî saat değildir."""
    if interval not in MATURITY or lag < 1:
        raise ValueError("Bilinmeyen periyot veya gecikme")
    times = pd.DatetimeIndex(bars.ts_utc)
    if not times.is_unique or not times.is_monotonic_increasing:
        raise ValueError("Bar etiketleri tekil ve sıralı olmalı")
    if len(times) <= lag:
        return {"windows": 0, "negative": 0, "zero": 0, "positive": 0}
    available = times[lag:] - (times[:-lag] + MATURITY[interval])
    seconds = available.total_seconds().to_numpy()
    return {"windows": len(seconds), "negative": int((seconds < 0).sum()),
            "zero": int((seconds == 0).sum()), "positive": int((seconds > 0).sum())}


def _raw_checks(path: Path, entry: dict, old_last: pd.Timestamp, cutoff: pd.Timestamp) -> dict:
    raw = pd.read_csv(path)
    # pd.to_datetime(..., utc=True) otherwise treats timezone-naive strings as
    # UTC, silently shifting an exchange-local timestamp. Require an offset.
    times = pd.Series([stamp(value) for value in raw.ts_utc], index=raw.index, dtype="datetime64[ns, UTC]")
    mature = (times > old_last) & (times + MATURITY[entry["interval"]] <= cutoff)
    # load_bars applies a supplied complete flag to *any* interval. Mirror it.
    if "complete" in raw:
        flags = raw.complete.astype(str).str.lower()
        complete = flags.isin({"true", "1"})
        invalid_flags = int((mature & ~flags.isin({"true", "false", "1", "0"})).sum())
    elif entry["interval"] == "4h":
        raise ValueError("4s satırlar tamamlanma bayrağı içermeli")
    else:
        complete = pd.Series(True, index=raw.index)
        invalid_flags = 0
    invalid_aggregation = 0
    if entry["interval"] == "4h":
        required = {"bar_count", "expected_bars", "derived_from"}
        if required - set(raw.columns):
            raise ValueError(f"4s türetim kolonları eksik: {sorted(required - set(raw.columns))}")
        counts = pd.to_numeric(raw.bar_count, errors="coerce")
        expected = pd.to_numeric(raw.expected_bars, errors="coerce")
        valid = (counts.notna() & np.isfinite(counts) & counts.between(1, 4) & counts.eq(np.floor(counts))
                 & expected.eq(4) & complete.eq(counts.eq(4)) & raw.derived_from.eq("1h"))
        invalid_aggregation = int((mature & ~valid).sum())
    kept = mature & complete
    bad = pd.Series(False, index=raw.index)
    for column in ("open", "high", "low", "close"):
        values = pd.to_numeric(raw[column], errors="coerce")
        bad |= ~np.isfinite(values) | (values <= 0)
    actions = []
    action_unknown = entry["kind"] == "equity" and not bool(kept.any())
    if entry["kind"] == "equity" and kept.any():
        for column in ("dividends", "stock_splits"):
            if column not in raw:
                action_unknown = True
                continue
            values = pd.to_numeric(raw[column], errors="coerce")
            if values.loc[kept].isna().any() or not np.isfinite(values.loc[kept]).all():
                action_unknown = True
            for index in raw.index[kept & values.fillna(0).ne(0)]:
                actions.append({"ts_utc": times.iloc[index].isoformat(), "field": column, "value": float(values.iloc[index])})
    return {"bad_complete_rows": int((kept & bad).sum()), "invalid_completion_flags": invalid_flags,
            "invalid_aggregation_rows": invalid_aggregation,
            "partial_mature_rows_excluded": int((mature & ~complete).sum()),
            "unmatured_new_rows": int(((times > old_last) & ~mature).sum()),
            "action_unknown": action_unknown, "corporate_actions": actions}


def preflight(freeze_path: Path, warmup_root: Path, new_root: Path, previous: Path, *,
              calendar_path: Path | None = None, as_of: pd.Timestamp | None = None,
              now: pd.Timestamp | None = None) -> dict:
    """Eksikleri ve belirsizlikleri göster; hiçbir veriyi veya kesiti değiştirme."""
    frozen = verify_freeze(freeze_path, warmup_root)
    recorded = stamp(now if now is not None else now_utc())
    cutoff = stamp(as_of if as_of is not None else recorded)
    if cutoff > recorded or cutoff < stamp(frozen["frozen_at_utc"]) or recorded < stamp(frozen["frozen_at_utc"]):
        raise ValueError("Kesit gelecekte veya kilitten önce olamaz")
    warm, fresh = warmup_root.resolve(), new_root.resolve()
    if fresh == warm or fresh.is_relative_to(warm) or warm.is_relative_to(fresh):
        raise ValueError("Yeni veri ve sabit ısınma kökleri ayrı olmalı")
    prior, _ = verify_previous(previous, sha256(freeze_path), cutoff, recorded)
    intervals = {row["interval"] for row in frozen["baseline_files"]}
    if not intervals <= set(MATURITY):
        raise ValueError(f"Beklenmeyen periyot: {intervals}")
    first_baseline = min(stamp(row["last_ts"]) for row in frozen["baseline_files"])
    calendar = (parse_calendar(calendar_path, intervals=intervals, first_baseline=first_baseline, cutoff=cutoff)
                if calendar_path is not None else None)
    rows = []
    timing: dict[tuple[str, int], Counter] = {}
    for entry in frozen["baseline_files"]:
        interval, asset = entry["interval"], entry["asset_id"]
        original_path = safe_relative(warmup_root, entry["relative_path"])
        old = load_bars(original_path)
        if old.empty or old.ts_utc.iloc[-1] != stamp(entry["last_ts"]):
            raise ValueError(f"Isınma son bar etiketi uyuşmuyor: {asset}/{interval}")
        old_last = old.ts_utc.iloc[-1]
        if entry["kind"] == "equity":
            for lag in (1, 2):
                timing.setdefault((interval, lag), Counter()).update(timing_windows(old, interval, lag))
        new_path = safe_relative(new_root, entry["relative_path"])
        record = {"asset_id": asset, "interval": interval, "kind": entry["kind"],
                  "relative_path": entry["relative_path"],
                  "baseline_last_ts": old_last.isoformat(), "new_file_status": "missing",
                  "new_file_sha256": None, "eligible_rows": 0, "forward_rows": 0,
                  "partial_mature_rows_excluded": 0, "unmatured_new_rows": 0,
                  "missing_expected_labels": None, "unexpected_labels": None,
                  "missing_examples": [], "unexpected_examples": [], "prior_prefix_verified": False,
                  "action_unknown": entry["kind"] == "equity", "corporate_actions": [], "error": None}
        appended = old.iloc[0:0].copy()
        if new_path.is_file():
            try:
                bars = validate_new_file(new_path, entry)
                check = _raw_checks(new_path, entry, old_last, cutoff)
                if check["invalid_completion_flags"]:
                    raise ValueError(f"{check['invalid_completion_flags']} belirsiz tamamlanma bayrağı")
                if check["invalid_aggregation_rows"]:
                    raise ValueError(f"{check['invalid_aggregation_rows']} tutarsız 4s türetim kaydı")
                if check["bad_complete_rows"]:
                    raise ValueError(f"{check['bad_complete_rows']} geçerli zamanda hatalı/eksik OHLC")
                appended = bars.loc[(bars.ts_utc > old_last) & (bars.ts_utc + MATURITY[interval] <= cutoff)].copy()
                record.update({"new_file_status": "valid", "new_file_sha256": sha256(new_path),
                               "eligible_rows": len(appended),
                               "forward_rows": int((appended.ts_utc >= FORWARD_START).sum()),
                               "partial_mature_rows_excluded": check["partial_mature_rows_excluded"],
                               "unmatured_new_rows": check["unmatured_new_rows"],
                               "action_unknown": check["action_unknown"], "corporate_actions": check["corporate_actions"]})
            except (ValueError, KeyError, OSError, TypeError) as exc:
                record.update({"new_file_status": "invalid", "error": str(exc)})
        combined = pd.concat([old, appended], ignore_index=True)
        key = f"{asset}|{interval}"
        prefix = prior["series_prefixes"].get(key)
        if prefix is not None and len(combined) >= prefix["rows"]:
            record["prior_prefix_verified"] = prefix_hash(combined.iloc[:prefix["rows"]]) == prefix["sha256"]
        if calendar is not None:
            labels = calendar["labels"][interval]
            expected = set(labels[(labels > old_last) & (labels + MATURITY[interval] <= cutoff)])
            actual = set(pd.DatetimeIndex(appended.ts_utc))
            missing, unexpected = sorted(expected - actual), sorted(actual - expected)
            record.update({"missing_expected_labels": len(missing), "unexpected_labels": len(unexpected),
                           "missing_examples": [t.isoformat() for t in missing[:5]],
                           "unexpected_examples": [t.isoformat() for t in unexpected[:5]]})
        rows.append(record)
    counts = Counter(row["new_file_status"] for row in rows)
    prefix_bad = sum(not r["prior_prefix_verified"] for r in rows)
    gap_count = sum(r["missing_expected_labels"] + r["unexpected_labels"] for r in rows) if calendar else None
    action_count = sum(len(r["corporate_actions"]) for r in rows)
    action_unknown = sum(r["action_unknown"] for r in rows if r["kind"] == "equity")
    forward_equity = sum(r["forward_rows"] for r in rows if r["kind"] == "equity")
    blockers = []
    if counts["invalid"] or prefix_bad:
        blockers.append("input_or_previous_prefix_invalid")
    if counts["missing"] or not sum(r["eligible_rows"] for r in rows):
        blockers.append("new_data_missing_or_incomplete")
    if calendar is None:
        blockers.append("expected_complete_bar_calendar_not_provided")
    elif gap_count:
        blockers.append("calendar_label_discrepancies")
    if action_count or action_unknown:
        blockers.append("corporate_actions_need_review")
    if cutoff < FORWARD_START:
        blockers.append("forward_start_not_reached")
    elif forward_equity == 0:
        blockers.append("no_eligible_forward_equity_bars")
    if "input_or_previous_prefix_invalid" in blockers:
        status = "blocked_integrity"
    elif "new_data_missing_or_incomplete" in blockers:
        status = "blocked_data"
    elif "expected_complete_bar_calendar_not_provided" in blockers:
        status = "blocked_calendar"
    elif "calendar_label_discrepancies" in blockers:
        status = "blocked_gaps"
    elif "corporate_actions_need_review" in blockers:
        status = "blocked_corporate_actions"
    elif "forward_start_not_reached" in blockers:
        status = "awaiting_forward_start"
    elif "no_eligible_forward_equity_bars" in blockers:
        status = "blocked_data"
    else:
        status = "manual_review_required"
    timing_summary = []
    for (interval, lag), values in sorted(timing.items()):
        timing_summary.append({"interval": interval, "entry_lag": lag, **dict(values)})
    calendar_info = ({"status": "not_provided", "independently_verified": False} if calendar is None else
                     {"status": "provided_not_independently_verified", "source": calendar["source"],
                      "sha256": calendar["file_sha256"],
                      "coverage_start_utc": calendar["coverage_start_utc"].isoformat(),
                      "coverage_end_utc": calendar["coverage_end_utc"].isoformat(), "independently_verified": False})
    return {"schema_version": 1, "status": status, "blockers": blockers,
            "recorded_at_utc": recorded.isoformat(), "as_of_utc": cutoff.isoformat(),
            "forward_start_utc": stamp(frozen["forward_start_utc"]).isoformat(), "freeze_sha256": sha256(freeze_path),
            "preflight_tool_sha256": sha256(Path(__file__)), "frozen_inputs_verified": len(frozen["baseline_files"]),
            "previous_manifest_sha256": sha256(previous / "manifest.json"),
            "previous_status": prior["status"], "new_root": str(new_root),
            "new_file_counts": {"valid": counts["valid"], "missing": counts["missing"], "invalid": counts["invalid"]},
            "eligible_new_rows": sum(r["eligible_rows"] for r in rows), "eligible_forward_equity_rows": forward_equity,
            "prior_prefix_mismatches": prefix_bad, "expected_label_discrepancies": gap_count,
            "corporate_action_events": action_count, "equity_series_action_status_unknown": action_unknown,
            "calendar": calendar_info, "baseline_timing_windows": timing_summary, "series": rows,
            "warnings": ["Kullanıcı takvimi ve seans/bar etiketleri bağımsız doğrulanmış değildir.",
                         "Sıfır kayıt penceresinde giriş etiketine kadar kayıt için tam zaman eşitliği gerekir; gerçekleşme kanıtı yoktur.",
                         "Kısmi barlar ve kurumsal işlem kayıtlarının doğruluğu ayrıca denetlenmelidir.",
                         "Ön-kontrol ve gözlem atomik değildir: aynı kesit saatini kullanın ve veri SHA değerlerini karşılaştırın.",
                         "Bu araç gözlem, emir, kârlılık, gerçek piyasa verisi veya harici zaman damgası üretmez."]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", type=Path, default=DEFAULT_FREEZE)
    parser.add_argument("--warmup-root", type=Path, default=Path("data/ohlcv"))
    parser.add_argument("--new-root", type=Path, default=Path("data/forward-ohlcv"))
    parser.add_argument("--previous", type=Path, default=DEFAULT_PREVIOUS)
    parser.add_argument("--calendar", type=Path, help="Kaynak ve beklenen tam bar etiketleri içeren kullanıcı takvimi JSON")
    parser.add_argument("--as-of", help="UTC ofsetli geçmiş kesit; gelecekte olamaz")
    parser.add_argument("--output", type=Path, help="Yeni rapor yolu; var olan dosya üzerine yazılmaz")
    args = parser.parse_args()
    result = preflight(args.freeze, args.warmup_root, args.new_root, args.previous,
                       calendar_path=args.calendar, as_of=stamp(args.as_of) if args.as_of else None)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    summary = {key: result[key] for key in ("status", "blockers", "recorded_at_utc", "frozen_inputs_verified",
               "new_file_counts", "eligible_new_rows", "eligible_forward_equity_rows", "prior_prefix_mismatches",
               "expected_label_discrepancies", "calendar", "baseline_timing_windows")}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if result["status"] != "manual_review_required":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
