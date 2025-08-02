from typing import List
from uuid import UUID
from fastapi import APIRouter, status
from dishka.integrations.fastapi import FromDishka, inject
from application.dtos.brand_dto import BrandDTO, CreateBrandDTO
from application.usecases.brand.create_brand_use_case import CreateBrandUseCase
from application.usecases.brand.delete_brand_use_case import DeleteBrandUseCase
from application.usecases.brand.get_all_brand_use_case import GetAllBrandUseCase


router = APIRouter(tags=["brands"])


@router.post("/brands/", status_code=status.HTTP_201_CREATED)
@inject
async def create_brand(
    brand_dto: CreateBrandDTO,
    use_case: FromDishka[CreateBrandUseCase]
) -> UUID:
    return await use_case.execute(brand_dto=brand_dto)

@router.get(
    "/brands/",
    status_code=status.HTTP_200_OK,
    response_model=List[BrandDTO],
)
@inject
async def get_all_brands(
    use_case: FromDishka[GetAllBrandUseCase]
) -> List[BrandDTO]:
    return await use_case.execute()


@router.delete("/brands/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_brand_by_id(
    brand_id: UUID,
    use_case: FromDishka[DeleteBrandUseCase],
):
    await use_case.execute(brand_id=brand_id)
