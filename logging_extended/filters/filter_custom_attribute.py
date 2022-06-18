from logging import Filter


class LogRecordTagger(Filter):

    def __init__(self, tag_name: str, tag_value, safe_mode: bool = True):
        super().__init__()
        self.tag_name: str = tag_name
        self.tag_value = tag_value
        self.safe_mode: bool = safe_mode

    def filter(self, log_record):
        if self.safe_mode and hasattr(log_record, self.tag_name):
            raise ValueError("Attempt to overwrite existing LogRecord attribute via LogRecordTagger")
        setattr(log_record, self.tag_name, self.tag_value)
        return True


class FuncNameTagger(LogRecordTagger):

    """
    Allows overwriting of the function name in the log record.

    This is not allowed with extra dict passed to log method.
    Should be used with LoggerAdapter.
    Should be removed in LoggerAdapter.log after logging the message.
    Useful for decorators to log actual name of the function.
    """

    def __init__(self, function_name: str):
        super().__init__('funcName', function_name, safe_mode=False)
