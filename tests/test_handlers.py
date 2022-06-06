import logging
from logging_extended import rewrite_filter_on_object
import pytest

from logging_extended.filters import Filter_exception


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


def test_filter_if_any(log_creator, colored_terminal_handler):
    print()

    rewrite_filter_on_object(colored_terminal_handler)  # rewrite built-in filter
    colored_terminal_handler.addFilter(lambda record: record.levelno == logging.DEBUG)
    colored_terminal_handler.addFilter(lambda record: record.levelno == logging.INFO)

    with log_creator as logger:  # in this context, logger returns LogRecord
        logger.addHandler(colored_terminal_handler)
        assert colored_terminal_handler.filter(logger.debug("message"))
        assert colored_terminal_handler.filter(logger.info("message"))
        assert not colored_terminal_handler.filter(logger.warning("message"))
        assert not colored_terminal_handler.filter(logger.error("message"))
        assert not colored_terminal_handler.filter(logger.critical("message"))

        colored_terminal_handler.addFilter(Filter_exception(reverse=True))

        assert colored_terminal_handler.filter(logger.debug("message"))
        assert colored_terminal_handler.filter(logger.info("message"))
        assert colored_terminal_handler.filter(logger.warning("message"))
        assert colored_terminal_handler.filter(logger.error("message"))
        assert colored_terminal_handler.filter(logger.critical("message"))


@pytest.mark.skip(reason="spam output")
def test_log_creator(log_creator, colored_terminal_handler):
    print()
    with log_creator as logger:
        logger.addHandler(colored_terminal_handler)
        logger.info("info long message")
        logger.warning("warning long message")
        logger.error("error long message")
        logger.critical("critical long message")
