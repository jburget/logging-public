import pickle
import struct
from logging import FileHandler
from logging import Formatter

from logging_extended.formatters import PickleFormatter
from logging_extended.formatters import PickleFormatter


class PickleHandler(FileHandler):
    """
    Handles LogRecord objects with fixed PickleFormatter
    """

    def __init__(self, *args, **kwargs):  # TODO: ensure mode is set to binary
        super().__init__(*args, **kwargs)
        self.setFormatter(PickleFormatter())
        self.terminator: bytes = b""  # must be empty to match chunk size

    def yield_chunks(self):  # TODO: lock file for reading
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

    def setFormatter(self, fmt: Formatter) -> None:
        assert isinstance(fmt, PickleFormatter), "PickleFormatter is required"
        super().setFormatter(fmt)
