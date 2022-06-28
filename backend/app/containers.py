from os import path

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton, Resource

from .constants import APP_DIR, CONFIG_FILE_NAME
from .db import Database
from .logger import get_logger
from .constants import LOG_DIR


class Container(DeclarativeContainer):
    """
    dependency injection container
    """

    config = Configuration(yaml_files=[path.join(APP_DIR, CONFIG_FILE_NAME)])

    logger = Resource(
        get_logger,
        level=config.logging["level"],
        fmt=config.logging["format"],
        out_folder=LOG_DIR
    )

    db = Singleton(
        Database,
        db_url=config.db_url,
        environment=config.environment
    )

