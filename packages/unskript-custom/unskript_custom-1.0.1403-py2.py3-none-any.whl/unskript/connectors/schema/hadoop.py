##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr


class HadoopEmrSchema(BaseModel):
    base_url: str = Field(
        title='Base URL',
        description='Base URL of Hadoop server')
    username: str = Field(
        default='',
        title='Username',
        description='Username for Basic Authentication'
    )
    password: SecretStr = Field(
        default='',
        title='Password',
        description='Password for the Given User for Basic Auth'
    )
