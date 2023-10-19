from fastapi import APIRouter

from .users.views import router as users_router

from .products.views import router as products_router

router = APIRouter()
router.include_router(router=users_router, prefix="/users")
router.include_router(router=products_router, prefix="/products")
