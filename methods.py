import requests

from logger import LamaLogger

logger = LamaLogger(token='3eaa763398f4a6d12d276d856e8c358991007cb7', project_id=1)


def get(url, params=None, **kwargs):
    response = requests.get(url, params=params, **kwargs)
    logger(response)
    return response


def post(url, data=None, json=None, **kwargs):
    response = requests.post(url, data=data, json=json, **kwargs)
    logger(response)
    return response


def patch(url, data=None, **kwargs):
    response = requests.patch(url, data=data, **kwargs)
    logger(response)
    return response


def put(url, data=None, **kwargs):
    response = requests.put(url, data=data, **kwargs)
    logger(response)
    return response


def delete(url, **kwargs):
    response = requests.delete(url, **kwargs)
    logger(response)
    return response
