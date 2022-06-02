import logging
from logging_extended import filter_if_any, rewrite_filter_on_object
import pytest

from logging_extended.handlers import PickleHandler


@pytest.mark.skip
def test_pickle_handler(logger):
    print()
    picklerer = PickleHandler(filename="log.log", mode="ab")
    logger.addHandler(picklerer)

    logger.debug("debug long message")
    logger.info("info long message")


def test_loading_pickle():
    print()
    picklerer = PickleHandler(filename="log.log", mode="rb")
    for chunk in picklerer.yield_chunks():
        print(chunk)


def test_filter_if_any(logger, terminalHandler, color_formatter):
    print()
    terminalHandler.setFormatter(color_formatter)
    rewrite_filter_on_object(terminalHandler)
    terminalHandler.addFilter(lambda record: record.levelno == logging.DEBUG)
    terminalHandler.addFilter(lambda record: record.levelno == logging.INFO)

    logger.debug("very long and useful message")
    logger.info("very long and useful message")
    logger.warning("very long and useful message")
    logger.error("very long and useful message")
    logger.critical("very long and useful message")
