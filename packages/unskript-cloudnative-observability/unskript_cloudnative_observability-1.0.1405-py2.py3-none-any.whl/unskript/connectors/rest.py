#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#

# REST library import
import requests
import os

from typing import Any

from pydantic import ValidationError


from unskript.connectors.schema.rest import RESTSchema
from unskript.connectors.interface import ConnectorInterface

class RESTConnector(ConnectorInterface):
    def get_handle(self, data)->Any:
        try:
            RESTCredential = RESTSchema(**data)
        except ValidationError as e:
            raise e
        session = BaseUrlSession(base_url=RESTCredential.base_url)
        if RESTCredential.username != "":
            session.auth = (RESTCredential.username, RESTCredential.password.get_secret_value())

        if RESTCredential.headers:
            session.headers.update(RESTCredential.headers)
        return session


class BaseUrlSession(requests.Session):
    """
        A Session with a URL that all requests will use as a base.
    """

    base_url = None

    def __init__(self, base_url):
        if base_url and \
            (not base_url.startswith("http://")  and not base_url.startswith("https://")):
            print("URL needs to specify protocol http or https")
            raise Exception("URL needs to specify protocol http or https")
        self.base_url = base_url
        super(BaseUrlSession, self).__init__()

    def request(self, method, url, *args, **kwargs):
        """Send the request after generating the complete URL."""
        url = self.create_url(url)
        return super(BaseUrlSession, self).request(
            method, url, *args, **kwargs
        )

    def create_url(self, url):
        """Create the URL based off this partial path."""
        if not url:
            raise Exception("Invalid URL, specify the URL")

        return os.path.join(self.base_url, url.lstrip("/"))


