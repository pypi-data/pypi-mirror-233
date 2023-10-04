##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from datadog import initialize, api

from unskript.connectors.schema.datadog import DatadogSchema
from unskript.connectors.interface import ConnectorInterface
from datadog_api_client import ApiClient
from datadog_api_client import Configuration
from datadog_api_client.v1.api.authentication_api import AuthenticationApi

PROTOCOL = "https://"

class DatadogConnector(ConnectorInterface):
    def get_handle(self, data) -> api:
        try:
            datadogCredential = DatadogSchema(**data)

            api_key = datadogCredential.api_key.get_secret_value()
            app_key = datadogCredential.app_key.get_secret_value()
            api_host = datadogCredential.api_host

            # initialize sets keys as a global variables
            initialize(api_key=api_key,
                       app_key=app_key,
                       api_host=PROTOCOL+api_host)

            api.handle_v2 = self.get_handle_v2(api_key, app_key, api_host)
        except Exception as e:
            raise e
        return api

    def get_handle_v2(self, api_key, app_key, api_host) -> Configuration:
        '''

        '''
        # Configure the api_key, app_key, and the site to use. The list of valid sites are:
        # ['datadoghq.com', 'us3.datadoghq.com', 'us5.datadoghq.com', 'datadoghq.eu', 'ddog-gov.com']
        configuration = Configuration()
        configuration.api_key["apiKeyAuth"] = api_key
        configuration.api_key["appKeyAuth"] = app_key
        configuration.server_variables["site"] = api_host
        with ApiClient(configuration) as api_client:
            api_instance = AuthenticationApi(api_client)
            api_instance.validate()
        return configuration
