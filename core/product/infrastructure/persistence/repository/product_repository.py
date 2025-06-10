from typing import List, Iterable, Optional, AsyncContextManager, Sequence
from uuid import UUID
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from domain.aggregates.product import ProductRoot
from infrastructure.persistence.models.category_model import CategoryModel
from infrastructure.persistence.models.brand_model import BrandModel
from infrastructure.persistence.models.product_model import ProductModel
from infrastructure.persistence.datamappers.product_mapper import ProductDataMapper
from infrastructure.persistence.decorators import transaction


class ProductRepository:
    def __init__(self, session_context_manager: AsyncContextManager[AsyncSession]) -> None:
        self.session_context_manager = session_context_manager
        self.mapper = ProductDataMapper()
    
    @transaction
    async def add(self,  session: AsyncSession, product: ProductRoot) -> None:
        product_model = self.mapper.entity_to_model(product)
        brands = await self._get_existing_brand(product.brand.id)
        categories = await self._get_existing_categories([category.id for category in product.categories])
        product_model.brand = brands
        product_model.categories = categories
        session.add(product_model)
        await session.commit()
    
    @transaction
    async def delete(self, session: AsyncSession, product: ProductRoot) -> None:
        await session.execute(
            delete(ProductModel).where(ProductModel.id == product.id)
        )
        await session.commit()
    
    @transaction
    async def update(self, session: AsyncSession, product: ProductRoot) -> None:
        stmt = await session.execute(
            select(
                ProductModel
            ).where(
                ProductModel.id == product.id
            ).options(
                joinedload(ProductModel.brand),
                joinedload(ProductModel.categories)   
            )
        )
        categories = self._get_existing_categories(session, [category.id for category in product.categories])
        brand = self._get_existing_brand(session, product.brand.id)
        product_model = stmt.scalars().one_or_none()
        
        if product_model and brand and categories:
            product_model.name = product.name.value
            product_model.description = product.description.value
            product_model.price = product.price.value
            product_model.attributes =  product.attributes
            product_model.brand = brand
            product_model.categories = categories
        await session.commit()
        
    @transaction
    async def get_by_id(self, session: AsyncSession, product_id: UUID) -> Optional[ProductRoot]:
        stmt = await session.execute(
            select(ProductModel).where(ProductModel.id == product_id)
        )
        product = stmt.scalars().one_or_none()
        return self.mapper.model_to_entity(product) if product else None
    
    @transaction
    async def get_all(self, session: AsyncSession) -> List[ProductRoot]:
        print("Fetching all products")
        stmt = await session.execute(select(ProductModel).options(
            joinedload(ProductModel.brand),
            joinedload(ProductModel.categories)
        ))
        print("Executing query to fetch all products")
        products = stmt.unique().scalars().all()
        print(f"Products found: {products}")
        print("ahhah", [self.mapper.model_to_entity(product) for product in products])
        return [self.mapper.model_to_entity(product) for product in products]

    @transaction
    async def _get_existing_brand(self, session: AsyncSession, brand_id: UUID) -> Optional[BrandModel]:
        stmt = await session.execute(select(BrandModel).where(BrandModel.id == brand_id))
        brand = stmt.scalars().one_or_none()
        return brand
    
    @transaction
    async def _get_existing_categories(self, session: AsyncSession, category_ids: List[UUID]) -> Sequence[CategoryModel]:
        
        stmt = await session.execute(select(CategoryModel).where(CategoryModel.id.in_(category_ids)))
        categories = stmt.scalars().all()
        
        if len(categories) != len(category_ids):
            raise ValueError("Some categories do not exist")
        return categories
        
