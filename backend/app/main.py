from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from .containers import Container
from .middleware.exception_handlers import log_server_errors, validation_error_handler
from .routers import router


def create_app() -> FastAPI:

    app = FastAPI()
    app.include_router(router)

    app.middleware("http")(log_server_errors)
    app.exception_handler(RequestValidationError)(validation_error_handler)

    container = Container()
    app.container = container

    return app


app = create_app()
