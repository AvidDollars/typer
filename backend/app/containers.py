from os import path

from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Singleton, Resource, Factory
from passlib.hash import argon2

from .constants import APP_DIR, CONFIG_FILE_NAME, LOG_DIR
from .db import Database
from .logger import get_logger
from .repositories import UserRepository, TextRepository, TypingSessionRepository, TextRatingRepository
from .services import \
    UserRegistrationEmailService, \
    UserService, \
    HashingService, \
    JwtToken, \
    TextService, \
    TypingSessionService, \
    TextRatingService


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

    text_repository = Factory(
        TextRepository,
        db=db
    )

    typing_session_repository = Factory(
        TypingSessionRepository,
        db=db
    )

    text_rating_repository = Factory(
        TextRatingRepository,
        db=db
    )

    # SERVICES
    user_registration_email_service = Factory(
        UserRegistrationEmailService,
        email_config=config.smtp
    )

    hashing_service = Singleton(
        HashingService,
        algorithm=argon2,
        pepper=config.pepper
    )

    jwt_token = Factory(
        JwtToken,
        secret=config.secret,
        token_expiration=config.jwt_token_expiration_in_hours,
        jwt_algorithm=config.jwt_algorithm
    )

    user_service = Factory(
        UserService,
        hashing_service=hashing_service,
        jwt_token=jwt_token,
        repository=user_repository
    )

    text_service = Factory(
        TextService,
        repository=text_repository
    )

    typing_session_service = Factory(
        TypingSessionService,
        repository=typing_session_repository,
        logger=logger
    )

    text_rating_service = Factory(
        TextRatingService,
        repository=text_rating_repository
    )
