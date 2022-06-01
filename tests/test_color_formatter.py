import logging

from logging_extended.formatters.color_formatter import *
from logging_extended import ColorFormatter

from logging import makeLogRecord


logger = logging.getLogger(__name__)
terminal = logging.StreamHandler()
logger.addHandler(terminal)
logger.setLevel(logging.DEBUG)


def test_format():
    formatter = ColorFormatter("%(name)s - %(levelname)-8s - %(message)s")
    terminal.setFormatter(formatter)
    print()
    logger.debug("very long and useful message")
    logger.info("very long and useful message")
    logger.warning("very long and useful message")
    logger.error("very long and useful message")
    logger.critical("very long and useful message")


def test_color_formatter():
    print()
    formatter = ColorFormatter()
    colors = formatter.colors.copy()
    formatter[logging.DEBUG] = sty.fg.black
    assert colors != formatter.colors
    assert formatter[logging.DEBUG] == sty.fg.black
    terminal.setFormatter(formatter)
    logger.debug("help meeeeee")
    logger.warning("no ha i told you")

    del formatter[logging.DEBUG]

    logger.debug("working")

    formatter.undefined_color = sty.fg.li_cyan
    assert formatter.undefined_color == sty.fg.li_cyan

    formatter.reset = sty.rs.fg
    assert formatter.reset == sty.rs.fg
