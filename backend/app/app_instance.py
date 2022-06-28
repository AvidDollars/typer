from fastapi import FastAPI
from .containers import Container


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container

    # for logging to file -> change "level" field from "DEBUG" to "INFO" | "WARNING" | "ERROR" | "CRITICAL"
    # example of usage -> app.logger.warning("description")
    app.logger = container.logger()

    return app
