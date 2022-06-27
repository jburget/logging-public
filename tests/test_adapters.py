from logging import LogRecord

import pytest
from logging_extended.adapters import StyleAdapter
from logging_extended.adapters import BraceAdapter


@pytest.mark.skip("spam output")
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


def helper_func(logger):
    logger.info("info long message")
    logger.warning("warning long message")
    try:
        raise ValueError("test value error")
    except ValueError:
        logger.exception("exception long message")


def test_function_name(style_adapter, queue_iterator, colored_terminal_handler):
    print()
    style_adapter.addHandler(colored_terminal_handler)

    style_adapter.debug("debug long message", func="test_function")
    style_adapter.info("info long message", func="test_function")
    style_adapter.warning("warning long message", func="test_function")
    for log in queue_iterator:
        assert log.funcName == "test_function"

    style_adapter.error("error long message")
    style_adapter.critical("critical long message")
    for log in queue_iterator:
        assert log.funcName == "test_function_name"

    helper_func(style_adapter)
    for log in queue_iterator:
        assert log.funcName == "helper_func"


def test_use_extras_to_format_message(brace_adapter, queue_iterator, colored_terminal_handler):
    print()
    brace_adapter.logger.addHandler(colored_terminal_handler)
    brace_adapter.debug("debug long message {key}", extra={"key": "value"})

    brace_adapter.extra = {"key": "value"}
    brace_adapter.debug("debug long message {key}")
    brace_adapter.debug("debug long message {id}", extra={"id": "value"})
    brace_adapter.debug("debug long {var} {key}", var="message", extra={"key": "value"})

    brace_adapter.debug("debug long {} {key}", "message", extra={"key": "value"})
    brace_adapter.debug("debug {1} {0} {key}", "message", "long", extra={"key": "value"})
    for log in queue_iterator:
        assert log.message == "debug long message value"


def test_adapters_chaining(brace_adapter, brace_adapter_2_chained, brace_adapter_3_chained, colored_terminal_handler, queue_iterator):
    print()
    brace_adapter_3_chained.addHandler(colored_terminal_handler)

    brace_adapter.extra = {"key": "value"}
    brace_adapter_3_chained.debug("debug long message {key}")
    brace_adapter_3_chained.debug("debug long message {id}", extra={"id": "value"})
    brace_adapter_3_chained.debug("debug long {var} {key}", var="message", extra={"key": "value"})
    brace_adapter_3_chained.debug("debug long {} {key}", "message", extra={"key": "value"})
    brace_adapter_3_chained.debug("debug {1} {0} {key}", "message", "long", extra={"key": "value"})
    for log in queue_iterator:
        assert log.message == "debug long message value"
        assert log.funcName == "test_adapters_chaining"

    brace_adapter_3_chained.extra = {"ip": 12345}
    brace_adapter_3_chained.debug("debug long message {ip}")
    for log in queue_iterator:
        assert log.message == "debug long message 12345"
        assert log.ip == 12345

    brace_adapter_2_chained.extra = {"ip": 0}
    brace_adapter_3_chained.debug("debug long message {ip}")
    for log in queue_iterator:
        assert log.message == "debug long message 12345"


def test_more_chaining(logger, queue_iterator):
    print()
    fname = "test_more_chaining"
    adapter = StyleAdapter(logger, {"key": "value"})
    adapter.info("info long message")
    adapter.warning("warning long message")
    for log in queue_iterator:
        assert log.funcName == fname
    new_adapter = StyleAdapter(adapter, {"new_key": "new value"})
    new_adapter.info("info long message")
    new_adapter.warning("warning long message")
    for log in queue_iterator:
        assert log.funcName == fname
    brand_new_adapter = StyleAdapter(new_adapter, {"brand_new_key": "brand new value"})
    brand_new_adapter.info("info long message")
    brand_new_adapter.warning("warning long message")
    for log in queue_iterator:
        assert log.funcName == fname
    brand_brand_new_adapter = StyleAdapter(brand_new_adapter, {"brand_brand_new_key": "brand brand new value"})
    brand_brand_new_adapter.info("info long message")
    brand_brand_new_adapter.warning("warning long message")
    for log in queue_iterator:
        assert log.funcName == fname


def test_crazy_mixing_chains(logger, queue_iterator, define_stats_level):
    print()
    fname = "test_crazy_mixing_chains"
    adapter = StyleAdapter(logger, {"key": "value"})
    new_adapter = StyleAdapter(adapter, {"new_key": "new value"})
    brand_new_adapter = StyleAdapter(new_adapter, {"brand_new_key": "brand new value"})
    brand_brand_new_adapter = StyleAdapter(brand_new_adapter, {"brand_brand_new_key": "brand brand new value"})
    brace_adapter = BraceAdapter(brand_brand_new_adapter, {"brace_key": "brace value"})
    brace_adapter.info("info long message")
    brace_adapter.warning("warning long message")
    for log in queue_iterator:
        assert log.funcName == fname
    new_brace_adapter = BraceAdapter(brace_adapter, {"new_brace_key": "new brace value"})
    new_brace_adapter.info("info long message")
    new_brace_adapter.warning("warning long message")
    for log in queue_iterator:
        assert log.funcName == fname

    last_style_adapter = StyleAdapter(new_brace_adapter, {"last_style_key": "last style value"})
    last_style_adapter.info("info long message")
    last_style_adapter.warning("warning long message")
    for log in queue_iterator:
        assert log.funcName == fname
    last_brace_adapter = BraceAdapter(last_style_adapter, {"last_brace_key": "last brace value"})
    last_brace_adapter.info("info long message")
    last_brace_adapter.warning("warning long message")
    for log in queue_iterator:
        assert log.funcName == fname
    very_last_brace_adapter = BraceAdapter(last_brace_adapter, {"very_last_brace_key": "very last brace value"})
    very_last_brace_adapter.info("info long message")
    very_last_brace_adapter.warning("warning long message")
    for log in queue_iterator:
        assert log.funcName == fname
    very_last_style_adapter = StyleAdapter(very_last_brace_adapter, {"very_last_style_key": "very last style value"})
    very_last_style_adapter.info("info long message")
    very_last_style_adapter.warning("warning long message")
    for log in queue_iterator:
        assert log.funcName == fname

    realy_last_style_adapter = StyleAdapter(very_last_style_adapter, {"realy_last_style_key": "realy last style value"})
    realy_last_style_adapter.info("info long message")
    realy_last_style_adapter.warning("warning long message")
    realy_last_style_adapter.stats("warning long message")
    for log in queue_iterator:
        assert log.funcName == fname
        assert log.realy_last_style_key == "realy last style value"

    realy_last_style_adapter.stats("info")
    for log in queue_iterator:
        assert log.levelno == 5

