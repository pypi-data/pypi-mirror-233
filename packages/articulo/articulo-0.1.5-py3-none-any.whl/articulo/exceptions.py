#!/usr/bin/env python3

"""This module contains all exception classes 
that can be raised during the process of
article downloading and parsing."""


class NoHTMLException(Exception):
    """
    Exception, raises when there is no html
    was recieved.
    """

    def __init__(self, url: str, *args: object) -> None:
        super().__init__(f"No HTML was recieved from {url}", *args)


class HTTPErrorException(Exception):
    """
    Exception, raises when there was
    an HTTP error recieved while requesting article content.
    """

    def __init__(self, message: str, http_code: int) -> None:
        self.message = message
        self.http_code = http_code
        super().__init__(message)


class MaxIterations(Exception):
    """
    Exception, raises when there is no parent
    element found during 100 iterations.
    """


class NoSuchElementException(Exception):
    """
    Exception, raises when there is some
    element cannot be found in page html.
    """


class NoTitleException(Exception):
    """
    Exception, raised when there is
    no title element found in page html.
    """

    def __init__(self, url: str) -> None:
        super().__init__(f"Document {url} has no tag containing artcile title in html.")
