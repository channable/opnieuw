# Opnieuw: Retries for humans
# Copyright 2019 Channable
#
# Licensed under the 3-clause BSD license, see the LICENSE file in the repository root.

from typing import Union


class RetryException(Exception):
    """
    Defines a custom RetryException that can be raised for specific errors we
    want to retry on.
    """


class BackoffAndRetryException(Exception):
    """
    A custom exception that can be raised for specific errors when a fixed
    wait time before retrying is in order. This can be particularly useful
    when requests are throttled and the response includes a Retry-After header.

    This will reset the counters for `max_calls_total`
    and `retry_window_after_first_call_in_seconds`
    """

    def __init__(self, seconds: Union[int, float]):
        self.seconds = seconds
