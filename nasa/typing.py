import warnings
from decimal import Decimal
from datetime import date, datetime
from typing import Dict, Text, Union, Optional

from nasa.exceptions import InvalidDateConvertible

IsoDateConvertible = Union[int, float, Decimal, Text, date, datetime]


class IsoDate:
    UNIT_CONVERSION: Dict = {
        "s": 1,
        "second": 1,
        "seconds": 1,
        "ms": 10e3,
        "millisecond": 10e3,
        "milliseconds": 10e3,
        "us": 10e6,
        "microsecond": 10e6,
        "microseconds": 10e6,
        "ns": 10e9,
        "nanosecond": 10e9,
        "nanoseconds": 10e9,
    }
    ISO_DATE_FORMAT: Text = "%Y-%m-%d"

    def __init__(
        self,
        arg: Optional[IsoDateConvertible],
        unit: Text = "s",
        format: Text = "%Y-%m-%d",
    ) -> None:
        if type(arg) in {int, float, Decimal}:
            if unit not in self.UNIT_CONVERSION.keys():
                message: Text = f"Invalid `unit` {unit}, will use default unit `s`. Valid unit values are {list(self.UNIT_CONVERSION.keys())}"
                warnings.warn(message, UserWarning)
            unix_seconds = arg / self.UNIT_CONVERSION.get(unit, "s")
            self.dt: datetime = datetime.utcfromtimestamp(unix_seconds)
        elif type(arg) is str:
            self.dt: datetime = datetime.strptime(arg, format)
        elif type(arg) in {date, datetime}:
            self.dt: Union[date, datetime] = arg
        else:
            message: Text = f"Invalid type {type(arg)} for `arg`, will set `arg` to None. Valid types for `arg` are [int, float, Decimal, str, date, datetime]"
            warnings.warn(message, UserWarning)
            self.dt: None = None

    def value(self) -> Optional[Text]:
        if self.dt is None:
            return None
        return self.dt.strftime(self.ISO_DATE_FORMAT)

    def __str__(self) -> Text:
        return self.value()

    def __repr__(self) -> Text:
        return self.value()
