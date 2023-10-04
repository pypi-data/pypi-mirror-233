##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field
from typing import Optional


class ElasticSearchSchema(BaseModel):
    host: str = Field(
        title='Host URL',
        description='''
        Elasticsearch Node URL. For eg: https://localhost:9200.
        NOTE: Please ensure that this is the Elastisearch URL and NOT Kibana URL.
        ''')
    api_key: str = Field(
        '',
        title='API Key',
        description='API Key based authentication.'
    )
    verify_certs: Optional[bool] = Field(
        default=True,
        title='Verify certs',
        description='''
        Verify server ssl certs. This can be set to true when working with private certs.
        '''
    )