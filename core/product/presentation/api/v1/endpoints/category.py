from uuid import UUID
from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide
from application.dtos.category_dto import CreateCategoryDTO, CategoryDTO
from application.interfaces.usecases.category_use_cases import (
    CreateCategoryUseCaseProtocol,
    GetAllCategoriesUseCaseProtocol,
    DeleteCategoryUseCaseProtocol,
)
from presentation.stub import Stub


router = APIRouter(tags=["categories"])


@router.post("/categories", status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CreateCategoryDTO,
    use_case: CreateCategoryUseCaseProtocol = Depends(Stub(CreateCategoryUseCaseProtocol))
):
    return await use_case.execute(category_dto=category)


@router.get("/categories", response_model=list[CategoryDTO], status_code=status.HTTP_200_OK)
async def get_all_categories(
    use_case: GetAllCategoriesUseCaseProtocol = Depends(Stub(GetAllCategoriesUseCaseProtocol)),
) -> list[CategoryDTO]:
    return await use_case.execute()


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    use_case: DeleteCategoryUseCaseProtocol = Depends(Stub(DeleteCategoryUseCaseProtocol)),
) -> None:
    await use_case.execute(category_id=category_id)
