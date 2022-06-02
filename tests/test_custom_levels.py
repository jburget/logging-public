import logging

import pytest

from logging_extended import set_custom_level


@pytest.mark.dependency
def test_set_custom_level(logger, log_creator, colored_terminal_handler):
    print()
    print(logging.getLevelName(5))
    set_custom_level('STATS', 5)

    assert logging.getLevelName(5) == 'STATS'
    assert logging.getLevelName("STATS") == 5

    logger.addHandler(colored_terminal_handler)
    logger.stats("very long and useful message")
    logger.debug("very long and useful message")


@pytest.mark.dependency(depends=["test_set_custom_level"])
def test_set_custom_level_with_existing_level(logger, log_creator, colored_terminal_handler):
    print()
    with pytest.raises(AssertionError):  # level 5 already exists
        set_custom_level('random name', 5)

    with pytest.raises(AssertionError):  # level `STATS` already exists
        set_custom_level('STATS', 6)

    logger.addHandler(colored_terminal_handler)
    logger.stats("very long and useful message")
    logger.debug("very long and useful message")
