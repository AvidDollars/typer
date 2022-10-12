from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from ..containers import Container
from ..middleware.exception_handlers import log_server_errors, validation_error_handler
from ..routers import router

__all__ = "create_app",


def create_app() -> FastAPI:
    container = Container()
    config = container.config()

    app = FastAPI(title=config.get("project_name") or "default name")
    app.container = container
    app.include_router(router)
    app.middleware("http")(log_server_errors)
    app.exception_handler(RequestValidationError)(validation_error_handler)

    return app
