from typing import List
from uuid import UUID
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from application.dtos.brand_dto import BrandDTO, CreateBrandDTO
from application.interfaces.usecases.brand_use_cases import (
    CreateBrandUseCaseProtocol,
    GetAllBrandsUseCaseProtocol,
    DeleteBrandUseCaseProtocol
)
from presentation.stub import Stub


router = APIRouter(tags=["brands"])


@router.post("/brands/", status_code=status.HTTP_201_CREATED)
async def create_brand(
    brand_dto: CreateBrandDTO,
    use_case: CreateBrandUseCaseProtocol = Depends(Stub(CreateBrandUseCaseProtocol)),
):
    return await use_case.execute(brand_dto=brand_dto)

@router.get(
    "/brands/",
    status_code=status.HTTP_200_OK,
    response_model=List[BrandDTO],
)
async def get_all_brands(
    use_case: GetAllBrandsUseCaseProtocol = Depends(Stub(GetAllBrandsUseCaseProtocol))
) -> List[BrandDTO]:
    return await use_case.execute()


@router.delete("/brands/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand_by_id(
    brand_id: UUID,
    use_case: DeleteBrandUseCaseProtocol = Depends(Stub(DeleteBrandUseCaseProtocol)),
):
    await use_case.execute(brand_id=brand_id)
