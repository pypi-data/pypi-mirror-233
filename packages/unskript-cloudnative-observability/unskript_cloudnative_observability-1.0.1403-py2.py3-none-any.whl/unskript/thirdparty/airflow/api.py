# -*- coding: utf-8 -*-
from __future__ import absolute_import

import requests


class Api(object):

    def __init__(self, host, userName, Password, apiversion="v1"):
        self.base_url = host + "/api/" + apiversion
        self.headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        self.auth = (userName, Password) if userName and Password else None

    def send(self, method, resource, resource_id=None, data=None, params=None):
        if data is None:
            data = {}
        if params is None:
            params = {}
        if resource_id is not None:
            resource = "%s/%s" % (resource, resource_id)
        response = requests.request(method, self.base_url + resource,
                                    auth=self.auth,
                                    headers=self.headers,
                                    json=data,
                                    params=params
                                    )
        if response.status_code != 200:
            return response.text
        else:
            return response.json()
