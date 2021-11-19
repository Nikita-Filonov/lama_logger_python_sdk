import requests

from logger import LamaLogger

logger = LamaLogger(token='2c407474-1911-465a-ae43-01ca1161f33c', project_id=1)


def get(url, params=None, **kwargs):
    response = requests.get(url, params=params, stream=True, **kwargs)
    logger(response)
    return response


def post(url, data=None, json=None, **kwargs):
    response = requests.post(url, data=data, json=json, stream=True, **kwargs)
    logger(response)
    return response


def patch(url, data=None, **kwargs):
    response = requests.patch(url, data=data, stream=True, **kwargs)
    logger(response)
    return response


def put(url, data=None, **kwargs):
    response = requests.put(url, data=data, stream=True, **kwargs)
    logger(response)
    return response


def delete(url, **kwargs):
    response = requests.delete(url, stream=True, **kwargs)
    logger(response)
    return response
