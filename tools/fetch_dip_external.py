"""Sabit MIT/yfinance arşivini araştırma önbelleğine indir; Git'e ekleme."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import tarfile
import urllib.request
from pathlib import Path

COMMIT = "f4a353bf9cf1ac3621c294fb397b812c5691e099"
URL = f"https://codeload.github.com/megecr/bist-pairs-trading/tar.gz/{COMMIT}"
ARCHIVE_SHA256 = "1c9cd340ae1b3505ca7c1c5e520b138bd4197294ba16a6a103d410f1be737f90"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(".cache/external-reference"))
    args = parser.parse_args()
    with urllib.request.urlopen(URL, timeout=60) as response:
        payload = response.read(20_000_001)
    if len(payload) > 20_000_000:
        raise ValueError("Harici arşiv beklenenden büyük")
    digest = hashlib.sha256(payload).hexdigest()
    if digest != ARCHIVE_SHA256:
        raise ValueError(f"Sabit arşiv SHA-256 uyuşmuyor: {digest}; kaynak yeniden incelenmeli")
    files: dict[str, bytes] = {}
    prefix = f"bist-pairs-trading-{COMMIT}/"
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        for item in archive:
            if not item.isfile() or not item.name.startswith(prefix):
                continue
            relative = item.name[len(prefix):]
            if relative == "LICENSE" or re.fullmatch(r"data/[A-Z0-9]+\.csv", relative):
                if relative in files or item.size > 5_000_000:
                    raise ValueError("Tekrarlı veya büyük harici dosya")
                member = archive.extractfile(item)
                if member is None:
                    raise ValueError("Arşiv dosyası okunamadı")
                files[relative] = member.read()
    if "LICENSE" not in files or len(files) < 2:
        raise ValueError("Arşivde MIT lisansı veya fiyat verisi yok")
    for relative, content in files.items():
        target = args.output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_bytes() != content:
            raise ValueError(f"Var olan farklı dosya üzerine yazılmadı: {target}")
        target.write_bytes(content)
    meta = {"repository": "https://github.com/megecr/bist-pairs-trading", "commit": COMMIT,
            "archive_sha256": digest, "csv_files": len(files) - 1,
            "license": "MIT; source repository", "warning": "Historical yfinance archive; not prospective or an independent provider."}
    (args.output / "SOURCE.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
