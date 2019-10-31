def calculate_exponential_multiplier(
    max_calls_total: int, retry_window_after_first_call_in_seconds: int
) -> float:
    r"""
    Solve the following equation for `m`:
        \sum_{k=0}^{n} m 2^k = <retry_window_after_first_call_in_seconds>

    where `n` is the number of attempts. Since we start at `k=0`, then `n = max_calls_total - 2`.

    An example:
        Let `max_calls_total = 4` and `retry_window_after_first_call_in_seconds = 120`, then we have
            \sum_{k=0}^{4 - 2} m 2^k = 120

        which expands into:
            m * 2^0 + m * 2^1 + m * 2^2 = 120
            m + 2m + 4m = 120
            7m = 120
            m = 120 / 7

    If we take a partial sum of this geometric sequence, we can simplify the equation:
        \sum_{k=0}^{n-1} 2^k ≈ 2^{max_calls_total - 1} - 1

    Using the example from above, we have:
        2^{4 - 1} -1 = 7

        ∴ 7m = 120 => m = 120 / 7
    """

    count = 2 ** (max_calls_total - 1) - 1
    multiplier = retry_window_after_first_call_in_seconds / count

    return multiplier
