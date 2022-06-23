from .helpers import BraceMessage
from .helpers import DollarMessage
from logging_extended.adapters.style_adapter import StyleAdapter

# https://stackoverflow.com/questions/13131400/logging-variable-data-with-new-format-string


class BaseStyleAdapter(StyleAdapter):

    def process(self, msg, kwargs):
        if kwargs.get("stacklevel") is not None:
                kwargs["stacklevel"] += 1
        else:
            kwargs["stacklevel"] = 2
        return super().process(msg, kwargs)


class BraceAdapter(BaseStyleAdapter):

    # https://github.com/python/cpython/blob/5849af7a80166e9e82040e082f22772bd7cf3061/Lib/logging/__init__.py#L1936
    # https://github.com/python/cpython/blob/5849af7a80166e9e82040e082f22772bd7cf3061/Lib/logging/__init__.py#L1660
    def log(self, level, msg, /, *args, **kwargs):
        if isinstance(msg, (BraceMessage, DollarMessage)):
            super().log(level, msg, *args, **kwargs)
        else:
            super().log(level, BraceMessage(msg, *args, **kwargs), **kwargs)


class DollarAdapter(BaseStyleAdapter):

    def log(self, level, msg, /, **kwargs):
        if isinstance(msg, (BraceMessage, DollarMessage)):
            super().log(level, msg, **kwargs)
        else:
            super().log(level, DollarMessage(msg, **kwargs), **kwargs)
