"""
Channable-retry: Retry for humans
"""
import pkgutil

from .retries import channable_retry_async, channable_retry
from .retry_exceptions import STANDARD_HTTP_EXCEPTIONS

# Check minimum required Python version
import sys
if sys.version_info < (2, 7):
    print("Channable-retry  requires Python 3.7")
    sys.exit(1)


# Channable-retry version
__version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()

__all__ = [__version__,  channable_retry_async, channable_retry]
