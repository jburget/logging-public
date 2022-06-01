import json
from logging import Formatter
from logging import LogRecord


# https://github.com/python/cpython/blob/02b5417f1107415abaf81acab7522f9aa84269ea/Lib/logging/__init__.py#L668


class JsonFormatter(Formatter):

    def format(self, record: LogRecord) -> str:

        # https://github.com/python/cpython/blob/8a221a853787c18d5acaf46f5c449d28339cde21/Lib/logging/handlers.py#L627

        ei = record.exc_info
        if ei:
            # just to get traceback text into record.exc_text ...
            dummy = self.format(record)
        # See issue #14436: If msg or args are objects, they may not be
        # available on the receiving end. So we convert the msg % args
        # to a string, save it as msg and zap the args.
        d = dict(record.__dict__)
        d['msg'] = record.getMessage()
        d['args'] = None
        d['exc_info'] = None
        # Issue #25685: delete 'message' if present: redundant with 'msg'
        d.pop('message', None)

        # now my own code
        data = d
        # convert to string only objects, that are not supported by json, exclude all functions
        # some problems with deleting item from iterated list: solved with this sad syntax
        for key in list(data.keys()):
            value = data[key]
            if value is None or isinstance(value, (str, float, int, list, dict, bool)):
                continue
            else:
                data[key] = str(value)
        return json.dumps(data, skipkeys=True)
