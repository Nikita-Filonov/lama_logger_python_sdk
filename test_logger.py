import json

import allure
import pytest

from methods import get, post, patch, put, delete

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token c239971892800c89a80170ee396687d485165b44'
}
endpoint = 'http://localhost:8000/api/v1/projects/1/requests/'
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
