##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any
from pydantic import ValidationError

from jira import JIRA, JIRAError


from unskript.connectors.schema.jira import JiraSchema
from unskript.connectors.interface import ConnectorInterface

class JiraConnector(ConnectorInterface):
    def get_handle(self, data) -> JIRA:
        try:
            jiraCredential = JiraSchema(**data)

        except ValidationError as e:
            raise e

        try:
            auth_jira = JIRA(basic_auth=(jiraCredential.email, jiraCredential.api_token.get_secret_value()),
                options={"server":jiraCredential.url})

        except JIRAError as e:
            errString = 'Not able to connect to Jira, error {}, code {}'.format(e.text, e.status_code)
            print(errString)
            raise Exception(errString)
        return auth_jira
