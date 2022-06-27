from fastapi import FastAPI
from .containers import Container


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container
    return app
