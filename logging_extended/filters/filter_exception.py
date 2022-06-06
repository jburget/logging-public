from logging import Filter


class Filter_exception(Filter):
    """
    by default return True, if log record has exc_info
    if reverse is True, return False, if log record has exc_info
    """

    def __init__(self, reverse: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reverse: bool = reverse

    def filter(self, log_record):
        # https://stackoverflow.com/questions/47432006/logging-exception-filters-in-python
        if self.reverse:
            return log_record.exc_info is None
        return log_record.exc_info is not None
