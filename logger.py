import json
import os
import threading
import uuid
from urllib import parse

import allure
from requests import Response, post

API_VERSION = 'v1'
LOGGER_ENDPOINT = os.environ.get('LAMA_LOGGER_ENDPOINT', 'http://localhost:8000')


def parse_query_params(url: str) -> dict:
    """Used to parse query params from url"""
    return dict(parse.parse_qsl(parse.urlsplit(url).query))


class LamaLogger:
    """
    Base logger class

    Examples:
        >>> import requests
        >>> lama_logger = LamaLogger(token='<your_token>', project_id='<your_project_id>')
        >>> response = requests.get('https://google.com/')
        >>> lama_logger(response)
    """
    endpoint = LOGGER_ENDPOINT
    api = f'{LOGGER_ENDPOINT}/api/{API_VERSION}'

    def __init__(self, token, project_id):
        self._token = token
        self.project_id = project_id

        self._node = None
        self._context_uuid = None

    def __call__(self, response: Response):
        request_id = str(uuid.uuid4())
        setattr(response, 'request_id', request_id)
        allure.attach(self.link_pattern(request_id), 'Logs', allure.attachment_type.HTML)

        thread = threading.Thread(target=self.send_logs, args=(response,))
        thread.start()

    @property
    def __headers(self):
        """Headers for send long request"""
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Token {self._token}',
        }

    def __to_payload(self, response: Response) -> dict:
        """Forms json for logger"""
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

    def link_pattern(self, request_id: str):
        """Wrapper for allure to attach like into step"""
        request_link = self.endpoint + f'/projects/{self.project_id}/?requestId={request_id}'
        return f'<head></head><body><a href="{request_link}" target="_blank">{request_link}</a></body>'

    def send_logs(self, response: Response):
        """Sending json to logger"""
        payload = self.__to_payload(response)
        endpoint = self.api + f'/projects/{self.project_id}/requests/create/'
        post(endpoint, data=json.dumps(payload), headers=self.__headers)

    def set_context(self, node: str = None):
        """
        Should be used to set context

        Example:
            @pytest.fixture(scope='function', autouse=True)
            def logger_context(request):
                logger.set_context(request.node.name)
                yield
                logger.drop_context()
        """
        self._node = node
        self._context_uuid = str(uuid.uuid4())

    def drop_context(self):
        """
        Should be used to drop context

        Example:
            @pytest.fixture(scope='function', autouse=True)
            def logger_context(request):
                logger.set_context(request.node.name)
                yield
                logger.drop_context()
        """
        self._node = None
        self._context_uuid = None
