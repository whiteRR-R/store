from uuid import UUID
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.address import Address
from domain.interfaces.repositories.address_repository import AddressRepository
from infrastructure.persistence.datamappers.address_datamapper import AddressDataMapper
from infrastructure.persistence.models.address_model import AddressModel


class SQLAlchemyAddressRepository(AddressRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.address_datamapper = AddressDataMapper()

    async def add(self, address: Address):
        address_model = self.address_datamapper.to_model(address)
        self.session.add(address_model)
        await self.session.refresh(address_model)

    async def get_by_id(self, address_id: UUID) -> Address | None:
        stmt = select(AddressModel).where(AddressModel.id == address_id)
        result = await self.session.execute(stmt)
        address = result.scalar_one_or_none()
        return self.address_datamapper.to_entity(address) if address else None

    async def update(self, address: Address):
        address_model = self.address_datamapper.to_model(address)
        await self.session.merge(address_model)

    async def delete(self, address_id: UUID):
        stmt = delete(AddressModel).where(AddressModel.id == address_id)
        await self.session.execute(stmt)
