import logging
from typing import Optional


class Csv_Formatter(logging.Formatter):
    """
    Subclass that takes care about special requirements of csv formatting
    """

    def __init__(self, fmt: Optional[str], *args, **kwargs):
        super().__init__(fmt=fmt, *args, **kwargs)

    def format(self, record: logging.LogRecord) -> str:
        return '"{}"'.format(super().format(record).replace('"', '""'))