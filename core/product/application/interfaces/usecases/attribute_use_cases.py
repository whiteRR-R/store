from typing import Protocol
from uuid import UUID
from application.dtos.attribute_dto import AttributeDTO


class CreateAttributeUseCaseProtocol(Protocol):
    async def execute(self, attribute_dto: AttributeDTO):
        ...


class DeleteAttributeUseCaseProtocol(Protocol):
    async def execute(self, id: UUID):
        ...


class GetAllAttributeUseCaseProtocol(Protocol):
    async def execute(self):
        ...
