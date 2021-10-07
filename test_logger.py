import json

import allure
import pytest

from methods import get, post, patch, put, delete

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token 3eaa763398f4a6d12d276d856e8c358991007cb7'
}
endpoint = 'https://lama-logger.herokuapp.com/api/v1/projects/3/requests/'
payload = json.dumps({'some': 'string'})


@pytest.mark.demo
class TestRequests:
    def test_get_request(self):
        with allure.step('Step 1'):
            get(endpoint, headers=headers)

    def test_post_request(self):
        with allure.step('Step 1'):
            post(endpoint, headers=headers, data=payload)

    def test_delete_request(self):
        with allure.step('Step 1'):
            delete(endpoint, data=payload)

    def test_patch_request(self):
        with allure.step('Step 1'):
            patch(endpoint, headers=headers, data=payload)

    def test_put_request(self):
        with allure.step('Step 1'):
            put(endpoint, headers=headers, data=payload)
