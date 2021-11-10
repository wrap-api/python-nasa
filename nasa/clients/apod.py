import warnings
from typing import Dict, Optional, Text, Union
from PIL.ImageFile import ImageFile

from nasa.clients.base import BaseClient
from nasa.typing import IsoDate, IsoDateConvertible, JSONType
from nasa.utils import get_url_image
from nasa.warnings import AttributesCollussionWarning


class ApodClient(BaseClient):
    def apod(
        self,
        date: Optional[IsoDateConvertible] = None,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
        count: Optional[int] = None,
        thumbs: bool = False,
        get_image: bool = False,
        get_hd_image: bool = False,
    ) -> JSONType:
        """Astronomy Picture of the Day https://github.com/nasa/apod-api

        Args:
            date (Optional[IsoDateConvertible], optional): The date of the APOD image to retrieve. Defaults to None.
            start_date (Optional[IsoDateConvertible], optional): The start of a date range, when requesting date for a range of dates. Cannot be used with date. Defaults to None.
            end_date (Optional[IsoDateConvertible], optional): The end of the date range, when used with start_date. Defaults to None or Today if start_date set.
            count (Optional[int], optional): If this is specified then count randomly chosen images will be returned. Cannot be used with date or start_date and end_date. Defaults to None.
            thumbs (bool, optional): Return the URL of video thumbnail. If an APOD is not a video, this parameter is ignored. Defaults to False.
            get_image (bool, optional): Return the Image alongside the response. Defaults to False.
            get_hd_image (bool, optional): Return the HD Image alongside the response. Defaults to False.

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
                message: Text = "start_date or end_date shouldn't be filled when the date is filled. Set them to None"
                warnings.warn(message, AttributesCollussionWarning)
                iso_start_date, iso_end_date = None, None
            if count is not None:
                message: Text = (
                    "count shouldn't be filled when the date is filled. Set it to None"
                )
                warnings.warn(message, AttributesCollussionWarning)
                count = None
        if (iso_start_date is None or iso_end_date is None) and count is not None:
            message: Text = "count shouldn't be filled when the start_date or end_date are filled. Set it to None"
            warnings.warn(message, AttributesCollussionWarning)
            count = None

        path: Text = "/planetary/apod"
        params: Dict[Text, Union[Text, int]] = {
            "date": iso_date,
            "start_date": iso_start_date,
            "end_date": iso_end_date,
            "count": count,
            "thumbs": thumbs,
        }
        response: JSONType = self._get(path, params)
        if get_image or get_hd_image:
            image_response: Dict[Text, Union[JSONType, Optional[ImageFile]]] = {
                "JSON": response
            }
            content_json: JSONType = response.json()
            if get_image:
                url: Text = content_json.get("url")
                image_response["image"] = get_url_image(url)
            if get_hd_image:
                hdurl: Text = content_json.get("hdurl")
                image_response["hd_image"] = get_url_image(hdurl)
            return image_response
        else:
            return response
