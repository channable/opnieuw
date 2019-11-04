Channable Retry
=========================
Channable Retry is a general-purpose retrying library, written in
Python, in order to simplify the task of adding retry behavior to both synchronous as well as asynchronous tasks.
Channable Retry is easy and straight forward to use. Why channable-retry?. Most retry packages lack either
adequate documentation on how to properly use the package and or are difficult to customize. Valuable time is
lost in trying to figure out how to properly utilize a retry package. Channable-retry makes
it incredibly easy to add retry functionality to any task that requires retry.
Suppose we want parse `https://tech.channable.com/atom.xml` and we want to add a retry to handle a specific network Exception.
We can add a channable retry to our network handler as follows:

```python

    import requests    
    from channable_retries import channable_retry
    from requests.exceptions import ConnectionError

    @channable_retry(
        retry_on_exceptions=ConnectionError,
        max_calls_total=4,
        retry_window_after_first_call_in_seconds=60,
    )
    def get_page() -> str:
      
        try:
            response = requests.get('https://tech.channable.com/atom.xml')
        except ConnectionError:
            raise ConnectionError()
        else:
            return repsonse.text
                
```
In the above decorator, `retry_on_exceptions` refers to exceptions we want to retry on, `max_calls_total` maximal number of retry attempts
we want to make, and `retry_window_after_first_call_in_seconds` refers to retry window within which the `max_calls_total` will be made. In this 
case we want to make a maximum of 4 retries spread uniformly on a 60 second interval.


Features
--------

- Generic Decorator API
- Specify retry exception (i.e. kind of exception that we want retry)
- Specify retry window after first call in seconds (i.e. exponential backoff sleeping between attempts)
- pre-shipped list of popular exception, which could easily be expanded


Installation
------------

To install channable_retries, simply:


    $ pip install channable_retries


Examples
----------

The short example above provides a concise demonstration of how channable_retries could be used. Let's dig deeper into channable_retries and add another exception to `retry_on_exceptions` to do a retry on:
  
```python

	from urllib3.exceptions import ProtocolError

    @channable_retry(
        retry_on_exceptions=(ConnectionError, ProtocolError)
        max_calls_total=4,
        retry_window_after_first_call_in_seconds=60,
    )
    def get_page() -> str:
      
        try:
            response = requests.post('https://tech.channable.com/atom.xml')
        except ConnectionError:
            raise ConnectionError()
        except urllib3.exceptions.ProtocolError:
        	raise ProtocolError()
        else:
            return response.text
```
We can pass the name of exception we want do retry for or a tuple of exceptions to the `retry_on_exceptions`.
As mentioned earlier Channable-retry was developed to make it more convenient to add retry behavior to any task. 

Let's make it a little bit more generic and add list of retry exception that should be used for 
running the retry:

```python

    STANDARD_HTTP_EXCEPTIONS =  (
        ConnectionError,
        ProtocolError,
        RetryException,
        ...
    )

    @channable_retry(
        retry_on_exceptions=STANDARD_HTTP_EXCEPTIONS
        max_calls_total=4,
        retry_window_after_first_call_in_seconds=60,
    )
    def get_page() -> str:
      
        try:
            response = requests.post('https://tech.channable.com/atom.xml')
        except ConnectionError:
            raise ConnectionError()
        except urllib3.exceptions.ProtocolError:
        	raise ProtocolError()
        else:
            return response.text

```

Now our retry is more generic, as exception raise which in `STANDARD_HTTP_EXCEPTIONS` will be 
retried. 


If you want retry behavior for async tasks, then there is also an async retry which basically work the same way but for async tasks.

Here is the example above but in async mood:
```python

    from channable_retries import channable_retry_async

    STANDARD_HTTP_EXCEPTIONS =  (
            ConnectionError,
            EOFError,
            RetryException,
            ...
        )

    @channable_retry_async(
        retry_on_exceptions=STANDARD_HTTP_EXCEPTIONS
        max_calls_total=4,
        retry_window_after_first_call_in_seconds=60,
    )
    async def get_page() -> str:
      
        try:
            response = await requests.post('https://tech.channable.com/atom.xml')
        except ConnectionError:
            raise ConnectionError()
        except urllib3.exceptions.ProtocolError:
        	raise ProtocolError()
        else:
            return await response.text

```
