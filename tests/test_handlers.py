import logging
import pytest

from logging_extended.filters import ExceptionInfoFilter


@pytest.mark.dependency
def test_pickle_handler(colored_logger, pickle_writer):
    print()
    colored_logger.addHandler(pickle_writer)

    colored_logger.debug("debug long message")
    colored_logger.info("info long message")


@pytest.mark.skip(reason="spam output")
@pytest.mark.dependency(depends=["test_pickle_handler"])
def test_loading_pickle(pickle_reader):
    print()
    for chunk in pickle_reader.yield_chunks():
        print(chunk)


def test_filter_if_any(logger, queue_iterator, any_filter):
    print()
    any_filter.addFilter(lambda l: l.levelno == logging.DEBUG)
    any_filter.addFilter(lambda l: l.levelno == logging.INFO)
    logger.addFilter(any_filter)

    logger.info("message")
    logger.debug("message")
    logger.warning("message")
    assert len(queue_iterator) == 2


@pytest.mark.skip(reason="spam output")
def test_log_creator(log_creator, colored_terminal_handler):
    print()
    with log_creator as logger:
        logger.addHandler(colored_terminal_handler)
        logger.info("info long message")
        logger.warning("warning long message")
        logger.error("error long message")
        logger.critical("critical long message")
