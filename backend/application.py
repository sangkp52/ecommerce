from fastapi import FastAPI

# from routers.users import router as users_routers
# from routers.products import router as products_routers
# from middlewares.cors import apply_cors_middleware
# from routers import api_router
# from auth.router import router as auth_router

from src.routers.users import router as users_routers
from src.routers.products import router as products_routers
from src.middlewares.cors import apply_cors_middleware
from src.routers import api_router
from src.auth.router import router as auth_router

def create_app() -> FastAPI:
    app = FastAPI()

    # Middlewares
    app = apply_cors_middleware(app)
    
    # Configuring routers
    app.include_router(api_router)
    app.include_router(auth_router)
    app.include_router(users_routers)
    app.include_router(products_routers)

    return app


@app.get("/")
def root():
    return RedirectResponse(url="/docs")