##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

import json

from typing import Any
from pydantic import ValidationError
from google.oauth2 import service_account

from unskript.connectors.schema.gcp import GCPSchema
from unskript.connectors.interface import ConnectorInterface

class GCPConnector(ConnectorInterface):
    def get_handle(self, data)->Any:
        try:
            gcpCredential = GCPSchema(**data)
        except ValidationError as e:
            raise e
        gcpClient = service_account.Credentials.from_service_account_info(info=json.loads(gcpCredential.credentials))
        return gcpClient