import json
import os
import threading
import uuid
from urllib import parse

import requests
from requests import Response

API_VERSION = 'v1'
LOGGER_ENDPOINT = os.environ.get('LAMA_LOGGER_ENDPOINT', 'https://lama-logger.herokuapp.com')


def parse_query_params(url: str) -> dict:
    return dict(parse.parse_qsl(parse.urlsplit(url).query))


class LamaLogger:
    endpoint = LOGGER_ENDPOINT
    api = f'{LOGGER_ENDPOINT}/api/{API_VERSION}'

    def __init__(self, token, project_id):
        self._token = token
        self.project_id = project_id

        self._node = None
        self._context_uuid = None

    def __call__(self, response: Response):
        self.__send_logs(response)

    @property
    def __headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Token {self._token}',
        }

    def __to_payload(self, response: Response) -> dict:
        try:
            response_body = response.json()
        except json.decoder.JSONDecodeError:
            response_body = response.content.decode('utf-8')

        return {
            'requestId': response.request_id,
            'method': response.request.method,
            'requestUrl': response.request.url,
            'requestHeaders': dict(response.request.headers),
            'requestBody': response.request.body,
            'statusCode': response.status_code,
            'responseBody': json.dumps(response_body),
            'responseHeaders': dict(response.headers),
            'duration': response.elapsed.total_seconds(),
            'queryParams': parse_query_params(response.request.url),
            'node': self._node,
            'nodeId': self._context_uuid
        }

    def __send(self, payload: dict):
        requests.post(
            self.api + f'/projects/{self.project_id}/requests/create/',
            data=json.dumps(payload),
            headers=self.__headers
        )

    def __send_logs(self, response: Response):
        payload = self.__to_payload(response)
        thread = threading.Thread(target=self.__send, args=(payload,))
        thread.start()

    def set_context(self, node: str = None):
        self._node = node
        self._context_uuid = str(uuid.uuid4())

    def drop_context(self):
        self._node = None
        self._context_uuid = None
