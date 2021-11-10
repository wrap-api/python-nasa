from typing import Dict, List, Optional, Set, Text, Tuple, Union

from PIL.ImageFile import ImageFile
from nasa.clients.base import BaseClient
from nasa.exceptions import (
    InvalidMarsCamera,
    InvalidMarsRover,
    InvalidMarsRoverCamera,
)
from nasa.typing import IsoDate, IsoDateConvertible, JSONType
from nasa.utils import get_urls_images


class MarsRoverPhotosClient(BaseClient):
    def mars_rover_photos(
        self,
        rover: Text,
        sol: Optional[int] = None,
        camera: Text = "all",
        page: int = 1,
        earth_date: Optional[IsoDateConvertible] = None,
        get_images: bool = False,
    ) -> Union[JSONType, Dict[Text, Union[JSONType, ImageFile]]]:
        """This API is designed to collect image data gathered by NASA's Curiosity, Opportunity, and Spirit rovers on Mars and make it more easily available to other developers, educators, and citizen scientists.

        Args:
            rover (Text): Rover Name, currently supports "curiousity", "opportunity", "spirit"
            sol (Optional[int], optional): sol (ranges from 0 to max found in endpoint). Defaults to None.
            camera (Text, optional): camera name abbreviation. Defaults to "all".
            page (int, optional): 25 items per page returned. Defaults to 1.
            earth_date (Optional[IsoDateConvertible], optional): corresponding date on earth for the given sol. Defaults to None.
            get_images (bool, optional): Whether to get images or not. Defaults to False.

        Raises:
            InvalidMarsRover: Raised when Mars Rover input is invalid
            InvalidMarsCamera: Raised when Mars Cameta input is invalid
            InvalidMarsRoverCamera: Raised when the combination of Mars Rover and Camera is invalid

        Returns:
            Union[JSONType, Dict[Text, Union[JSONType, ImageFile]]]: Only JSON if get_images is False else will includes the images
        """
        rovers: Set[Text] = {"curiousity", "opportunity", "spirit"}
        cameras: Set[Text] = {
            "FHAZ",  # Front Hazard Avoidance Camera
            "RHAZ",  # Rear Hazard Avoidance Camera
            "MAST",  # Mast Camera
            "CHEMCAM",  # Chemistry and Camera Complex
            "MAHLI",  # Mars Hand Lens Imager
            "MARDI",  # Mars Descent Imager
            "NAVCAM",  # Navigation Camera
            "PANCAM",  # Panoramic Camera
            "MINITES",  # Miniature Thermal Emission Spectrometer (Mini-TES)
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
            message: Text = (
                f"Invalid camera {camera}. Valid rover values are {tuple(cameras)}"
            )
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
            images: List[ImageFile] = get_urls_images(
                [record.get("img_src") for record in response.get("photos")]
            )
            return {"JSON": response, "Images": images}
        else:
            return response

    def mars_rover_photos_all_pages(
        self,
        rover: Text,
        sol: Optional[int] = None,
        camera: Text = "all",
        earth_date: Optional[IsoDateConvertible] = None,
        get_images: bool = False,
    ) -> Union[JSONType, Dict[Text, Union[JSONType, ImageFile]]]:
        """Get all pages from Mars Rover Photos API

        Args:
            rover (Text): Rover Name, currently supports "curiousity", "opportunity", "spirit"
            sol (Optional[int], optional): sol (ranges from 0 to max found in endpoint). Defaults to None.
            camera (Text, optional): camera name abbreviation. Defaults to "all".
            earth_date (Optional[IsoDateConvertible], optional): corresponding date on earth for the given sol. Defaults to None.
            get_images (bool, optional): Whether to get images or not. Defaults to False.

        Returns:
            Union[JSONType, Dict[Text, Union[JSONType, ImageFile]]]: Only JSON if get_images is False else will includes the images
        """
        photos_list: List[JSONType] = list()
        images_list: List[ImageFile] = list()
        page: int = 1
        while True:
            response: Union[
                JSONType, Dict[Text, Union[JSONType, ImageFile]]
            ] = self.mars_rover_photos(
                rover=rover,
                sol=sol,
                camera=camera,
                page=page,
                earth_date=earth_date,
                get_images=get_images,
            )
            photos: JSONType = (
                response["JSON"]["photos"] if get_images else response["photos"]
            )
            if bool(photos):
                break
            else:
                photos_list.extend(photos)
            if get_images:
                images_list.extend(response["Image"])
            page += 1
        if get_images:
            return {"JSON": {"photos": photos_list}, "Image": images_list}
        else:
            return {"photos": photos_list}
