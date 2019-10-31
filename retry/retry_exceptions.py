import requests.exceptions
import urllib3.exceptions  # type: ignore
from urllib.error import HTTPError


class RetryException(Exception):
    """
    Defines a custom RetryException that can be raised for specific errors we want to retry on.
    """


def retry_if_server_failure(exception: BaseException) -> bool:
    """
    Define the exceptions we want to retry on if there is a server failure.
    """
    http_exceptions_to_retry = [500, 503]

    if isinstance(exception, requests.exceptions.ChunkedEncodingError):
        return True
    elif isinstance(exception, requests.exceptions.ConnectionError):
        # NOTE: requests.exceptions.ConnectionError is completely unrelated
        # to ConnectionError from the standard library below.
        return True
    elif isinstance(exception, ConnectionError):
        return True
    elif isinstance(exception, EOFError):
        return True
    elif isinstance(exception, urllib3.exceptions.ProtocolError):
        return True
    elif isinstance(exception, urllib3.exceptions.ReadTimeoutError):
        return True
    elif isinstance(exception, requests.exceptions.Timeout):
        return True
    elif isinstance(exception, requests.exceptions.SSLError):
        return True
    elif isinstance(exception, HTTPError):
        return exception.getcode() in http_exceptions_to_retry
    elif isinstance(exception, RetryException):
        return True
    else:
        return False


# The same list of exceptions as above, but for use with @channable_retry.
# Does not include HTTPError because @channable_retry does not conditionally
# catch exceptions; catch manually and raise RetryException instead.
# Some subclasses of HTTPError, such as ProtocolError and SSLError, are included.
STANDARD_HTTP_EXCEPTIONS = (
    ConnectionError,
    EOFError,
    RetryException,
    requests.exceptions.ChunkedEncodingError,
    # NOTE: requests.exceptions.ConnectionError is completely unrelated to the
    # above ConnectionError from the standard library. We need to handle both.
    requests.exceptions.ConnectionError,
    requests.exceptions.SSLError,
    requests.exceptions.Timeout,
    urllib3.exceptions.ProtocolError,
    urllib3.exceptions.ReadTimeoutError,
)