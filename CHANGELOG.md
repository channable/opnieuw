Changelog
=========

3.0.0
-----

Work in progress.

**Breaking changes**:

- `DoCall` has been removed. `retry` and `retry_async` will now execute the decorated
  function immediately and wait as defined by `DoWait`. If you need an immediate retry,
  you can `yield DoWait(0, 0, 0, 0)`.`
- `Action` has been removed as there is now only a `DoWait` class.

Release highlights:

- Remove `DoCall` and only have a `DoWait` to simplify the retyring logic.
- Remove `Action` as it is no longer required.


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
