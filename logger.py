import json
import os
import threading

import requests
from requests import Response

API_VERSION = 'v1'
LOGGER_ENDPOINT = os.environ.get('LAMA_LOGGER_ENDPOINT', 'https://lama-logger.herokuapp.com')


class LamaLogger:
    endpoint = LOGGER_ENDPOINT
    api = f'{LOGGER_ENDPOINT}/api/{API_VERSION}'

    def __init__(self, token, project_id):
        self._token = token
        self.project_id = project_id

    def __call__(self, response: Response):
        thread = threading.Thread(target=self.__send_logs, args=(response,))
        thread.start()

    @property
    def __headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Token {self._token}'
        }

    @staticmethod
    def __to_payload(response: Response) -> dict:
        try:
            response_body = response.json()
        except json.decoder.JSONDecodeError:
            response_body = response.content.decode('utf-8')

        return {
            'request_id': response.request_id,
            'method': response.request.method,
            'request_url': response.request.url,
            'request_headers': dict(response.request.headers),
            'request_body': response.request.body,
            'response_code': response.status_code,
            'response_body': json.dumps(response_body),
            'response_headers': dict(response.headers),
        }

    def __send_logs(self, response: Response):
        payload = self.__to_payload(response)
        requests.post(
            self.api + f'/projects/{self.project_id}/requests/',
            data=json.dumps(payload),
            headers=self.__headers
        )
