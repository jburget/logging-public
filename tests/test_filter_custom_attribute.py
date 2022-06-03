from _pytest.fixtures import fixture

from logging_extended.filters import LogRecordTag


@fixture
def tag_app_id():
    return LogRecordTag(tag_name="app_id", tag_value=12)


def test_app_id(tag_app_id, log_creator, colored_terminal_handler):
    print()
    log_creator.addHandler(colored_terminal_handler)
    log_creator.addFilter(tag_app_id)
    with log_creator as logger:
        assert hasattr(logger.debug("message"), 'app_id')
        assert logger.debug('test').app_id == 12
