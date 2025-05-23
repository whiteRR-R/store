from domain.entities.brand import Brand
from domain.value_objects.brand_name import BrandName
from application.dtos.brand_dto import BrandDTO, CreateBrandDTO
from uuid import UUID


class BrandFactory:
    @staticmethod
    def from_params(brand_id: UUID, brand_name: str):
        return Brand(
            id=brand_id,
            brand_name=BrandName(brand_name)
        )

    @staticmethod
    def from_dto(brand_dto: CreateBrandDTO):
        return Brand(
            brand_name=BrandName(brand_dto.name),
        )

    @staticmethod
    def to_dto(brand: Brand):
        return BrandDTO(
            id=brand.id.hex,
            name=brand.name.value
        )
