from .app_instance import create_app
from .routers import router

app = create_app()
app.include_router(router)
