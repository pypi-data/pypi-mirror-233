##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any
from pydantic import ValidationError
import requests
from requests.sessions import Session

from unskript.connectors.schema.grafana import GrafanaSchema
from unskript.connectors.interface import ConnectorInterface

class Grafana(object):
    def __init__(self, session: Session, host: str):
        self.session = session
        self.host = host


class GrafanaConnector(ConnectorInterface):
    def get_handle(self, data)->Grafana:
        try:
            grafanaCredential = GrafanaSchema(**data)
        except ValidationError as e:
            raise e

        session = requests.Session()
        session.headers = {"Authorization": "Bearer " + grafanaCredential.api_key}
        return Grafana(session,grafanaCredential.host)