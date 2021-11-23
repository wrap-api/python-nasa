from typing import Dict, Text, Union
from PIL.ImageFile import ImageFile
import requests
from requests.models import HTTPError, Response
from nasa.auth import NASAAuth
from nasa.exceptions import NASAHTTPError

from nasa.typing import JSONType
from nasa.utils import get_url_image


class BaseClient:
    BASE_URL: Text = "https://api.nasa.gov"

    def __init__(self, api_key: Text = "DEMO_KEY") -> None:
        self.__api_key: Text = api_key

    def _get(
        self, path: Text, params: Dict[Text, JSONType] = dict()
    ) -> Union[JSONType, ImageFile]:
        """Making a GET request to the base url with given path and params.

        Args:
            path (Text): path to be concatinated to the base url
            params (Dict, optional): parameters to be passed as query in url. Defaults to dict().

        Returns:
            Union[JSONType, ImageFile]: Depends on the result of the response handler
        """
        url: Text = f"{self.BASE_URL}{path}"
        response: Response = requests.get(url, params, auth=NASAAuth(self.__api_key))
        return self._response_handler(response)

    def _response_handler(self, response: Response) -> Union[JSONType, ImageFile]:
        """Handling Response from the API according to the requirements

        Args:
            response (Response): response object from the API captured by requests library

        Raises:
            NASAHTTPError: Customized and Extended HTTPError from requests library

        Returns:
            Union[JSONType, ImageFile]: Depends on the content-type of the API response
        """
        try:
            response.raise_for_status()
        except HTTPError as error:
            raise NASAHTTPError(error.strerror)
        content_type: Text = response.headers.get("Content-Type")
        if content_type == "application/json":
            content: JSONType = response.json()
        elif content_type.split("/")[0] == "image":
            content: ImageFile = get_url_image(response.url)
        else:
            content: Text = response.text
        return content
