from types import SimpleNamespace

import pandas as pd

from replayman.errors import AccessDenied, RateLimited, TransientHTTP
from replayman.runner import Downloader, chunk_ranges


def frame_for(start, interval):
    ts = pd.Timestamp(start) + pd.Timedelta(hours=1)
    return pd.DataFrame(
        {"Open": [10], "High": [11], "Low": [9], "Close": [10.5], "Volume": [100]},
        index=pd.DatetimeIndex([ts], tz="UTC"),
    )


class FakeProvider:
    def __init__(self, fail_first=False):
        self.calls = []
        self.failed_once = set()
        self.fail_first = fail_first

    def fetch(self, asset, interval, start, end, before_request=None):
        key = (asset.id, interval, start.isoformat(), end.isoformat())
        self.calls.append(key)
        if before_request:
            before_request()
        if self.fail_first and key not in self.failed_once:
            self.failed_once.add(key)
            raise TransientHTTP(503)
        return SimpleNamespace(frame=frame_for(start, interval), from_cache=False, metadata={"fetchedAt": "2026-01-01T00:00:00Z"})


class BlockingProvider:
    def __init__(self, exc):
        self.exc = exc
        self.calls = 0

    def fetch(self, *args, **kwargs):
        self.calls += 1
        if kwargs.get("before_request"):
            kwargs["before_request"]()
        raise self.exc


def make_clock():
    now = [1_000_000.0]

    def clock():
        return now[0]

    def sleep(seconds):
        now[0] += seconds

    return clock, sleep


def test_chunk_ranges_cover_without_gap():
    start = pd.Timestamp("2025-11-14", tz="UTC")
    end = pd.Timestamp("2026-11-14", tz="UTC")
    chunks = chunk_ranges(start, end, 55)
    assert chunks[0][0] == start
    assert chunks[-1][1] == end
    assert all(a[1] == b[0] for a, b in zip(chunks, chunks[1:]))


def test_runner_success_and_resume(settings, catalog_path):
    clock, sleep = make_clock()
    provider = FakeProvider()
    summary = Downloader(settings, catalog_path, provider=provider, sleep=sleep, clock=clock).run(limit=1, intervals=("1d",))
    assert summary["status"] == "completed"
    assert summary["network_requests"] == 1
    assert len(list((settings.output_dir / "BIST_ASELS").glob("*/1d.csv"))) == 1
    assert (settings.report_dir / "summary.json").exists()
    calls = len(provider.calls)
    summary2 = Downloader(settings, catalog_path, provider=provider, sleep=sleep, clock=clock).run(limit=1, intervals=("1d",))
    assert summary2["network_requests"] == 0
    assert len(provider.calls) == calls


def test_runner_retries_transient_then_succeeds(settings, catalog_path):
    clock, sleep = make_clock()
    provider = FakeProvider(fail_first=True)
    summary = Downloader(settings, catalog_path, provider=provider, sleep=sleep, clock=clock).run(limit=1, intervals=("1d",))
    assert summary["status"] == "completed"
    assert summary["network_requests"] == 2
    assert summary["task_counts"]["complete"] == 1


def test_runner_access_denied_stops(settings, catalog_path):
    clock, sleep = make_clock()
    provider = BlockingProvider(AccessDenied(403))
    summary = Downloader(settings, catalog_path, provider=provider, sleep=sleep, clock=clock).run(limit=2, intervals=("1d",))
    assert summary["status"] == "blocked"
    assert provider.calls == 1


def test_runner_stops_on_rate_limit_without_sleep_and_respects_cooldown(settings, catalog_path):
    now = [1_000_000.0]
    sleeps = []

    def sleep(seconds):
        sleeps.append(seconds)
        now[0] += seconds

    provider = BlockingProvider(RateLimited(retry_after=20))
    downloader = Downloader(settings, catalog_path, provider=provider, sleep=sleep, clock=lambda: now[0])
    summary = downloader.run(limit=2, intervals=("1d",))
    assert summary["status"] == "blocked"
    assert provider.calls == 1
    assert not sleeps
    summary = downloader.run(limit=2, intervals=("1d",))
    assert summary["status"] == "blocked"
    assert provider.calls == 1
    assert not sleeps
    now[0] += 21
    downloader.run(limit=2, intervals=("1d",))
    assert provider.calls == 2


def test_runner_request_budget_leaves_pending(settings, catalog_path):
    clock, sleep = make_clock()
    provider = FakeProvider()
    summary = Downloader(settings, catalog_path, provider=provider, sleep=sleep, clock=clock).run(
        limit=2, intervals=("1d",), max_requests=1
    )
    assert summary["status"] == "limited"
    assert summary["network_requests"] == 1
    assert summary["task_counts"]["pending"] == 1
