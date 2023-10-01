#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#

from pydantic import BaseModel, Field, SecretStr
from typing import Optional

class RESTSchema(BaseModel):
    base_url: str = Field(
        title='Base URL',
        description='Base URL of REST server')
    username: str = Field(
        '',
        title='Username',
        description='Username for Basic Authentication'
    )
    password: SecretStr = Field(
        '',
        title='Password',
        description='Password for the Given User for Basic Auth'
    )
    headers: Optional[dict] = Field(
        title='Headers',
        description='''
            A dictionary of http headers to be used to communicate with the host.
            Example: {“Authorization”: “bearer my_oauth_token_to_the_host”}
            These headers will be included in all requests.
        '''
    )
