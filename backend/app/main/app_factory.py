import ssl

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from containers import Container
from middleware.exception_handlers import log_server_errors, validation_error_handler
from routers import router

__all__ = "create_app",

# TODO: CORS/SSL for DEV/PROD ENVS
def create_app() -> FastAPI:
    container = Container()
    container.init_resources()
    config = container.config()

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile='/shared/dev_cert.pem', keyfile='/shared/dev_key.pem')

    app = FastAPI(title=config["project_name"])
    app.container = container
    app.include_router(router)
    app.middleware("http")(log_server_errors)
    app.exception_handler(RequestValidationError)(validation_error_handler)

    # config.get("environment", "production") -> DEV/PROD CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://localhost:4200"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        max_age=86_400 # cache preflight requests for 1 day
    )
    app.add_middleware(HTTPSRedirectMiddleware)

    return app
