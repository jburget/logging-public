from logging import LoggerAdapter
from inspect import stack

from logging_extended.loggers import BraceString


# https://stackoverflow.com/questions/13131400/logging-variable-data-with-new-format-string


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


class BraceMessage:
    def __init__(self, msg, /, *args, **kwargs):
        self.msg = msg
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        # print(f"{self.msg}")
        # print(*[i.function for i in stack()[:8]])
        return str(self.msg).format(*self.args, **self.kwargs)


class DollarMessage:
    def __init__(self, fmt, /, **kwargs):
        self.fmt = fmt
        self.kwargs = kwargs

    def __str__(self):
        from string import Template
        return Template(self.fmt).substitute(**self.kwargs)


# https://docs.python.org/3/howto/logging-cookbook.html#use-of-alternative-formatting-styles
class BraceAdapter(LoggerAdapter):  # TODO: extra dict call with log func for adding attr to LogRecord
    # extra will be assigned to BraceAdapter, and passed with every log message as extra parameter
    # thus LogRecords will be customized per Adapter, and customizations will be lost when Adapter is destroyed
    # also custimization will be separate between Adapters assigned to the same logger
    # TODO: make sure that extra is collected during init of the object and also during logging
    def __init__(self, logger, extra=None):
        super().__init__(logger, extra or {})

    def log(self, level, msg, /, *args, **kwargs):
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
            self.logger._log(level, BraceMessage(msg, *args, **kwargs), ())


class DollarAdapter(LoggerAdapter):

    def __init__(self, logger, extra=None):
        super().__init__(logger, extra or {})

    def log(self, level, fmt, /, **kwargs):
        if self.isEnabledFor(level):
            fmt, kwargs = self.process(fmt, kwargs)
            self.logger._log(level, DollarMessage(fmt, **kwargs), ())
