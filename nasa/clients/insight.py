from typing import Dict, Text, Union
from warnings import warn
from nasa.clients.base import BaseClient
from nasa.typing import JSONType
from nasa.warnings import UnsupportedInputWarning


class InsightClient(BaseClient):
    def insight(self, version: float = 1.0, feedtype: Text = "json") -> JSONType:
        """NASA’s InSight Mars lander takes continuous weather measurements (temperature, wind, pressure) on the surface of Mars at Elysium Planitia, a flat, smooth plain near Mars’ equator.

        Args:
            version (float, optional): The version of this API. Defaults to 1.0.
            feedtype (Text, optional): The format of what is returned. Currently the default is JSON and only JSON works. Defaults to "json".

        Returns:
            JSONType: JSON Response of the API
        """
        if feedtype != "json":
            message: Text = u"Currently only supports JSON. Set feedtype to JSON"
            warn(message, UnsupportedInputWarning)
            feedtype = "json"
        path: Text = "/insight_weather"
        params: Dict[Text, Union[float, Text]] = {
            "version": version,
            "feedtype": feedtype,
        }
        return self._get(path, params)
