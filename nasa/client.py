from io import BytesIO
from typing import Dict, Optional, Set, Tuple, Union, Text, List
import warnings
from PIL.ImageFile import ImageFile
import requests
from requests import Response
from requests import api
from requests.exceptions import HTTPError
from PIL import Image

from nasa.auth import NASAAuth
from nasa.decorators import NASADecorator
from nasa.exceptions import (
    InvalidDonkiAPIType,
    InvalidEarthAPIType,
    InvalidEpicImageType,
    InvalidMarsCamera,
    InvalidMarsRover,
    InvalidMarsRoverCamera,
    InvalidNeoAPIType,
    NASAHTTPError,
)
from nasa.typing import (
    IsoDate,
    IsoDateConvertible,
    JSONType,
)

main_decorator: NASADecorator = NASADecorator()

@main_decorator.decorate_all_methods(main_decorator.catch_unidentidied_error)
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
    ) -> JSONType:
        """Astronomy Picture of the Day https://github.com/nasa/apod-api

        Args:
            date (Optional[IsoDateConvertible], optional): The date of the APOD image to retrieve. Defaults to None.
            start_date (Optional[IsoDateConvertible], optional): The start of a date range, when requesting date for a range of dates. Cannot be used with date. Defaults to None.
            end_date (Optional[IsoDateConvertible], optional): The end of the date range, when used with start_date. Defaults to None or Today if start_date set.
            count (Optional[int], optional): If this is specified then count randomly chosen images will be returned. Cannot be used with date or start_date and end_date. Defaults to None.
            thumbs (bool, optional): Return the URL of video thumbnail. If an APOD is not a video, this parameter is ignored. Defaults to False.

        Returns:
            JSONType: Response body structure
            {
                "date": "YYYY-mm-dd",
                "explanation": "",
                "hdurl": "https://apod.nasa.gov/apod/image/{image_id}/{filename}.{format}",
                "media_type": "image",
                "service_version": "v1",
                "title": "",
                "url": "https://apod.nasa.gov/apod/image/{image_id}/{filename}.{format}"
            }
        """
        iso_date: Optional[Text] = IsoDate(date).value()
        iso_start_date: Optional[Text] = IsoDate(start_date).value()
        iso_end_date: Optional[Text] = IsoDate(end_date).value()
        if iso_date is not None:
            if iso_start_date is not None or iso_end_date is not None:
                message: Text = u"start_date or end_date shouldn't be filled when the date is filled. Set them to None"
                warnings.warn(message, UserWarning)
                iso_start_date, iso_end_date = None, None
            if count is not None:
                message: Text = u"count shouldn't be filled when the date is filled. Set it to None"
                warnings.warn(message, UserWarning)
                count = None
        if (iso_start_date is None or iso_end_date is None) and count is not None:
            message: Text = u"count shouldn't be filled when the start_date or end_date are filled. Set it to None"
            warnings.warn(message, UserWarning)
            count = None

        path: Text = "/planetary/apod"
        params: Dict[Text, Union[Text, int]] = {
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
    ) -> JSONType:
        """Near Earth Object Web Service

        Args:
            api_type (Text): Possible values are (feed, lookup, browse)
            start_date (Optional[IsoDateConvertible], optional): Starting date for asteroid search. Defaults to None.
            end_date (Optional[IsoDateConvertible], optional): Ending date for asteroid search. Defaults to None.
            asteroid_id (Optional[int], optional): Asteroid SPK-ID correlates to the NASA JPL small body. Defaults to None.

        Raises:
            InvalidNeoAPIType: [description]

        Returns:
            JSONType: [description]
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
        path: Text = f"{base_path}{type_path.get(api_type)}"
        iso_start_date: Optional[Text] = IsoDate(start_date).value()
        iso_end_date: Optional[Text] = IsoDate(end_date).value()
        params: Dict[Text, Union[Text, int, None]] = {
            "start_date": iso_start_date,
            "end_date": iso_end_date,
            "asteroid_id": asteroid_id,
        }
        return self._get(path, params)

    def donki(
        self,
        api_type: Text,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
        most_accurate_only: bool = True,
        speed: Optional[int] = None,
        half_angle: Optional[int] = None,
        catalog: Optional[Text] = None,
        notification_type: Optional[Text] = None,
    ) -> JSONType:
        """[summary]

        Args:
            api_type (Text): [description]
            start_date (Optional[IsoDateConvertible], optional): [description]. Defaults to None.
            end_date (Optional[IsoDateConvertible], optional): [description]. Defaults to None.
            most_accurate_only (bool, optional): [description]. Defaults to True.
            speed (Optional[int], optional): [description]. Defaults to None.
            half_angle (Optional[int], optional): [description]. Defaults to None.
            catalog (Optional[Text], optional): [description]. Defaults to None.
            notification_type (Optional[Text], optional): [description]. Defaults to None.

        Raises:
            InvalidDonkiAPIType: [description]

        Returns:
            JSONType: [description]
        """
        api_types: Set[Text] = {
            "CME",
            "CMEAnalysis",
            "GST",
            "IPS",
            "FLR",
            "SEP",
            "MPC",
            "RBE",
            "HSS",
            "WSAEnlilSimulations",
            "notifications",
        }
        if api_type not in api_types:
            message: Text = f"Invalid api_type {api_type}. Valid api_type values are {tuple(api_types)}"
            raise InvalidDonkiAPIType(message)
        if api_type is not "CMEAnalysis":
            most_accurate_only = None
            speed = None
            half_angle = None
            catalog = None
        if api_type is not "notifications":
            notification_type = None
        path: Text = f"/DONKI/{api_type}"
        params: Dict[Text, Union[Text, bool, int, None]] = {
            "start_date": start_date,
            "end_date": end_date,
            "mostAccurateOnly": most_accurate_only,
            "speed": speed,
            "halfAngle": half_angle,
            "catalog": catalog,
            "type": notification_type,
        }
        return self._get(path, params)

    def earth(
        self,
        api_type: Text,
        lat: float,
        lon: float,
        dim: Optional[float] = None,
        date: IsoDateConvertible = None,
        cloud_score: Optional[bool] = False,
    ):
        """[summary]

        Args:
            api_type (Text): [description]
            lat (float): [description]
            lon (float): [description]
            dim (Optional[float], optional): [description]. Defaults to None.
            date (IsoDateConvertible, optional): [description]. Defaults to None.
            cloud_score (Optional[bool], optional): [description]. Defaults to False.

        Raises:
            InvalidEarthAPIType: [description]

        Returns:
            [type]: [description]
        """
        api_types: Set[Text] = {"imagery", "assets"}
        if api_type not in api_types:
            message: Text = f"Invalid api_type {api_type}. Valid api_type values are {tuple(api_types)}"
            raise InvalidEarthAPIType(message)
        if api_type is not "imagery":
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

    def epic(
        self,
        image_type: Text,
        date: Optional[IsoDateConvertible] = None,
        available: bool = False,
        get_images: bool = False,
    ) -> Union[JSONType, Dict[Text, Union[JSONType, ImageFile]]]:
        """[summary]

        Args:
            image_type (Text): [description]
            date (Optional[IsoDateConvertible], optional): [description]. Defaults to None.
            available (bool, optional): [description]. Defaults to False.
            get_images (bool, optional): [description]. Defaults to False.

        Raises:
            InvalidEpicImageType: [description]

        Returns:
            Union[JSONType, Dict[Text, Union[JSONType, ImageFile]]]: [description]
        """
        image_types: Set[Text] = {"natural", "enhanced"}
        iso_date: Optional[Text] = IsoDate(date).value()
        if available:
            iso_date = None
        if image_type not in image_types:
            message: Text = f"Invalid image_type {image_type}. Valid image_type values are {tuple(image_types)}"
            raise InvalidEpicImageType(message)
        base_path: Text = f"/EPIC/api/{image_type}"
        if iso_date is None:
            path: Text = f"{base_path}/available"
        else:
            path: Text = f"{base_path}/date/{iso_date}"
        response: JSONType = self._get(path)
        if get_images:
            images: List[ImageFile] = [
                self._get(
                    "/".join(
                        [
                            "",
                            "EPIC",
                            "archive",
                            image_type,
                            record["date"][:10].replace("-", "/"),
                            "png",
                            record["image"],
                            ".png",
                        ]
                    )
                )
                for record in response
            ]
            return {"JSON": response, "Images": images}
        else:
            return response

    def insight(
        self, version: float = 1.0, feedtype: Text = "json"
    ) -> JSONType:
        """[summary]

        Args:
            version (float, optional): [description]. Defaults to 1.0.
            feedtype (Text, optional): [description]. Defaults to "json".

        Returns:
            JSONType: [description]
        """
        path: Text = "/insight_weather"
        params: Dict[Text, Union[float, Text]] = {
            "version": version,
            "feedtype": feedtype,
        }
        return self._get(path, params)

    def mars_rover_photos(
        self,
        rover: Text,
        sol: Optional[int] = None,
        camera: Text = "all",
        page: int = 1,
        earth_date: Optional[IsoDateConvertible] = None,
        get_images: bool = False,
    ) -> Union[JSONType, Dict[Text, Union[JSONType, ImageFile]]]:
        """[summary]

        Args:
            rover (Text): [description]
            sol (Optional[int], optional): [description]. Defaults to None.
            camera (Text, optional): [description]. Defaults to "all".
            page (int, optional): [description]. Defaults to 1.
            earth_date (Optional[IsoDateConvertible], optional): [description]. Defaults to None.
            get_images (bool, optional): [description]. Defaults to False.

        Raises:
            InvalidMarsRover: [description]
            InvalidMarsCamera: [description]
            InvalidMarsRoverCamera: [description]

        Returns:
            Union[JSONType, Dict[Text, Union[JSONType, ImageFile]]]: [description]
        """
        rovers: Set[Text] = {"curiousity", "opportunity", "spirit"}
        cameras: Set[Text] = {
            "FHAZ",
            "RHAZ",
            "MAST",
            "CHEMCAM",
            "MAHLI",
            "MARDI",
            "NAVCAM",
            "PANCAM",
            "MINITES",
            "all",
        }
        rover_cameras: Set[Tuple] = {
            ("curiousity", "FHAZ"),
            ("curiousity", "RHAZ"),
            ("curiousity", "MAST"),
            ("curiousity", "CHEMCAM"),
            ("curiousity", "MAHLI"),
            ("curiousity", "MARDI"),
            ("curiousity", "NAVCAM"),
            ("curiousity", "PANCAM"),
            ("opportunity", "FHAZ"),
            ("opportunity", "RHAZ"),
            ("opportunity", "NAVCAM"),
            ("opportunity", "PANCAM"),
            ("opportunity", "MINITES"),
            ("spirit", "FHAZ"),
            ("spirit", "RHAZ"),
            ("spirit", "NAVCAM"),
            ("spirit", "PANCAM"),
            ("spirit", "MINITES"),
        }
        if rover not in rovers:
            message: Text = (
                f"Invalid rover {rover}. Valid rover values are {tuple(rovers)}"
            )
            raise InvalidMarsRover(message)
        if camera not in cameras:
            message: Text = f"Invalid camera {camera}. Valid rover values are {tuple(cameras)}"
            raise InvalidMarsCamera(message)
        if (rover, camera) not in rover_cameras:
            message: Text = f"Invalid rover and camera combination {(rover, camera)}. Valid rover camera combinations are {tuple(rover_cameras)}"
            raise InvalidMarsRoverCamera(message)
        iso_earth_date: Optional[Text] = IsoDate(earth_date).value()
        if iso_earth_date is not None:
            sol = None
        path: Text = f"/mars-photos/api/v1/rovers/{rover}/photos"
        params: Dict[Text, Union[int, Text, None]] = {
            "sol": sol,
            "camera": camera,
            "page": page,
            "earth_date": earth_date,
        }
        response: JSONType = self._get(path, params)
        if get_images:
            images: List[ImageFile] = [
                Image.open(
                    BytesIO(requests.get(record.get("img_src")).content)
                )
                for record in response.get("photos")
            ]
            return {"JSON": response, "Images": images}
        else:
            return response

    def tech_transfer(self, api_type: Text, keyword: Text = "") -> JSONType:
        """[summary]

        Args:
            api_type (Text): [description]
            keyword (Text, optional): [description]. Defaults to "".

        Raises:
            InvalidMarsRover: [description]

        Returns:
            JSONType: [description]
        """
        api_types: Set[Text] = {
            "patent",
            "patent_issued",
            "software",
            "Spinoff",
        }
        if api_type not in api_types:
            message: Text = f"Invalid api_type {api_type}. Valid api_type values are {tuple(api_type)}"
            raise InvalidMarsRover(message)
        path: Text = f"/techtransfer/{api_type}/{keyword}"
        return self._get(path)

    def techport(
        self,
        id_parameter: Optional[int] = None,
        updated_since: IsoDateConvertible = None,
    ) -> JSONType:
        """[summary]

        Args:
            id_parameter (Optional[int], optional): [description]. Defaults to None.
            updated_since (IsoDateConvertible, optional): [description]. Defaults to None.

        Returns:
            JSONType: [description]
        """
        if id_parameter is None:
            str_id_parameter: Text = ""
        else:
            str_id_parameter: Text = str(id_parameter)
        iso_updated_since: Text = IsoDate(updated_since).value()
        path: Text = f"/techport/api/projects/{str_id_parameter}"
        params: Dict[Text, Text] = {"updatedSince": iso_updated_since}
        return self._get(path, params)

    def _get(
        self, path: Text, params: Dict = dict()
    ) -> Union[JSONType, ImageFile]:
        """[summary]

        Args:
            path (Text): [description]
            params (Dict, optional): [description]. Defaults to dict().

        Returns:
            Union[JSONType, ImageFile]: [description]
        """
        url: Text = f"{self.BASE_URL}{path}"
        response: Response = requests.get(
            url, params, auth=NASAAuth(self.__api_key)
        )
        return self._response_handler(response)

    def _response_handler(
        self, response: Response
    ) -> Union[JSONType, ImageFile]:
        """[summary]

        Args:
            response (Response): [description]

        Raises:
            NASAHTTPError: [description]

        Returns:
            Union[JSONType, ImageFile]: [description]
        """
        try:
            response.raise_for_status()
        except HTTPError as error:
            raise NASAHTTPError(error.strerror)
        content_type: Text = response.headers.get("Content-Type")
        if content_type == "application/json":
            content: JSONType = response.json()
        elif content_type.split("/")[0] == "image":
            content: ImageFile = Image.open(BytesIO(response.content))
        else:
            content: Text = response.text
        return content
