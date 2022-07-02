from os import path

from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Singleton, Resource, Factory
from passlib.hash import argon2

from .constants import APP_DIR, CONFIG_FILE_NAME, LOG_DIR
from .db import Database
from .logger import get_logger
from .repositories import UserRepository
from .services import UserRegistrationEmailService, UserService, HashingService, AuthService


class Container(DeclarativeContainer):
    """ dependency injection container """

    # WIRING CONFIG
    wiring_config = WiringConfiguration(packages=[".routers", ".middleware"])

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

    # REPOSITORIES
    user_repository = Factory(
        UserRepository,
        registration_token_expiration=config.registration_token_expiration_in_hours,
        db=db
    )

    # SERVICES
    user_registration_email_service = Factory(
        UserRegistrationEmailService,
        email_config=config.smtp,
    )

    hashing_service = Singleton(
        HashingService,
        algorithm=argon2,
        pepper=config.pepper
    )

    auth_service = Factory(
        AuthService,
        secret=config.secret,
        token_expiration=config.jwt_token_expiration_in_hours
    )

    user_service = Factory(
        UserService,
        hashing_service=hashing_service,
        auth_service=auth_service,
        repository=user_repository
    )
