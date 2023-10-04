import json
from executor.exceptions import ExecutorRequestError
from bs4 import BeautifulSoup as bs
from executor.executors import ExecutorsEnum
from executor.requests import requests

class ExecutorResponse(object):
    def __init__(self, body=None, http_status=None, headers=None, call=None):
        self._body = body
        self._http_status = http_status
        self._headers = headers or {}
        self._call = call

    def body(self):
        """Returns the response body."""
        return self._body

    def json(self):
        """Returns the response body -- in json if possible."""
        try:
            return json.loads(self._body)
        except (TypeError, ValueError):
            return self._body
    
    def html(self):
        """Return the response body -- in hmlt if possible"""
        try:
            return bs(self._body, 'html.parser')
        except (TypeError, ValueError):
            return self._body
    
    def headers(self):
        """Return the response headers."""
        return self._headers

    def etag(self):
        """Returns the ETag header value if it exists."""
        return self._headers.get('ETag')

    def status(self):
        """Returns the http status code of the response."""
        return self._http_status

    def is_success(self):
        """Returns boolean indicating if the call was successful."""

        if self._http_status <= 400:
            return True
        else:
            # Something else
            return False

    def is_failure(self):
        """Returns boolean indicating if the call failed."""
        return not self.is_success()

    def error(self):
        """
        Returns a ExecutorRequestError (located in the exceptions module) with
        an appropriate debug message.
        """
        if self.is_failure():
            return ExecutorRequestError(
                "Call was not successful",
                self.status(),
                self.headers(),
                self.body(),
            )
        else:
            return None


class ExecutorRequest:
    def __init__(self, executor = ExecutorsEnum.BASIC) -> None:
        self.executor = executor
        self.response = None

    def __call__(self, url, params=None, headers=None, **kwargs):
        
        if self.executor == ExecutorsEnum.BASIC:
            self.response = requests.get(url, params=params, headers=headers, **kwargs)
        elif self.executor == ExecutorsEnum.SELENIUM_REMOTE:
            pass
        elif self.executor == ExecutorsEnum.SELENIUM_WEBDRIVER:
            pass
        elif self.executor == ExecutorsEnum.SPLASH:
            pass
        else:
            pass
        
        if self.response == None: return None
        exec_response = ExecutorResponse(
            body=self.response.text,
            headers=self.response.headers,
            http_status=self.response.status_code,
        )

        if exec_response.is_failure():
            raise exec_response.error()
        return exec_response

        