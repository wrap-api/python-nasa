class BaseNASAException(Exception):
    pass


class NASAHTTPError(BaseNASAException):
    pass


class InvalidNeoAPITypeError(BaseNASAException):
    pass


class InvalidDateConvertible(BaseNASAException):
    pass
