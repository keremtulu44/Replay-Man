"""Sıralı, beklemeli, açık kapsamlı ve seri-sürümlü indirme kuyruğu."""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Callable, Mapping

import pandas as pd

from .catalog import Asset, load_catalog
from .config import Settings
from .errors import RETRYABLE_KINDS, RunLimitReached, classify_error
from .normalize import merge_save_prices, normalize_prices, read_prices
from .provider import YahooProvider
from .ratelimit import RequestGate
from .report import write_reports
from .resample import daily_comparison, derive_timeframes, save_derived
from .series import Series, build_series, derived_path, price_path, publish_manifest
from .state import State, TaskScope

logger = logging.getLogger(__name__)
EPOCH = pd.Timestamp("2000-01-01", tz="UTC")


def chunk_ranges(start: pd.Timestamp, end: pd.Timestamp, days: int) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    if start >= end:
        return []
    step = pd.Timedelta(days=days)
    boundary = EPOCH + ((start - EPOCH) // step) * step
    out = []
    while boundary < end:
        lo, hi = max(start, boundary), min(end, boundary + step)
        if lo < hi:
            out.append((lo, hi))
        boundary += step
    return out


def plan_task_list(
    assets: list[Asset], settings: Settings, now: pd.Timestamp | None = None,
    series_by_asset: Mapping[str, Series] | None = None,
) -> list[tuple[str, str, str, str, str]]:
    now = now or pd.Timestamp.now(tz="UTC")
    start = now.normalize() - pd.DateOffset(years=settings.history_years)
    series_by_asset = series_by_asset or {a.id: build_series(a, settings) for a in assets}
    tasks = []
    for asset in assets:
        for interval in settings.intervals:
            end = now.floor("h") if interval == "1h" else now.normalize()
            ranges = chunk_ranges(start, end, settings.hourly_chunk_days) if interval == "1h" else ([(start, end)] if start < end else [])
            for lo, hi in ranges:
                tasks.append((asset.id, series_by_asset[asset.id].id, interval, lo.isoformat(), hi.isoformat()))
    return tasks


def check_plan(
    settings: Settings, catalog_path: str | Path, symbols: list[str] | None = None,
    limit: int | None = None,
) -> dict:
    assets, digest = load_catalog(catalog_path, symbols=symbols, limit=limit)
    series = {a.id: build_series(a, settings) for a in assets}
    tasks = plan_task_list(assets, settings, series_by_asset=series)
    return {
        "status": "check", "assets": len(assets), "planned_tasks": len(tasks),
        "catalog_hash": digest, "intervals": list(settings.intervals),
        "series_ids": {asset_id: value.id for asset_id, value in series.items()},
        "network_requests": 0,
        "min_request_interval_seconds": settings.min_request_interval_seconds,
        "jitter_seconds": settings.jitter_seconds,
        "batch_request_count": settings.batch_request_count,
        "batch_pause_seconds": settings.batch_pause_seconds,
        "max_requests_per_hour": settings.max_requests_per_hour,
    }


class Downloader:
    def __init__(
        self, settings: Settings, catalog_path: str | Path, provider=None,
        sleep: Callable[[float], None] = time.sleep, clock: Callable[[], float] = time.time,
    ) -> None:
        self.settings = settings
        self.catalog_path = Path(catalog_path)
        self.provider = provider
        self.sleep = sleep
        self.clock = clock

    def run(
        self, symbols: list[str] | None = None, limit: int | None = None,
        intervals: tuple[str, ...] | None = None, retry_failed: bool = False,
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
        series_by_asset = {asset.id: build_series(asset, settings) for asset in assets}
        scope = TaskScope(tuple((a.id, series_by_asset[a.id].id) for a in assets), settings.intervals)
        for asset in assets:
            publish_manifest(settings, asset, series_by_asset[asset.id])
        state = State(settings.state_path, clock=self.clock)
        provider = self.provider or YahooProvider(settings)
        gate = RequestGate(settings, state, sleep=self.sleep, clock=self.clock)
        run_id = state.start_run()
        state.upsert_assets(assets, catalog_hash)
        state.set_meta("catalog_hash", catalog_hash)
        state.reset_running(scope=scope)
        planned = state.plan_tasks(plan_task_list(assets, settings, series_by_asset=series_by_asset))
        if retry_failed:
            logger.info("Seçili kapsamda yeniden denemeye alınan görev: %s", state.reset_failed(scope=scope))
        logger.info("Varlık: %s | yeni görev: %s | seçili görevler: %s", len(assets), planned, state.task_counts(scope=scope))
        if state.migrated_legacy_tasks:
            logger.warning("Seri kimliği olmayan eski görevler tasks_legacy_v1 tablosunda korundu; yeni seri kuyruğu oluşturuldu")

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
                cooldown_until = state.get_float("cooldown_until", 0.0)
                if self.clock() < cooldown_until:
                    status = "blocked"
                    stop_reason = f"Yahoo hız sınırı bekleme süresi devam ediyor: {cooldown_until - self.clock():.0f} sn"
                    break
                due = state.due_tasks(self.clock(), settings.max_attempts_per_task, scope=scope)
                if not due:
                    next_retry = state.next_retry_time(settings.max_attempts_per_task, scope=scope)
                    if next_retry is None:
                        break
                    if sweep == settings.max_sweeps - 1:
                        status = "incomplete"
                        stop_reason = "Seçili kapsamda yeniden deneme hakkı olan görevler kaldı; tekrar çalıştırın"
                        break
                    delay = max(0.0, next_retry - self.clock())
                    logger.info("Sonraki deneme turuna kadar bekleniyor: %.1f sn", delay)
                    self.sleep(delay)
                    continue
                logger.info("Deneme turu %s/%s | işlenecek görev: %s", sweep + 1, settings.max_sweeps, len(due))
                for task in due:
                    asset = by_id[task.asset_id]
                    series = series_by_asset[task.asset_id]
                    state.mark_running(task)
                    label = f"{asset.local_symbol} {task.interval} {task.start[:10]}->{task.end[:10]}"
                    try:
                        result = provider.fetch(asset, task.interval, pd.Timestamp(task.start), pd.Timestamp(task.end), before_request=before_request)
                        fetched_at = str(result.metadata.get("fetchedAt") or pd.Timestamp.now(tz="UTC").isoformat())
                        normalized, quality = normalize_prices(
                            result.frame, asset, task.interval, fetched_at,
                            settings=settings, series_id=series.id, metadata=result.metadata,
                        )
                        total_rows = merge_save_prices(price_path(settings, asset, series, task.interval), normalized)
                        state.mark_complete(task, len(normalized), result.from_cache)
                        cache_hits += int(result.from_cache)
                        saved_rows += len(normalized)
                        consecutive_errors = 0
                        logger.info("OK %s | %s satır | toplam %s | %s | kalite=%s", label, len(normalized), total_rows,
                                    "önbellek" if result.from_cache else "ağ", quality)
                    except RunLimitReached as exc:
                        state.mark_pending_no_attempt(task)
                        status, stop_reason, stop = "limited", str(exc), True
                        break
                    except KeyboardInterrupt:
                        state.mark_pending_no_attempt(task)
                        status, stop_reason, stop = "interrupted", "Kullanıcı durdurdu", True
                        break
                    except Exception as exc:
                        failure = classify_error(exc)
                        logger.warning("HATA %s | %s | %s", label, failure.kind, failure.message)
                        if failure.kind == "access_denied":
                            state.mark_failed(task, failure.kind, failure.message)
                            status, stop_reason, stop = "blocked", failure.message, True
                            break
                        if failure.kind == "rate_limit":
                            cooldown = max(failure.retry_after or 0.0, settings.rate_limit_cooldown_seconds)
                            state.set_float("cooldown_until", self.clock() + cooldown)
                            if task.attempts + 1 >= settings.max_attempts_per_task:
                                state.mark_failed(task, failure.kind, failure.message)
                            else:
                                state.mark_retry(task, failure.kind, failure.message, cooldown)
                            status, stop_reason, stop = "blocked", f"Yahoo hız sınırı; {cooldown:.0f} sn sonra tekrar deneyin", True
                            logger.warning("%s", stop_reason)
                            break
                        if failure.kind in RETRYABLE_KINDS:
                            consecutive_errors += 1
                            attempts = task.attempts + 1
                            if consecutive_errors >= settings.consecutive_error_limit:
                                state.mark_retry(task, failure.kind, failure.message, settings.retry_max_seconds)
                                status, stop_reason, stop = "circuit_open", "Art arda geçici hata sınırı aşıldı; istekler durduruldu", True
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
            counts = state.task_counts(scope=scope)
            if status == "completed" and (counts.get("pending", 0) or counts.get("failed", 0)):
                status = "incomplete" if counts.get("pending", 0) else "completed_with_errors"
        finally:
            state.reset_running(scope=scope)
            derived = self._derive_all(assets, settings, series_by_asset) if settings.derive_timeframes else {}
            summary = {
                "status": status, "stop_reason": stop_reason, "assets": len(assets),
                "network_requests": requests_this_run, "cache_hits": cache_hits,
                "normalized_rows": saved_rows, "task_counts": state.task_counts(scope=scope),
                "queue_task_counts": state.global_task_counts(),
                "scope": {"asset_ids": [a.id for a in assets], "intervals": list(settings.intervals),
                          "series_ids": {a.id: series_by_asset[a.id].id for a in assets}},
                "legacy_tasks_preserved": state.migrated_legacy_tasks,
                "derived": derived, "catalog_hash": catalog_hash,
                "finished_at": pd.Timestamp.now(tz="UTC").isoformat(),
            }
            try:
                write_reports(settings, state, summary, scope=scope)
                state.finish_run(run_id, status, summary)
            finally:
                if self.provider is None:
                    provider.close()
                state.close()
        logger.info("Bitti: %s | ağ isteği=%s | önbellek=%s", status, requests_this_run, cache_hits)
        return summary

    def _derive_all(self, assets: list[Asset], settings: Settings, series_by_asset: Mapping[str, Series]) -> dict:
        derived_assets = comparisons = mismatches = errors = 0
        for asset in assets:
            series = series_by_asset[asset.id]
            try:
                hourly = read_prices(price_path(settings, asset, series, "1h"))
                if hourly.empty:
                    continue
                frames = derive_timeframes(hourly, asset, series_id=series.id)
                if not frames:
                    continue
                directory = derived_path(settings, asset, series)
                for label, frame in frames.items():
                    save_derived(directory / f"{label}.csv", frame)
                derived_assets += 1
                native = read_prices(price_path(settings, asset, series, "1d"))
                if "1d_from_1h" in frames and not native.empty:
                    comparison = daily_comparison(native, frames["1d_from_1h"])
                    if not comparison.empty:
                        save_derived(directory / "daily_comparison.csv", comparison)
                        comparisons += int(len(comparison))
                        mismatches += int((~comparison["match"].astype(bool)).sum())
            except Exception as exc:
                errors += 1
                logger.warning("Türetim/okuma hatası %s: %s", asset.local_symbol, exc)
        return {"assets": derived_assets, "daily_comparisons": comparisons, "daily_mismatches": mismatches, "errors": errors}
