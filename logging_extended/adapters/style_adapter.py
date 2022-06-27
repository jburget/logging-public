from logging import LoggerAdapter

from logging_extended.adapters import BraceMessage
from logging_extended.adapters import DollarMessage
from logging_extended.filters import FuncNameTagger


class BaseAdapter(LoggerAdapter):

    def __init__(self, logger, extra=None):
        super().__init__(logger, extra or {})

    # # https://github.com/python/cpython/blob/5849af7a80166e9e82040e082f22772bd7cf3061/Lib/logging/__init__.py#L1936
    # def process(self, msg, kwargs):
    #     """
    #     merge self.extra dict with kwargs extra dict
    #     extra dict is used for creating custom LogRecord attributes
    #     :param msg:
    #     :param kwargs:
    #     :return:
    #     """
    #     # https://stackoverflow.com/questions/577234/python-extend-for-a-dictionary
    #     # print(f"{msg = }")
    #     # print(f"{kwargs = }")
    #     # print(f"{self.extra = }")
    #     # print()
    #
    #     if (extra := kwargs.get("extra")) is not None and self.extra is not None:
    #         # print(extra)
    #         kwargs["extra"] = {**self.extra, **extra}
    #     elif kwargs.get('extra') is None and self.extra is not None:
    #         kwargs['extra'] = dict(self.extra)  # nested Adapters could modify it, if not copied
    #     # print(kwargs["extra"])
    #     if isinstance(msg, (BraceMessage, DollarMessage)):
    #         # print(f"{msg.kwargs=}")
    #         msg.kwargs.update(kwargs["extra"])
    #         # print(msg.kwargs)
    #
    #     for key in list(kwargs.keys()):  # remove kwargs, that cannot be passed to logger._log
    #         if key not in self._reserved_attrs:
    #             del kwargs[key]
    #
    #     return msg, kwargs

    def log(self, level, msg, /, *args, **kwargs):
        """
        Delegate a log call to the underlying logger, after adding
        contextual information from this adapter instance.

        Uses func kwarg to rename funcName in LogRecord
        """
        # some pain with stacklevel to log correct funcName in LogRecord
        # no idea how it works
        if kwargs.get("stacklevel") is not None:
                kwargs["stacklevel"] += 2
        else:
            kwargs["stacklevel"] = 3  # that means this is top level adapter

        if (func := kwargs.pop("func", None)) is not None:
            func_name_tagger = FuncNameTagger(func)
            self.addFilter(func_name_tagger)
            super().log(level, msg, *args, **kwargs)
            self.removeFilter(func_name_tagger)
        else:
            super().log(level, msg, **kwargs)

    def addHandler(self, handler):
        self.logger.addHandler(handler)

    def removeHandler(self, handler):
        self.logger.removeHandler(handler)

    def setLevel(self, level) -> None:
        self.logger.setLevel(level)

    @property
    def filters(self):
        return self.logger.filters

    def addFilter(self, filter):
        self.logger.addFilter(filter)

    def removeFilter(self, filter):
        self.logger.removeFilter(filter)


class MergeExtrasAdapter(BaseAdapter):
    __reserved_attrs = ["args", "exc_info", "extra", "stack_info", "stacklevel"]

    # https://github.com/python/cpython/blob/5849af7a80166e9e82040e082f22772bd7cf3061/Lib/logging/__init__.py#L1936
    def merge_extras(self, msg, kwargs):
        """
        merge self.extra dict with kwargs extra dict
        extra dict is used for creating custom LogRecord attributes
        :param msg:
        :param kwargs:
        :return:
        """
        if self.extra is not None:
            if (extra := kwargs.get("extra")) is not None:
                kwargs["extra"] = {**self.extra, **extra}
            else:
                kwargs['extra'] = dict(self.extra)  # nested Adapters could modify it, if not copied

        for key in list(kwargs.keys()):  # remove kwargs, that cannot be passed to logger._log
            if key not in self.__reserved_attrs:
                del kwargs[key]

        return msg, kwargs

    def process(self, msg, kwargs):
        return self.merge_extras(msg, kwargs)
