from logging import Filter


class LevelFilter(Filter):
    """Returns True if the log record's level is equal to level attribute."""

    # https://stackoverflow.com/questions/8162419/python-logging-specific-level-only
    def __init__(self, level: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__level: int = level

    def filter(self, log_record):
        return log_record.levelno == self.__level
