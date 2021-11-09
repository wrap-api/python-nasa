from typing import Text, Type


class BaseNASAException(Exception):
    CODE: Text = "NASA-001"

    def __init__(self, message: Text) -> None:
        coded_message: Text = f"{self.CODE} - {message}"
        super().__init__(coded_message)


class NASAHTTPError(BaseNASAException):
    CODE: Text = "NASA-002"


class NASAInvalidInput(BaseNASAException):
    CODE: Text = "NASA-003"


class InvalidNeoAPIType(NASAInvalidInput):
    CODE: Text = "NASA-003A"


class InvalidDonkiAPIType(NASAInvalidInput):
    CODE: Text = "NASA-003B"


class InvalidEarthAPIType(NASAInvalidInput):
    CODE: Text = "NASA-003C"


class InvalidEpicImageType(NASAInvalidInput):
    CODE: Text = "NASA-003D"


class InvalidMarsRover(NASAInvalidInput):
    CODE: Text = "NASA-003E"


class InvalidMarsCamera(NASAInvalidInput):
    CODE: Text = "NASA-003F"


class InvalidMarsRoverCamera(NASAInvalidInput):
    CODE: Text = "NASA-003G"


class InvalidTechTransferAPIType(NASAInvalidInput):
    CODE: Text = "NASA-003H"

class NASAUnidentifiedError(BaseNASAException):
    CODE: Text = "NASA-999"
    def __init__(self, message: Text, error_type: Type) -> None:
        typed_message: Text = f"{error_type.__name__} - {message}"
        super().__init__(typed_message)
