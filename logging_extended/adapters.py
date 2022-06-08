from logging import LoggerAdapter
from inspect import stack
from string import Template


# https://stackoverflow.com/questions/13131400/logging-variable-data-with-new-format-string


class StyleAdapter(LoggerAdapter):
    _reserved_attrs = ["args", "exc_info", "extra", "stack_info", "stacklevel"]

    def __init__(self, logger, extra=None):
        super().__init__(logger, extra or {})

    # https://github.com/python/cpython/blob/5849af7a80166e9e82040e082f22772bd7cf3061/Lib/logging/__init__.py#L1936
    def process(self, msg, kwargs):
        """
        merge self.extra dict with kwargs extra dict
        extra dict is used for creating custom LogRecord attributes
        :param msg:
        :param kwargs:
        :return:
        """
        # https://stackoverflow.com/questions/577234/python-extend-for-a-dictionary
        # print(f"{msg = }")
        # print(f"{kwargs = }")
        # print(f"{self.extra = }")
        # print()

        if (extra := kwargs.get("extra")) is not None and self.extra is not None:
            # print(extra)
            kwargs["extra"] = {**self.extra, **extra}
        elif kwargs.get('extra') is None and self.extra is not None:
            kwargs['extra'] = dict(self.extra)  # nested Adapters could modify it, if not copied
        # print(kwargs["extra"])
        if isinstance(msg, (BraceMessage, DollarMessage)):
            # print(f"{msg.kwargs=}")
            msg.kwargs.update(kwargs["extra"])
            # print(msg.kwargs)

        for key in list(kwargs.keys()):  # remove kwargs, that cannot be passed to logger._log
            if key not in self._reserved_attrs:
                del kwargs[key]

        return msg, kwargs

    def log(self, level, msg, /, *args, **kwargs):
        super().log(level, msg, **kwargs)


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
        return Template(self.fmt).substitute(**self.kwargs)


# https://docs.python.org/3/howto/logging-cookbook.html#use-of-alternative-formatting-styles
class BraceAdapter(StyleAdapter):

    # https://github.com/python/cpython/blob/5849af7a80166e9e82040e082f22772bd7cf3061/Lib/logging/__init__.py#L1936
    # https://github.com/python/cpython/blob/5849af7a80166e9e82040e082f22772bd7cf3061/Lib/logging/__init__.py#L1660
    def log(self, level, msg, /, *args, **kwargs):
        super().log(level, BraceMessage(msg, *args, **kwargs), **kwargs)


class DollarAdapter(StyleAdapter):

    def log(self, level, msg, /, **kwargs):
        super().log(level, DollarMessage(msg, **kwargs), **kwargs)

# TODO: for logging from decorators correct func name, use maybe stacklevel from
# https://github.com/python/cpython/blob/5849af7a80166e9e82040e082f22772bd7cf3061/Lib/logging/__init__.py#L1660
