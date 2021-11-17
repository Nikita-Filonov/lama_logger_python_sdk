import uuid

import allure
import requests

from logger import LamaLogger

logger = LamaLogger(token='1ec4ebe3-24ff-4e3d-a750-feb53a5d647b', project_id=1)


def link_pattern(request_id):
    request_link = logger.endpoint + f'/projects/{logger.project_id}/?requestId={request_id}'
    return f'<head></head><body><a href="{request_link}" target="_blank">{request_link}</a></body>'


def response_middleware(response):
    request_id = str(uuid.uuid4())
    setattr(response, 'request_id', request_id)
    allure.attach(link_pattern(request_id), 'Logs', allure.attachment_type.HTML)
    logger(response)


def get(url, params=None, **kwargs):
    response = requests.get(url, params=params, stream=True, **kwargs)
    response_middleware(response)
    return response


def post(url, data=None, json=None, **kwargs):
    response = requests.post(url, data=data, json=json, stream=True, **kwargs)
    response_middleware(response)
    return response


def patch(url, data=None, **kwargs):
    response = requests.patch(url, data=data, stream=True, **kwargs)
    response_middleware(response)
    return response


def put(url, data=None, **kwargs):
    response = requests.put(url, data=data, stream=True, **kwargs)
    response_middleware(response)
    return response


def delete(url, **kwargs):
    response = requests.delete(url, stream=True, **kwargs)
    response_middleware(response)
    return response
