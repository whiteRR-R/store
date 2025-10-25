import uuid
from sqlalchemy import Boolean, LargeBinary, String, UUID
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.persistence.models.base import Base



class UserOutboxModel(Base):
    __tablename__ = "user_outbox"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4())
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    payload: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    processed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

