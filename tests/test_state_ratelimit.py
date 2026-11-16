import random

from replayman.ratelimit import RequestGate
from replayman.state import State, TaskScope


def test_state_retry_and_resume(settings):
    now = [100.0]
    scope = TaskScope((("A", "series-a"),), ("1h",))
    with State(settings.state_path, clock=lambda: now[0]) as state:
        state.plan_tasks([("A", "series-a", "1h", "s", "e")])
        task = state.due_tasks(now[0], 3, scope=scope)[0]
        state.mark_running(task)
        state.reset_running(scope=scope)
        task = state.due_tasks(now[0], 3, scope=scope)[0]
        state.mark_retry(task, "transient", "boom", 10)
        now[0] = 105.0
        assert state.due_tasks(now[0], 3, scope=scope) == []
        now[0] = 111.0
        due = state.due_tasks(now[0], 3, scope=scope)
        assert len(due) == 1
        assert due[0].attempts == 1
        state.mark_complete(due[0], 5, False)
        assert state.task_counts(scope=scope) == {"complete": 1}


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


def test_tenth_request_triggers_15_second_break_even_after_restart(settings):
    now = [1000.0]
    slept = []

    def sleep(seconds):
        slept.append(seconds)
        now[0] += seconds

    settings = settings.with_overrides(min_request_interval_seconds=1, jitter_seconds=0,
                                       batch_request_count=10, batch_pause_seconds=15)
    with State(settings.state_path) as state:
        gate = RequestGate(settings, state, sleep=sleep, clock=lambda: now[0])
        for _ in range(10):
            gate.before_request()
        assert slept == [1] * 9
        last = now[0]
    # Yeni bir çalıştırma grup sayacını sıfırlamaz.
    with State(settings.state_path) as state:
        gate = RequestGate(settings, state, sleep=sleep, clock=lambda: now[0])
        gate.before_request()
        assert now[0] - last == 15
        assert slept[-1] == 15
        gate.before_request()
        assert slept[-1] == 1
        for _ in range(8):
            gate.before_request()
        last = now[0]
        gate.before_request()
        assert now[0] - last == 15


def test_no_extra_batch_delay_if_already_waited(settings):
    now = [1000.0]
    slept = []
    settings = settings.with_overrides(min_request_interval_seconds=0, jitter_seconds=0)
    with State(settings.state_path) as state:
        gate = RequestGate(settings, state, sleep=slept.append, clock=lambda: now[0])
        for _ in range(10):
            gate.before_request()
        now[0] += 20
        gate.before_request()
        assert not slept
