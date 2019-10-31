Channable Retry
=========================
Channable Retry is an *** licensed general-purpose retrying library, written in
Python, to simplify the task of adding retry behavior to both synchronous as well as asynchronous tasks.
Channable Retry is easy and straight forward to use. Why channable-retry?. Most retry packages lack either
adequate documentation on how to properly use the package and or difficult to customize. Valueble time is
lost in trying to figure out which parameters to set and how to set those parameter. channable-retry makes
it really easy to add retry functionality to any task that requires retry. Suppose we want parse `www.example.com/retry` and we want to add a retry to handle specific netwrok Exception.
Then we can add a channable retry for handling network exceptions in the following way:


    from channable_retries import channable_retry
    from requests.exceptions import ConnectionError

    @channable_retry(
        retry_on_exceptions=ConnectionError,
        max_calls_total=4,
        retry_window_after_first_call_in_seconds=60,
    )
    def get_page(url: str, headers:Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
      
        try:
            response = requests.post(url, json=data, headers=headers)
        except ConnectionError:
            raise ConnectionError()


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

The short example above provides a conceive demonstration of how channable_retries could be used. Let's dig deeper into channable_retries and apply it various other
scenario where it could applied.

One scenario is that we want to do retries on multiple exceptions. Using channable retries, we could easily extend the above example to retry teh netwrok request for
multiple exceptions.  


	from channable_retries import channable_retry
    from requests.exceptions import ConnectionError
	from urllib3.exceptions import ProtocolError

    @channable_retry(
        retry_on_exceptions=(ConnectionError, STANDARD_HTTP_EXCEPTIONS)
        max_calls_total=4,
        retry_window_after_first_call_in_seconds=60,
    )
    def get_page(url: str, headers:Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
      
        try:
            response = requests.post(url, json=data, headers=headers)
        except ConnectionError:
            raise ConnectionError()
        except urllib3.exceptions.ProtocolError:
        	raise ProtocolError()


Let's make it a little bit more generic and add list of retry exception that should be used for running 
the retry:

    from channable_retry import STANDARD_HTTP_EXCEPTIONS

    @channable_retry(
        retry_on_exceptions=STANDARD_HTTP_EXCEPTIONS
        max_calls_total=4,
        retry_window_after_first_call_in_seconds=60,
    )
    def get_page(url: str, headers:Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
      
        try:
            response = requests.post(url, json=data, headers=headers)
        except ConnectionError:
            raise ConnectionError()

Any combination of stop, wait, etc. is also supported to give you the freedom to mix and match.

Contribute
----------


License
-------
Channable-retry is licensed under the 3-clause BSD license.

