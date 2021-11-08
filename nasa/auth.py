from typing import Text
from requests.auth import AuthBase
from requests.models import PreparedRequest


class NASAAuth(AuthBase):
    def __init__(self, api_key: Text = "DEMO_KEY") -> None:
        self.__api_key = api_key

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        request.prepare_url(request.url, {"api_key": self.__api_key})
        return request
