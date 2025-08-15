from domain.entities.address import Address
from infrastructure.persistence.models.address_model import AddressModel


class AddressDataMapper:
    def to_entity(self, address_model: AddressModel) -> Address:
        return Address(
            id=address_model.id,
            user_id=address_model.user_id,
            country=address_model.country,
            city=address_model.city,
            street=address_model.street,
            postal_code=address_model.postal_code,
        )

    def to_model(self, address: Address) -> AddressModel:
        return AddressModel(
            id=address.id,
            user_id=address.user_id,
            country=address.country,
            city=address.city,
            street=address.street,
            postal_code=address.postal_code,
        )
