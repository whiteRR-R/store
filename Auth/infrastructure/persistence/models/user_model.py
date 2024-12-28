from infrastructure.persistence.types.role_type import RoleType
from domain.valueobject.role import Role
from infrastructure.persistence.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String

class UserModel(Base):
    __tablename__ = "user_model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    role: Mapped[Role] = mapped_column(RoleType, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
 