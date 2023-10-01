##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field
from enum import Enum, IntEnum
from typing import Optional
from pydantic import validator
from pydantic.types import UUID1

"""
    connector type inventory (should have been uuid instead of string?)
"""


class ConnectorEnum(str, Enum):
    aws = "CONNECTOR_TYPE_AWS"
    k8s = "CONNECTOR_TYPE_K8S"
    k8 = "CONNECTOR_TYPE_K8"
    gcp = "CONNECTOR_TYPE_GCP"
    slack = "CONNECTOR_TYPE_SLACK"
    posgresql = "CONNECTOR_TYPE_POSTGRESQL"
    mongodb = "CONNECTOR_TYPE_MONGODB"
    jenkins = "CONNECTOR_TYPE_JENKINS"
    mysql = "CONNECTOR_TYPE_MYSQL"
    jira = "CONNECTOR_TYPE_JIRA"
    rest = "CONNECTOR_TYPE_REST"
    elasticsearch = "CONNECTOR_TYPE_ELASTICSEARCH"
    kafka = "CONNECTOR_TYPE_KAFKA"
    grafana = "CONNECTOR_TYPE_GRAFANA"
    redis = "CONNECTOR_TYPE_REDIS"
    ssh = "CONNECTOR_TYPE_SSH"
    prometheus = "CONNECTOR_TYPE_PROMETHEUS"
    stripe = "CONNECTOR_TYPE_STRIPE"
    datadog = "CONNECTOR_TYPE_DATADOG"
    zabbix = "CONNECTOR_TYPE_ZABBIX"
    pingdom = "CONNECTOR_TYPE_PINGDOM"
    opensearch = "CONNECTOR_TYPE_OPENSEARCH"
    infra = "CONNECTOR_TYPE_INFRA"
    hadoop = "CONNECTOR_TYPE_HADOOP"
    airflow = "CONNECTOR_TYPE_AIRFLOW"
    mssql = "CONNECTOR_TYPE_MSSQL"
    splunk = "CONNECTOR_TYPE_SPLUNK"
    snowflake = "CONNECTOR_TYPE_SNOWFLAKE"
    salesforce = "CONNECTOR_TYPE_SALESFORCE"
    mantishub = "CONNECTOR_TYPE_MANTISHUB"
    azure = "CONNECTOR_TYPE_AZURE"
    github = "CONNECTOR_TYPE_GITHUB"
    nomad = "CONNECTOR_TYPE_NOMAD"
    netbox = "CONNECTOR_TYPE_NETBOX"
    chatgpt = "CONNECTOR_TYPE_CHATGPT"
    opsgenie = "CONNECTOR_TYPE_OPSGENIE"


"""
    per Action schema defined on the Action that describes credential requirements
    of the Action (needed, type...)

    this needs to be present in the metadata config of the Action
    front end will read this from the ActionMetadata (implemented as codeSnippetMd)
    and show the appropriate drop-down widget

    Note that in future this can be a list so that multiple credentials can also
    be supported
"""


class ActionCredentialSchema(BaseModel):
    credential_required: bool = Field(
        title="Does this Action need a credential",
        default=True
    )
    credential_type: ConnectorEnum = Field(
        title="Connector Type"
    )


"""
    per Task schema that defines that describes the credential value that is configured
    by the front end for the Task (known as credentialDict today)
"""


class TaskCredentialValueSchema(BaseModel):
    credential_name: Optional[str] = Field(
        title="Connector Name"
    )
    credential_type: Optional[ConnectorEnum] = Field(
        title="Connector Type"
    )
    credential_id: Optional[str] = Field(
        title="Connector ID"
    )
    credential_user_id: Optional[str] = Field(
        title="User ID"
    )
    credential_service_id: Optional[str] = Field(
        title="Service ID"
    )

    @validator("credential_service_id", always=True)
    def mutually_exclusive(cls, v, values):
        if values["credential_name"] is not None and v:
            raise ValueError("'credential_name' and 'credential_service_id' are mutually exclusive.")
        if values["credential_user_id"] is not None and v:
            raise ValueError("'credential_user_id' and 'credential_service_id' are mutually exclusive.")
        if values["credential_name"] is not None and values["credential_user_id"] is not None:
            raise ValueError("'credential_name' and 'credential_user_id' are mutually exclusive.")
        return v
