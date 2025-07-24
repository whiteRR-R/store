from uuid import UUID
from fastapi import APIRouter, status
from dishka.integrations.fastapi import FromDishka, inject
from application.dtos.category_dto import CreateCategoryDTO, CategoryDTO
from application.usecases.category.create_category_use_case import CreateCategoryUseCase
from application.usecases.category.delete_category_use_case import DeleteCategoryUseCase
from application.usecases.category.get_all_category_use_case import GetAllCategoryUseCase


router = APIRouter(tags=["categories"])


@router.post("/categories", status_code=status.HTTP_201_CREATED)
@inject
async def create_category(
    category: CreateCategoryDTO,
    use_case: FromDishka[CreateCategoryUseCase]
):
    return await use_case.execute(category_dto=category)


@router.get("/categories", response_model=list[CategoryDTO], status_code=status.HTTP_200_OK)
@inject
async def get_all_categories(
    use_case: FromDishka[GetAllCategoryUseCase],
) -> list[CategoryDTO]:
    return await use_case.execute()


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_category(
    category_id: UUID,
    use_case: FromDishka[DeleteCategoryUseCase],
) -> None:
    await use_case.execute(category_id=category_id)
