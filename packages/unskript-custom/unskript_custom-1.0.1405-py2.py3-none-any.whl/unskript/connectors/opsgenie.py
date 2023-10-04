##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Any
import opsgenie_sdk
from pydantic import ValidationError

from unskript.connectors.interface import ConnectorInterface
from unskript.connectors.schema.opsgenie import OpsgenieSchema


class OpsgenieConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            opsGenieCredential = OpsgenieSchema(**data)
        except ValidationError as e:
            raise e
        try:
            configuration = opsgenie_sdk.Configuration()
            configuration.api_key['Authorization'] = opsGenieCredential.api_token.get_secret_value()
            api_instance = opsgenie_sdk.AccountApi(opsgenie_sdk.ApiClient(configuration))
        except Exception as e:
            raise e

        return api_instance