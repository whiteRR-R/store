from typing import List, Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, status, File, UploadFile
from application.dtos.product_dto import (
    CreateProductDTO,
    DeleteImageDTO,
    ProductDTO,
    ImageDTO,
    AttributeDTO,
    )
from presentation.stub import Stub
from application.dtos.filter_dto import ProductFilterDTO
from application.interfaces.usecases.product_use_cases import (
    CreateProductUseCaseProtocol, GetAllProductsUseCaseProtocol,
    GetProductByIdUseCaseProtocol, DeleteProductUseCaseProtocol,
    AddProductAttributeUseCaseProtocol, DeleteProductAttributeUseCaseProtocol,
    UpdateProductDescriptionUseCaseProtocol, UpdateProductPriceUseCaseProtocol,
    AddProductImageUseCaseProtocol, DeleteProductImageUseCaseProtocol,
)


router = APIRouter(tags=["products"])


@router.post(
    "/products/",
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_dto: CreateProductDTO,
    use_case: Annotated[CreateProductUseCaseProtocol, Depends(Stub(CreateProductUseCaseProtocol))]
):
    await use_case.execute(product_dto=product_dto)


@router.post("/products/{product_id}/images")
async def add_product_image(
    product_id: UUID,
    use_case: Annotated[AddProductImageUseCaseProtocol, Depends(Stub(AddProductImageUseCaseProtocol))],
    images: List[UploadFile] = File(...)
):
    image_dto = [ImageDTO(file=image.file, filename=image.filename or "") for image in images]
    await use_case.execute(product_id=product_id, images=image_dto)

@router.post(
    "/products/{product_id}/attributes/",
    status_code=status.HTTP_201_CREATED,
)
async def add_product_attribute(
    product_id: UUID,
    attribute_dto: AttributeDTO,
    use_case: Annotated[AddProductAttributeUseCaseProtocol, Depends(Stub(AddProductAttributeUseCaseProtocol))]
):
    await use_case.execute(product_id=product_id, attribute_dto=attribute_dto)

@router.get(
    "/products/",
    response_model=List[ProductDTO],
    status_code=status.HTTP_200_OK,
)
async def get_all_products(
    use_case: Annotated[GetAllProductsUseCaseProtocol, Depends(Stub(GetAllProductsUseCaseProtocol))],
    filters: ProductFilterDTO = Depends(),
) -> List[ProductDTO]:
    return await use_case.execute(filters)


@router.get(
    "/products/{product_id}",
    response_model=ProductDTO,
    status_code=status.HTTP_200_OK,
)
async def get_product_by_id(
    product_id: UUID,
    use_case: Annotated[GetProductByIdUseCaseProtocol, Depends(Stub(GetProductByIdUseCaseProtocol))]
) -> ProductDTO:
    return await use_case.execute(product_id=product_id)


@router.patch(
    "/products/{product_id}/description",
    status_code=status.HTTP_200_OK,
)
async def update_product_description(
    product_id: UUID,
    description: str,
    use_case: Annotated[UpdateProductDescriptionUseCaseProtocol, Depends(Stub(UpdateProductDescriptionUseCaseProtocol))]
):    
    await use_case.execute(product_id=product_id, description=description)


@router.patch(
    "/products/{product_id}/price",
    status_code=status.HTTP_200_OK
)
async def update_product_price(
    product_id: UUID,
    price: int,
    use_case: Annotated[UpdateProductPriceUseCaseProtocol, Depends(Stub(UpdateProductPriceUseCaseProtocol))]
):
    await use_case.execute(product_id=product_id, price=price)


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_product_by_id(
    product_id: UUID,
    use_case: Annotated[DeleteProductUseCaseProtocol, Depends(Stub(DeleteProductUseCaseProtocol))]
):
    await use_case.execute(product_id=product_id)


@router.delete(
    "/products/{product_id}/attributes/{attribute_id}",
    status_code=status.HTTP_200_OK,
)
async def remove_product_attribute(
    product_id: UUID,
    attribute_id: UUID,
    attribute_dto: AttributeDTO,
    use_case: Annotated[DeleteProductAttributeUseCaseProtocol, Depends(Stub(DeleteProductAttributeUseCaseProtocol))]
):
    await use_case.execute(product_id=product_id, attribute_dto=attribute_dto)


@router.delete(
    "/products/{product_id}/image",
    status_code=status.HTTP_204_NO_CONTENT
)
async def remove_product_image(
    product_id: UUID,
    image_dto: DeleteImageDTO,
    use_case: Annotated[DeleteProductImageUseCaseProtocol, Depends(Stub(DeleteProductImageUseCaseProtocol))]
):
    await use_case.execute(product_id=product_id, image=image_dto)
