from dishka import Provider, Scope, provide
from domain.interfaces.repositories.attribute_repository import AttributeRepositoryProtocol
from domain.interfaces.repositories.brand_repository import BrandRepositoryProtocol
from domain.interfaces.repositories.category_repository import CategoryRepositoryProtocol
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from infrastructure.persistence.repository.product_repository import SQLAlchemyProductRepository
from infrastructure.persistence.repository.attribute_repository import SQLAlchemyAttributeRepository
from infrastructure.persistence.repository.brand_repository import SQLAlchemyBrandRepository
from infrastructure.persistence.repository.category_repository import SQLAlchemyCategoryRepository


class RepositoryProvider(Provider):
    scope = Scope.REQUEST
    
    product_repository = provide(SQLAlchemyProductRepository, provides=ProductRepositoryProtocol)
    attribute_repository = provide(SQLAlchemyAttributeRepository, provides=AttributeRepositoryProtocol)
    brand_repository = provide(SQLAlchemyBrandRepository, provides=BrandRepositoryProtocol)
    category_repository = provide(SQLAlchemyCategoryRepository, provides=CategoryRepositoryProtocol)
