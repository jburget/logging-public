from logging import LogRecord

import pytest


def test_bracket_style_adapter(brace_adapter, colored_terminal_handler):
    print()
    brace_adapter.logger.addHandler(colored_terminal_handler)
    x = "x_value"
    y = "y_value"

    brace_adapter.debug("debug long message {} || {}", x, y)
    brace_adapter.debug("debug long message {1} || {0}", x, y)

    brace_adapter.info("{y} info long message {x}", x=x, y=y)
    brace_adapter.info("{x} info long message {y}", x=x, y=y)

    brace_adapter.info("{} info long message {y}", x, y=y)

    brace_adapter.warning("{} warning long message {}, {key}", "bracket", "next bracket", key="key")

    brace_adapter.error("error long message")
    print()
    brace_adapter.critical("critical long message")


def test_dollar_style_adapter(dollar_adapter):
    print()
    x = "x_value"
    y = "y_value"

    dollar_adapter.debug("debug long message $x || $y", x=x, y=y)
    dollar_adapter.debug("debug long message $x", x=x, y=y)


def test_extras_log_record(logger, queue_handler, queue_iterator):
    print()
    logger.addHandler(queue_handler)
    logger.info("info long message", extra={"key": "value"})

    for record in queue_iterator:
        assert isinstance(record, LogRecord)
        assert hasattr(record, "key")
        assert record.key == "value"


@pytest.mark.dependency
def test_process(style_adapter, queue_iterator):
    print()

    style_adapter.debug("debug long message", extra={"id": 1234})
    for log in queue_iterator:
        assert log.id == 1234
    style_adapter.info("info long message", extra={"id": 1})
    for log in queue_iterator:
        assert log.id == 1

    style_adapter.extra = {"key": "value"}  # now every log."key"="value"

    style_adapter.warning("warning long message")
    style_adapter.error("error long message")
    style_adapter.critical("critical long message")
    for log in queue_iterator:
        assert log.key == "value"

    style_adapter.debug("debug long message", extra={"id": 1234})
    for log in queue_iterator:
        assert log.id == 1234
        assert log.key == "value"

    style_adapter.extra["id"] = 1  # should be overwritten
    style_adapter.info("info long message", extra={"id": 2})
    for log in queue_iterator:
        assert log.id == 2
        assert log.key == "value"


@pytest.mark.dependency(depends=["test_process"])
def test_brace_adapter(brace_adapter, queue_iterator, colored_terminal_handler):
    brace_adapter.logger.addHandler(colored_terminal_handler)
    print()
    brace_adapter.debug("debug long message {}, {}", "arg1", "arg2", extra={"id": 1234})
    brace_adapter.debug("debug long message {1}, {0}", "arg2", "arg1", extra={"id": 1234})
    for log in queue_iterator:
        assert log.message == "debug long message arg1, arg2"
        assert log.msg == "debug long message arg1, arg2"

    # crazy formatting
    brace_adapter.debug("debug long message {key}: {value}", key="key", value="value", extra={"id": 1234})
    brace_adapter.debug("debug long message {}: {value}", "key", value="value", extra={"id": 1234})
    brace_adapter.debug("debug long message {key}: {}", "value", key="key", extra={"id": 1234})
    brace_adapter.debug("debug long message {key}: {1}", "text", "value", key="key", extra={"id": 1234})
    for log in queue_iterator:
        assert log.message == "debug long message key: value"
        assert log.msg == "debug long message key: value"


def test_use_extras_to_format_message(brace_adapter, queue_iterator, colored_terminal_handler):
    print()
    brace_adapter.logger.addHandler(colored_terminal_handler)
    brace_adapter.debug("debug long message {key}", extra={"key": "value"})

    brace_adapter.extra = {"id": 1234}
    brace_adapter.debug("debug long message {id}", extra={"key": "value"})
    brace_adapter.debug("debug long message {id}, {key}", extra={"key": "value"})
    brace_adapter.debug("debug long message {id}, {key}, {var}", var="something", extra={"key": "value"})


def test_adapters_chaining(style_adapter):
    print()
