from typing import Text
from unittest.case import TestCase
from unittest.mock import Mock, patch

from requests.models import Response
from nasa.clients.apod import ApodClient

from nasa.typing import IsoDate
from nasa.warnings import AttributesCollussionWarning, InvalidInputWarning


class TestWarnings(TestCase):
    def test_invalid_input_warning(self):
        # Arrange
        invalid_date: Text = "Invalid Date"
        # Assert
        with self.assertWarns(InvalidInputWarning):
            # Act
            IsoDate(invalid_date)

    @patch("requests.get")
    def test_attributes_collussion_warning(self, mock_request: Mock):
        # Arrange
        apod_client: ApodClient = ApodClient()
        mock_response: Response = Response()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "plain/text"}
        mock_request.return_value = mock_response
        # Assert
        with self.assertWarns(AttributesCollussionWarning):
            # Act
            apod_client.apod(
                date="2021-01-15", start_date="2021-01-01", end_date="2021-01-31"
            )
