from dishka import Provider, Scope, provide
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
from application.usecases.attribute.create_attribute_use_case import CreateAttributeUseCase
from application.usecases.attribute.delete_attribute_use_case import DeleteAttributeUseCase
from application.usecases.attribute.get_all_attribute_use_case import GetAllAttributeUseCase


class UseCaseProvider(Provider):
    scope = Scope.REQUEST
    
    add_product_image = provide(AddProductImageUseCase)
    delete_product_image = provide(DeleteProductImageUseCase)
    
    
    create_brand = provide(CreateBrandUseCase)
    delete_brand = provide(DeleteBrandUseCase)
    get_all_brand = provide(GetAllBrandUseCase)
    
    
    create_category = provide(CreateCategoryUseCase)
    delete_category = provide(DeleteCategoryUseCase)
    get_all_category = provide(GetAllCategoryUseCase)
    
    create_attribute = provide(CreateAttributeUseCase)
    delete_attribute = provide(DeleteAttributeUseCase)
    get_all_attribute = provide(GetAllAttributeUseCase)
    
    
    create_product = provide(CreateProductUseCase)
    delete_product = provide(DeleteProductUseCase)
    get_all_product = provide(GetAllProductUseCase)
    get_by_id_product = provide(GetByIdProductUseCase)
    update_product_description = provide(UpdateProductDescriptionUseCase)
    update_product_price = provide(UpdateProductPriceUseCase)
    add_product_attribute = provide(AddProductAttributeUseCase)
    delete_product_attribute = provide(DeleteProductAttributeUseCase)
    
    
    
    
