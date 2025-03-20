from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from domain.entities.product import Product
from infrastructure.persistence.models.product import ProductModel


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self):
        stmt = await self.session.execute(select(ProductModel))
        products = stmt.scalars().all()
        return products
    
    async def find_by_name(self, name: str):
        stmt = await self.session.execute(
            select(ProductModel)
            .where(ProductModel.name == name)
        )
        product = stmt.scalar_one_or_none()
        return product

    async def find_by_category(self, category: str):
        stmt = await self.session.execute(
            select(ProductModel)
            .where(ProductModel.category == category)
        )
        products = stmt.scalars().all()
        return products
