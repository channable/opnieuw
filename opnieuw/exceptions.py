# Opnieuw: Retries for humans
# Copyright 2019 Channable
#
# Licensed under the 3-clause BSD license, see the LICENSE file in the repository root.


class RetryException(Exception):
    """
    Defines a custom RetryException that can be raised for specific errors we
    want to retry on.

    E.g.: Cdiscount can return an `UnexpectedException` containing little info,
    but is usually automatically resolved on a retry. We raise this Exception
    which is also defined as a server failure below.
    """
