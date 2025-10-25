from uuid import UUID
from fastapi import APIRouter, status
from dishka.integrations.fastapi import FromDishka, inject
from application.dtos.attribute_dto import AttributeDTO
from application.usecases.attribute.create_attribute_use_case import CreateAttributeUseCase
from application.usecases.attribute.delete_attribute_use_case import DeleteAttributeUseCase
from application.usecases.attribute.get_all_attribute_use_case import GetAllAttributeUseCase


router = APIRouter(tags=["attributes"])


@router.post("/attributes", status_code=status.HTTP_201_CREATED)
@inject
async def create_attribute(
    attribute_dto: AttributeDTO,
    use_case: FromDishka[CreateAttributeUseCase]
):
    await use_case.execute(attribute_dto)


@router.get("/attributes", status_code=status.HTTP_200_OK)
@inject
async def get_all_attributes(
    use_case: FromDishka[GetAllAttributeUseCase]
):
    attributes = await use_case.execute()
    return attributes


@router.delete("/attributes/{attribute_id}", status_code=status.HTTP_200_OK)
@inject
async def delete_attribute_by_id(
    attribute_id: UUID,
    use_case: FromDishka[DeleteAttributeUseCase]
):
    await use_case.execute(attribute_id)
