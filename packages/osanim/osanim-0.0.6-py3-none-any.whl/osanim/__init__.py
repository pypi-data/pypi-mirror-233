from .xone import *
from .schoolz import *
# import xone
# import schoolz

import requests

class _BaseAPI:
    _base_url = 'api.osanim.com'
    _uri = ''
   
    def __init__(self, token: str):
        self._token = token

    def _api_call(self, method='GET', payload=None, headers: dict = None) -> dict:
        """
        Calls Endpoint with appropriate payload
        :param method:
        :param payload:
        :return:
        """
        response: dict = {}

        try:
            endpoint = f'{self._base_url}/{self._uri}'
            if headers is not None:
                headers['Content-Type'] = 'application/json'
                headers['Authorization'] = f'Bearer {self._token}'

            req = requests.request(url=endpoint, method=method, json=payload, headers=headers)
            req.text
            if req.ok:
                try:
                    response = req.json()
                except requests.exceptions.JSONDecodeError:
                    response = {'status': True}
            else:
                response = req.json()

        except requests.exceptions.ConnectionError:
            response['status'] = "Server Error"
            response['message'] = "Network Problem: Unable to reach server"

        except requests.exceptions.Timeout:
            response['status'] = "Server Error"
            response['message'] = "Request Timeout"

        except requests.exceptions.RequestException as e:

            response['status'] = "System Error"
            response['message'] = e

        return response



