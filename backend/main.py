from fastapi import FastAPI
from application import create_app
from prometheus_fastapi_instrumentator import Instrumentator
from src.routers import api_router, root_router
from src.auth.router import router as auth_router

app = create_app()

# if __name__ == "__main__":
#     app.run()

app = FastAPI()

Instrumentator().instrument(app).expose(app)
app.include_router(api_router)
app.include_router(root_router)
app.include_router(auth_router)
