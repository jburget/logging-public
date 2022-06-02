import logging
import pathlib
from logging import DEBUG
from logging import LogRecord
from logging import StreamHandler
from logging import getLogRecordFactory
from logging import setLogRecordFactory

from pytest import fixture
from logging import getLogger
from logging_extended import ColorFormatter


@fixture(scope="function")
def logger() -> logging.Logger:
    logger = getLogger(__name__)
    logger.setLevel(1)
    while logger.handlers:  # remove all handlers, avoid duplicate handlers during test
        logger.removeHandler(logger.handlers[0])
    return logger


@fixture
def terminalHandler() -> StreamHandler:
    return StreamHandler()


@fixture
def terminalLogger(logger, terminalHandler) -> logging.Logger:
    logger.addHandler(terminalHandler)
    return logger


@fixture
def color_formatter():
    return ColorFormatter("%(name)s - %(levelname)-8s - %(message)s")


@fixture
def colored_terminal_handler(terminalHandler, color_formatter):
    terminalHandler.setFormatter(color_formatter)
    return terminalHandler


@fixture
def colored_logger(terminalLogger, terminalHandler, color_formatter):
    terminalHandler.setFormatter(color_formatter)
    return terminalLogger


class LogFactory:

    def __init__(self):
        self.old_factory = getLogRecordFactory()
        self.logs: list[LogRecord] = []

    def pop(self):
        return self.logs.pop()

    def __call__(self, *args, **kwargs):
        record = self.old_factory(*args, **kwargs)
        self.logs.append(record)
        return record


def instantiate_factory_storage():
    factory = LogFactory()
    setLogRecordFactory(factory)
    return factory


class LogCreator(logging.getLoggerClass()):

    def __enter__(self):
        self.logs_storage: LogFactory = instantiate_factory_storage()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def debug(self, msg, *args, **kwargs):
        super(LogCreator, self).debug(msg, *args, **kwargs)
        return self.logs_storage.pop()

    def info(self, msg, *args, **kwargs):
        super(LogCreator, self).info(msg, *args, **kwargs)
        return self.logs_storage.pop()

    def warning(self, msg, *args, **kwargs):
        super(LogCreator, self).warning(msg, *args, **kwargs)
        return self.logs_storage.pop()

    def error(self, msg, *args, **kwargs):
        super(LogCreator, self).error(msg, *args, **kwargs)
        return self.logs_storage.pop()

    def critical(self, msg, *args, **kwargs):
        super(LogCreator, self).critical(msg, *args, **kwargs)
        return self.logs_storage.pop()

    def exception(self, msg, *args, exc_info=True, **kwargs):
        super(LogCreator, self).exception(msg, *args, exc_info=exc_info, **kwargs)
        return self.logs_storage.pop()


@fixture
def log_creator():
    return LogCreator(__name__)


def base_log_records(log_factory_storage, logger):
    logger.debug("debug long message")
    logger.info("info long message")
    logger.warning("warning long message")
    logger.error("error long message")
    logger.critical("critical long message")
    return log_factory_storage


# files
@fixture(scope="session")
def file_pickle_log():
    # before test - create resource
    file_path = pathlib.Path("pickled.log")
    file_path.touch()
    yield file_path
    # after test - remove resource
    file_path.unlink()
