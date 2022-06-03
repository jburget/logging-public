from logging_extended import ColorFormatter


def test_brace_string(logger, terminalHandler):
    print()
    formatter = ColorFormatter(fmt="{levelname:^9} - {message}", style="{")

    terminalHandler.setFormatter(formatter)
    logger.addHandler(terminalHandler)
    x = "hello"
    y = 100_0000000000
    print("{x}".format(x=x))
    print(f"{x=}")
    print(f"{y:+,}")
    # https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string
    logger.debug("debug long message")
    logger.info("info long message")
    logger.warning("warning long message")
    logger.error("error long message")
    logger.critical("critical long message")
