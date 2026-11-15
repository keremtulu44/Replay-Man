#!/usr/bin/env python3
"""Bilgi tabanı kapsamını, sayfa bütünlüğünü ve referansları denetler."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/knowledge"
EXPECTED = {"ATK-TR-D1.0-2026-08": (530, 24), "PTA-C1-2026": (139, 21), "PTA-C2-2026": (109, 13)}


def main() -> int:
    errors = []
    total = 0
    for source_id, (pages, chapters) in EXPECTED.items():
        path = BASE / "processed" / f"{source_id}-cards.jsonl"
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        total += len(rows)
        if len(rows) != pages: errors.append(f"{source_id}: kart={len(rows)} beklenen={pages}")
        page_numbers = [row["page"] for row in rows]
        if page_numbers != list(range(1, pages + 1)): errors.append(f"{source_id}: sayfa sırası/kapsamı bozuk")
        seen_chapters = {row["chapter"] for row in rows if row["chapter"] is not None}
        if seen_chapters != set(range(1, chapters + 1)): errors.append(f"{source_id}: bölüm kapsamı bozuk={sorted(seen_chapters)}")
        for row in rows:
            if not row["source_excerpt"].strip(): errors.append(f"{row['id']}: boş kaynak")
            if row["source_id"] != source_id: errors.append(f"{row['id']}: kaynak kimliği")
            for topic in row["topics"]:
                if not topic["id"] or topic["score"] <= 0: errors.append(f"{row['id']}: konu kaydı")
    theme_count = len(list((BASE / "processed/themes").glob("*.md")))
    if theme_count != 22: errors.append(f"tema={theme_count} beklenen=22")
    chapter_files = len(list((BASE / "processed/chapters").glob("*/*.md")))
    expected_chapters = sum(value[1] for value in EXPECTED.values())
    if chapter_files != expected_chapters: errors.append(f"bölüm dosyası={chapter_files} beklenen={expected_chapters}")
    report = {"status": "passed" if not errors else "failed", "sources": 3, "pages_and_cards": total,
              "chapters": expected_chapters, "chapter_dossiers": chapter_files, "topic_dossiers": theme_count,
              "errors": errors}
    (BASE / "processed/audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
