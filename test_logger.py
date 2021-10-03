import json
import unittest
from time import sleep

from methods import get, post, patch, put, delete

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token 3eaa763398f4a6d12d276d856e8c358991007cb7'
}
endpoint = 'https://lama-logger.herokuapp.com/api/v1/projects/1/requests/'
payload = json.dumps({'some': 'string'})


class TestRequests(unittest.TestCase):
    def test_get_request(self):
        sleep(5)
        get(endpoint, headers=headers)

    def test_post_request(self):
        post(endpoint, headers=headers, data=payload)

    def test_delete_request(self):
        delete(endpoint, data=payload)

    def test_patch_request(self):
        patch(endpoint, headers=headers, data=payload)

    def test_put_request(self):
        put(endpoint, headers=headers, data=payload)
