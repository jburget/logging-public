import logging
from logging_extended import filter_if_any, rewrite_filter_on_object
import pytest
from pytest import fixture

from logging_extended.handlers import PickleHandler
from logging_extended.formatters import PickleFormatter
from logging_extended.filters import Filter_exception


@fixture
def pickle_reader(file_pickle_log):
    return PickleHandler(filename=file_pickle_log, mode="rb")


@fixture
def pickle_writer(file_pickle_log):
    return PickleHandler(filename=file_pickle_log, mode="wb")


def test_pickle_handler(colored_logger, pickle_writer):
    print()
    colored_logger.addHandler(pickle_writer)

    colored_logger.debug("debug long message")
    colored_logger.info("info long message")


@pytest.mark.skip(reason="spam output")
def test_loading_pickle(pickle_reader):
    print()
    for chunk in pickle_reader.yield_chunks():
        print(chunk)


def test_filter_if_any(log_creator, terminalHandler, color_formatter):
    print()
    terminalHandler.setFormatter(color_formatter)

    rewrite_filter_on_object(terminalHandler)  # rewrite built-in filter
    terminalHandler.addFilter(lambda record: record.levelno == logging.DEBUG)
    terminalHandler.addFilter(lambda record: record.levelno == logging.INFO)

    with log_creator as logger:  # in this context, logger returns LogRecord
        logger.addHandler(terminalHandler)
        assert terminalHandler.filter(logger.debug("message"))
        assert terminalHandler.filter(logger.info("message"))
        assert not terminalHandler.filter(logger.warning("message"))
        assert not terminalHandler.filter(logger.error("message"))
        assert not terminalHandler.filter(logger.critical("message"))

        terminalHandler.addFilter(Filter_exception(reverse=True))

        assert terminalHandler.filter(logger.debug("message"))
        assert terminalHandler.filter(logger.info("message"))
        assert terminalHandler.filter(logger.warning("message"))
        assert terminalHandler.filter(logger.error("message"))
        assert terminalHandler.filter(logger.critical("message"))


@pytest.mark.skip(reason="spam output")
def test_log_creator(log_creator, colored_terminal_handler):
    print()
    with log_creator as logger:
        logger.addHandler(colored_terminal_handler)
        logger.info("info long message")
        logger.warning("warning long message")
        logger.error("error long message")
        logger.critical("critical long message")
