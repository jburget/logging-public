from logging import LogRecord
from logging.handlers import SocketHandler
from logging import Formatter


class PickleFormatter(Formatter):

    serializer = SocketHandler("", 0)

    def format(self, record: LogRecord) -> bytes:
        # https://github.com/python/cpython/blob/8a221a853787c18d5acaf46f5c449d28339cde21/Lib/logging/handlers.py#L627
        return self.serializer.makePickle(record)

