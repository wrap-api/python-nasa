from typing import Dict, Optional, Set, Text, Union
import warnings
from PIL.ImageFile import ImageFile

from nasa.clients.base import BaseClient
from nasa.exceptions import NASAInvalidInput
from nasa.typing import IsoDate, IsoDateConvertible, JSONType
from nasa.warnings import AttributesCollussionWarning


class EarthClient(BaseClient):
    def earth(
        self,
        api_type: Text,
        lat: float,
        lon: float,
        dim: Optional[float] = None,
        date: Optional[IsoDateConvertible] = None,
        cloud_score: Optional[bool] = False,
    ) -> Union[JSONType, ImageFile]:
        """NASA Earth API

        Args:
            api_type (Text): API Type to hit
            lat (float): Latitude to be shown
            lon (float): Longitude to be shown
            dim (Optional[float], optional): width and height of image in degrees. Defaults to None.
            date (IsoDateConvertible, optional): date of image; if not supplied, then the most recent image (i.e., closest to today) is returned. Defaults to None.
            cloud_score (Optional[bool], optional): Imagery API type only. [NOT CURRENTLY AVAILABLE!!!!] calculate the percentage of the image covered by clouds. Defaults to False.

        Raises:
            NASAInvalidInput: Raised when the provided API Type is not valid

        Returns:
            Union[JSONType, ImageFile]: Imagery API will response with image which will be handled using PIL. Else, it'll response with JSON
        """
        api_types: Set[Text] = {"imagery", "assets"}
        if api_type not in api_types:
            message: Text = f"Invalid api_type {api_type}. Valid api_type values are {tuple(api_types)}"
            raise NASAInvalidInput(message)
        if api_type != "imagery" and cloud_score is not None:
            message: Text = "cloud_score shouldn't be filled if the api_type is not imagery. Set it to None"
            warnings.warn(message, AttributesCollussionWarning)
            cloud_score = None
        iso_date: Optional[Text] = IsoDate(date).value()
        path: Text = f"/planetary/earth/{api_type}"
        params: Dict[Text, Union[float, Text, bool, None]] = {
            "lat": lat,
            "lon": lon,
            "dim": dim,
            "date": iso_date,
            "cloud_score": cloud_score,
        }
        return self._get(path, params)

    def earth_imagery(
        self,
        lat: float,
        lon: float,
        dim: Optional[float] = None,
        date: Optional[IsoDateConvertible] = None,
        cloud_score: Optional[bool] = False,
    ) -> ImageFile:
        """NASA Earth Imagery API

        Args:
            lat (float): Latitude to be shown
            lon (float): Longitude to be shown
            dim (Optional[float], optional): width and height of image in degrees. Defaults to None.
            date (IsoDateConvertible, optional): date of image; if not supplied, then the most recent image (i.e., closest to today) is returned. Defaults to None.
            cloud_score (Optional[bool], optional): Imagery API type only. [NOT CURRENTLY AVAILABLE!!!!] calculate the percentage of the image covered by clouds. Defaults to False.

        Returns:
            ImageFile: Response with Image which will be handled by PIL.
        """
        return self.earth(
            api_type="imagery",
            lat=lat,
            lon=lon,
            dim=dim,
            date=date,
            cloud_score=cloud_score,
        )

    def earth_assets(
        self,
        lat: float,
        lon: float,
        dim: Optional[float] = None,
        date: Optional[IsoDateConvertible] = None,
    ) -> JSONType:
        """NASA Earth Assets API

        Args:
            lat (float): Latitude to be shown
            lon (float): Longitude to be shown
            dim (Optional[float], optional): width and height of image in degrees. Defaults to None.
            date (IsoDateConvertible, optional): date of image; if not supplied, then the most recent image (i.e., closest to today) is returned. Defaults to None.

        Returns:
            JSONType: Parsed response from the API
        """
        return self.earth(api_type="assets", lat=lat, lon=lon, dim=dim, date=date)
