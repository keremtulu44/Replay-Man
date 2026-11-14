import random

from replayman.ratelimit import RequestGate
from replayman.state import State


def test_state_retry_and_resume(settings):
    now = [100.0]
    with State(settings.state_path, clock=lambda: now[0]) as state:
        state.plan_tasks([("A", "1h", "s", "e")])
        task = state.due_tasks(now[0], 3)[0]
        state.mark_running(task)
        state.reset_running()
        task = state.due_tasks(now[0], 3)[0]
        state.mark_retry(task, "transient", "boom", 10)
        now[0] = 105.0
        assert state.due_tasks(now[0], 3) == []
        now[0] = 111.0
        due = state.due_tasks(now[0], 3)
        assert len(due) == 1
        assert due[0].attempts == 1
        state.mark_complete(due[0], 5, False)
        assert state.task_counts() == {"complete": 1}


def test_gate_min_interval_and_hourly_budget(settings):
    now = [1000.0]
    slept = []

    def clock():
        return now[0]

    def sleep(seconds):
        slept.append(seconds)
        now[0] += seconds

    settings = settings.with_overrides(min_request_interval_seconds=5, max_requests_per_hour=2)
    with State(settings.state_path) as state:
        gate = RequestGate(settings, state, sleep=sleep, clock=clock, rng=random.Random(0))
        gate.before_request()
        gate.before_request()
        assert slept[-1] >= 5
        gate.before_request()
        assert now[0] >= 4600.0
        assert state.request_count_since(now[0] - 3600) <= 2


def test_gate_respects_persistent_cooldown(settings):
    now = [100.0]
    slept = []

    def sleep(seconds):
        slept.append(seconds)
        now[0] += seconds

    with State(settings.state_path) as state:
        state.set_float("cooldown_until", 150.0)
        gate = RequestGate(settings, state, sleep=sleep, clock=lambda: now[0])
        gate.before_request()
        assert now[0] >= 150.0
