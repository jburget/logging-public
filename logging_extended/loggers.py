import logging
from functools import partialmethod

from logging_extended.my_logging import EMERGENCY
from logging_extended.my_logging import STATS


class BraceString(str):

    def __mod__(self, other):
        return self.format(*other)

    def __str__(self):
        return self


class MyLogger(logging.Logger):
    """
    logging.setLoggerClass(MyLogger)
    """

    def __init__(self, name: str):
        super().__init__(name)
        # https://stackoverflow.com/questions/49662666/unable-to-call-function-defined-by-partialmethod
        self.stats = partialmethod(self.__class__.log, STATS).__get__(self, self.__class__)
        self.emergency = partialmethod(self.__class__.log, EMERGENCY).__get__(self, self.__class__)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None):
        """
        Allows overwriting already existing log attributes like funcName for decorators.
        """
        rv = logging._logRecordFactory(name, level, fn, lno, msg, args, exc_info, func,
                                       sinfo)
        if extra is not None:
            for key in extra:
                rv.__dict__[key] = extra[key]
        return rv


