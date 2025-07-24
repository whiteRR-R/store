from typing import List, Optional, AsyncContextManager, Sequence
from uuid import UUID
from sqlalchemy import select, delete, desc, asc
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from domain.aggregates.product import ProductRoot
from application.dtos.filter_dto import ProductFilterDTO, SortOrder
from infrastructure.persistence.models.category_model import CategoryModel
from infrastructure.persistence.models.brand_model import BrandModel
from infrastructure.persistence.models.product_model import ProductModel
from infrastructure.persistence.models.image_model import ProductImageModel
from infrastructure.persistence.models.association_models import AssosiationProductAttributeModel
from infrastructure.persistence.datamappers.product_mapper import ProductDataMapper
from infrastructure.exceptions import NotFoundException


class SQLAlchemyProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.mapper = ProductDataMapper()
        
    async def _get_brand(self, brand_id: UUID) -> Optional[BrandModel]:
        stmt = await self.session.execute(select(BrandModel).where(BrandModel.id == brand_id))
        return stmt.scalars().one_or_none()


    async def _get_categories(self, category_ids: List[UUID]) -> List[CategoryModel]:
        stmt = await self.session.execute(select(CategoryModel).where(CategoryModel.id.in_(category_ids)))
        categories = stmt.scalars().all()
        return list(categories)
    
    
    async def add(self, product: ProductRoot) -> None:
        product_model = self.mapper.entity_to_model(product)
        brand = await self._get_brand(product.brand.id)
        categories = await self._get_categories([category.id for category in product.categories])
        
        if not brand or not categories:
            raise NotFoundException("Brand or categories do not exist")
        
        product_model.brand = brand
        product_model.categories = categories

        self.session.add(product_model)


    async def delete(self, product: ProductRoot) -> None:
        await self.session.execute(delete(ProductModel).where(ProductModel.id == product.id))


    async def update(self, product: ProductRoot) -> None:
        stmt = await self.session.execute(
            select(ProductModel)
            .where(ProductModel.id == product.id)
            .options(
                joinedload(ProductModel.brand),
                joinedload(ProductModel.categories),
                selectinload(ProductModel.images),
            )
        )
        product_model = stmt.unique().scalars().one_or_none()

        brand = await self._get_brand(product.brand.id)
        categories = await self._get_categories([category.id for category in product.categories])

        if product_model and brand and categories:
            product_model.name = product.name.value
            product_model.description = product.description.value
            product_model.price = product.price.value
            product_model.attributes = product.attributes
            product_model.brand = brand

            product_model.categories.clear()
            product_model.categories.extend(categories)

            product_model.images.clear()
            product_model.images.extend([ProductImageModel(url=image_urls) for image_urls in product.images])


    async def get_by_id(self, product_id: UUID) -> Optional[ProductRoot]:
        stmt = await self.session.execute(
            select(ProductModel)
            .where(ProductModel.id == product_id)
            .options(
                joinedload(ProductModel.brand),
                joinedload(ProductModel.categories),
                selectinload(ProductModel.images),
                selectinload(ProductModel.attributes)
            )
        )
        product = stmt.unique().scalars().first()
        return self.mapper.model_to_entity(product) if product else None


    async def get_all(self, filters: ProductFilterDTO) -> List[ProductRoot]:
        stmt = select(ProductModel).options(
                joinedload(ProductModel.brand),
                joinedload(ProductModel.categories),
                selectinload(ProductModel.images),
                joinedload(ProductModel.attribute_links)
            )

        if filters.min_price is not None:
            stmt = stmt.where(ProductModel.price >= filters.min_price)
        if filters.max_price is not None:
            stmt = stmt.where(ProductModel.price <= filters.max_price)

        order_column = getattr(ProductModel, filters.sort_by.value)

        if filters.order == SortOrder.desc:
            stmt = stmt.order_by(desc(order_column))
        else:
            stmt = stmt.order_by(asc(order_column))

        result = await self.session.execute(stmt)
        products = result.unique().scalars().all()
        return [self.mapper.model_to_entity(product) for product in products]
