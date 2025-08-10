import uuid
from sqlalchemy import Integer, String, LargeBinary, UUID
from sqlalchemy.orm import mapped_column, Mapped
from domain.entities.user import User
from infrastructure.persistence.database import Base


class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, default=uuid.uuid4(), primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    role: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
