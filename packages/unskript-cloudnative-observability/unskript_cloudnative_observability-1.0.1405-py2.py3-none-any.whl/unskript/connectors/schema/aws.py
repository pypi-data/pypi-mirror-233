##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Union

from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Union
from typing_extensions import Literal

class AssumeRoleSchema(BaseModel):
    auth_type: Literal['Assume Role']
    role_arn: str = Field(
        title='Role ARN',
        description='ARN of the role to be assumed.')
    role_session_name: str = Field(
        title='Role Session Name',
        description='Unique identifier for the session when the above role is assumed.')
    external_id: SecretStr = Field(
        '',
        title='External ID',
        description='A unique identifier that might be required when you assume a role.')

    class Config:
        title = 'Assume Role'

class AccessKeySchema(BaseModel):
    auth_type: Literal['Access Key']
    access_key: str = Field(
        title='Access Key',
        description='Access Key to use for authentication.')
    secret_access_key: SecretStr = Field(
        title='Secret Access Key',
        description='Secret Access Key to use for authentication.'
    )

    class Config:
        title = 'Access Key'

class AWSSchema(BaseModel):
    authentication: Union[AccessKeySchema, AssumeRoleSchema] = Field(..., discriminator='auth_type')
