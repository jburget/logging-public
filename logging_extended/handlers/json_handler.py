import json
from logging import FileHandler
from logging import Formatter
from logging import LogRecord
from logging import makeLogRecord

from logging_extended.formatters import JsonFormatter


class JsonHandler(FileHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().setFormatter(JsonFormatter("%(message)s"))

    def setFormatter(self, fmt: Formatter) -> None:
        pass

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
