from logging import CRITICAL
from logging import DEBUG
from logging import ERROR
from logging import Formatter
from logging import INFO
from logging import WARNING
from sty import fg, Style, ef

import sty


# https://github.com/shiena/ansicolor
# https://sty.mewo.dev

fg.warning = Style(fg.li_yellow, ef.bold)
fg.info = Style(fg.li_blue, ef.bold)
fg.debug = Style(fg.white, ef.bold)
fg.error = Style(fg.red)
fg.critical = Style(fg.li_red, ef.bold)
fg.stats = Style(fg.li_magenta, ef.bold)
fg.undefined = Style(fg.li_cyan, ef.bold)


class ColorFormatter(Formatter):
    # https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
    # https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colors: dict[int, sty.register] = {
                5       : fg.stats,
                DEBUG   : fg.debug,
                INFO    : fg.info,
                WARNING : fg.warning,
                ERROR   : fg.error,
                CRITICAL: fg.critical
        }

        self.__reset: sty.register.RsRegister = sty.rs.all
        self.__undefined_color: sty.register = fg.undefined

    def format(self, record):
        log_color = self.colors.get(record.levelno, self.undefined_color)
        formatted_log = super().format(record)
        return f"{log_color}{formatted_log}{self.reset}"

    @property
    def reset(self):
        return self.__reset

    @reset.setter
    def reset(self, value):
        assert isinstance(value, sty.primitive.Style)
        self.__reset = value

    @reset.deleter
    def reset(self):
        self.__reset = sty.rs.all

    @property
    def undefined_color(self):
        return self.__undefined_color

    @undefined_color.setter
    def undefined_color(self, value: sty.register):
        assert isinstance(value, sty.register.Style)
        self.__undefined_color = value

    @undefined_color.deleter
    def undefined_color(self):
        self.__undefined_color = fg.undefined

    def __setitem__(self, key, value):
        self.colors[key] = value

    def __getitem__(self, item):
        return self.colors[item]

    def __delitem__(self, key):
        del self.colors[key]
