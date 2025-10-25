from fastapi import APIRouter
from presentation.api.v1.endpoints.user import router as user_endpoints

router = APIRouter()

router.include_router(user_endpoints, prefix="/api/v1/users", tags=["users"])
