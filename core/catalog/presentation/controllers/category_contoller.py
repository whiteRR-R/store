from domain.interfaces.category_service import CategoryServiceProtocol
from presentation.requests.category_create import CategoryCreateRequest
from presentation.responses.categories import CategoriesResponse
from fastapi import APIRouter


class CategoryController:
    def __init__(self, category_service: CategoryServiceProtocol):
        self.router = APIRouter()
        self.category_service = category_service
        
        self.router.add_api_route(
            path="/categories",
            endpoint=self.add_category,
            methods=["POST"],
        )
    
        self.router.add_api_route(
            path="/categories",
            endpoint=self.get_all_categories,
            methods=["GET"],
            response_model=CategoriesResponse,
        )
        
    async def add_category(self, category: CategoryCreateRequest):
        """Add a new category."""
        await self.category_service.add_category(name=category.name, description=category.description)
    
    async def get_all_categories(self) -> CategoriesResponse:
        """Retrieve all categories."""
        categories = await self.category_service.get_all_categories()
        return categories
