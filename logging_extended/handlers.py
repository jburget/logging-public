import json
import pickle
import struct
import types
from logging import FileHandler
from logging import LogRecord
from logging import makeLogRecord

from .formatters import PickleFormatter

from logging_extended.formatters.json_formatter import JsonFormatter


class Handler_json(FileHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFormatter(JsonFormatter("%(message)s"))

    @classmethod
    def restore_record_from_json(cls, json_dict: dict) -> LogRecord:
        """
        Uses logging.makeLogRecord to create LogRecord from dict object
        :param json_dict:
        :return: logging.LogRecord
        """
        return makeLogRecord(json_dict)  # https://docs.python.org/3/library/logging.html#logging.makeLogRecord

    def json_restore_log_carefully(self):
        """
        Generator, that reads file lines and yields LogRecords
        """
        with open(self.baseFilename, mode="r") as f:
            for line in f:
                yield self.restore_record_from_json(json_dict=json.loads(line))


class PickleHandler(FileHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFormatter(PickleFormatter())
        self.terminator: bytes = b""  # must be empty to match chunk size

    def yield_chunks(self):
        with open(self.baseFilename, "rb") as f:
            while True:
                first_four_bytes = f.read(4)
                if not first_four_bytes:
                    break
                size = struct.unpack(">L", first_four_bytes[:4])[0]
                yield struct.pack(">L", size) + f.read(size)

    @staticmethod
    def decode_chunk(chunk: bytes):
        return pickle.loads(chunk[4:])

    def yield_decoded_chunks(self):
        for chunk in self.yield_chunks():
            yield self.decode_chunk(chunk)


def filter_if_any(self, record: LogRecord) -> bool:
    """
    Returns True if any of filters passes
    Must be assigned to object with rewrite_filter_on_object

    Determine if a record is loggable by consulting all the filters.
    The default is to allow the record to be logged; any filter can veto
    this and the record is then dropped. Returns a zero value if a record
    is to be dropped, else non-zero.
    .. versionchanged:: 3.2
       Allow filters to be just callables.
    .. my version..
    passes if any filter returns True

    :param record:
    :return: bool
    """
    for f in self.filters:
        if (
                hasattr(f, 'filter')
                and f.filter(record)
                or not hasattr(f, 'filter')
                and f(record)
        ):
            return True
    return not self.filters


def rewrite_filter_on_object(obj: object):
    """Rewrites filter method to filter_if_any on object"""
    obj.filter = types.MethodType(filter_if_any, obj)
