import json

import allure
import pytest

from methods import get, post, patch, put, delete

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token e1872b9d264446e77f7b7edbee42412e20fdf41a'
}
endpoint = 'https://lama-logger.herokuapp.com/api/v1/projects/1/requests/?hello=12345&hello2=123123'
payload = json.dumps({'some': 'string'})


@pytest.mark.demo
class TestRequests:
    count = range(10)

    @pytest.mark.chain
    @pytest.mark.parametrize('x', count)
    def test_get_request(self, x):
        with allure.step('Step 1'):
            get(endpoint, headers=headers)
            delete(endpoint, data=payload)
            post(endpoint, headers=headers, data=payload)
            patch(endpoint, headers=headers, data=payload)
            patch(endpoint, headers=headers, data=payload)

    @pytest.mark.parametrize('x', count)
    def test_post_request(self, x):
        with allure.step('Step 1'):
            post(endpoint, headers=headers, data=payload)

    @pytest.mark.parametrize('x', count)
    def test_delete_request(self, x):
        with allure.step('Step 1'):
            delete(endpoint, data=payload)

    @pytest.mark.parametrize('x', count)
    def test_patch_request(self, x):
        with allure.step('Step 1'):
            patch(endpoint, headers=headers, data=payload)

    @pytest.mark.parametrize('x', count)
    def test_put_request(self, x):
        with allure.step('Step 1'):
            put(endpoint, headers=headers, data=payload)
