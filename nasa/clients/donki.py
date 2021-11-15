from typing import Dict, Optional, Set, Text, Union
from warnings import warn
from nasa.clients.base import BaseClient
from nasa.exceptions import NASAInvalidInput
from nasa.typing import IsoDate, IsoDateConvertible, JSONType
from nasa.warnings import AttributesCollussionWarning


class DonkiClient(BaseClient):
    def donki(
        self,
        api_type: Text,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
        most_accurate_only: Optional[bool] = None,
        speed: Optional[int] = None,
        half_angle: Optional[int] = None,
        catalog: Optional[Text] = None,
        notification_type: Optional[Text] = None,
    ) -> JSONType:
        """The Space Weather Database Of Notifications, Knowledge, Information

        Args:
            api_type (Text): API Type to hit
            start_date (Optional[IsoDateConvertible] = None, optional): Start date of data retrieved. Defaults to None.
            end_date (Optional[IsoDateConvertible] = None, optional): End date of data retrieved. Defaults to None.
            most_accurate_only (bool, optional): CMEAnalysis API only. If False, it'll query all, if True will query the most accurate only. Defaults to True.
            speed (Optional[int], optional): CMEAnalysis API only. Query the speed value. Defaults to None.
            half_angle (Optional[int], optional): CMEAnalysis API only. Query the half angle. Defaults to None.
            catalog (Optional[Text], optional): CMEAnalysis API only. Query the catalog. Defaults to None.
            notification_type (Optional[Text], optional): notifications API only. Defaults to None.

        Raises:
            NASAInvalidInput: Raises when the API Type given is invalid
            NASAInvalidInput: Raises when the Notification Type given is invalid

        Returns:
            JSONType: Parsed response body from the API
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
        notification_types: Set[Text] = {
            "all",
            "FLR",
            "SEP",
            "CME",
            "IPS",
            "MPC",
            "GST",
            "RBE",
            "report",
        }
        if api_type not in api_types:
            message: Text = f"Invalid api_type {api_type}. Valid api_type values are {tuple(api_types)}"
            raise NASAInvalidInput(message)
        if api_type != "CMEAnalysis" and (
            most_accurate_only is not None
            or speed is not None
            or half_angle is not None
            or catalog is not None
        ):
            message: Text = "CMEAnalysis query parameters shouldn't be filled when the api_type is not CMEAnalysis. Set them to None"
            warn(message, AttributesCollussionWarning)
            most_accurate_only = None
            speed = None
            half_angle = None
            catalog = None
        if api_type != "notifications" and notification_type is not None:
            message: Text = "notification_type shouldn't be filled when the api_type is not notifications. Set it to None"
            warn(message, AttributesCollussionWarning)
            notification_type = None
        if (
            notification_type is not None
            and notification_type not in notification_types
        ):
            message: Text = f"Invalid notification_type value {notification_type}. Valid notification_type values are {tuple(notification_types)}"
            raise NASAInvalidInput(message)
        iso_start_date: Text = IsoDate(start_date).value()
        iso_end_date: Text = IsoDate(end_date).value()
        path: Text = f"/DONKI/{api_type}"
        params: Dict[Text, Union[Text, bool, int, None]] = {
            "startDate": iso_start_date,
            "endDate": iso_end_date,
            "mostAccurateOnly": most_accurate_only,
            "speed": speed,
            "halfAngle": half_angle,
            "catalog": catalog,
            "type": notification_type,
        }
        return self._get(path, params)

    def donki_cme(
        self,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
    ) -> JSONType:
        """The Space Weather Database Of Notifications, Knowledge, Information. Coronal Mass Ejection API

        Args:
            start_date (Optional[IsoDateConvertible] = None, optional): Start date of data retrieved. Defaults to None.
            end_date (Optional[IsoDateConvertible] = None, optional): End date of data retrieved. Defaults to None.

        Returns:
            JSONType: Parsed response body from the API
        """
        return self.donki(api_type="CME", start_date=start_date, end_date=end_date)

    def donki_cme_analysis(
        self,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
        most_accurate_only: bool = True,
        speed: Optional[int] = None,
        half_angle: Optional[int] = None,
        catalog: Optional[Text] = None,
    ) -> JSONType:
        """The Space Weather Database Of Notifications, Knowledge, Information. Coronal Mass Ejection Analysis API

        Args:
            start_date (Optional[IsoDateConvertible] = None, optional): Start date of data retrieved. Defaults to None.
            end_date (Optional[IsoDateConvertible] = None, optional): End date of data retrieved. Defaults to None.
            most_accurate_only (bool, optional): If False, it'll query all, if True will query the most accurate only. Defaults to True.
            speed (Optional[int], optional): Query the speed value. Defaults to None.
            half_angle (Optional[int], optional): Query the half angle. Defaults to None.
            catalog (Optional[Text], optional): Query the catalog. Defaults to None.

        Returns:
            JSONType: Parsed response body from the API
        """
        return self.donki(
            api_type="CMEAnalysis",
            start_date=start_date,
            end_date=end_date,
            most_accurate_only=most_accurate_only,
            speed=speed,
            half_angle=half_angle,
            catalog=catalog,
        )

    def donki_gst(
        self,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
    ) -> JSONType:
        """The Space Weather Database Of Notifications, Knowledge, Information. Geomagnetic Storm API

        Args:
            start_date (Optional[IsoDateConvertible] = None, optional): Start date of data retrieved. Defaults to None.
            end_date (Optional[IsoDateConvertible] = None, optional): End date of data retrieved. Defaults to None.

        Returns:
            JSONType: Parsed response body from the API
        """
        return self.donki(api_type="GST", start_date=start_date, end_date=end_date)

    def donki_ips(
        self,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
    ) -> JSONType:
        """The Space Weather Database Of Notifications, Knowledge, Information. Interplanetary Shock API

        Args:
            start_date (Optional[IsoDateConvertible] = None, optional): Start date of data retrieved. Defaults to None.
            end_date (Optional[IsoDateConvertible] = None, optional): End date of data retrieved. Defaults to None.

        Returns:
            JSONType: Parsed response body from the API
        """
        return self.donki(api_type="IPS", start_date=start_date, end_date=end_date)

    def donki_flr(
        self,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
    ) -> JSONType:
        """The Space Weather Database Of Notifications, Knowledge, Information. Solar Flare API

        Args:
            start_date (Optional[IsoDateConvertible] = None, optional): Start date of data retrieved. Defaults to None.
            end_date (Optional[IsoDateConvertible] = None, optional): End date of data retrieved. Defaults to None.

        Returns:
            JSONType: Parsed response body from the API
        """
        return self.donki(api_type="FLR", start_date=start_date, end_date=end_date)

    def donki_sep(
        self,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
    ) -> JSONType:
        """The Space Weather Database Of Notifications, Knowledge, Information. Solar Energetic Particle API

        Args:
            start_date (Optional[IsoDateConvertible] = None, optional): Start date of data retrieved. Defaults to None.
            end_date (Optional[IsoDateConvertible] = None, optional): End date of data retrieved. Defaults to None.

        Returns:
            JSONType: Parsed response body from the API
        """
        return self.donki(api_type="SEP", start_date=start_date, end_date=end_date)

    def donki_mpc(
        self,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
    ) -> JSONType:
        """The Space Weather Database Of Notifications, Knowledge, Information. Magnetopause Crossing API

        Args:
            start_date (Optional[IsoDateConvertible] = None, optional): Start date of data retrieved. Defaults to None.
            end_date (Optional[IsoDateConvertible] = None, optional): End date of data retrieved. Defaults to None.

        Returns:
            JSONType: Parsed response body from the API
        """
        return self.donki(api_type="MPC", start_date=start_date, end_date=end_date)

    def donki_rbe(
        self,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
    ) -> JSONType:
        """The Space Weather Database Of Notifications, Knowledge, Information. Radiation Belt Enhancement API

        Args:
            start_date (Optional[IsoDateConvertible] = None, optional): Start date of data retrieved. Defaults to None.
            end_date (Optional[IsoDateConvertible] = None, optional): End date of data retrieved. Defaults to None.

        Returns:
            JSONType: Parsed response body from the API
        """
        return self.donki(api_type="RBE", start_date=start_date, end_date=end_date)

    def donki_hss(
        self,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
    ) -> JSONType:
        """The Space Weather Database Of Notifications, Knowledge, Information. Hight Speed Stream API

        Args:
            start_date (Optional[IsoDateConvertible] = None, optional): Start date of data retrieved. Defaults to None.
            end_date (Optional[IsoDateConvertible] = None, optional): End date of data retrieved. Defaults to None.

        Returns:
            JSONType: Parsed response body from the API
        """
        return self.donki(api_type="HSS", start_date=start_date, end_date=end_date)

    def donki_wsa_enlil_simulations(
        self,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
    ) -> JSONType:
        """The Space Weather Database Of Notifications, Knowledge, Information. WSA+EnlilSimulation API

        Args:
            start_date (Optional[IsoDateConvertible] = None, optional): Start date of data retrieved. Defaults to None.
            end_date (Optional[IsoDateConvertible] = None, optional): End date of data retrieved. Defaults to None.

        Returns:
            JSONType: Parsed response body from the API
        """
        return self.donki(
            api_type="WSAEnlilSimulations", start_date=start_date, end_date=end_date
        )

    def donki_notifications(
        self,
        start_date: Optional[IsoDateConvertible] = None,
        end_date: Optional[IsoDateConvertible] = None,
        notification_type: Optional[Text] = None,
    ) -> JSONType:
        """The Space Weather Database Of Notifications, Knowledge, Information. Notifications API

        Args:
            start_date (Optional[IsoDateConvertible] = None, optional): Start date of data retrieved. Defaults to None.
            end_date (Optional[IsoDateConvertible] = None, optional): End date of data retrieved. Defaults to None.
            notification_type (Optional[Text], optional): Defaults to None.

        Returns:
            JSONType: Parsed response body from the API
        """
        return self.donki(
            api_type="notifications",
            start_date=start_date,
            end_date=end_date,
            notification_type=notification_type,
        )
