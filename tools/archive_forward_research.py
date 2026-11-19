"""Kilitli ileri araştırmayı yerel arşive al ve arşivi çıkarmadan doğrula.

SHA ve yerel saat bağımsız zaman damgası, değiştirilemez saklama veya işlem kanıtı
sağlamaz. Bu araç mevcut kilidi değiştirmez ve yeni bir kilit oluşturmaz.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

FREEZE_NAME = "research/measurements/dip-research/forward-freeze.json"
SNAPSHOT_NAME = "research/measurements/dip-research/forward-initial"
BASE_NAME = "data/ohlcv"
INDEX_NAME = "_archive/MANIFEST.json"
NOTE_NAME = "_archive/README.txt"
EXTRA_FILES = (
    "replayman/__init__.py", "requirements.txt", "requirements-dev.txt",
    "research/measurements/dip-research/requirements-forward.txt",
    "tools/archive_forward_research.py",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_name(value: str) -> str:
    name = PurePosixPath(value)
    if (not value or "\\" in value or name.is_absolute() or ".." in name.parts
            or any(part in {"", "."} for part in name.parts) or str(name) != value):
        raise ValueError(f"Güvensiz arşiv yolu: {value}")
    return value


def safe_local(root: Path, relative: str) -> Path:
    safe_name(relative)
    root = root.resolve()
    path = root.joinpath(*PurePosixPath(relative).parts)
    if not path.resolve().is_relative_to(root):
        raise ValueError(f"Yerel yol kök dışına çıkıyor: {relative}")
    return path


def parse_stamp(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Zaman damgasında UTC ofseti gerekli")
    return result.astimezone(timezone.utc)


def collect_files(workspace: Path, warmup_root: Path, freeze_path: Path, snapshot_dir: Path,
                  *, extras: tuple[str, ...] = EXTRA_FILES) -> tuple[dict, dict[str, tuple[Path, str, str]]]:
    """Orijinal kilit/ilk kesitin ve tüm kaynakların hash'lerini doğrula."""
    workspace, warmup_root = workspace.resolve(), warmup_root.resolve()
    freeze_bytes = freeze_path.read_bytes()
    freeze = json.loads(freeze_bytes)
    if freeze.get("schema_version") != 1 or parse_stamp(freeze["frozen_at_utc"]) >= parse_stamp(freeze["forward_start_utc"]):
        raise ValueError("İleri kilidin sürümü veya zaman sırası geçersiz")
    if not freeze.get("code_sha256") or not freeze.get("baseline_files"):
        raise ValueError("İleri kilitte kod veya ısınma verisi yok")
    files: dict[str, tuple[Path, str, str]] = {}

    def add(name: str, source: Path, expected: str | None, category: str) -> None:
        safe_name(name)
        if not source.is_file():
            raise ValueError(f"Arşiv girdisi yok: {source}")
        actual = digest(source.read_bytes())
        if expected is not None and actual != expected:
            raise ValueError(f"Arşiv girdisi hash uyuşmazlığı: {source}")
        if name in files:
            old_path, old_hash, _ = files[name]
            if old_hash != actual or old_path.resolve() != source.resolve():
                raise ValueError(f"Arşivde çakışan yol: {name}")
            return
        files[name] = (source, actual, category)

    add(FREEZE_NAME, freeze_path, digest(freeze_bytes), "freeze")
    for name, expected in freeze["code_sha256"].items():
        add(name, safe_local(workspace, name), expected, "frozen_code")
    keys = set()
    for row in freeze["baseline_files"]:
        relative = safe_name(row["relative_path"])
        key = (row["asset_id"], row["interval"])
        if key in keys:
            raise ValueError(f"Kilit içinde yinelenen seri: {key}")
        keys.add(key)
        parts = PurePosixPath(relative).parts
        if (len(parts) < 4 or parts[-4] != row["asset_id"] or parts[-3] != row["series_id"]
                or parts[-2] != "bars" or PurePosixPath(relative).stem != row["interval"]):
            raise ValueError(f"Kilit seri kimliği/yolu uyuşmuyor: {relative}")
        source = safe_local(warmup_root, relative)
        add(f"{BASE_NAME}/{relative}", source, row["sha256"], "baseline_csv")
        series_relative = str(PurePosixPath(relative).parent.parent / "series.json")
        add(f"{BASE_NAME}/{series_relative}", safe_local(warmup_root, series_relative),
            row["series_manifest_sha256"], "baseline_policy")
    snapshot_path = snapshot_dir / "manifest.json"
    initial = json.loads(snapshot_path.read_text(encoding="utf-8"))
    if initial.get("freeze_sha256") != digest(freeze_bytes) or not initial.get("files_sha256"):
        raise ValueError("İlk kesit kilidi veya çıktı manifesti uyuşmuyor")
    add(f"{SNAPSHOT_NAME}/manifest.json", snapshot_path, None, "initial_manifest")
    for name, expected in initial["files_sha256"].items():
        add(f"{SNAPSHOT_NAME}/{safe_name(name)}", safe_local(snapshot_dir, name), expected, "initial_output")
    for name in extras:
        add(name, safe_local(workspace, name), None, "auxiliary_not_frozen")
    return freeze, files


def _tar_entry(tar: tarfile.TarFile, name: str, data: bytes) -> None:
    info = tarfile.TarInfo(safe_name(name))
    info.size = len(data)
    info.mode = 0o644
    info.mtime = 0
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    tar.addfile(info, io.BytesIO(data))


def create_archive(archive: Path, workspace: Path, warmup_root: Path, freeze_path: Path,
                   snapshot_dir: Path, *, extras: tuple[str, ...] = EXTRA_FILES) -> dict:
    """Üzerine yazmadan arşiv oluştur; her kaynağı paketlenirken tekrar doğrula."""
    archive.parent.mkdir(parents=True, exist_ok=True)
    sidecar = Path(str(archive) + ".sha256")
    if archive.exists() or sidecar.exists():
        raise FileExistsError("Arşiv veya SHA dosyası zaten var; üzerine yazılmadı")
    freeze, files = collect_files(workspace, warmup_root, freeze_path, snapshot_dir, extras=extras)
    made_at = datetime.now(timezone.utc)
    note = (
        "Replay-Man yerel ileri-araştırma arşivi\n"
        "Bu arşiv ve saat yereldir; harici zaman damgası veya değiştirilemez saklama DEĞİLDİR.\n"
        f"Orijinal kilit, {len(freeze['baseline_files'])} ısınma CSV'si, fiyat politikaları, kilitli kod ve ilk kesit korunur.\n"
        "Diğer OHLCV dosyaları, harici yfinance arşivi ve yeni ileri veriler dahil değildir.\n"
        "Özgün kilidi yeniden oluşturmayın; harici ve güvenli bir yerde ayrıca saklayın.\n"
    ).encode("utf-8")
    manifest = {"schema_version": 1, "created_at_utc": made_at.isoformat(),
                "forward_start_utc": freeze["forward_start_utc"],
                "local_creation_before_forward_start": made_at < parse_stamp(freeze["forward_start_utc"]),
                "freeze_sha256": files[FREEZE_NAME][1],
                "initial_manifest_sha256": files[f"{SNAPSHOT_NAME}/manifest.json"][1],
                "runtime": freeze["runtime"], "baseline_series": len(freeze["baseline_files"]),
                "external_timestamp_attestation": False,
                "warning": "Local hash/time only; no independent timestamp, immutable storage or trading evidence.",
                "files": []}
    created = False
    try:
        with archive.open("xb") as handle:
            created = True
            with tarfile.open(fileobj=handle, mode="w:gz", format=tarfile.PAX_FORMAT) as tar:
                for name, (source, expected, category) in sorted(files.items()):
                    content = source.read_bytes()
                    if digest(content) != expected:
                        raise ValueError(f"Arşiv hazırlanırken kaynak değişti: {source}")
                    _tar_entry(tar, name, content)
                    manifest["files"].append({"path": name, "sha256": expected, "bytes": len(content), "category": category})
                _tar_entry(tar, NOTE_NAME, note)
                manifest["files"].append({"path": NOTE_NAME, "sha256": digest(note), "bytes": len(note), "category": "archive_note"})
                _tar_entry(tar, INDEX_NAME, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        report = verify_archive(archive)
        archive_hash = digest(archive.read_bytes())
        with sidecar.open("x", encoding="utf-8") as handle:
            handle.write(f"{archive_hash}  {archive.name}\n")
        return {**report, "archive": str(archive), "sha256": archive_hash, "sha256_file": str(sidecar)}
    except Exception:
        if created:
            archive.unlink(missing_ok=True)
        raise


def verify_archive(archive: Path, *, expected_sha256: str | None = None) -> dict:
    """Arşivi diske çıkarmadan dosya, kilit ve ilk kesit ilişkilerini doğrula."""
    whole_hash = digest(archive.read_bytes())
    if expected_sha256 is not None and whole_hash != expected_sha256:
        raise ValueError("Arşiv SHA-256 uyuşmazlığı")
    with tarfile.open(archive, mode="r:gz") as tar:
        members = tar.getmembers()
        names = [safe_name(member.name) for member in members]
        if len(set(names)) != len(names) or any(not x.isfile() or x.size > 100_000_000 for x in members):
            raise ValueError("Arşivde yinelenen, dosya olmayan veya büyük üye var")
        if sum(x.size for x in members) > 500_000_000 or INDEX_NAME not in names:
            raise ValueError("Arşiv boyutu veya indeksi geçersiz")
        entries = {member.name: member for member in members}

        def read(name: str) -> bytes:
            member = entries.get(name)
            if member is None:
                raise ValueError(f"Arşiv üyesi eksik: {name}")
            handle = tar.extractfile(member)
            if handle is None:
                raise ValueError(f"Arşiv üyesi okunamıyor: {name}")
            return handle.read()

        index = json.loads(read(INDEX_NAME))
        if index.get("schema_version") != 1:
            raise ValueError("Arşiv manifest sürümü geçersiz")
        listed = index.get("files", [])
        expected = {safe_name(row["path"]): row for row in listed}
        if len(expected) != len(listed) or set(expected) | {INDEX_NAME} != set(names):
            raise ValueError("Arşiv manifesti dosya listesiyle uyuşmuyor")
        for name, row in expected.items():
            content = read(name)
            if len(content) != row["bytes"] or digest(content) != row["sha256"]:
                raise ValueError(f"Arşiv üyesi hash uyuşmazlığı: {name}")
        freeze_bytes = read(FREEZE_NAME)
        if digest(freeze_bytes) != index["freeze_sha256"]:
            raise ValueError("Arşiv kilit hash'i uyuşmuyor")
        freeze = json.loads(freeze_bytes)
        if len(freeze["baseline_files"]) != index["baseline_series"]:
            raise ValueError("Arşiv ısınma serisi sayısı uyuşmuyor")
        for name, hashed in freeze["code_sha256"].items():
            if digest(read(safe_name(name))) != hashed:
                raise ValueError(f"Arşivdeki kilitli kod uyuşmuyor: {name}")
        keys = set()
        for row in freeze["baseline_files"]:
            key = (row["asset_id"], row["interval"])
            if key in keys:
                raise ValueError("Arşivde yinelenen ısınma serisi")
            keys.add(key)
            rel = safe_name(row["relative_path"])
            data_name = f"{BASE_NAME}/{rel}"
            policy_name = f"{BASE_NAME}/{PurePosixPath(rel).parent.parent / 'series.json'}"
            if digest(read(data_name)) != row["sha256"] or digest(read(policy_name)) != row["series_manifest_sha256"]:
                raise ValueError(f"Arşivdeki ısınma girdisi uyuşmuyor: {rel}")
        initial_bytes = read(f"{SNAPSHOT_NAME}/manifest.json")
        initial = json.loads(initial_bytes)
        if digest(initial_bytes) != index["initial_manifest_sha256"] or initial["freeze_sha256"] != digest(freeze_bytes):
            raise ValueError("Arşivdeki ilk kesit/kilit bağı uyuşmuyor")
        for name, hashed in initial["files_sha256"].items():
            if digest(read(f"{SNAPSHOT_NAME}/{safe_name(name)}")) != hashed:
                raise ValueError(f"Arşivdeki ilk kesit çıktısı uyuşmuyor: {name}")
    return {"status": "verified", "files": len(expected), "baseline_series": len(freeze["baseline_files"]),
            "freeze_sha256": index["freeze_sha256"], "initial_status": initial["status"],
            "created_at_utc": index["created_at_utc"],
            "local_creation_before_forward_start": index["local_creation_before_forward_start"],
            "external_timestamp_attestation": False,
            "scope": "Archive integrity only; local SHA/time is not independent attestation or execution evidence."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create", help="Mevcut kilit ve ısınma girdilerini yeni yerel arşive kaydet")
    create.add_argument("--archive", type=Path, required=True)
    create.add_argument("--workspace", type=Path, default=Path("."))
    create.add_argument("--warmup-root", type=Path, default=Path("data/ohlcv"))
    create.add_argument("--freeze", type=Path, default=Path(FREEZE_NAME))
    create.add_argument("--snapshot", type=Path, default=Path(SNAPSHOT_NAME))
    verify = sub.add_parser("verify", help="Arşivi çıkarmadan kendi indeksi ve SHA dosyasıyla doğrula")
    verify.add_argument("--archive", type=Path, required=True)
    verify.add_argument("--expected-sha256", help="Haricen bilinen SHA-256; yoksa yerel .sha256 dosyası kullanılır")
    args = parser.parse_args()
    if args.command == "create":
        workspace = args.workspace.resolve()
        resolve = lambda path: path if path.is_absolute() else workspace / path
        result = create_archive(args.archive, workspace, resolve(args.warmup_root), resolve(args.freeze), resolve(args.snapshot))
    else:
        expected = args.expected_sha256
        if expected is None:
            sidecar = Path(str(args.archive) + ".sha256")
            parts = sidecar.read_text(encoding="utf-8").strip().split()
            if len(parts) != 2 or parts[1] != args.archive.name:
                raise ValueError("Arşiv SHA dosyası geçersiz")
            expected = parts[0]
        result = verify_archive(args.archive, expected_sha256=expected)
        result.update({"archive": str(args.archive), "sha256": expected})
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
