import uuid
from sqlalchemy import Integer, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from domain.entities.user import UserRole, UserStatus
from infrastructure.persistence.models.address_model import AddressModel
from infrastructure.persistence.models.base import Base


class UserModel(Base):
    __tablename__ = "user"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(String(20), nullable=False, default=UserRole.USER.value)
    status: Mapped[UserStatus] = mapped_column(String(20), nullable=False, default=UserStatus.INACTIVE.value)

    addresses: Mapped[list["AddressModel"]] = relationship(
        "AddressModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )
