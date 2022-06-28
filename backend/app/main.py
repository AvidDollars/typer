from fastapi import FastAPI

from .containers import Container
from .routers import router


def create_app() -> FastAPI:

    app = FastAPI()
    app.include_router(router)

    container = Container()
    app.container = container

    return app


app = create_app()
