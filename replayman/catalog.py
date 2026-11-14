"""Sembol kataloğu okuma."""
from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path

REQUIRED = {"id", "category", "name", "local_symbol", "yahoo_symbol", "asset_type", "currency", "enabled"}


@dataclass(frozen=True)
class Asset:
    id: str
    category: str
    name: str
    local_symbol: str
    yahoo_symbol: str
    asset_type: str
    currency: str
    enabled: str


def load_catalog(
    path: str | Path,
    symbols: list[str] | None = None,
    limit: int | None = None,
) -> tuple[list[Asset], str]:
    path = Path(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Katalogda eksik kolonlar: {', '.join(sorted(missing))}")
        assets: list[Asset] = []
        seen_ids: set[str] = set()
        seen_symbols: set[str] = set()
        for line, row in enumerate(reader, start=2):
            if (row.get("enabled") or "").strip().lower() not in {"true", "1", "yes"}:
                continue
            values = {key: (row.get(key) or "").strip() for key in REQUIRED}
            if any(not value for value in values.values()):
                raise ValueError(f"Katalog satırı {line}: boş zorunlu alan")
            if values["id"] in seen_ids:
                raise ValueError(f"Tekrar eden id: {values['id']}")
            if values["yahoo_symbol"] in seen_symbols:
                raise ValueError(f"Tekrar eden yahoo_symbol: {values['yahoo_symbol']}")
            seen_ids.add(values["id"])
            seen_symbols.add(values["yahoo_symbol"])
            assets.append(Asset(**values))
    if symbols:
        wanted = {s.strip().upper() for s in symbols if s.strip()}
        assets = [
            a for a in assets
            if a.local_symbol.upper() in wanted
            or a.yahoo_symbol.upper() in wanted
            or a.id.upper() in wanted
        ]
        missing = wanted - {a.local_symbol.upper() for a in assets} - {a.yahoo_symbol.upper() for a in assets} - {a.id.upper() for a in assets}
        if missing:
            raise ValueError(f"Katalogda bulunamayan semboller: {', '.join(sorted(missing))}")
    if limit is not None:
        if limit < 1:
            raise ValueError("limit >= 1 olmalı")
        assets = assets[:limit]
    if not assets:
        raise ValueError("Katalogda etkin varlık yok")
    return assets, digest
