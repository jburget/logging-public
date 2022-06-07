from logging import LogRecord


def test_bracket_style_adapter(bracket_adapter):
    print()
    x = "x_value"
    y = "y_value"
    z = "z_value"

    # bracket_adapter.setLevel(40)
    # bracket_adapter.logger.handlers = []

    bracket_adapter.debug("debug long message {} || {}", x, y)
    bracket_adapter.debug("debug long message {1} || {0}", x, y)

    bracket_adapter.info("{y} info long message {x}", x=x, y=y)
    bracket_adapter.info("{x} info long message {y}", x=x, y=y)

    bracket_adapter.info("{} info long message {y}", x, y=y)

    bracket_adapter.warning("{} warning long message {}, {key}", "bracket", "next bracket", key="key")

    bracket_adapter.error("error long message")
    print()
    bracket_adapter.critical("critical long message")


def test_dollar_style_adapter(dollar_adapter):
    print()
    x = "x_value"
    y = "y_value"
    z = "z_value"

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
