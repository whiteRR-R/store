import uuid
from sqlalchemy import Boolean, Integer, String, LargeBinary, UUID
from sqlalchemy.orm import mapped_column, Mapped
from infrastructure.persistence.database import Base


class AuthOutboxModel(Base):
    __tablename__ = "auth_outbox"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    payload: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    processed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
