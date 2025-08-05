from typing import Iterable, Protocol
from uuid import UUID


class AttributeRepositoryProtocol(Protocol):
    async def add(self, key: str):
        ...

    async def get_by_id(self, id: UUID):
        ...
    
    async def get_by_ids(self, ids: Iterable[UUID]):
        ...
    
    async def retrieve_attribute_value(self, product_id: UUID, attribute_id: UUID):
        ...
        
    async def get_all(self):
        ...
        
    async def delete(self, id: UUID):
        ...
