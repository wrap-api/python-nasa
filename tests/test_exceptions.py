from typing import Text
from unittest import TestCase
from unittest.mock import Mock, patch
from requests.models import Response

from nasa.clients.base import BaseClient
from nasa.clients.main import Client
from nasa.exceptions import NASAContentTypeNotImage, NASAHTTPError, NASAInvalidInput
from nasa.utils import get_url_image


class TextException(TestCase):
    def test_nasa_http_error(self):
        # Arrange
        mock_response: Response = Response()
        mock_response.status_code = 500
        client: BaseClient = BaseClient()
        # Assert
        with self.assertRaises(NASAHTTPError):
            # Act
            client._response_handler(mock_response)

    def test_nasa_invalid_input(self):
        # Arrange
        client: Client = Client()
        api_type: Text = "INVALID_API_TYPE"
        # Assert
        with self.assertRaises(NASAInvalidInput):
            # Act
            client.donki(api_type=api_type)

    @patch("requests.get")
    def test_content_type_not_image(self, mock_request: Mock):
        # Arrange
        mock_url: Text = "some_url"
        mock_request(mock_url)
        # Assert
        with self.assertRaises(NASAContentTypeNotImage):
            # Act
            get_url_image(mock_url)
