"""İstek aralığı, saatlik bütçe ve kalıcı cooldown."""
from __future__ import annotations

import logging
import random
import time
from typing import Callable

from .config import Settings
from .state import State

logger = logging.getLogger(__name__)


class RequestGate:
    def __init__(
        self,
        settings: Settings,
        state: State,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.time,
        rng: random.Random | None = None,
    ) -> None:
        self.settings = settings
        self.state = state
        self.sleep = sleep
        self.clock = clock
        self.rng = rng or random.Random()

    def _sleep_until(self, target: float) -> None:
        delay = target - self.clock()
        if delay > 0:
            self.sleep(delay)

    def before_request(self) -> None:
        now = self.clock()
        cooldown = self.state.get_float("cooldown_until", 0.0)
        if now < cooldown:
            self._sleep_until(cooldown)
            now = self.clock()

        last = self.state.last_request()
        interval = self.settings.min_request_interval_seconds
        if self.settings.jitter_seconds > 0:
            interval += self.rng.uniform(0, self.settings.jitter_seconds)
        if last is not None:
            request_id, last_time = last
            deadline = last_time + interval
            if request_id % self.settings.batch_request_count == 0:
                deadline = max(deadline, last_time + self.settings.batch_pause_seconds)
                if deadline > now:
                    logger.info("%s istek tamamlandı; %.1f sn grup arası", self.settings.batch_request_count, deadline - now)
            self._sleep_until(deadline)
            now = self.clock()

        window_start = now - 3600.0
        count = self.state.request_count_since(window_start)
        if count >= self.settings.max_requests_per_hour:
            oldest = self.state.oldest_request_since(window_start)
            if oldest is not None:
                self._sleep_until(oldest + 3600.0 + 0.01)
                now = self.clock()
        self.state.record_request(now)
