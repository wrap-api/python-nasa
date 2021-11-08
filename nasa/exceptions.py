from typing import Text


class BaseNASAException(Exception):
    CODE: Text = "NASA-001"


class NASAHTTPError(BaseNASAException):
    CODE: Text = "NASA-002"


class InvalidNeoAPITypeError(BaseNASAException):
    CODE: Text = "NASA-003"


class InvalidDateConvertible(BaseNASAException):
    CODE: Text = "NASA-004"
