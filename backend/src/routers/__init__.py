from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from .products import router as product_router
from .users import router as user_router


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(product_router)
api_router.include_router(user_router)

root_router = APIRouter()

@root_router.get("/")
def root():
    return RedirectResponse(url="/docs")