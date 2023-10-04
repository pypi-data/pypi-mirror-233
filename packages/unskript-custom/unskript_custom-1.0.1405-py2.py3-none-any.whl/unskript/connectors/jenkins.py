##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any
import jenkinsapi
from jenkinsapi.jenkins import Jenkins
from pydantic import ValidationError

from unskript.connectors.schema.jenkins import JenkinsSchema
from unskript.connectors.interface import ConnectorInterface

class JenkinsConnector(ConnectorInterface):
    def get_handle(self, data)->Any:
        try:
            jenkinsCredential = JenkinsSchema(**data)
        except ValidationError as e:
            raise e

        try:
            server = Jenkins(jenkinsCredential.url,
            username=jenkinsCredential.user_name, password=jenkinsCredential.password.get_secret_value())


        except jenkinsapi.jenkins.JenkinsAPIException  as e:
            errString = 'Not able to connect to Jenkins, error {}'.format(e)
            print(errString)
            raise Exception(errString)
        return server