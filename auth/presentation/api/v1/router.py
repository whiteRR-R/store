from fastapi import APIRouter
from presentation.api.v1.endpoints.auth import router as auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/api/v1/auth")
