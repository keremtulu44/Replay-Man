#!/usr/bin/env python3
"""Replay-Man veri indirici. Kurulum: python run.py --install; çalıştırma: python run.py"""
from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def install_dependencies() -> int:
    requirements = ROOT / "requirements.txt"
    print("Bağımlılıklar kuruluyor...", flush=True)
    result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements)])
    if result.returncode != 0:
        print("Kurulum başarısız. Python 3.11+ ve pip kullandığınızdan emin olun.", file=sys.stderr)
        return result.returncode
    print("Kurulum tamam. Şimdi: python run.py")
    return 0


def acquire_lock(path: Path, force: bool = False):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if force:
            path.unlink()
        else:
            raise FileExistsError(
                f"Kilit dosyası var: {path}. Başka indirici çalışıyor olabilir. "
                "Eminseniz --force-unlock kullanın."
            )
    path.write_text(str(os.getpid()), encoding="utf-8")
    return path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Yahoo tabanlı, beklemeli ve kaldığı yerden devam eden BIST veri indirici")
    parser.add_argument("--install", action="store_true", help="requirements.txt bağımlılıklarını kur ve çık")
    parser.add_argument("--config", default=str(ROOT / "config/settings.json"), help="Ayar JSON dosyası")
    parser.add_argument("--catalog", default=str(ROOT / "data/universe.csv"), help="Sembol kataloğu CSV")
    parser.add_argument("--check", action="store_true", help="Ağa çıkmadan katalog/ayar/görev planını doğrula")
    parser.add_argument("--status", action="store_true", help="Son rapor özetini göster")
    parser.add_argument("--symbols", help="Virgülle ayrılmış yerel/Yahoo sembolleri: ASELS,THYAO,GC=F")
    parser.add_argument("--limit", type=int, help="Katalogdaki ilk N etkin varlık")
    parser.add_argument("--interval", choices=["1h", "1d", "both"], default="both", help="İndirilecek periyot")
    parser.add_argument("--retry-failed", action="store_true", help="Geçici hatalarla başarısız görevleri yeniden kuyruğa al")
    parser.add_argument("--max-requests", type=int, help="Bu çalıştırmadaki ağ isteği üst sınırı")
    parser.add_argument("--force-unlock", action="store_true", help="Eski kilit dosyasını kaldır")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.install:
        return install_dependencies()
    try:
        from replayman.config import Settings
        from replayman.runner import Downloader, check_plan
    except ImportError as exc:
        print(f"Eksik bağımlılık: {exc}\nÖnce: python run.py --install", file=sys.stderr)
        return 2

    try:
        settings = Settings.load(args.config, base_dir=ROOT)
    except Exception as exc:
        print(f"Ayar hatası: {exc}", file=sys.stderr)
        return 2

    if args.status:
        summary_path = settings.report_dir / "summary.json"
        if not summary_path.exists():
            print("Henüz rapor yok. Önce python run.py çalıştırın.")
            return 0
        print(summary_path.read_text(encoding="utf-8"))
        return 0

    settings.log_dir.mkdir(parents=True, exist_ok=True)
    log_file = settings.log_dir / "replayman.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(log_file, encoding="utf-8")],
        force=True,
    )
    logging.getLogger("yfinance").setLevel(logging.ERROR)
    logging.getLogger("peewee").setLevel(logging.WARNING)

    if args.check:
        try:
            print(json.dumps(check_plan(settings, args.catalog), ensure_ascii=False, indent=2))
            return 0
        except Exception as exc:
            print(f"Kontrol hatası: {exc}", file=sys.stderr)
            return 2

    lock = None
    try:
        lock = acquire_lock(settings.lock_path, force=args.force_unlock)
        symbols = [s.strip() for s in args.symbols.split(",")] if args.symbols else None
        intervals = ("1h", "1d") if args.interval == "both" else (args.interval,)
        downloader = Downloader(settings, args.catalog)
        summary = downloader.run(
            symbols=symbols,
            limit=args.limit,
            intervals=intervals,
            retry_failed=args.retry_failed,
            max_requests=args.max_requests,
        )
        print("\nÖzet:")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        print(f"Rapor: {settings.report_dir / 'latest.md'}")
        status = summary["status"]
        if status in {"completed", "completed_with_errors"}:
            return 0 if status == "completed" else 1
        if status == "limited":
            return 3
        if status in {"blocked", "circuit_open"}:
            return 2
        if status == "interrupted":
            return 130
        return 1
    except FileExistsError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nDurduruldu. İlerleme kaydedildi; aynı komutla devam edebilirsiniz.", file=sys.stderr)
        return 130
    except Exception as exc:
        logging.exception("Çalıştırma hatası")
        print(f"Hata: {exc}", file=sys.stderr)
        return 2
    finally:
        if lock is not None:
            lock.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
