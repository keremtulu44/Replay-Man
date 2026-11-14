"""İndirme kuyruğu: sıralı, beklemeli, yeniden denemeli, kaldığı yerden devam."""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Callable

import pandas as pd

from .catalog import Asset, load_catalog
from .config import Settings
from .errors import RETRYABLE_KINDS, RunLimitReached, classify_error
from .normalize import merge_save_prices, normalize_prices, read_prices
from .provider import YahooProvider
from .ratelimit import RequestGate
from .report import write_reports
from .resample import daily_comparison, derive_timeframes, save_derived
from .state import State, Task

logger = logging.getLogger(__name__)
EPOCH = pd.Timestamp("2000-01-01", tz="UTC")


def chunk_ranges(start: pd.Timestamp, end: pd.Timestamp, days: int) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    if start >= end:
        return []
    step = pd.Timedelta(days=days)
    boundary = EPOCH + ((start - EPOCH) // step) * step
    out = []
    while boundary < end:
        lo = max(start, boundary)
        hi = min(end, boundary + step)
        if lo < hi:
            out.append((lo, hi))
        boundary += step
    return out


def plan_task_list(assets: list[Asset], settings: Settings, now: pd.Timestamp | None = None) -> list[tuple[str, str, str, str]]:
    now = now or pd.Timestamp.now(tz="UTC")
    start = now.normalize() - pd.DateOffset(years=settings.history_years)
    tasks = []
    for asset in assets:
        for interval in settings.intervals:
            end = now.floor("h") if interval == "1h" else now.normalize()
            if interval == "1h":
                ranges = chunk_ranges(start, end, settings.hourly_chunk_days)
            else:
                ranges = [(start, end)] if start < end else []
            for lo, hi in ranges:
                tasks.append((asset.id, interval, lo.isoformat(), hi.isoformat()))
    return tasks


def check_plan(settings: Settings, catalog_path: str | Path) -> dict:
    assets, digest = load_catalog(catalog_path)
    tasks = plan_task_list(assets, settings)
    return {
        "status": "check",
        "assets": len(assets),
        "planned_tasks": len(tasks),
        "catalog_hash": digest,
        "intervals": list(settings.intervals),
        "network_requests": 0,
        "min_request_interval_seconds": settings.min_request_interval_seconds,
        "max_requests_per_hour": settings.max_requests_per_hour,
    }


class Downloader:
    def __init__(
        self,
        settings: Settings,
        catalog_path: str | Path,
        provider=None,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self.settings = settings
        self.catalog_path = Path(catalog_path)
        self.provider = provider
        self.sleep = sleep
        self.clock = clock

    def run(
        self,
        symbols: list[str] | None = None,
        limit: int | None = None,
        intervals: tuple[str, ...] | None = None,
        retry_failed: bool = False,
        max_requests: int | None = None,
    ) -> dict:
        overrides = {}
        if intervals is not None:
            overrides["intervals"] = intervals
        if max_requests is not None:
            overrides["max_requests_per_run"] = max_requests
        settings = self.settings.with_overrides(**overrides) if overrides else self.settings
        settings.ensure_dirs()
        assets, catalog_hash = load_catalog(self.catalog_path, symbols=symbols, limit=limit)
        by_id = {asset.id: asset for asset in assets}
        state = State(settings.state_path, clock=self.clock)
        provider = self.provider or YahooProvider(settings)
        gate = RequestGate(settings, state, sleep=self.sleep, clock=self.clock)
        run_id = state.start_run()
        state.upsert_assets(assets, catalog_hash)
        state.set_meta("catalog_hash", catalog_hash)
        state.reset_running()
        planned = state.plan_tasks(plan_task_list(assets, settings))
        if retry_failed:
            reset = state.reset_failed()
            logger.info("Yeniden denemeye alınan başarısız görev: %s", reset)
        logger.info("Varlık: %s | yeni görev: %s | mevcut görevler: %s", len(assets), planned, state.task_counts())

        requests_this_run = 0
        cache_hits = 0
        saved_rows = 0
        consecutive_errors = 0
        stop = False
        status = "completed"
        stop_reason = None

        def before_request() -> None:
            nonlocal requests_this_run
            if requests_this_run >= settings.max_requests_per_run:
                raise RunLimitReached("Bu çalıştırmanın istek bütçesi doldu")
            gate.before_request()
            requests_this_run += 1

        try:
            for sweep in range(settings.max_sweeps):
                now = self.clock()
                due = state.due_tasks(now, settings.max_attempts_per_task)
                if not due:
                    next_retry = state.next_retry_time(settings.max_attempts_per_task)
                    if next_retry is None:
                        break
                    if sweep == settings.max_sweeps - 1:
                        status = "incomplete"
                        stop_reason = "Yeniden deneme hakkı olan görevler kaldı; tekrar çalıştırın"
                        break
                    delay = max(0.0, next_retry - self.clock())
                    logger.info("Sonraki deneme turuna kadar bekleniyor: %.1f sn", delay)
                    self.sleep(delay)
                    continue
                logger.info("Deneme turu %s/%s | işlenecek görev: %s", sweep + 1, settings.max_sweeps, len(due))
                for task in due:
                    asset = by_id.get(task.asset_id)
                    if asset is None:
                        state.mark_failed(task, "permanent", "Varlık artık katalogda yok")
                        continue
                    state.mark_running(task)
                    label = f"{asset.local_symbol} {task.interval} {task.start[:10]}->{task.end[:10]}"
                    try:
                        result = provider.fetch(
                            asset,
                            task.interval,
                            pd.Timestamp(task.start),
                            pd.Timestamp(task.end),
                            before_request=before_request,
                        )
                        fetched_at = str(result.metadata.get("fetchedAt") or pd.Timestamp.now(tz='UTC').isoformat())
                        normalized, quality = normalize_prices(result.frame, asset, task.interval, fetched_at)
                        path = settings.output_dir / asset.id / f"{task.interval}.csv"
                        total_rows = merge_save_prices(path, normalized)
                        state.mark_complete(task, len(normalized), result.from_cache)
                        cache_hits += int(result.from_cache)
                        saved_rows += len(normalized)
                        consecutive_errors = 0
                        if not result.from_cache:
                            state.set_float("rate_limit_strikes", 0.0)
                        logger.info(
                            "OK %s | %s satır | toplam %s | %s | kalite=%s",
                            label, len(normalized), total_rows,
                            "önbellek" if result.from_cache else "ağ", quality,
                        )
                    except RunLimitReached as exc:
                        state.mark_pending_no_attempt(task)
                        status = "limited"
                        stop_reason = str(exc)
                        stop = True
                        break
                    except KeyboardInterrupt:
                        state.mark_pending_no_attempt(task)
                        status = "interrupted"
                        stop_reason = "Kullanıcı durdurdu"
                        stop = True
                        break
                    except Exception as exc:
                        failure = classify_error(exc)
                        logger.warning("HATA %s | %s | %s", label, failure.kind, failure.message)
                        if failure.kind == "access_denied":
                            state.mark_failed(task, failure.kind, failure.message)
                            status = "blocked"
                            stop_reason = failure.message
                            stop = True
                            break
                        if failure.kind == "rate_limit":
                            strikes = state.get_float("rate_limit_strikes", 0.0) + 1
                            state.set_float("rate_limit_strikes", strikes)
                            cooldown = max(failure.retry_after or 0.0, settings.rate_limit_cooldown_seconds)
                            state.set_float("cooldown_until", self.clock() + cooldown)
                            if strikes >= settings.rate_limit_strike_limit:
                                state.mark_failed(task, failure.kind, failure.message)
                                status = "blocked"
                                stop_reason = f"Yahoo hız sınırı tekrarlandı; {cooldown:.0f} sn cooldown kaydedildi"
                                stop = True
                                break
                            state.mark_retry(task, failure.kind, failure.message, cooldown)
                            logger.warning("Hız sınırı: %.0f sn beklenip tekrar denenecek", cooldown)
                            continue
                        if failure.kind in RETRYABLE_KINDS:
                            consecutive_errors += 1
                            attempts = task.attempts + 1
                            if consecutive_errors >= settings.consecutive_error_limit:
                                state.mark_retry(task, failure.kind, failure.message, settings.retry_max_seconds)
                                status = "circuit_open"
                                stop_reason = "Art arda geçici hata sınırı aşıldı; istekler durduruldu"
                                stop = True
                                break
                            if attempts >= settings.max_attempts_per_task:
                                state.mark_failed(task, failure.kind, failure.message)
                            else:
                                delay = min(settings.retry_base_seconds * (2 ** (attempts - 1)), settings.retry_max_seconds)
                                state.mark_retry(task, failure.kind, failure.message, delay)
                            continue
                        state.mark_failed(task, failure.kind, failure.message)
                if stop:
                    break
            counts = state.task_counts()
            if status == "completed" and (counts.get("pending", 0) or counts.get("failed", 0)):
                status = "incomplete" if counts.get("pending", 0) else "completed_with_errors"
        finally:
            state.reset_running()
            derived = self._derive_all(assets, settings) if settings.derive_timeframes else {}
            summary = {
                "status": status,
                "stop_reason": stop_reason,
                "assets": len(assets),
                "network_requests": requests_this_run,
                "cache_hits": cache_hits,
                "normalized_rows": saved_rows,
                "task_counts": state.task_counts(),
                "derived": derived,
                "catalog_hash": catalog_hash,
                "finished_at": pd.Timestamp.now(tz='UTC').isoformat(),
            }
            write_reports(settings, state, summary)
            state.finish_run(run_id, status, summary)
            if self.provider is None:
                provider.close()
            state.close()
        logger.info("Bitti: %s | ağ isteği=%s | önbellek=%s", status, requests_this_run, cache_hits)
        return summary

    def _derive_all(self, assets: list[Asset], settings: Settings) -> dict:
        derived_assets = 0
        comparisons = 0
        mismatches = 0
        for asset in assets:
            hourly_path = settings.output_dir / asset.id / "1h.csv"
            hourly = read_prices(hourly_path)
            if hourly.empty:
                continue
            try:
                frames = derive_timeframes(hourly, asset)
            except Exception as exc:
                logger.warning("Türetim hatası %s: %s", asset.local_symbol, exc)
                continue
            if not frames:
                continue
            derived_assets += 1
            for label, frame in frames.items():
                save_derived(settings.derived_dir / asset.id / f"{label}.csv", frame)
            native = read_prices(settings.output_dir / asset.id / "1d.csv")
            if "1d_from_1h" in frames and not native.empty:
                comparison = daily_comparison(native, frames["1d_from_1h"])
                if not comparison.empty:
                    save_derived(settings.derived_dir / asset.id / "daily_comparison.csv", comparison)
                    comparisons += int(len(comparison))
                    mismatches += int((~comparison["match"].astype(bool)).sum())
        return {"assets": derived_assets, "daily_comparisons": comparisons, "daily_mismatches": mismatches}
