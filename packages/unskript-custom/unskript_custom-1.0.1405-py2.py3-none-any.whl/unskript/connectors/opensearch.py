##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any
from opensearchpy import OpenSearch
from pydantic import ValidationError

from unskript.connectors.schema.opensearch import OpenSearchSchema
from unskript.connectors.interface import ConnectorInterface

class OpenSearchConnector(ConnectorInterface):
    def get_handle(self, data)->Any:
        try:
            osCredential = OpenSearchSchema(**data)
        except ValidationError as e:
            raise e

        host = {'host': osCredential.host, 'port': osCredential.port}

        if not osCredential.username.__eq__(""):
            http_auth = (osCredential.username, osCredential.password.get_secret_value())

            osHandle = OpenSearch(hosts=[host],
                                     http_auth=http_auth,
                                     use_ssl=osCredential.use_ssl)
        else:
            osHandle = OpenSearch(hosts=[host], use_ssl=osCredential.use_ssl)
        return osHandle



