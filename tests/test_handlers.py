import logging
import pickle
import struct
from logging_extended import filter_if_any, rewrite_filter_on_object
import pytest

from logging_extended.handlers import PickleHandler
from logging import getLogger


logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)


@pytest.mark.skip
def test_pickle_handler():
    picklerer = PickleHandler(filename="log.log", mode="ab")
    logger.addHandler(picklerer)

    logger.debug("debug long message")
    logger.info("info long message")


def get_size_of_chunk(chunk):
    return struct.unpack(">L", chunk[:4])[0]


def test_loading_pickle():
    print()
    picklerer = PickleHandler(filename="log.log", mode="rb")
    for chunk in picklerer.yield_chunks():
        print(chunk)


def test_filter_if_any():
    print()

    from logging_extended import ColorFormatter

    logger = logging.getLogger(__name__)
    terminal = logging.StreamHandler()
    logger.addHandler(terminal)
    logger.setLevel(logging.DEBUG)



    formatter = ColorFormatter("%(name)s - %(levelname)-8s - %(message)s")

    terminal.setFormatter(formatter)
    rewrite_filter_on_object(terminal)
    terminal.addFilter(lambda record: record.levelno == logging.DEBUG)
    terminal.addFilter(lambda record: record.levelno == logging.INFO)
    print()
    logger.debug("very long and useful message")
    logger.info("very long and useful message")
    logger.warning("very long and useful message")
    logger.error("very long and useful message")
    logger.critical("very long and useful message")