"""Ayar yükleme ve doğrulama."""
from __future__ import annotations

import json
from dataclasses import dataclass, fields, replace
from pathlib import Path
from typing import Any

PATH_FIELDS = {
    "cache_dir", "output_dir", "derived_dir", "report_dir",
    "state_path", "lock_path", "log_dir",
}


@dataclass(frozen=True)
class Settings:
    history_years: int = 1
    intervals: tuple[str, ...] = ("1h", "1d")
    hourly_chunk_days: int = 55
    daily_chunk_days: int = 366
    request_timeout_seconds: float = 25.0
    min_request_interval_seconds: float = 5.0
    jitter_seconds: float = 1.5
    max_requests_per_hour: int = 200
    max_requests_per_run: int = 1000
    max_attempts_per_task: int = 3
    retry_base_seconds: float = 30.0
    retry_max_seconds: float = 900.0
    max_sweeps: int = 4
    rate_limit_cooldown_seconds: float = 1800.0
    rate_limit_strike_limit: int = 2
    consecutive_error_limit: int = 6
    auto_adjust: bool = False
    back_adjust: bool = False
    repair: bool = False
    keepna: bool = True
    actions: bool = True
    prepost: bool = False
    derive_timeframes: bool = True
    cache_dir: Path = Path("data/cache")
    output_dir: Path = Path("data/prices")
    derived_dir: Path = Path("data/derived")
    report_dir: Path = Path("data/reports")
    state_path: Path = Path("data/state.sqlite3")
    lock_path: Path = Path("data/state.lock")
    log_dir: Path = Path("logs")

    @classmethod
    def load(cls, path: str | Path, base_dir: str | Path | None = None) -> "Settings":
        path = Path(path)
        base = Path(base_dir) if base_dir is not None else path.resolve().parent.parent
        raw: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        known = {f.name for f in fields(cls)}
        unknown = sorted(set(raw) - known)
        if unknown:
            raise ValueError(f"Bilinmeyen ayarlar: {', '.join(unknown)}")
        values: dict[str, Any] = {}
        for key, value in raw.items():
            if key == "intervals":
                value = tuple(value)
            elif key in PATH_FIELDS:
                value = Path(value)
                if not value.is_absolute():
                    value = base / value
            values[key] = value
        settings = cls(**values)
        settings.validate()
        return settings

    def validate(self) -> None:
        if not 1 <= self.history_years <= 2:
            raise ValueError("history_years 1 veya 2 olmalı (saatlik Yahoo sınırı için)")
        if not self.intervals or any(i not in {"1h", "1d"} for i in self.intervals):
            raise ValueError("intervals yalnızca 1h ve/veya 1d içerebilir")
        if len(set(self.intervals)) != len(self.intervals):
            raise ValueError("intervals tekrar eden değer içeriyor")
        if not 1 <= self.hourly_chunk_days <= 700:
            raise ValueError("hourly_chunk_days 1..700 olmalı")
        if not 1 <= self.daily_chunk_days <= 3660:
            raise ValueError("daily_chunk_days 1..3660 olmalı")
        positives = [
            self.request_timeout_seconds, self.max_requests_per_hour,
            self.max_requests_per_run, self.max_attempts_per_task,
            self.retry_base_seconds, self.retry_max_seconds, self.max_sweeps,
            self.rate_limit_cooldown_seconds, self.rate_limit_strike_limit,
            self.consecutive_error_limit,
        ]
        if any(v <= 0 for v in positives):
            raise ValueError("Sayaç/süre ayarları pozitif olmalı")
        if self.min_request_interval_seconds < 0 or self.jitter_seconds < 0:
            raise ValueError("Bekleme süreleri negatif olamaz")
        if self.retry_max_seconds < self.retry_base_seconds:
            raise ValueError("retry_max_seconds >= retry_base_seconds olmalı")
        if self.auto_adjust and self.back_adjust:
            raise ValueError("auto_adjust ve back_adjust aynı anda açık olamaz")

    def ensure_dirs(self) -> None:
        for name in PATH_FIELDS:
            path = getattr(self, name)
            if name.endswith("_dir"):
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)

    def with_overrides(self, **kwargs: Any) -> "Settings":
        out = replace(self, **kwargs)
        out.validate()
        return out
