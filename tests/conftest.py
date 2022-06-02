from logging import DEBUG
from logging import LogRecord
from logging import StreamHandler
from logging import getLogRecordFactory
from logging import setLogRecordFactory

from pytest import fixture
from logging import getLogger


class LogFactory:
    logs: list[LogRecord] = []

    def __init__(self):
        self.old_factory = getLogRecordFactory()

    def __call__(self, *args, **kwargs):
        log = self.old_factory(*args, **kwargs)
        self.logs.append(log)
        return log


@fixture
def log_factory_storage() -> list[LogRecord]:
    factory = LogFactory()
    setLogRecordFactory(factory)
    return factory.logs


@fixture
def logger():
    logger = getLogger(__name__)
    logger.setLevel(DEBUG)
    return logger


@fixture
def terminalHandler():
    return StreamHandler()


@fixture
def terminalLogger(logger, terminalHandler):
    logger.addHandler(terminalHandler)
    return logger
