"""Bir gözlem kesitinin incelenmiş ön-kontrolle tutarlı olup olmadığını kontrol et.

Bu, dış zaman damgası, doğru piyasa verisi veya emir gerçekleşmesi kanıtı değildir.
Ön-kontrol ve gözlem atomik değildir; giriş dosyalarını işlem sırasında değiştirmeyin.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import pandas as pd

import tools.preflight_forward_observation as preflight_tool
from tools.forward_dip_research import now_utc, stamp, verify_previous
from tools.measure_dip_pilot import sha256


def _keyed(rows, *, description: str) -> dict[tuple[str, str], dict]:
    result = {}
    for row in rows:
        key = (row["asset_id"], row["interval"])
        if key in result:
            raise ValueError(f"{description}: yinelenen seri {key}")
        result[key] = row
    return result


def _csv_rows(path: Path, required: set[str]) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not required <= set(reader.fieldnames):
            raise ValueError(f"Kesit CSV kolonları eksik: {path}")
        return list(reader)


def verify(preflight_path: Path, snapshot: Path, previous: Path, freeze: Path, *,
           now: pd.Timestamp | None = None) -> dict:
    """Hash, kapsam ve as-of eşleşmesini kontrol et; hiçbir dosyayı değiştirme."""
    report = json.loads(preflight_path.read_text(encoding="utf-8"))
    if (report.get("schema_version") != 1 or report.get("status") != "manual_review_required"
            or report.get("blockers") != [] or report.get("expected_label_discrepancies") != 0
            or report.get("prior_prefix_mismatches") != 0
            or report.get("corporate_action_events") != 0 or report.get("equity_series_action_status_unknown") != 0):
        raise ValueError("Ön-kontrol engelli veya manuel inceleme aşamasına ulaşmamış")
    if report.get("preflight_tool_sha256") != sha256(Path(preflight_tool.__file__)):
        raise ValueError("Ön-kontrol aracı rapordan sonra değişmiş; yeni ön-kontrol gerekli")
    cutoff = stamp(report["as_of_utc"])
    preflight_recorded = stamp(report["recorded_at_utc"])
    current = stamp(now if now is not None else now_utc())
    if cutoff > preflight_recorded or preflight_recorded > current:
        raise ValueError("Ön-kontrol kesit veya kayıt zamanı geçersiz")
    freeze_hash, previous_hash = sha256(freeze), sha256(previous / "manifest.json")
    if freeze_hash != report["freeze_sha256"] or previous_hash != report["previous_manifest_sha256"]:
        raise ValueError("Ön-kontrolün kilidi veya önceki kesiti değişmiş")
    verify_previous(previous, freeze_hash, cutoff, preflight_recorded)
    frozen = json.loads(freeze.read_text(encoding="utf-8"))
    if stamp(frozen["forward_start_utc"]) != stamp(report["forward_start_utc"]):
        raise ValueError("İleri başlangıç zamanı uyuşmuyor")
    frozen_rows = _keyed(frozen["baseline_files"], description="Kilit")
    checked = _keyed(report["series"], description="Ön-kontrol")
    if (set(checked) != set(frozen_rows) or len(checked) != report["frozen_inputs_verified"]
            or report["new_file_counts"] != {"valid": len(checked), "missing": 0, "invalid": 0}):
        raise ValueError("Ön-kontrol kilitli seri kapsamıyla uyuşmuyor")
    for key, row in checked.items():
        original = frozen_rows[key]
        if (row["relative_path"] != original["relative_path"] or row["kind"] != original["kind"]
                or row["new_file_status"] != "valid" or not row["new_file_sha256"]
                or row["prior_prefix_verified"] is not True
                or row["missing_expected_labels"] != 0 or row["unexpected_labels"] != 0
                or row["action_unknown"] or row["corporate_actions"]):
            raise ValueError(f"Ön-kontrol serisi tutarsız: {key}")
    observed, _ = verify_previous(snapshot, freeze_hash, cutoff, current)
    if (observed.get("schema_version") != 1 or stamp(observed["as_of_utc"]) != cutoff
            or stamp(observed["recorded_at_utc"]) < preflight_recorded
            or stamp(observed["forward_start_utc"]) != stamp(frozen["forward_start_utc"])
            or observed.get("previous_manifest_sha256") != previous_hash):
        raise ValueError("Gözlem kesit saati, kayıt sırası veya önceki kesit uyuşmuyor")
    required_outputs = {"signals.csv", "outcomes.csv", "reference_pivots.csv", "confirmation_status.csv",
                        "series_coverage.csv", "new_input_manifest.csv"}
    if not required_outputs <= set(observed.get("files_sha256", {})):
        raise ValueError("Gözlem manifestinde gerekli çıktı hash'leri eksik")
    if observed.get("status") not in {"collecting", "review_required"}:
        raise ValueError("Gözlemde ileri veri yok veya gözlem durumu geçersiz")
    manifest_rows = _keyed(_csv_rows(snapshot / "new_input_manifest.csv",
                                     {"asset_id", "interval", "relative_path", "sha256", "new_eligible_rows"}),
                           description="Gözlem girişleri")
    coverage = _keyed(_csv_rows(snapshot / "series_coverage.csv",
                                {"asset_id", "interval", "kind", "appended_rows", "forward_rows"}),
                      description="Gözlem kapsamı")
    if set(manifest_rows) != set(checked) or set(coverage) != set(checked):
        raise ValueError("Gözlemdeki yeni veri veya kapsam seri listesi ön-kontrolle uyuşmuyor")
    for key, row in checked.items():
        entry, actual = manifest_rows[key], coverage[key]
        if (entry["relative_path"] != row["relative_path"] or entry["sha256"] != row["new_file_sha256"]
                or int(entry["new_eligible_rows"]) != row["eligible_rows"]
                or actual["kind"] != row["kind"] or int(actual["appended_rows"]) != row["eligible_rows"]
                or int(actual["forward_rows"]) != row["forward_rows"]):
            raise ValueError(f"Gözlem girdisi veya olgun bar sayısı ön-kontrolle uyuşmuyor: {key}")
    if report["eligible_new_rows"] != sum(row["eligible_rows"] for row in checked.values()):
        raise ValueError("Ön-kontroldeki toplam uygun bar sayısı uyuşmuyor")
    forward_rows = sum(row["forward_rows"] for row in checked.values() if row["kind"] == "equity")
    if (forward_rows <= 0 or report["eligible_forward_equity_rows"] != forward_rows
            or observed["forward_equity_bars"] != forward_rows):
        raise ValueError("İleri hisse barı sayısı uyuşmuyor")
    verified_at = stamp(now if now is not None else now_utc())
    return {"status": "consistent_manual_review_still_required", "series_compared": len(checked),
            "verified_at_utc": verified_at.isoformat(), "as_of_utc": cutoff.isoformat(),
            "preflight_sha256": sha256(preflight_path),
            "verification_tool_sha256": sha256(Path(__file__)),
            "snapshot_manifest_sha256": sha256(snapshot / "manifest.json"),
            "previous_manifest_sha256": previous_hash, "freeze_sha256": freeze_hash,
            "external_timestamp_attestation": False,
            "warnings": ["Tutarlılık doğrulaması doğru piyasa verisi veya insan incelemesi yerine geçmez.",
                         "Motorun kayıt zamanı hesaplama başlangıcıdır; çıktıların tamamlanma zamanını kanıtlamaz.",
                         "Kontrol ve gözlem atomik değildir; eşleşme harici zaman damgası veya emir kanıtı değildir."]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", required=True, type=Path)
    parser.add_argument("--snapshot", required=True, type=Path)
    parser.add_argument("--previous", required=True, type=Path)
    parser.add_argument("--freeze", type=Path, default=preflight_tool.DEFAULT_FREEZE)
    parser.add_argument("--output", type=Path, help="Benzersiz rapor yolu; üzerine yazılmaz")
    args = parser.parse_args()
    result = verify(args.preflight, args.snapshot, args.previous, args.freeze)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
