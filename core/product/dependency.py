from functools import lru_cache
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from application.interfaces.usecases.brand_use_cases import CreateBrandUseCaseProtocol, DeleteBrandUseCaseProtocol, GetAllBrandsUseCaseProtocol
from application.interfaces.usecases.category_use_cases import CreateCategoryUseCaseProtocol, DeleteCategoryUseCaseProtocol, GetAllCategoriesUseCaseProtocol
from presentation.stub import Stub
from domain.interfaces.repositories.attribute_repository import AttributeRepositoryProtocol
from domain.interfaces.repositories.brand_repository import BrandRepositoryProtocol
from domain.interfaces.repositories.category_repository import CategoryRepositoryProtocol
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol
from domain.interfaces.storages.s3_image_storage import S3ImageStorageProtocol
from application.usecases.brand.create_brand_use_case import CreateBrandUseCase
from application.usecases.brand.delete_brand_use_case import DeleteBrandUseCase
from application.usecases.brand.get_all_brand_use_case import GetAllBrandUseCase
from application.usecases.category.create_category_use_case import CreateCategoryUseCase
from application.usecases.category.delete_category_use_case import DeleteCategoryUseCase
from application.usecases.category.get_all_category_use_case import GetAllCategoryUseCase
from application.usecases.product.add_product_attribute_use_case import AddProductAttributeUseCase
from application.usecases.product.add_product_image_use_case import AddProductImageUseCase
from application.usecases.product.delete_product_attribute_use_case import DeleteProductAttributeUseCase
from application.usecases.product.delete_product_image_use_case import DeleteProductImageUseCase
from application.usecases.product.delete_product_use_case import DeleteProductUseCase
from application.usecases.product.get_all_product_use_case import GetAllProductUseCase
from application.usecases.product.get_by_id_product_use_case import GetByIdProductUseCase
from application.usecases.product.update_product_description_use_case import UpdateProductDescriptionUseCase
from application.usecases.product.update_product_price_use_case import UpdateProductPriceUseCase
from application.usecases.product.create_product_use_case import CreateProductUseCase
from application.interfaces.usecases.product_use_cases import AddProductAttributeUseCaseProtocol, AddProductImageUseCaseProtocol, CreateProductUseCaseProtocol, DeleteProductAttributeUseCaseProtocol, DeleteProductImageUseCaseProtocol, DeleteProductUseCaseProtocol, GetAllProductsUseCaseProtocol, GetProductByIdUseCaseProtocol, UpdateProductDescriptionUseCaseProtocol, UpdateProductPriceUseCaseProtocol
from infrastructure.persistence.database import Database
from infrastructure.persistence.repository.brand_repository import SQLAlchemyBrandRepository
from infrastructure.persistence.repository.product_repository import SQLAlchemyProductRepository
from infrastructure.persistence.repository.category_repository import SQLAlchemyCategoryRepository
from infrastructure.persistence.repository.attribute_repository import SQLAlchemyAttributeRepository
from infrastructure.storage.s3_storage import S3ImageStorage
from config import config_manager


@lru_cache
def create_database():
    return Database(database_url=config_manager.database.URL)


async def get_session(database: Database = Depends(create_database)):
    async with database.get_session() as session:
        yield session
 
        
@lru_cache
def create_s3_storage(
    bucket_name: str,
    endpoint_url: str,
    access_key: str,
    secret_key: str,
):
    return S3ImageStorage(
        bucket_name=bucket_name,
        endpoint_url=endpoint_url,
        access_key=access_key,
        secret_key=secret_key,
    )
async def create_product_repository(session: AsyncSession = Depends(Stub(AsyncSession))):
    return SQLAlchemyProductRepository(session)


async def create_brand_repository(session: AsyncSession = Depends(Stub(AsyncSession))):
    return SQLAlchemyBrandRepository(session)


async def create_category_repository(session: AsyncSession = Depends(Stub(AsyncSession))):
    return SQLAlchemyCategoryRepository(session)


async def create_attribute_repository(session: AsyncSession = Depends(Stub(AsyncSession))):
    return SQLAlchemyAttributeRepository(session)


async def get_create_product_use_case(
    product_repository: ProductRepositoryProtocol = Depends(Stub(ProductRepositoryProtocol)),
    category_repository: CategoryRepositoryProtocol = Depends(Stub(CategoryRepositoryProtocol)),
    brand_repository: BrandRepositoryProtocol = Depends(Stub(BrandRepositoryProtocol)),
    attribute_repository: AttributeRepositoryProtocol = Depends(Stub(AttributeRepositoryProtocol))
):
    return CreateProductUseCase(
        product_repository=product_repository,
        category_repository=category_repository,
        brand_repository=brand_repository,
        attribute_repository=attribute_repository
    )


async def get_all_product_use_case(
    product_repository: ProductRepositoryProtocol = Depends(Stub(ProductRepositoryProtocol)),
):
    return GetAllProductUseCase(product_repository=product_repository)


async def get_by_id_product_use_case(
    product_repository: ProductRepositoryProtocol = Depends(Stub(ProductRepositoryProtocol)),
):
    return GetByIdProductUseCase(product_repository=product_repository)


async def get_delete_product_use_case(
    product_repository: ProductRepositoryProtocol = Depends(Stub(ProductRepositoryProtocol)),
):
    return DeleteProductUseCase(product_repository=product_repository)


async def get_create_category_use_case(
    category_repository: CategoryRepositoryProtocol = Depends(Stub(CategoryRepositoryProtocol)),
):
    return CreateCategoryUseCase(category_repository=category_repository)


async def get_all_category_use_case(
    category_repository: CategoryRepositoryProtocol = Depends(Stub(CategoryRepositoryProtocol)),
):
    return GetAllCategoryUseCase(category_repository=category_repository)


async def get_delete_category_use_case(
    category_repository: CategoryRepositoryProtocol = Depends(Stub(CategoryRepositoryProtocol)),
):
    return DeleteCategoryUseCase(category_repository=category_repository)


async def get_create_brand_use_case(
    brand_repository: BrandRepositoryProtocol = Depends(Stub(BrandRepositoryProtocol)),
):
    return CreateBrandUseCase(brand_repository=brand_repository)


async def get_all_brand_use_case(
    brand_repository: BrandRepositoryProtocol = Depends(Stub(BrandRepositoryProtocol)),
):
    return GetAllBrandUseCase(brand_repository=brand_repository)


async def get_delete_brand_use_case(
    brand_repository: BrandRepositoryProtocol = Depends(Stub(BrandRepositoryProtocol)),
):
    return DeleteBrandUseCase(brand_repository=brand_repository)


async def get_add_product_attribute_use_case(
    product_repository: ProductRepositoryProtocol = Depends(Stub(ProductRepositoryProtocol)),
):
    return AddProductAttributeUseCase(product_repository=product_repository)


async def get_delete_product_attribute_use_case(
    product_repository: ProductRepositoryProtocol = Depends(Stub(ProductRepositoryProtocol)),
):
    return DeleteProductAttributeUseCase(product_repository=product_repository)


async def get_update_product_description_use_case(
    product_repository: ProductRepositoryProtocol = Depends(Stub(ProductRepositoryProtocol)),
):
    return UpdateProductDescriptionUseCase(product_repository=product_repository)


async def get_update_product_price_use_case(
    product_repository: ProductRepositoryProtocol = Depends(Stub(ProductRepositoryProtocol)),
):
    return UpdateProductPriceUseCase(product_repository=product_repository)


async def get_add_product_image_use_case(
    product_repository: ProductRepositoryProtocol = Depends(Stub(ProductRepositoryProtocol)),
    s3_storage: S3ImageStorageProtocol = Depends(Stub(S3ImageStorageProtocol)),
):
    return AddProductImageUseCase(
        product_repository=product_repository,
        s3_storage=s3_storage,
    )


async def get_delete_product_image_use_case(
    product_repository: ProductRepositoryProtocol = Depends(Stub(ProductRepositoryProtocol)),
    s3_storage: S3ImageStorageProtocol = Depends(Stub(S3ImageStorageProtocol)),
):
    return DeleteProductImageUseCase(
        product_repository=product_repository,
        s3_storage=s3_storage,
    )


def all_dependencies(app: FastAPI):
    app.dependency_overrides[Database] = create_database
    app.dependency_overrides[AsyncSession] = get_session
    app.dependency_overrides[ProductRepositoryProtocol] = create_product_repository
    app.dependency_overrides[CategoryRepositoryProtocol] = create_category_repository
    app.dependency_overrides[BrandRepositoryProtocol] = create_brand_repository
    app.dependency_overrides[AttributeRepositoryProtocol] = create_attribute_repository
    app.dependency_overrides[S3ImageStorageProtocol] = create_s3_storage

    app.dependency_overrides[CreateProductUseCaseProtocol] = get_create_product_use_case
    app.dependency_overrides[GetAllProductsUseCaseProtocol] = get_all_product_use_case
    app.dependency_overrides[GetProductByIdUseCaseProtocol] = get_by_id_product_use_case
    app.dependency_overrides[DeleteProductUseCaseProtocol] = get_delete_product_use_case

    app.dependency_overrides[CreateCategoryUseCaseProtocol] = get_create_category_use_case
    app.dependency_overrides[GetAllCategoriesUseCaseProtocol] = get_all_category_use_case
    app.dependency_overrides[DeleteCategoryUseCaseProtocol] = get_delete_category_use_case

    app.dependency_overrides[CreateBrandUseCaseProtocol] = get_create_category_use_case
    app.dependency_overrides[GetAllBrandsUseCaseProtocol] = get_all_brand_use_case
    app.dependency_overrides[DeleteBrandUseCaseProtocol] = get_delete_brand_use_case

    app.dependency_overrides[AddProductAttributeUseCaseProtocol] = get_add_product_attribute_use_case
    app.dependency_overrides[DeleteProductAttributeUseCaseProtocol] = get_delete_product_attribute_use_case
    app.dependency_overrides[UpdateProductDescriptionUseCaseProtocol] = get_update_product_description_use_case
    app.dependency_overrides[UpdateProductPriceUseCaseProtocol] = get_update_product_price_use_case
    app.dependency_overrides[AddProductImageUseCaseProtocol] = get_add_product_image_use_case
    app.dependency_overrides[DeleteProductImageUseCaseProtocol] = get_delete_product_image_use_case
