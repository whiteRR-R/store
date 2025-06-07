from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import Provide, inject
from application.dtos.product_dto import CreateProductDTO, ProductDTO
from application.interfaces.usecases.product_use_cases import (
    CreateProductUseCaseProtocol, GetAllProductsUseCaseProtocol,
    GetProductByIdUseCaseProtocol, DeleteProductUseCaseProtocol
)
from container import Container


router = APIRouter(tags=["products"])


@router.post(
    "/products/",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_product(
    product_dto: CreateProductDTO,
    use_case: CreateProductUseCaseProtocol = Depends(
        Provide[Container.create_product_use_case]
    ),
):
    await use_case.execute(product_dto=product_dto)


@router.get(
    "/products/",
    response_model=List[ProductDTO],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all_products(
    use_case: GetAllProductsUseCaseProtocol = Depends(
        Provide[Container.get_all_product_use_case]
    ),
) -> List[ProductDTO]:
    return await use_case.execute()


@router.get(
    "/products/{product_id}",
    response_model=ProductDTO,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_product_by_id(
    product_id: UUID,
    use_case: GetProductByIdUseCaseProtocol = Depends(
        Provide[Container.get_by_id_product_use_case]
    ),
) -> ProductDTO:
    return await use_case.execute(product_id=product_id)


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_product_by_id(
    product_id: UUID,
    use_case: DeleteProductUseCaseProtocol = Depends(
        Provide[Container.delete_product_use_case]
    ),
):
    await use_case.execute(product_id=product_id)
