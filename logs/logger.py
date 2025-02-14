import time
import logging

from config import TODAY, LOG_PATH

ESC = "\x1b"
RESET = f"{ESC}[0m"
ANSI_COLORS = {
    "fg": {
        "green": f"{ESC}[1;38;5;47m",
        "pink": f"{ESC}[1;38;5;219m",
        "lime": f"{ESC}[1;38;5;154m",
        "red": f"{ESC}[1;38;5;197m",
        "violet": f"{ESC}[1;38;5;135m",
        "yellow": f"{ESC}[1;38;5;227m",
    },
    "bg": {
        "green": f"{ESC}[1;48;5;47m",
        "pink": f"{ESC}[1;48;5;219m",
        "lime": f"{ESC}[1;48;5;154m",
        "red": f"{ESC}[1;48;5;197m",
        "violet": f"{ESC}[1;48;5;135m",
        "yellow": f"{ESC}[1;48;5;227m",
        "pp": f"{ESC}[1;48;5;207m",
    },
    "reset": RESET,
}


def get_logger(name, level=logging.DEBUG, log_file=f"{LOG_PATH}{TODAY}.log"):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    formatter = logging.Formatter("%(asctime)s | %(name)s:%(lineno)d | %(levelname)s: %(message)s")
    formatter.converter = time.gmtime

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
