from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from domain.interfaces.product_repository import ProductRepositoryInterface
from domain.entities.product import Product
from infrastructure.persistence.models.product import ProductModel


class ProductRepository(ProductRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def create(self, product: Product):
        new_product = ProductModel(product)
        return new_product
    
    async def update(self, product: Product):
        update_data = {
            "name": product.name,
            "description": product.description,
            "category": product.category.name,
            "price": product.price,
            "quantity": product.quantity,
        }
    
        result = await self.session.execute(
            update(ProductModel)
            .where(ProductModel.name == product.name)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        
        if result.rowcount == 0:
            raise NoResultFound(f"User with id {product.name} not found.")

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