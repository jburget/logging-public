from logging import LoggerAdapter

from logging_extended.loggers import BraceString


class BracketStyleAdapter(LoggerAdapter):
    """
    Supports {} formatting of log messages

    Can handle only positional args like {1}
    does not support kwargs like a=5
    """

    def __init__(self, logger, extra=None):
        super().__init__(logger, extra)

    def process(self, msg, kwargs):
        if kwargs.get("extra") is not None and self.extra is not None:
            kwargs["extra"] = {**kwargs["extra"], **self.extra}
        elif self.extra is not None:  # if log func has no info but adapter class has, then include it in record
            kwargs["extra"] = self.extra
        return BraceString(msg), kwargs
