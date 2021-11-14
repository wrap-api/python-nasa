from typing import Set, Text
from nasa.clients.base import BaseClient
from nasa.exceptions import NASAInvalidInput
from nasa.typing import JSONType


class TechTransferClient(BaseClient):
    def tech_transfer(self, api_type: Text, keyword: Text = "") -> JSONType:
        """This endpoint provides structured, searchable developer access to NASA’s patents, software, and technology spinoff descriptions that have been curated to support technology transfer.

        Args:
            api_type (Text): Type of API to be hit
            keyword (Text, optional): keyword to be highlighted. Defaults to "".

        Raises:
            NASAInvalidInput: Raises when the api_type provided is invalid

        Returns:
            JSONType: JSON object returned from the response
        """
        api_types: Set[Text] = {"patent", "patent_issued", "software", "Spinoff"}
        if api_type not in api_types:
            message: Text = f"Invalid api_type {api_type}. Valid api_type values are {tuple(api_type)}"
            raise NASAInvalidInput(message)
        path: Text = f"/techtransfer/{api_type}/{keyword}"
        return self._get(path)

    def tech_transfer_patent(self, keyword: Text = "") -> JSONType:
        """This endpoint provides structured, searchable developer access to NASA’s patents descriptions that have been curated to support technology transfer.

        Args:
            keyword (Text, optional): keyword to be highlighted. Defaults to "".

        Raises:
            NASAInvalidInput: Raises when the api_type provided is invalid

        Returns:
            JSONType: JSON object returned from the response
        """
        return self.tech_transfer(api_type="patent", keyword=keyword)

    def tech_transfer_patent_issued(self, keyword: Text = "") -> JSONType:
        """This endpoint provides structured, searchable developer access to NASA’s patents issued descriptions that have been curated to support technology transfer.

        Args:
            keyword (Text, optional): keyword to be highlighted. Defaults to "".

        Raises:
            NASAInvalidInput: Raises when the api_type provided is invalid

        Returns:
            JSONType: JSON object returned from the response
        """
        return self.tech_transfer(api_type="patent_issued", keyword=keyword)

    def tech_transfer_software(self, keyword: Text = "") -> JSONType:
        """This endpoint provides structured, searchable developer access to NASA’s software descriptions that have been curated to support technology transfer.

        Args:
            keyword (Text, optional): keyword to be highlighted. Defaults to "".

        Raises:
            NASAInvalidInput: Raises when the api_type provided is invalid

        Returns:
            JSONType: JSON object returned from the response
        """
        return self.tech_transfer(api_type="software", keyword=keyword)

    def tech_transfer_spinoff(self, keyword: Text = "") -> JSONType:
        """This endpoint provides structured, searchable developer access to NASA’s technology spinoff descriptions that have been curated to support technology transfer.

        Args:
            keyword (Text, optional): keyword to be highlighted. Defaults to "".

        Raises:
            NASAInvalidInput: Raises when the api_type provided is invalid

        Returns:
            JSONType: JSON object returned from the response
        """
        return self.tech_transfer(api_type="Spinoff", keyword=keyword)
