##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr


class ZabbixSearchSchema(BaseModel):
    url: str = Field(
        title='URL',
        description='url of zabbix server')
    api_token: SecretStr = Field(
        '',
        title='API Token',
        description='API token based authentication.'
    )