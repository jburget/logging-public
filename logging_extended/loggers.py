import logging


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

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None):
        """
        Allows overwriting already existing log attributes like funcName for decorators.
        """
        rv = logging._logRecordFactory(name, level, fn, lno, msg, args, exc_info, func,
                                       sinfo)  # TODO maybe use makeLogRecord instead
        if extra is not None:
            for key in extra:
                rv.__dict__[key] = extra[key]
        return rv


