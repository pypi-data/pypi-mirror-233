#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#

from simple_salesforce import Salesforce, SalesforceLogin
from typing import Any
from pydantic import ValidationError
from unskript.connectors.schema.salesforce import SalesforceSchema
from unskript.connectors.interface import ConnectorInterface


class SalesforceConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            salesforceCredential = SalesforceSchema(**data)
        except ValidationError as e:
            raise e
        session_id, instance = SalesforceLogin(username=salesforceCredential.Username,
                                               password=salesforceCredential.Password.get_secret_value(),
                                               security_token=salesforceCredential.Security_Token)
        sf = Salesforce(instance=instance, session_id=session_id)

        return sf
