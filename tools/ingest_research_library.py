#!/usr/bin/env python3
"""Katalogdaki PDF'leri sayfa kaybı olmadan aranabilir JSONL kaynağına dönüştürür."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "research/library/catalog.json"
OUTPUT = ROOT / "research/knowledge/source-pages"


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = {"schema_version": 1, "sources": []}
    for book in catalog["books"]:
        path = ROOT / book["path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != book["sha256"]:
            raise ValueError(f"Kaynak özeti uyuşmuyor: {path}")
        reader = PdfReader(path)
        target = OUTPUT / f"{book['id']}.jsonl"
        chars = 0
        with target.open("w", encoding="utf-8") as handle:
            for page_number, page in enumerate(reader.pages, 1):
                text = (page.extract_text() or "").replace("\u0000", "").strip()
                chars += len(text)
                record = {
                    "source_id": book["id"],
                    "page": page_number,
                    "text": text,
                }
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        manifest["sources"].append({
            "source_id": book["id"],
            "pdf_sha256": digest,
            "pages": len(reader.pages),
            "characters": chars,
            "jsonl": target.relative_to(ROOT).as_posix(),
        })
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
