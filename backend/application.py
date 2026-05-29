from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.routers import api_router, root_router
from src.auth.router import router as auth_router
from src.routers.users import router as users_routers
from src.routers.products import router as products_routers
from src.middlewares.cors import apply_cors_middleware


def create_app() -> FastAPI:
    app = FastAPI()

    app = apply_cors_middleware(app)

    app.include_router(api_router)
    app.include_router(root_router)
    app.include_router(auth_router)
    app.include_router(users_routers)
    app.include_router(products_routers)

    Instrumentator().instrument(app).expose(
        app,
        endpoint="/metrics",
        include_in_schema=False
    )

    return app