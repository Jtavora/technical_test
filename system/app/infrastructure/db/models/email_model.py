from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    Text,
    DateTime,
)
from sqlalchemy.sql import func

from system.app.infrastructure.db.base import Base


class EmailModel(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    from_email = Column(String(255), nullable=False, index=True)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)

    category = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False, default=0.0)
    draft_reply = Column(Text, nullable=False)
    requires_human_review = Column(Boolean, nullable=False, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )