Opnieuw
=======

Opnieuw is a general-purpose retrying library, written in Python, in
order to simplify the task of adding retry behavior to both synchronous as well
as asynchronous tasks. Opnieuw is easy and straightforward to use.

Opnieuw makes it easy to add robust retries:

 * There is a single retry strategy, exponential backoff with jitter, which
   makes it impossible to forget to add jitter.
 * It has just two parameters, to eliminate the possibility of invalid and
   nonsensical combinations.
 * Parameters are named clearly, to avoid confusing e.g. number of calls
   (including the initial one) with number of retries (excluding the initial
   call).
 * The parameters are intuitive: instead of configuring the base delay for
   exponential backoff, Opnieuw accepts a maximum number of calls to make, and
   maximum time after the first call to still retry.
 * Time units are clear from parameter names to make the decorated code obvious,
   and readable without needing to refer to documentation.

See our [announcement post][post] for a bit more background on why we wrote
Opnieuw.

Example
-------

Suppose we want to parse `https://tech.channable.com/atom.xml` and we want to
add a retry to handle a specific network Exception. We can add Opnieuw to our
network handler as follows:

```python
import requests
from requests.exceptions import ConnectionError, HTTPError

from opnieuw import retry

@retry(
    retry_on_exceptions=(ConnectionError, HTTPError),
    max_calls_total=4,
    retry_window_after_first_call_in_seconds=60,
)
def get_page() -> str:
    response = requests.get('https://tech.channable.com/atom.xml')
    return response.text
```

 * `retry_on_exceptions` specifies which exceptions we want to retry on.

 * `max_calls_total` is the maximum number of times that the decorated function
   gets called, including the initial call.

 * `retry_window_after_first_call_in_seconds` is the maximum number of seconds
   after the first call was initiated, where we would still do a new attempt.

Features
--------

 * Generic decorator API
 * Specify retry exception (i.e. type of exception that we want retry)
 * [Exponential backoff with jitter][exponential-backoff]
 * Pre-shipped list of popular exceptions, which can easily be expanded

Installation
------------

To install Opnieuw, simply:

    $ pip install opnieuw

More examples
--------

The short example above provides a concise demonstration of how Opnieuw could
be used. Let's dig deeper into Opnieuw and add another exception to
`retry_on_exceptions` to do a retry on:

```python
from urllib.error import URLError
import requests
from opnieuw import RetryException, retry

@retry(
    retry_on_exceptions=(ConnectionError, RetryException, URLError),
    max_calls_total=4,
    retry_window_after_first_call_in_seconds=60,
)
def get_page() -> str:
    response = requests.get('https://tech.channable.com/atom.xml')

    if response.status_code != 200:
        raise RetryException

    return response.text
```

We can pass the name of exception we want do retry for or a tuple of exceptions
to the `retry_on_exceptions`. As mentioned earlier Opnieuw was developed to
make it more convenient to add retry behavior to any task.

Let's make it a little bit more generic and define a list of retry exceptions
that should trigger a retry of the function:

```python
STANDARD_HTTP_EXCEPTIONS = (
    ConnectionError,
    ProtocolError,
    RetryException,
    ...
)

@retry(
    retry_on_exceptions=STANDARD_HTTP_EXCEPTIONS,
    max_calls_total=4,
    retry_window_after_first_call_in_seconds=60,
)
def get_page() -> str:
    response = requests.post('https://tech.channable.com/atom.xml')
    return response.text
```

Now our retry is more generic, as exceptions raised which are in
`STANDARD_HTTP_EXCEPTIONS` will be retried.

If you want retry behavior for async tasks, then there is also an async retry
which basically work the same way, but for async tasks.

Here is the example above but in async mode:

```python
from opnieuw import retry_async

STANDARD_HTTP_EXCEPTIONS = (
    ConnectionError,
    EOFError,
    RetryException,
    ...
)

@retry_async(
    retry_on_exceptions=STANDARD_HTTP_EXCEPTIONS,
    max_calls_total=4,
    retry_window_after_first_call_in_seconds=60,
)
async def get_page() -> str:
    response = requests.get('https://tech.channable.com/atom.xml')
    return response.text
```

[post]: https://tech.channable.com/posts/2020-02-05-opnieuw.html
[exponential-backoff]: https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
