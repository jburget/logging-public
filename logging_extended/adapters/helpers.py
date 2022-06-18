from string import Template

# https://docs.python.org/3/howto/logging-cookbook.html#use-of-alternative-formatting-styles


class BraceMessage:
    def __init__(self, msg, /, *args, **kwargs):
        self.msg = msg
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        # print(f"{self.msg=}")
        # print(f"{self.args=}")
        # print(*[i.function for i in stack()[:8]])
        return str(self.msg).format(*self.args, **self.kwargs)


class DollarMessage:
    def __init__(self, fmt, /, **kwargs):
        self.fmt = fmt
        self.kwargs = kwargs

    def __str__(self):
        return Template(self.fmt).substitute(**self.kwargs)
