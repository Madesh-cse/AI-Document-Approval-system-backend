from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AuditAction(str, Enum):
    UPLOADED_DOCUMENT = "uploaded_document"
    PROCESSING_STARTED = "processing_started"
    DOCUMENT_CLASSIFIED = "document_classified"
    DATA_EXTRACTED = "data_extracted"
    VALIDATION_FAILED = "validation_failed"
    SENT_FOR_REVIEW = "sent_for_review"
    APPROVED_DOCUMENT = "approved_document"
    REJECTED_DOCUMENT = "rejected_document"
    DOCUMENT_QA = "document_qa"


class AuditStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    action: Mapped[AuditAction] = mapped_column(
        SQLEnum(AuditAction),
        nullable=False,
        index=True,
    )

    status: Mapped[AuditStatus] = mapped_column(
        SQLEnum(AuditStatus),
        nullable=False,
        default=AuditStatus.SUCCESS,
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    document_id: Mapped[int | None] = mapped_column(
        ForeignKey("documents.id"),
        nullable=True,
        index=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )