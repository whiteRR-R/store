from pydantic import BaseModel, Field
from uuid import UUID


class AddressDTO(BaseModel):
    address_id: UUID
    user_id: UUID
    country: str = Field(..., max_length=100)
    city: str = Field(..., max_length=100)
    street: str = Field(..., max_length=200)
    postal_code: str = Field(..., max_length=20)
    apartment: str | None = Field(None, max_length=50)


class UpdateAddressDTO(BaseModel):
    country: str | None = Field(None, max_length=100)
    city: str | None = Field(None, max_length=100)
    street: str | None = Field(None, max_length=200)
    postal_code: str | None = Field(None, max_length=20)
    apartment: str | None = Field(None, max_length=50)

