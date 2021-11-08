from json.decoder import JSONDecodeError
from typing import Dict, Optional, Union, Text
import warnings
import requests
from requests import Response
from requests import api
from requests.exceptions import HTTPError

from nasa.auth import NASAAuth
from nasa.exceptions import InvalidNeoAPITypeError, NASAHTTPError
from nasa.typing import IsoDate, IsoDateConvertible


class Client:
    BASE_URL: Text = "https://api.nasa.gov"

    def __init__(self, api_key: Text = "DEMO_KEY") -> None:
        self.__api_key: Text = api_key

    def apod(
        self,
        date: Optional[IsoDateConvertible] = None,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
        count: Optional[int] = None,
        thumbs: bool = False,
    ) -> Dict:
        iso_date: Optional[Text] = IsoDate(date).value()
        iso_start_date: Optional[Text] = IsoDate(start_date).value()
        iso_end_date: Optional[Text] = IsoDate(end_date).value()
        if iso_date is not None and (
            iso_start_date is not None or iso_end_date is not None
        ):
            message: Text = u"`start_date` or `end_date` shouldn't be filled when the `date` is filled. Set them to None"
            warnings.warn(message, UserWarning)
            iso_start_date, iso_end_date = None, None
        path: Text = "/planetary/apod"
        params: Dict = {
            "date": iso_date,
            "start_date": iso_start_date,
            "end_date": iso_end_date,
            "count": count,
            "thumbs": thumbs,
        }
        return self._get(path, params)

    def neo(
        self,
        api_type: Text,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
        asteroid_id: Optional[int] = None,
    ) -> Dict:
        base_path: Text = "/neo/rest/v1"
        type_path: Dict = {"feed": "/feed", "lookup": "/neo/", "browse": "/neo/browse"}
        if api_type not in type_path.keys():
            message: Text = f"Invalid api_type {api_type}. Valid api_type values are {list(type_path.keys())}"
            raise InvalidNeoAPITypeError(message)
        path: Text = f"{base_path}{type_path.get(api_type)}"
        params: Dict = {
            "start_date": start_date,
            "end_date": end_date,
            "asteroid_id": asteroid_id,
        }
        return self._get(path, params)

    def donki(
        self,
        api_type: Text,
        start_date: Optional[Text] = None,
        end_date: Optional[Text] = None,
    ):
        pass

    def _get(self, path: Text, params: Dict) -> Union[Dict, Text]:
        url: Text = f"{self.BASE_URL}{path}"
        response: Response = requests.get(url, params, auth=NASAAuth(self.__api_key))
        return self._response_handler(response)

    def _response_handler(self, response: Response) -> Union[Dict, Text]:
        try:
            response.raise_for_status()
        except HTTPError as error:
            raise NASAHTTPError(error)
        try:
            content: Dict = response.json()
        except JSONDecodeError:
            content: Text = response.text
        finally:
            return content
