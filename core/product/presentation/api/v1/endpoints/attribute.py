from uuid import UUID
from fastapi import APIRouter, Depends, status
from application.dtos.attribute_dto import AttributeDTO
from application.interfaces.usecases.attribute_use_cases import CreateAttributeUseCaseProtocol, GetAllAttributeUseCaseProtocol, DeleteAttributeUseCaseProtocol
from presentation.stub import Stub


router = APIRouter(tags=["attributes"])


@router.post("/attributes", status_code=status.HTTP_201_CREATED)
async def create_attribute(
    attribute_dto: AttributeDTO,
    use_case: CreateAttributeUseCaseProtocol = Depends(Stub(CreateAttributeUseCaseProtocol))
):
    await use_case.execute(attribute_dto)


@router.get("/attributes", status_code=status.HTTP_200_OK)
async def get_all_attributes(
    use_case: GetAllAttributeUseCaseProtocol = Depends(Stub(GetAllAttributeUseCaseProtocol))
):
    attributes = await use_case.execute()
    return attributes


@router.delete("/attributes/{attribute_id}", status_code=status.HTTP_200_OK)
async def delete_attribute_by_id(
    attribute_id: UUID,
    use_case: DeleteAttributeUseCaseProtocol = Depends(Stub(DeleteAttributeUseCaseProtocol))
):
    await use_case.execute(attribute_id)
