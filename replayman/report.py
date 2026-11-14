"""Çalıştırma raporları."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from .config import Settings
from .state import State


def write_reports(settings: Settings, state: State, summary: dict) -> None:
    directory = Path(settings.report_dir)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    tasks = state.all_tasks()
    task_fields = ["asset_id", "interval", "start", "end", "status", "attempts", "next_retry_at", "error_kind", "last_error", "rows", "from_cache", "updated_at"]
    with (directory / "tasks.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=task_fields)
        writer.writeheader()
        for row in tasks:
            writer.writerow({key: row[key] for key in task_fields})
    with (directory / "errors.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=task_fields)
        writer.writeheader()
        for row in tasks:
            if row["status"] == "failed" or row["last_error"]:
                writer.writerow({key: row[key] for key in task_fields})
    coverage_fields = ["asset_id", "interval", "complete", "failed", "pending", "rows"]
    with (directory / "coverage.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=coverage_fields)
        writer.writeheader()
        for row in state.coverage():
            writer.writerow({key: row[key] for key in coverage_fields})

    counts = summary.get("task_counts", {})
    lines = [
        "# Replay-Man indirme raporu",
        "",
        f"- Durum: **{summary.get('status')}**",
        f"- Varlık: {summary.get('assets')}",
        f"- Bu çalıştırmadaki ağ isteği: {summary.get('network_requests')}",
        f"- Önbellekten gelen görev: {summary.get('cache_hits')}",
        f"- Görevler: {counts}",
        f"- Türetilen varlık: {summary.get('derived', {}).get('assets', 0)}",
        f"- Günlük karşılaştırma uyuşmazlığı: {summary.get('derived', {}).get('daily_mismatches', 0)}",
    ]
    if summary.get("stop_reason"):
        lines.append(f"- Not: {summary['stop_reason']}")
    lines += [
        "",
        "Dosyalar:",
        "- `tasks.csv`: tüm görevler ve yeniden deneme zamanları",
        "- `errors.csv`: başarısız/hatalı görevler",
        "- `coverage.csv`: varlık ve periyot kapsama özeti",
        "",
        "Aynı komutu tekrar çalıştırmak tamamlanan görevleri atlar, bekleyen görevleri sürdürür.",
    ]
    (directory / "latest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
