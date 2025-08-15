from domain.entities.address import Address
from application.dtos.address import AddressDTO


class AddressFactory:
    @staticmethod
    def from_dto(address_dto: AddressDTO) -> Address:
        return Address(
            user_id=address_dto.user_id,
            street=address_dto.street,
            city=address_dto.city,
            country=address_dto.country,
            postal_code=address_dto.postal_code,
            apartment=address_dto.apartment
        )
    
    @staticmethod
    def to_dto(address: Address) -> AddressDTO:
        return AddressDTO(
            address_id=address.id,
            user_id=address.user_id,
            street=address.street,
            city=address.city,
            country=address.country,
            postal_code=address.postal_code,
            apartment=address.apartment
        )
