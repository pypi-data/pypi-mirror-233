"""Utils."""

import logging


class COLOR_FORMAT:
    RESET = '\033[0m'  # noqa
    BOLD = '\033[01m'  # noqa
    FAINT = '\033[02m'  # noqa
    ITALIC = '\033[03m'  # noqa
    UNDERLINE = '\033[04m'  # noqa

    REVERSE = '\033[07m'  # noqa
    INVISIBLE = '\033[08m'  # noqa
    STRIKETHROUGH = '\033[09m'  # noqa


class COLOR_FOREGROUND:
    BLACK = '\033[30m'  # noqa
    RED = '\033[31m'  # noqa
    GREEN = '\033[32m'  # noqa
    YELLOW = '\033[33m'  # noqa
    BLUE = '\033[34m'  # noqa
    MAGENTA = '\033[35m'  # noqa
    CYAN = '\033[36m'  # noqa
    LIGHT_GRAY = '\033[37m'  # noqa
    GRAY = '\033[90m'  # noqa
    LIGHT_RED = '\033[91m'  # noqa
    LIGHT_GREEN = '\033[92m'  # noqa
    LIGHT_YELLOW = '\033[93m'  # noqa
    LIGHT_BLUE = '\033[94m'  # noqa
    LIGHT_MAGENTA = '\033[95m'  # noqa
    LIGHT_CYAN = '\033[96m'  # noqa
    WHITE = '\033[97m'  # noqa


class COLOR_BACKGROUND:  # noqa
    BLACK = '\033[40m'  # noqa
    RED = '\033[41m'  # noqa
    GREEN = '\033[42m'  # noqa
    YELLOW = '\033[43m'  # noqa
    BLUE = '\033[44m'  # noqa
    MAGENTA = '\033[45m'  # noqa
    CYAN = '\033[46m'  # noqa
    LIGHT_GRAY = '\033[47m'  # noqa
    GRAY = '\033[100m'  # noqa
    LIGHT_RED = '\033[101m'  # noqa
    LIGHT_GREEN = '\033[102m'  # noqa
    LIGHT_YELLOW = '\033[103m'  # noqa
    LIGHT_BLUE = '\033[104m'  # noqa
    LIGHT_MAGENTA = '\033[105m'  # noqa
    LIGHT_CYAN = '\033[106m'  # noqa
    WHITE = '\033[107m'  # noqa


LEVEL_TO_FORMAT_CMDS = {
    logging.CRITICAL: [COLOR_FOREGROUND.MAGENTA, COLOR_FORMAT.BOLD],
    logging.ERROR: [COLOR_FOREGROUND.RED],
    logging.WARNING: [COLOR_FOREGROUND.YELLOW],
    logging.INFO: [COLOR_FOREGROUND.GREEN],
    logging.DEBUG: [COLOR_FOREGROUND.GRAY, COLOR_FORMAT.FAINT],
    logging.NOTSET: [COLOR_FOREGROUND.GRAY],
}


class CustomLoggingFormatter(logging.Formatter):
    def format(self, record):
        format_cmds = LEVEL_TO_FORMAT_CMDS[record.levelno]
        return (
            ''.join(format_cmds)
            + (f'[{record.name}] ' if record.name else '')
            + record.msg
            + COLOR_FORMAT.RESET
        )


class Log(logging.Logger):
    def __init__(self, name: str, level: int = logging.DEBUG):
        super(Log, self).__init__(name, level)
        self.propagate = False

        formatter = CustomLoggingFormatter()
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(formatter)
        self.handlers = [sh]  # noqa


_log = Log('')
