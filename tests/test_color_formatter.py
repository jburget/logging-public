import logging
import sty
from pytest import fixture

from logging_extended import ColorFormatter


@fixture
def color_formatter():
    return ColorFormatter("%(name)s - %(levelname)-8s - %(message)s")


@fixture
def colored_logger(terminalLogger, terminalHandler, color_formatter):
    terminalHandler.setFormatter(color_formatter)
    return terminalLogger


def test_format(colored_logger):
    print()
    colored_logger.debug("very long and useful message")
    colored_logger.info("very long and useful message")
    colored_logger.warning("very long and useful message")
    colored_logger.error("very long and useful message")
    colored_logger.critical("very long and useful message")


def test_color_formatter(terminalLogger, terminalHandler):
    print()
    formatter = ColorFormatter()
    colors = formatter.colors.copy()
    formatter[logging.DEBUG] = sty.fg.black
    assert colors != formatter.colors
    assert formatter[logging.DEBUG] == sty.fg.black
    terminalHandler.setFormatter(formatter)
    terminalLogger.debug("help meeeeee")
    terminalLogger.warning("no ha i told you")

    del formatter[logging.DEBUG]

    terminalLogger.debug("working")

    formatter.undefined_color = sty.fg.li_cyan
    assert formatter.undefined_color == sty.fg.li_cyan

    formatter.reset = sty.rs.fg
    assert formatter.reset == sty.rs.fg
