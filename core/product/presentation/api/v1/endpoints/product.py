from typing import List, Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, status, File, UploadFile
from dishka.integrations.fastapi import FromDishka, inject
from application.dtos.filter_dto import ProductFilterDTO
from application.dtos.product_dto import (
    CreateProductDTO,
    DeleteImageDTO,
    ProductDTO,
    ImageDTO,
    AttributeDTO,
    )
from application.usecases.product.add_product_attribute_use_case import AddProductAttributeUseCase
from application.usecases.product.add_product_image_use_case import AddProductImageUseCase
from application.usecases.product.delete_product_attribute_use_case import DeleteProductAttributeUseCase
from application.usecases.product.delete_product_image_use_case import DeleteProductImageUseCase
from application.usecases.product.delete_product_use_case import DeleteProductUseCase
from application.usecases.product.get_all_product_use_case import GetAllProductUseCase
from application.usecases.product.get_by_id_product_use_case import GetByIdProductUseCase
from application.usecases.product.update_product_description_use_case import UpdateProductDescriptionUseCase
from application.usecases.product.update_product_price_use_case import UpdateProductPriceUseCase
from application.usecases.product.create_product_use_case import CreateProductUseCase


router = APIRouter(tags=["products"])


@router.post("/products/", status_code=status.HTTP_201_CREATED,
)
@inject
async def create_product(
    product_dto: CreateProductDTO,
    use_case: FromDishka[CreateProductUseCase]
):
    await use_case.execute(product_dto=product_dto)


@router.post("/products/{product_id}/images")
@inject
async def add_product_image(
    product_id: UUID,
    use_case: FromDishka[AddProductImageUseCase],
    images: List[UploadFile] = File(...)
):
    image_dto = [ImageDTO(file=image.file, filename=image.filename or "") for image in images]
    await use_case.execute(product_id=product_id, images=image_dto)


@router.post("/products/{product_id}/attributes/", status_code=status.HTTP_201_CREATED)
@inject
async def add_product_attribute(
    product_id: UUID,
    attribute_dto: AttributeDTO,
    use_case: FromDishka[AddProductAttributeUseCase]
):
    await use_case.execute(product_id=product_id, attribute_dto=attribute_dto)


@router.get("/products/", response_model=List[ProductDTO], status_code=status.HTTP_200_OK)
@inject
async def get_all_products(
    use_case: FromDishka[GetAllProductUseCase],
    filters: ProductFilterDTO = Depends(),
) -> List[ProductDTO]:
    return await use_case.execute(filters)


@router.get("/products/{product_id}",response_model=ProductDTO,status_code=status.HTTP_200_OK)
@inject
async def get_product_by_id(
    product_id: UUID,
    use_case: FromDishka[GetByIdProductUseCase]
) -> ProductDTO:
    return await use_case.execute(product_id=product_id)


@router.patch("/products/{product_id}/description",status_code=status.HTTP_200_OK)
@inject
async def update_product_description(
    product_id: UUID,
    description: str,
    use_case: FromDishka[UpdateProductDescriptionUseCase]
):    
    await use_case.execute(product_id=product_id, description=description)


@router.patch("/products/{product_id}/price",status_code=status.HTTP_200_OK)
@inject
async def update_product_price(
    product_id: UUID,
    price: int,
    use_case: FromDishka[UpdateProductPriceUseCase]
):
    await use_case.execute(product_id=product_id, price=price)


@router.delete("/products/{product_id}",status_code=status.HTTP_200_OK)
@inject
async def delete_product_by_id(
    product_id: UUID,
    use_case: FromDishka[DeleteProductUseCase]
):
    await use_case.execute(product_id=product_id)


@router.delete("/products/{product_id}/attributes/", status_code=status.HTTP_200_OK)
@inject
async def remove_product_attribute(
    product_id: UUID,
    attribute_dto: AttributeDTO,
    use_case: FromDishka[DeleteProductAttributeUseCase]
):
    await use_case.execute(product_id=product_id, attribute_dto=attribute_dto)


@router.delete("/products/{product_id}/image",status_code=status.HTTP_204_NO_CONTENT)
@inject
async def remove_product_image(
    product_id: UUID,
    image_dto: DeleteImageDTO,
    use_case: FromDishka[DeleteProductImageUseCase]
):
    await use_case.execute(product_id=product_id, image=image_dto)
