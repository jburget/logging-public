from logging import Filter


class LogRecordTag(Filter):

    def __init__(self, tag_name: str, tag_value):
        super().__init__()
        self.tag_name: str = tag_name
        self.tag_value = tag_value

    def filter(self, log_record):
        setattr(log_record, self.tag_name, self.tag_value)
        return True
