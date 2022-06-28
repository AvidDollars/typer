import logging
from datetime import date
from os import makedirs, path


def get_logger(*, level, fmt, out_folder):
    logger = logging.getLogger("app_logger")
    logger.setLevel(level)

    if level == "DEBUG":
        handler = logging.StreamHandler()
    else:
        makedirs(out_folder, exist_ok=True)
        handler = logging.FileHandler(filename=path.join(out_folder, f"{date.today()}.log"))

    logger.addHandler(handler)

    formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)

    return logger
