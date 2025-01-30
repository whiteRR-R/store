from domain.entities.user import User
from domain.valueobject.role import Role
from domain.valueobject.email import Email
from domain.valueobject.username import Username
from infrastructure.persistence.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, LargeBinary


class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    role: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    
    def __init__(self, user: User):
        """ Маппинг из доменной модели в ORM-модель. """
        self.username = user.username
        self.role = user.role
        self.email = user.email
        self.hashed_password = user.hash_password
