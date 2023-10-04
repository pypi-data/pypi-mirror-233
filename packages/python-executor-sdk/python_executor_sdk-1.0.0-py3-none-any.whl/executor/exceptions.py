# Copyright (c) Hao Hoang (haohoangofficial@mail.com)

"""
The exceptions module contains Exception subclasses whose instances might be
raised by the sdk.
"""

import json
from bs4 import BeautifulSoup as bs

class ExecutorError(Exception):
    """
    All errors specific to Executor api requests and Executor ads design will be
    subclassed from ExecutorError which is subclassed from Exception.
    """
    pass


class ExecutorRequestError(ExecutorError):
    """
    Raised when an api request fails. Returned by error() method on a
    ExecutorResponse object returned through a callback function (relevant
    only for failure callbacks) if not raised at the core api call method.
    """

    def __init__(
        self, message,
        http_status,
        http_headers,
        body
    ):
        self._message = message
        self._http_status = http_status
        self._http_headers = http_headers
        try:
            self._body = json.loads(body)
        except (TypeError, ValueError):
            try:
                self._body = bs(self._body, 'html.parser')
            except (TypeError, ValueError):
                self._body = body

    def http_status(self):
        return self._http_status

    def http_headers(self):
        return self._http_headers

    def body(self):
        return self._body

    def get_message(self):
        return self._message


class ExecutorBadObjectError(ExecutorError):
    """Raised when a guarantee about the object validity fails."""
    pass

class ExecutorBadParameterError(ExecutorError):
    """Raised when a guarantee about the parameter validity fails."""
    pass

class ExecutorUnavailablePropertyException(ExecutorError):
    """Raised when an object's property or method is not available."""
    pass
