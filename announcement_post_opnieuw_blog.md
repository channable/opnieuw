# How you too can retry your life and bounce back from failure
										
In this post, we want to introduce our new, easy to use, intuitive and simple retry package: [Opnieuw][opnieuw], which is responsible for all the (network) retry task in [Channable][channable].

Opnieuw is a general-purpose retrying library, written in Python, in order to simplify the task of adding retry behavior to both synchronous as well as asynchronous tasks.

Channable is a feed processing tool where users can define rules to optimize their product feeds. At Channable we consume a lot of external apis for our daily operations and having a good retry handler is extremely import for us in making those operations run smoothly. For example, we sometimes get `ConnectionError` for whatever reason when making an api call to an external server. By retrying our request we can usually solve this problem. 

Before writing our own retry package, we extensively experimented with other retry packages. Unfortunately, when using those retry packages we experienced multiple difficulties, especially when we tried to customize them to fit our needs. Most of them had counter-intuitive parameters settings, which in turn made them difficult to customize. In addition, their documentations did not really help either in tackling those issues. Take as an example the time related arguments, so if we have a parameter `delay` which is supposed to manage the retry delays, it was unclear whether the time unit was in seconds or milliseconds, which both are reasonable values for some of our calls to external APIs. In some cases too much flexibility was provided with regard to parameter tuning which only lead to nonsensical combinations of parameters. In other cases, retry strategies were opt in, which made it easy to forget to explicitly choose one e.g. jitter or exponential back-off.

Opnieuw is easy and straightforward to use and it was designed to tackle all the above mentioned issues. Let's look at a trivial example in order to demonstrate the power of Opnieuw and to show how easy and intuitive it is to use it. Suppose we want to parse `https://tech.channable.com/atom.xml` and we want to add a retry behavior to it in order to handle a specific network Exception. We can add Opnieuw to our
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


As is clear from the above example, by decorating the function we add a retry behavior. The parameters are intuitive and easy to use. `retry_on_exceptions` refers to kind of exceptions we want to catch. It could be a single or multiple (tuple) exceptions, `max_calls_total` refers to the number of total retry attempts we would like to make and finally, `retry_window_after_first_call_in_seconds` is the maximal retry window in seconds, which this case is 60 seconds. This means that in the above example, we would like to have 4 retry attempts within a 60 second window in case of `ConnectionError` exception. It is simple and easy, there is no complexity involved in here and we are using the exponential backoff algorithm. There is also a async variant for retrying asynchronous tasks. All the parameters remain the same, the only difference is that it is used with async functions/methods. Below an example of an asynchronous function with async retry behavior:

```python
from opnieuw import retry_async


@retry_async(
    retry_on_exceptions=ConnectionError,
    max_calls_total=4,
    retry_window_after_first_call_in_seconds=60,
)
async def get_page() -> str:
    response = requests.get('https://tech.channable.com/atom.xml')
    return response.text
```


## Conclusion

At Channable. We had a bitter experience using other retry packages as they were counter-intuitive, unclear and extremely difficult to customize. Opnieuw tackles all these issues, it is simple, easy, and very intuitive to use, and we are open-sourcing it today, We set out to create a simple, easy to use and intuitive retry package for most of our network operations and we have achieved that objective.

[channable]:  https://www.channable.com/
[opnieuw]: https://github.com/channable/opnieuw/blob/master/README.md

post to : https://github.com/channable/tech.channable.com/issues/25