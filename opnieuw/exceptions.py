# Opnieuw: Retries for humans
# Copyright 2019 Channable
#
# Licensed under the 3-clause BSD license, see the LICENSE file in the repository root.


class RetryException(Exception):
    """
    Defines a custom RetryException that can be raised for specific errors we
    want to retry on.
    """
