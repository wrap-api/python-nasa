from typing import Any, Dict, Text, Tuple, Type, Callable

from nasa.exceptions import NASAUnidentifiedError


class NASADecorator:
    def __init__(self, **kwargs: Dict[Text, Any]) -> None:
        self.params = kwargs

    @staticmethod
    def catch_unidentidied_error(
        *args: Tuple[Any], **kwargs: Dict[Text, Any]
    ) -> Callable:
        def wrapper(function: Callable) -> Any:
            try:
                result: Any = function(*args, **kwargs)
            except Exception as error:
                raise NASAUnidentifiedError(str(error))
            else:
                return result

        return wrapper

    @staticmethod
    def decorate_all_methods(decorator: Callable) -> Callable:
        def decorate(cls: Type):
            for attr in dir(cls):
                if callable(getattr(cls, attr)):
                    setattr(cls, attr, decorator(getattr(cls, attr)))
            return cls

        return decorate
