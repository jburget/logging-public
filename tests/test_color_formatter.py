import logging

import pytest
import sty

from logging_extended.formatters import display_sty_palette


@pytest.mark.skip("spam output")
def test_colored_levels(colored_logger):
    print()
    colored_logger.log(2, "very long and useful message")  # color is not defined for level 2
    colored_logger.log(5, "very long and useful message")
    colored_logger.debug("very long and useful message")
    colored_logger.info("very long and useful message")
    colored_logger.warning("very long and useful message")
    colored_logger.error("very long and useful message")
    colored_logger.critical("very long and useful message")


def test_managing_colors(color_formatter):
    print()
    color_formatter[logging.DEBUG] = sty.fg.black
    color_formatter[logging.INFO] = sty.fg.yellow
    assert color_formatter[logging.DEBUG] == sty.fg.black
    assert color_formatter[logging.INFO] == sty.fg.yellow

    del color_formatter[logging.DEBUG]
    assert color_formatter[logging.DEBUG] == sty.fg.undefined

    color_formatter.undefined_color = sty.fg.li_cyan
    assert color_formatter.undefined_color == sty.fg.li_cyan

    color_formatter.reset = sty.rs.fg
    assert color_formatter.reset == sty.rs.fg


@pytest.mark.skip("spam output")
def test_display_sty_palette():
    print()
    display_sty_palette(display_blocks=True)
