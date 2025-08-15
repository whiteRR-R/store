from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Address:
    user_id: UUID
    country: str
    city: str
    street: str
    postal_code: str
    id: UUID = uuid4()
    apartment: Optional[str] = None

    def relocate(self, country: str, city: str, street: str, postal_code: str):
        if not country or not city or not street or not postal_code:
            raise ValueError("All address fields must be provided")
        self.country = country
        self.city = city
        self.street = street
        self.postal_code = postal_code

    def change_city(self, city: str):
        if not city:
            raise ValueError("City cannot be empty")
        self.city = city

    def change_apartment(self, apartment: Optional[str]):
        self.apartment = apartment
