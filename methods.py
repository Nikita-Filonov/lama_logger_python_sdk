import requests
from requests import request

from logger import LamaLogger

logger = LamaLogger(token='<your_token>', project_id='<your_project_id>')


def basic_request(method: str, url: str, **kwargs):
    """
    :param method: Http method, like GET, POST, PUT, PATCH, DELETE
    :param url: Endpoint url
    If user is None then by default ``DEFAULT_USER`` is used. If you want to
    use other user, then provide credentials as:
    {
        "username": <some_email>,
        "password": <some_password>,
        "client_id": "insomnia",
        "client_secret": "insomnia",
        "grant_type": "password"
    }
    If set to True, then request will have header like:
    {'Authorization': 'Bearer <some_token>'}
    some of requests should have for example {'Content-type': 'application/json'}, but
    others do not need any headers.

    All available headers can be viewed in ``HeadersTemplates``. If you want to add your
    custom headers, then add new headers to ``HeadersTemplates``, and pass it inside
    method like this:
    post(<url>, data={}, headers_type=HeadersTemplates.MY_CUSTOM)

    :param kwargs: additional params
    :return: :class:`Response <Response>` object

    This method has included logger, if you want to stop seeing API logs,
    then in settings.py set ``REQUESTS_LOGGING`` to False.

    ``Verify`` property by default set in setting.py ``CERT_PATH``. We need
    this property because if not set, then we will unable to make request.
    If set to False, then we will get insecure warning, but if set to
    some cert path, then no warnings and no errors.
    """
    kwargs.setdefault('stream', True)

    response = request(method, url, **kwargs)
    logger(response)

    return response


def get(url, params=None, **kwargs):
    """
    Sends a GET request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return basic_request('get', url, params=params, **kwargs)


def post(url, json=None, **kwargs):
    """
    Sends a POST request.

    :param user: user to get token
    :param url: URL for the new :class:`Request` object.
    :param json: (optional) json data to send in the body of the :class:`Request`.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return basic_request('post', url, json=json, **kwargs)


def put(url, json=None, **kwargs):
    """
    Sends a PUT request.

    :param url: URL for the new :class:`Request` object.
    :param json: (optional) json data to send in the body of the :class:`Request`.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return basic_request('put', url, json=json, **kwargs)


def patch(url, json=None, **kwargs):
    """
    Sends a PATCH request.

    :param url: URL for the new :class:`Request` object.

    :param json: (optional) json data to send in the body of the :class:`Request`.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return basic_request('patch', url, json=json, **kwargs)


def delete(url, **kwargs):
    """
    Sends a DELETE request.

    :param url: URL for the new :class:`Request` object.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return basic_request('delete', url, **kwargs)
