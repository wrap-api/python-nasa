from typing import Dict, List, Optional, Set, Text, Union
import warnings

from PIL.ImageFile import ImageFile
from nasa.clients.base import BaseClient
from nasa.exceptions import NASAInvalidInput
from nasa.typing import IsoDate, IsoDateConvertible, JSONType
from nasa.warnings import AttributesCollussionWarning


class EpicClient(BaseClient):
    def epic(
        self,
        image_type: Text,
        date: Optional[IsoDateConvertible] = None,
        available: bool = False,
        get_images: bool = False,
    ) -> Union[JSONType, Dict[Text, Union[JSONType, ImageFile]]]:
        """The EPIC API provides information on the daily imagery collected by Earth Polychromatic Imaging Camera (EPIC) instrument.

        Args:
            image_type (Text): Possible values are natural or enhanced
            date (Optional[IsoDateConvertible], optional): filter image available on specific date. Defaults to None.
            available (bool, optional): listing of all dates. Defaults to False.
            get_images (bool, optional): If true return the response with images handled using PIL. Defaults to False.

        Raises:
            NASAInvalidInput: raised when the image type is not valid

        Returns:
            Union[JSONType, Dict[Text, Union[JSONType, ImageFile]]]: If get_images is True then the output will be Dictionary of PIL Image file. Else the outpul will be JSON
        """
        image_types: Set[Text] = {"natural", "enhanced"}
        iso_date: Optional[Text] = IsoDate(date).value()
        if available and iso_date is not None:
            message: Text = "date shouldn't be filled when the available parameter is True. Set it to None"
            warnings.warn(message, AttributesCollussionWarning)
            iso_date = None
        if image_type not in image_types:
            message: Text = f"Invalid image_type {image_type}. Valid image_type values are {tuple(image_types)}"
            raise NASAInvalidInput(message)
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

    def epic_natural(
        self,
        date: Optional[IsoDateConvertible] = None,
        available: bool = False,
        get_images: bool = False,
    ) -> Union[JSONType, Dict[Text, Union[JSONType, ImageFile]]]:
        """The EPIC Natural API provides information on the daily imagery collected by Earth Polychromatic Imaging Camera (EPIC) instrument.

        Args:
            date (Optional[IsoDateConvertible], optional): filter image available on specific date. Defaults to None.
            available (bool, optional): listing of all dates. Defaults to False.
            get_images (bool, optional): If true return the response with images handled using PIL. Defaults to False.

        Raises:
            NASAInvalidInput: raised when the image type is not valid

        Returns:
            Union[JSONType, Dict[Text, Union[JSONType, ImageFile]]]: If get_images is True then the output will be Dictionary of PIL Image file. Else the outpul will be JSON
        """
        return self.epic(
            image_type="natural", date=date, available=available, get_images=get_images
        )

    def epic_enhanced(
        self,
        date: Optional[IsoDateConvertible] = None,
        available: bool = False,
        get_images: bool = False,
    ) -> Union[JSONType, Dict[Text, Union[JSONType, ImageFile]]]:
        """The EPIC Enhanced API provides information on the daily imagery collected by Earth Polychromatic Imaging Camera (EPIC) instrument.

        Args:
            date (Optional[IsoDateConvertible], optional): filter image available on specific date. Defaults to None.
            available (bool, optional): listing of all dates. Defaults to False.
            get_images (bool, optional): If true return the response with images handled using PIL. Defaults to False.

        Raises:
            NASAInvalidInput: raised when the image type is not valid

        Returns:
            Union[JSONType, Dict[Text, Union[JSONType, ImageFile]]]: If get_images is True then the output will be Dictionary of PIL Image file. Else the outpul will be JSON
        """
        return self.epic(
            image_type="enhanced", date=date, available=available, get_images=get_images
        )
