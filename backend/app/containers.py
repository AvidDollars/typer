from os import path

from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Singleton, Resource, Factory

from .constants import APP_DIR, CONFIG_FILE_NAME, LOG_DIR
from .db import Database
from .logger import get_logger
from .services import EmailService


class Container(DeclarativeContainer):
    """
    dependency injection container
    """

    # WIRING CONFIG
    wiring_config = WiringConfiguration(packages=[".routers"])

    # CONFIG
    config = Configuration(yaml_files=[path.join(APP_DIR, CONFIG_FILE_NAME)])

    # LOGGER
    logger = Resource(
        get_logger,
        level=config.logging["level"],
        fmt=config.logging["format"],
        out_folder=LOG_DIR
    )

    # DATABASE
    db = Singleton(
        Database,
        db_url=config.db_url,
        environment=config.environment
    )

    # SERVICES
    email_service = Factory(
        EmailService,
        email_config=config.smtp,
        logger=logger
    )
