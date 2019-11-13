Opnieuw
=========================
Opnieuw is a general-purpose retrying library, written in Python, in
order to simplify the task of adding retry behavior to both synchronous as well
as asynchronous tasks. Opnieuw is easy and straightforward to use.

Why Opnieuw? Most retry packages lack either adequate documentation on how to
properly use the package and or are difficult to customize. Valuable time is
lost in trying to figure out how to properly utilize a retry package. Opnieuw
makes it incredibly easy to add retry functionality to any task that requires
retry.

Suppose we want to parse `https://tech.channable.com/atom.xml` and we want to
add a retry to handle a specific network Exception. We can add Opnieuw to our
network handler as follows:

```python
import requests
from requests.exceptions import ConnectionError

from opnieuw import retry

@retry(
    retry_on_exceptions=ConnectionError,
    max_calls_total=4,
    retry_window_after_first_call_in_seconds=60,
)
def get_page() -> str:
    response = requests.get('https://tech.channable.com/atom.xml')
    return response.text
```

In the above decorator, `retry_on_exceptions` refers to exceptions we want to
retry on, `max_calls_total` maximal number of retry attempts we want to make,
and `retry_window_after_first_call_in_seconds` refers to retry window within
which the `max_calls_total` will be made. In this case we want to make
a maximum of 4 retries spread uniformly on a 60 second interval.

Features
--------

- Generic Decorator API
- Specify retry exception (i.e. kind of exception that we want retry)
- Specify retry window after first call in seconds (i.e. exponential backoff sleeping between attempts)
- Pre-shipped list of popular exceptions, which can easily be expanded


Installation
------------

To install Opnieuw, simply:

    $ pip install opnieuw

Examples
----------

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
    retry_on_exceptions=STANDARD_HTTP_EXCEPTIONS
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
