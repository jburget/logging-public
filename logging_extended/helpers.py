import types
from logging import Filterer
from logging import LogRecord


def _filter_if_any(self: Filterer, record: LogRecord) -> bool:
    """
    Returns True if any of filters passes
    Must be assigned to filterer with rewrite_filter_on_filterer function

    Determine if a record is loggable by consulting all the filters.
    The default is to allow the record to be logged; any filter can veto
    this and the record is then dropped. Returns a zero value if a record
    is to be dropped, else non-zero.
    .. versionchanged:: 3.2
       Allow filters to be just callables.
    :param record:
    :return: bool
    """
    for f in self.filters:
        if (
                (hasattr(f, 'filter')
                 and f.filter(record))
                or (not hasattr(f, 'filter')
                    and f(record))
        ):
            return True
    return not self.filters


def rewrite_filter_on_filterer(obj: Filterer):
    """Rewrites filter method to filter_if_any method on logging.Filterer object"""
    obj.filter = types.MethodType(_filter_if_any, obj)
