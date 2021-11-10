from typing import Text, Type


class BaseNASAException(Exception):
    CODE: Text = "NASA-ERROR-001"

    def __init__(self, message: Text) -> None:
        coded_message: Text = f"{self.CODE} - {message}"
        super().__init__(coded_message)


class NASAHTTPError(BaseNASAException):
    CODE: Text = "NASA-ERROR-002"


class NASAInvalidInput(BaseNASAException):
    CODE: Text = "NASA-ERROR-003"


class InvalidNeoAPIType(NASAInvalidInput):
    CODE: Text = "NASA-ERROR-003A"


class MissingNeoAsteroidID(NASAInvalidInput):
    CODE: Text = "NASA-ERROR-003B"


class InvalidDonkiAPIType(NASAInvalidInput):
    CODE: Text = "NASA-ERROR-003C"


class InvalidDonkiNotificationType(NASAInvalidInput):
    CODE: Text = "NASA-ERROR-003D"


class InvalidEarthAPIType(NASAInvalidInput):
    CODE: Text = "NASA-ERROR-003E"


class InvalidEpicImageType(NASAInvalidInput):
    CODE: Text = "NASA-ERROR-003F"


class InvalidMarsRover(NASAInvalidInput):
    CODE: Text = "NASA-ERROR-003G"


class InvalidMarsCamera(NASAInvalidInput):
    CODE: Text = "NASA-ERROR-003H"


class InvalidMarsRoverCamera(NASAInvalidInput):
    CODE: Text = "NASA-ERROR-003I"


class InvalidTechTransferAPIType(NASAInvalidInput):
    CODE: Text = "NASA-ERROR-003J"


class NASAContentTypeNotImage(BaseNASAException):
    CODE: Text = "NASA-ERROR-004"


class NASAUnidentifiedError(BaseNASAException):
    CODE: Text = "NASA-ERROR-999"

    def __init__(self, message: Text, error_type: Type) -> None:
        typed_message: Text = f"{error_type.__name__} - {message}"
        super().__init__(typed_message)
