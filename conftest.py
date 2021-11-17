import pytest

from methods import logger


@pytest.fixture(scope='function', autouse=True)
def logger_context(request):
    logger.set_context(request.node.name)
    yield
    logger.drop_context()
