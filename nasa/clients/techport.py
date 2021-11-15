from typing import Dict, Optional, Text
from nasa.clients.base import BaseClient
from nasa.typing import IsoDate, IsoDateConvertible, JSONType


class TechPortClient(BaseClient):
    def techport(
        self,
        id_parameter: Optional[int] = None,
        updated_since: IsoDateConvertible = None,
    ) -> JSONType:
        """Techport allows the public to discover the technologies NASA is working on every day to explore space, understand the universe, and improve aeronautics

        Args:
            id_parameter (Optional[int], optional): The id value of the TechPort record. ID values can be obtained through the standard TechPort search feature and are visible in the website URLs, e.g. http://techport.nasa.gov/view/0000, where 0000 is the ID value. Alternatively, a request to /api/projects will display all valid IDs in the system. Defaults to None.
            updated_since (IsoDateConvertible, optional): Latest updated date queried. Defaults to None.

        Returns:
            JSONType: JSON response from API
        """
        if id_parameter is None:
            str_id_parameter: Text = ""
        else:
            str_id_parameter: Text = str(id_parameter)
        iso_updated_since: Text = IsoDate(updated_since).value()
        path: Text = f"/techport/api/projects/{str_id_parameter}"
        params: Dict[Text, Text] = {"updatedSince": iso_updated_since}
        return self._get(path, params)
