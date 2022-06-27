from os import path

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton

from .constants import APP_DIR, CONFIG_FILE_NAME
from .db import Database


class Container(DeclarativeContainer):
    """
    dependency injection container
    """

    config = Configuration(yaml_files=[path.join(APP_DIR, CONFIG_FILE_NAME)])

    db = Singleton(
        Database,
        db_url=config.db_url,
        environment=config.environment
    )

