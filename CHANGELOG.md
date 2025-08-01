Changelog
=========

3.1.0
-----

Work in progress.

Release highlights:

- A `UserWarning` will be raised whenever `max_calls_total` is lower than 2.
- Replace setup.py by pyproject.toml and add Python 3.13 + 3.14 support

3.0.0
-----

Released 2023-10-06.

**Breaking changes**:

- `DoCall`, `DoWait` and `RetryState` have been removed. They have been replaced by
  `BackoffCalculator`. This class exposes a method `get_backoff`. This method should return either
  a `float` representing the time to wait or `None` if there should be no more retries/waits.
- Python 3.8+ is now required to run `opnieuw`.

Release highlights:

- Remove `DoCall`, `DoWait` and `RetryState`.
- Use `BackoffCalculator` to keep track of the time to wait between retries and refactor
  retrying logic accordingly.
- Add chaining of previously retried exceptions. `opnieuw` will now correctly set the
  `__cause__` attribute of any exception leaving the decorator with a chain of all the
  previously retried exceptions.
- Python 3.8+ is now required to run `opnieuw`.


2.0.0
-----

Released 2022-05-18.

**Breaking changes**:

- `clock.TestClock` was renamed to `clock.DummyClock`.

Release highlights:

- Rename `clock.TestClock` to `clock.DummyClock`.
- Relint and upgrade the codebase.
- Fix a typing issues for `retry_async`.

1.2.1
-----

Released 2023-05-04.

Release highlights:

- Use more modern typing concepts such as `ParamSpec`.

1.2.0
-----

Released 2022-05-18.

**Breaking changes**:

- `RetryState` namespaces are now context-local instead of global. This ensures that modifying the
  retry behavior doesn't bleed unexpectedly when used in concurrent code.

Release highlights:

- Expose `replace_retry_state` context manager to customize the retry behavior for a specific namespace.
- Add `util.no_retries` context manager to disable retries for a specific namespace.

1.1.0
-----

Released 2020-05-08.

**Breaking changes**:

- None.

Release highlights:

- Prevent waiting while running tests via `test_util.retry_immediately`

1.0.0
-----

Released 2020-04-07.

**Breaking changes**:

- None.

Release highlights:

- Expose type information via [PEP-561](https://www.python.org/dev/peps/pep-0561/).
- Support running retry with `max_calls_total=1` - @ierror

0.0.3
-----

Initial (pre)release. See [the blogpost](https://tech.channable.com/posts/2020-02-05-opnieuw.html) to learn more.
