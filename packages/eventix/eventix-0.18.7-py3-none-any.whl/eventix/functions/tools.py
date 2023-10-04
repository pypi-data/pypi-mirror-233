import importlib
import logging
import os
from uuid import uuid4

import pkg_resources
import toml


def uid() -> str:
    return str(uuid4()).replace("-", "")


_uid = uid


def version():
    v = importlib.metadata.version('eventix')
    return v


def setup_logging(without_time: bool = False, level: str = "INFO", module: bool = False, prefix: str = ""):
    time_str = '%(asctime)s ' if not without_time else ''
    module = '[%(name)s]' if module else ''
    f = f"{time_str}{module}[%(levelname)8s]{prefix} %(message)s"

    logging.basicConfig(
        level=level,
        format=f,
        handlers=[
            logging.StreamHandler()
        ]
    )
