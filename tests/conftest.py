from logging import DEBUG, Logger, basicConfig, getLogger

from pytest import fixture


@fixture
def logger() -> Logger:
    basicConfig(level=DEBUG)
    return getLogger()
