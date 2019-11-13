# Opnieuw: Retries for humans
# Copyright 2019 Channable
#
# Licensed under the 3-clause BSD license, see the LICENSE file in the repository root.

import time
from abc import ABC, abstractmethod


class Clock(ABC):
    @abstractmethod
    def seconds_since_epoch(self) -> float:
        """Returns seconds since epoch."""


class MonotonicClock(Clock):
    """Effectual clock for use in production."""

    def seconds_since_epoch(self) -> float:
        return time.monotonic()


class TestClock(Clock):
    """Fake clock for use in tests."""

    def __init__(self) -> None:
        self.time = 0.0

    def advance_to(self, t: float) -> None:
        assert t >= self.time, "Clock should not go backwards"
        self.time = t

    def seconds_since_epoch(self) -> float:
        return self.time
