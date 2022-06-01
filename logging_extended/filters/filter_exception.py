from logging import Filter


class Filter_exception(Filter):
    """
    https://stackoverflow.com/questions/47432006/logging-exception-filters-in-python

    by default return True, if log record has exc_info
    """

    def __init__(self, reverse: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reverse: bool = reverse

    def filter(self, log_record):
        if self.reverse:
            return log_record.exc_info is None
        return log_record.exc_info is not None
