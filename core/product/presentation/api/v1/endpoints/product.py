from typing import Dict, List
from uuid import UUID
from fastapi import APIRouter, Body, Depends, status, File, UploadFile, Form
from dependency_injector.wiring import Provide, inject
from application.dtos.product_dto import (
    CreateProductDTO,
    DeleteImageDTO,
    ProductDTO,
    ImageDTO,
    AttributeDTO,
    )
from application.dtos.filter_dto import ProductFilterDTO
from application.interfaces.usecases.product_use_cases import (
    CreateProductUseCaseProtocol, GetAllProductsUseCaseProtocol,
    GetProductByIdUseCaseProtocol, DeleteProductUseCaseProtocol,
    AddProductAttributeUseCaseProtocol, DeleteProductAttributeUseCaseProtocol,
    UpdateProductDescriptionUseCaseProtocol, UpdateProductPriceUseCaseProtocol,
    AddProductImageUseCaseProtocol, DeleteProductImageUseCaseProtocol,
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


@router.post("/products/{product_id}/images")
@inject
async def add_product_image(
    product_id: UUID,
    images: List[UploadFile] = File(...),
    use_case: AddProductImageUseCaseProtocol = Depends(
        Provide[Container.add_product_image_use_case]
    )
):
    image_dto = [ImageDTO(file=image.file, filename=image.filename or "") for image in images]
    await use_case.execute(product_id=product_id, images=image_dto)

@router.post(
    "/products/{product_id}/attributes/",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def add_product_attribute(
    product_id: UUID,
    attribute_dto: AttributeDTO,
    use_case: AddProductAttributeUseCaseProtocol = Depends(
        Provide[Container.add_product_attribute_use_case]
    ),
):
    await use_case.execute(product_id=product_id, attribute_dto=attribute_dto)

@router.get(
    "/products/",
    response_model=List[ProductDTO],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all_products(
    filters: ProductFilterDTO = Depends(),
    use_case: GetAllProductsUseCaseProtocol = Depends(
        Provide[Container.get_all_product_use_case]
    ),
) -> List[ProductDTO]:
    return await use_case.execute(filters)


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


@router.patch(
    "/products/{product_id}/description",
    status_code=status.HTTP_200_OK,
)
@inject
async def update_product_description(
    product_id: UUID,
    description: str,
    use_case: UpdateProductDescriptionUseCaseProtocol = Depends(
        Provide[Container.update_product_description_use_case]
    ),
):    
    await use_case.execute(product_id=product_id, description=description)


@router.patch(
    "/products/{product_id}/price",
    status_code=status.HTTP_200_OK
)
@inject
async def update_product_price(
    product_id: UUID,
    price: int,
    use_case: UpdateProductPriceUseCaseProtocol = Depends(
        Provide[Container.update_product_price_use_case]
    )
):
    await use_case.execute(product_id=product_id, price=price)


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_product_by_id(
    product_id: UUID,
    use_case: DeleteProductUseCaseProtocol = Depends(
        Provide[Container.delete_product_use_case]
    ),
):
    await use_case.execute(product_id=product_id)


@router.delete(
    "/products/{product_id}/attributes/{attribute_id}",
    status_code=status.HTTP_200_OK,
)
@inject
async def remove_product_attribute(
    product_id: UUID,
    attribute_id: UUID,
    attribute_dto: AttributeDTO,
    use_case: DeleteProductAttributeUseCaseProtocol = Depends(
        Provide[Container.delete_product_attribute_use_case]
    ),
):
    await use_case.execute(product_id=product_id, attribute_dto=attribute_dto)


@router.delete(
    "/products/{product_id}/image",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def remove_product_image(
    product_id: UUID,
    image_dto: DeleteImageDTO,
    use_case: DeleteProductImageUseCaseProtocol = Depends(
        Provide[Container.delete_product_image_use_case]
    )
):
    await use_case.execute(product_id=product_id, image=image_dto)
