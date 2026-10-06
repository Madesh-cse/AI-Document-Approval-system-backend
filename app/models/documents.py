from datetime import datetime
from enum import Enum
from typing import Any

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class DocumentStatus(str, Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        nullable=False,
    )

    storage_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    status: Mapped[DocumentStatus] = mapped_column(
        SQLEnum(DocumentStatus),
        default=DocumentStatus.DRAFT,
        nullable=False,
    )

    document_category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    classification_confidence: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    classification_reason: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )

    extracted_data: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    guardrail_passed: Mapped[bool | None] = mapped_column(
        nullable=True,
    )

    guardrail_errors: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    processing_error: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )
    
    rejection_reason: Mapped[str | None] = mapped_column(
      String(2000),
      nullable=True,
    )
    
    approval_deadline: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    calendar_event_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    calendar_event_created: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    uploaded_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    owner = relationship(
        "User",
        backref="documents",
    )