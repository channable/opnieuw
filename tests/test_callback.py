# Opnieuw: Retries for humans
# Copyright 2019 Channable
#
# Licensed under the 3-clause BSD license, see the LICENSE file in the repository root.

import pytest
from opnieuw import retry
from opnieuw.retries import _validate_retry_parameters


class TestParameterValidation:
    def test_invalid_max_calls_total(self) -> None:
        with pytest.raises(ValueError, match="`max_calls_total` must be at least 1"):
            _validate_retry_parameters(max_calls_total=0, retry_window_after_first_call_in_seconds=60)

    def test_negative_retry_window(self) -> None:
        with pytest.raises(ValueError, match="`retry_window_after_first_call_in_seconds` must be non-negative"):
            _validate_retry_parameters(max_calls_total=3, retry_window_after_first_call_in_seconds=-1)


class TestOnRetryCallback:
    def test_sync_callback(self) -> None:
        retries = []

        @retry(
            retry_on_exceptions=(ValueError,),
            max_calls_total=3,
            retry_window_after_first_call_in_seconds=1,
            on_retry=lambda attempt, exc, backoff: retries.append(attempt)
        )
        def fail_twice() -> str:
            if len(retries) < 2:
                raise ValueError("Failed")
            return "Success"

        assert fail_twice() == "Success"
        assert retries == [1, 2]

    @pytest.mark.asyncio
    async def test_async_callback(self) -> None:
        retries = []

        @retry(
            retry_on_exceptions=(ValueError,),
            max_calls_total=3,
            retry_window_after_first_call_in_seconds=1,
            on_retry=lambda attempt, exc, backoff: retries.append(attempt)
        )
        async def fail_twice() -> str:
            if len(retries) < 2:
                raise ValueError("Failed")
            return "Success"

        assert await fail_twice() == "Success"
        assert retries == [1, 2]

    def test_callback_exception_does_not_break_retry(self, caplog) -> None:
        attempts = 0

        @retry(
            retry_on_exceptions=(ValueError,),
            max_calls_total=2,
            retry_window_after_first_call_in_seconds=10,
            on_retry=lambda *_: (_ for _ in ()).throw(RuntimeError("Callback failed"))
        )
        def fail_once() -> str:
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise ValueError("Failed")
            return "Success"

        with caplog.at_level("ERROR"):
            result = fail_once()

        assert result == "Success"
        assert attempts == 2
        assert "on_retry callback failed" in caplog.text
