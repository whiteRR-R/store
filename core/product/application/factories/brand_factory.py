from domain.entities.brand import Brand
from domain.value_objects.brand_name import BrandName
from uuid import UUID


class BrandFactory:
    @staticmethod
    def create(id: UUID, brand_name: str):
        return Brand(
            id=id,
            brand_name=BrandName(brand_name)
        )
