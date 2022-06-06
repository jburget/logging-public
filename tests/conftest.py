import logging
import pathlib
from logging import DEBUG
from logging import StreamHandler
from logging import getLogRecordFactory
from logging import setLogRecordFactory

from pytest import fixture
from logging import getLogger
from logging_extended import ColorFormatter
from logging_extended import DollarAdapter
from logging_extended import PickleHandler
from logging_extended import set_custom_level
from logging_extended import BraceAdapter


@fixture(scope="function")
def logger() -> logging.Logger:
    logger = getLogger(__name__)
    logger.setLevel(1)
    while logger.handlers:  # remove all handlers, avoid duplicate handlers during test
        logger.removeHandler(logger.handlers[0])
    return logger


@fixture
def terminal_handler() -> StreamHandler:
    return StreamHandler()


@fixture
def color_formatter():
    return ColorFormatter(fmt="{name} - {levelname:^9} - {message}", style="{")


@fixture
def colored_terminal_handler(terminal_handler, color_formatter):
    terminal_handler.setFormatter(color_formatter)
    return terminal_handler


@fixture
def colored_logger(logger, colored_terminal_handler):
    logger.addHandler(colored_terminal_handler)
    return logger


@fixture
def bracket_adapter(colored_logger):
    return BraceAdapter(colored_logger, {})


@fixture
def dollar_adapter(colored_logger):
    return DollarAdapter(colored_logger, {})


class LogCreator(logging.Logger):
    """
    Returns LogRecord object when used as logger

    when context is not entered, cannot be used as logger
    changes LogFactory on enter and restores on exit
    object is callable to be also used as LogFactory
    """

    def __init__(self, name, level=DEBUG):
        super().__init__(name, level)
        self.old_factory = getLogRecordFactory()
        self.__logs_storage = []

    def __enter__(self):
        setLogRecordFactory(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        setLogRecordFactory(self.old_factory)

    def __call__(self, *args, **kwargs):
        record = self.old_factory(*args, **kwargs)
        self.__logs_storage.append(record)
        return record

    def pop(self):
        try:
            return self.__logs_storage.pop()
        except IndexError as e:
            raise Warning("No log record in storage, maybe caused by not using as context manager") from e

    def debug(self, msg, *args, **kwargs):
        super(LogCreator, self).debug(msg, *args, **kwargs)
        return self.pop()

    def info(self, msg, *args, **kwargs):
        super(LogCreator, self).info(msg, *args, **kwargs)
        return self.pop()

    def warning(self, msg, *args, **kwargs):
        super(LogCreator, self).warning(msg, *args, **kwargs)
        return self.pop()

    def error(self, msg, *args, **kwargs):
        super(LogCreator, self).error(msg, *args, **kwargs)
        return self.pop()

    def critical(self, msg, *args, **kwargs):
        super(LogCreator, self).critical(msg, *args, **kwargs)
        return self.pop()

    def exception(self, msg, *args, exc_info=True, **kwargs):
        super(LogCreator, self).exception(msg, *args, exc_info=exc_info, **kwargs)
        return self.pop()


@fixture
def log_creator() -> LogCreator:
    return LogCreator(__name__)


@fixture
def generate_basic_log_records(log_creator) -> list[logging.LogRecord]:
    with log_creator as l:
        records = [
                l.debug("short message"),
                l.info("short message"),
                l.warning("short message"),
                l.error("short message"),
                l.critical("short message")
        ]
    return records


# files
@fixture(scope="session")
def file_pickle_log() -> pathlib.Path:
    # before test - create resource
    file_path = pathlib.Path("pickled.log")
    file_path.touch()
    yield file_path
    # after test - remove resource
    file_path.unlink()


@fixture
def define_stats_level() -> None:
    set_custom_level("stats", 5)


@fixture
def pickle_reader(file_pickle_log) -> PickleHandler:
    return PickleHandler(filename=file_pickle_log, mode="rb")


@fixture
def pickle_writer(file_pickle_log) -> PickleHandler:
    return PickleHandler(filename=file_pickle_log, mode="wb")
