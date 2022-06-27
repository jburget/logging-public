from logging import Filter


class ExceptionInfoFilter(Filter):
    """
    by default return True, if log record has exc_info or exc_text
    Can be reversed

    warning: in some situations, LogRecord.exc_info is removed during logging
    for this reason is better to filter logs based on level logging.ERROR
    """

    def __init__(self, reverse: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reverse: bool = reverse

    def filter(self, log_record):
        # https://stackoverflow.com/questions/47432006/logging-exception-filters-in-python
        is_exception = log_record.exc_text is not None or log_record.exc_info is not None
        if self.reverse:
            return not is_exception
        return is_exception
