# -*- coding: utf-8 -*-
from __future__ import absolute_import

import requests


class Api(object):

    def __init__(self, host, api_token):
        self.base_url = host + "/api/rest"
        self.headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': api_token
        }
        self.validate_api = self.validate(self.base_url, self.headers)

    def validate(self, base_url, headers):
        try:
            resource = '/projects'
            response = requests.request("GET", base_url + resource,
                                        headers=headers,
                                        json={},
                                        params={}
                                        )
            response.raise_for_status()
            return response.status_code
        except Exception as e:
            print(f'Client hit an exception, {str(e)}')
            raise e


    def send(self, method, resource, resource_id=None, data=None, params=None):
        if data is None:
            data = {}
        if params is None:
            params = {}
        if resource_id is not None:
            resource = "%s/%s" % (resource, resource_id)
        response = requests.request(method, self.base_url + resource,
                                    headers=self.headers,
                                    json=data,
                                    params=params
                                    )
        if response.status_code != 200:
            return response.reason
        else:
            return response.json()
