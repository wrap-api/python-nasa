import warnings
from typing import Dict, Optional, Text, Union
from nasa.clients.base import BaseClient
from nasa.exceptions import InvalidNeoAPIType, MissingNeoAsteroidID
from nasa.typing import IsoDate, IsoDateConvertible, JSONType
from nasa.warnings import AttributesCollussionWarning


class NeoClient(BaseClient):
    def neo(
        self,
        api_type: Text,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
        asteroid_id: Optional[int] = None,
    ) -> JSONType:
        """Near Earth Object Web Service

        Args:
            api_type (Text): Possible values are (feed, lookup, browse)
            start_date (Optional[IsoDateConvertible], optional): Starting date for asteroid search. Defaults to None.
            end_date (Optional[IsoDateConvertible], optional): Ending date for asteroid search. Defaults to None.
            asteroid_id (Optional[int], optional): Asteroid SPK-ID correlates to the NASA JPL small body. Defaults to None.

        Raises:
            InvalidNeoAPIType: Raises when the API Type given is invalid

        Returns:
            JSONType: Parsed response body from the API
        """
        base_path: Text = "/neo/rest/v1"
        type_path: Dict[Text, Text] = {
            "feed": "/feed",
            "lookup": "/neo/",
            "browse": "/neo/browse",
        }
        if api_type not in type_path.keys():
            message: Text = f"Invalid api_type {api_type}. Valid api_type values are {tuple(type_path.keys())}"
            raise InvalidNeoAPIType(message)
        if api_type == "lookup" and asteroid_id is None:
            message: Text = "Missing asteroid_id"
            raise MissingNeoAsteroidID(message)
        if api_type == "lookup" and (start_date is not None or end_date is not None):
            message: Text = f"start_date or end_date shouldn't be filled when the api_type is {api_type}. Set them to None"
            warnings.warn(message, AttributesCollussionWarning)
            iso_start_date, iso_end_date = None, None
        elif api_type == "feed" and asteroid_id is not None:
            message: Text = f"asteroid_id shouldn't be filled when the api_type is {api_type}. Set it to None"
            warnings.warn(message, AttributesCollussionWarning)
            asteroid_id = None
        elif api_type == "browse" and (
            asteroid_id is not None or start_date is not None or end_date is not None
        ):
            message: Text = f"start_date, end_date and asteroid_id shouldn't be filled when the api_type is {api_type}. Set them to None"
            warnings.warn(message, AttributesCollussionWarning)
            asteroid_id, start_date, end_date = None, None, None
        path: Text = f"{base_path}{type_path.get(api_type)}"
        iso_start_date: Optional[Text] = IsoDate(start_date).value()
        iso_end_date: Optional[Text] = IsoDate(end_date).value()
        params: Dict[Text, Union[Text, int, None]] = {
            "start_date": iso_start_date,
            "end_date": iso_end_date,
            "asteroid_id": asteroid_id,
        }
        return self._get(path, params)

    def neo_feed(
        self,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
    ) -> JSONType:
        """Near Earth Object Web Service Feed Endpoint

        Args:
            start_date (Optional[IsoDateConvertible], optional): Starting date for asteroid search. Defaults to None.
            end_date (Optional[IsoDateConvertible], optional): Ending date for asteroid search. Defaults to None.

        Returns:
            JSONType: Parsed response body from the API
        """
        return self.neo(api_type="feed", start_date=start_date, end_date=end_date)

    def neo_lookup(
        self,
        asteroid_id: int,
    ) -> JSONType:
        """Near Earth Object Web Service Lookup Endpoint

        Args:
            asteroid_id (Optional[int], optional): Asteroid SPK-ID correlates to the NASA JPL small body. Defaults to None.

        Returns:
            JSONType: Parsed response body from the API
        """
        return self.neo(api_type="lookup", asteroid_id=asteroid_id)

    def neo_browse(self) -> JSONType:
        """Near Earth Object Web Service Browse Endpoint

        Returns:
            JSONType: Parsed response body from the API
        """
        return self.neo(api_type="browse")
