import logging

from functools import partialmethod


def set_custom_level(level_name: str, level_number: int):
    """
    Set a custom level to the logging module.

    custom levels and related log methods are not available in the logging module global scope
    :param level_name: is converted to upper case for constant-like names, e.g. 'STATS'
    :param level_number:
    :return: None
    """
    assert logging.getLevelName(level_number).startswith('Level'), "Level name already exists"
    assert not isinstance(logging.getLevelName(level_name), int), "Level name already exists"

    const_name = level_name.upper()
    func_name = level_name.lower()

    logging.addLevelName(level_number, const_name)

    setattr(logging.getLoggerClass(), func_name, partialmethod(logging.getLoggerClass().log, level_number))
    setattr(logging.LoggerAdapter, func_name, partialmethod(logging.LoggerAdapter.log, level_number))

# custom log levels https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility
# logging.stats = partial(logging.log, STATS)
# logging.LoggerAdapter.stats = partialmethod(logging.LoggerAdapter.log, STATS)
# well, didn't work, because partial was used instead of partialmethod, of course there was missing required argument
