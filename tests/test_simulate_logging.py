from pytest import fixture
from logging import getLogger


@fixture
def construct_logging_system(colored_terminal_handler, pickle_writer):
    root = getLogger(__name__)
    root.addHandler(colored_terminal_handler)
    root.addHandler(pickle_writer)
