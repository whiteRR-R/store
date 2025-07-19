from fastapi import APIRouter
from presentation.api.v1.endpoints.product import router as product_router
from presentation.api.v1.endpoints.brand import router as brand_router
from presentation.api.v1.endpoints.category import router as category_router
from presentation.api.v1.endpoints.attribute import router as attribute_router


router = APIRouter(prefix="/api/v1")

router.include_router(product_router)
router.include_router(brand_router)
router.include_router(category_router)
router.include_router(attribute_router)