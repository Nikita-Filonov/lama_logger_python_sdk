import json
import threading

import requests
from requests import Response

API_VERSION = 'v1'


class LamaLogger:
    api = f'https://lama-logger.herokuapp.com/api/{API_VERSION}'

    def __init__(self, token, project_id):
        self._token = token
        self._project_id = project_id

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
            response_body = str(response.content)

        return {
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
            self.api + f'/projects/{self._project_id}/requests/',
            data=json.dumps(payload),
            headers=self.__headers
        )
