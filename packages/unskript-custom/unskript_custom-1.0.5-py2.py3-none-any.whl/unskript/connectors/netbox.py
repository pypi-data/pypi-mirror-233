##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Any
import pynetbox
from pydantic import ValidationError

from unskript.connectors.interface import ConnectorInterface
from unskript.connectors.schema.netbox import NetboxSchema


class NetboxConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            netboxCredential = NetboxSchema(**data)
        except ValidationError as e:
            raise e
        try:
            if netboxCredential.threading:
                # For Threading
                netboxClient = pynetbox.api(netboxCredential.host, threading=netboxCredential.threading)
            elif netboxCredential.token!='':
                # For Token (Write operation)
                netboxClient = pynetbox.api(netboxCredential.host, token=netboxCredential.token.get_secret_value())
            else:
                # For Read Only
                netboxClient = pynetbox.api(netboxCredential.host)
        except Exception as e:
            raise e

        return netboxClient
