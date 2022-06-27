from logging import Filterer
from logging import LogRecord


class AnyFilterer(Filterer):

    """
    Manages list of filters, just like Handler or Logger

    :return LogRecord, if any of filters returns true or LogRecord object
    """

    def filter(self, record: LogRecord):
        filters_copy = self.filters.copy()
        results = []
        self.filters.clear()

        for f in filters_copy:
            self.addFilter(f)
            result = super().filter(record)
            results.append(result)
            if isinstance(result, LogRecord):
                record = result
            self.removeFilter(f)

        self.filters.extend(filters_copy)
        return record if any(results) else False
