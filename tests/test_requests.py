from typing import Dict, Text
from unittest import TestCase
from unittest.mock import Mock, patch
from nasa.auth import NASAAuth
from nasa.clients.apod import ApodClient
from nasa.clients.base import BaseClient
from nasa.clients.donki import DonkiClient
from nasa.clients.earth import EarthClient
from nasa.clients.epic import EpicClient
from nasa.clients.insight import InsightClient
from nasa.clients.mars_rover_photos import MarsRoverPhotosClient
from nasa.clients.neo import NeoClient
from nasa.clients.tech_transfer import TechTransferClient
from nasa.clients.techport import TechPortClient

from nasa.typing import JSONType


class TestRequests(TestCase):
    API_KEY: Text = "Example-Key"
    parameters: Dict[Text, JSONType] = {
        "test_base_client": {"path": "", "params": {}},
        "test_apod_client": {
            "path": "/planetary/apod",
            "params": {
                "date": None,
                "start_date": None,
                "end_date": None,
                "count": None,
                "thumbs": False,
            },
        },
        "test_donki_client": {
            "path": "/DONKI/CME",
            "params": {
                "startDate": None,
                "endDate": None,
                "mostAccurateOnly": None,
                "speed": None,
                "halfAngle": None,
                "catalog": None,
                "type": None,
            },
        },
        "test_earth_client": {
            "path": "/planetary/earth/assets",
            "params": {
                "lat": 0,
                "lon": 0,
                "dim": None,
                "date": None,
                "cloud_score": None,
            },
        },
        "test_epic_client": {"path": "/EPIC/api/natural/available", "params": {}},
        "test_insight_client": {
            "path": "/insight_weather",
            "params": {"version": 1.0, "feedtype": "json"},
        },
        "test_mars_rover_photos_client": {
            "path": "/mars-photos/api/v1/rovers/curiousity/photos",
            "params": {"sol": None, "camera": "all", "page": 1, "earth_date": None},
        },
        "test_neo_client": {
            "path": "/neo/rest/v1/neo/browse",
            "params": {"start_date": None, "end_date": None, "asteroid_id": None},
        },
        "test_tech_transfer_client": {"path": "/techtransfer/patent/", "params": {}},
        "test_techport_client": {
            "path": "/techport/api/projects/",
            "params": {"updatedSince": None},
        },
    }

    @patch("requests.get")
    def test_base_client(self, mock_get_requests: Mock) -> None:
        # Arrange
        parameter: Dict[Text, JSONType] = self.parameters["test_base_client"]
        path: Text = parameter["path"]
        params = parameter["params"]
        client: BaseClient = BaseClient(self.API_KEY)
        url: Text = f"{client.BASE_URL}{path}"
        # Act
        client._get(path, params)
        # Assert
        mock_get_requests.assert_called_once_with(
            url, params, auth=NASAAuth(self.API_KEY)
        )

    @patch("requests.get")
    def test_apod_client(self, mock_get_requests: Mock) -> None:
        # Arrange
        parameter: Dict[Text, JSONType] = self.parameters["test_apod_client"]
        path: Text = parameter["path"]
        params = parameter["params"]
        client: ApodClient = ApodClient(self.API_KEY)
        url: Text = f"{client.BASE_URL}{path}"
        # Act
        client.apod()
        # Assert
        mock_get_requests.assert_called_once_with(
            url, params, auth=NASAAuth(self.API_KEY)
        )

    @patch("requests.get")
    def test_donki_client(self, mock_get_requests: Mock) -> None:
        # Arrange
        parameter: Dict[Text, JSONType] = self.parameters["test_donki_client"]
        path: Text = parameter["path"]
        params = parameter["params"]
        client: DonkiClient = DonkiClient(self.API_KEY)
        url: Text = f"{client.BASE_URL}{path}"
        # Act
        client.donki_cme()
        # Assert
        mock_get_requests.assert_called_once_with(
            url, params, auth=NASAAuth(self.API_KEY)
        )

    @patch("requests.get")
    def test_earth_client(self, mock_get_requests: Mock) -> None:
        # Arrange
        parameter: Dict[Text, JSONType] = self.parameters["test_earth_client"]
        path: Text = parameter["path"]
        params = parameter["params"]
        client: EarthClient = EarthClient(self.API_KEY)
        url: Text = f"{client.BASE_URL}{path}"
        # Act
        client.earth_assets(params["lat"], params["lon"])
        # Assert
        mock_get_requests.assert_called_once_with(
            url, params, auth=NASAAuth(self.API_KEY)
        )

    @patch("requests.get")
    def test_epic_client(self, mock_get_requests: Mock) -> None:
        # Arrange
        parameter: Dict[Text, JSONType] = self.parameters["test_epic_client"]
        path: Text = parameter["path"]
        params = parameter["params"]
        client: EpicClient = EpicClient(self.API_KEY)
        url: Text = f"{client.BASE_URL}{path}"
        # Act
        client.epic_natural()
        # Assert
        mock_get_requests.assert_called_once_with(
            url, params, auth=NASAAuth(self.API_KEY)
        )

    @patch("requests.get")
    def test_insight_client(self, mock_get_requests: Mock) -> None:
        # Arrange
        parameter: Dict[Text, JSONType] = self.parameters["test_insight_client"]
        path: Text = parameter["path"]
        params = parameter["params"]
        client: InsightClient = InsightClient(self.API_KEY)
        url: Text = f"{client.BASE_URL}{path}"
        # Act
        client.insight()
        # Assert
        mock_get_requests.assert_called_once_with(
            url, params, auth=NASAAuth(self.API_KEY)
        )

    @patch("requests.get")
    def test_mars_rover_photos_client(self, mock_get_requests: Mock) -> None:
        # Arrange
        parameter: Dict[Text, JSONType] = self.parameters[
            "test_mars_rover_photos_client"
        ]
        path: Text = parameter["path"]
        params = parameter["params"]
        client: MarsRoverPhotosClient = MarsRoverPhotosClient(self.API_KEY)
        url: Text = f"{client.BASE_URL}{path}"
        # Act
        client.mars_rover_photos("curiousity")
        # Assert
        mock_get_requests.assert_called_once_with(
            url, params, auth=NASAAuth(self.API_KEY)
        )

    @patch("requests.get")
    def test_neo_client(self, mock_get_requests: Mock) -> None:
        # Arrange
        parameter: Dict[Text, JSONType] = self.parameters["test_neo_client"]
        path: Text = parameter["path"]
        params = parameter["params"]
        client: NeoClient = NeoClient(self.API_KEY)
        url: Text = f"{client.BASE_URL}{path}"
        # Act
        client.neo_browse()
        # Assert
        mock_get_requests.assert_called_once_with(
            url, params, auth=NASAAuth(self.API_KEY)
        )

    @patch("requests.get")
    def test_tech_transfer_client(self, mock_get_requests: Mock) -> None:
        # Arrange
        parameter: Dict[Text, JSONType] = self.parameters["test_tech_transfer_client"]
        path: Text = parameter["path"]
        params = parameter["params"]
        client: TechTransferClient = TechTransferClient(self.API_KEY)
        url: Text = f"{client.BASE_URL}{path}"
        # Act
        client.tech_transfer_patent()
        # Assert
        mock_get_requests.assert_called_once_with(
            url, params, auth=NASAAuth(self.API_KEY)
        )

    @patch("requests.get")
    def test_techport_client(self, mock_get_requests: Mock) -> None:
        # Arrange
        parameter: Dict[Text, JSONType] = self.parameters["test_techport_client"]
        path: Text = parameter["path"]
        params = parameter["params"]
        client: TechPortClient = TechPortClient(self.API_KEY)
        url: Text = f"{client.BASE_URL}{path}"
        # Act
        client.techport()
        # Assert
        mock_get_requests.assert_called_once_with(
            url, params, auth=NASAAuth(self.API_KEY)
        )
