from infrastructure.persistence.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, UUID


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    def __repr__(self):
        return f"<CategoryModel(id={self.id}, name={self.name}, description={self.description})>"
