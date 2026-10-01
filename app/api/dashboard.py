from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.documents import Document, DocumentStatus
from app.models.user import User
from app.schemas.dashboard import (
    DashboardLifecycle,
    DashboardResponse,
    DashboardStats,
    RecentDocument,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_documents = db.scalar(
        select(func.count(Document.id)).where(
            Document.uploaded_by == current_user.id
        )
    ) or 0

    pending_review = db.scalar(
        select(func.count(Document.id)).where(
            Document.uploaded_by == current_user.id,
            Document.status == DocumentStatus.PENDING_REVIEW,
        )
    ) or 0

    approved = db.scalar(
        select(func.count(Document.id)).where(
            Document.uploaded_by == current_user.id,
            Document.status == DocumentStatus.APPROVED,
        )
    ) or 0

    rejected = db.scalar(
        select(func.count(Document.id)).where(
            Document.uploaded_by == current_user.id,
            Document.status == DocumentStatus.REJECTED,
        )
    ) or 0

    lifecycle_rows = db.execute(
        select(
            Document.status,
            func.count(Document.id),
        )
        .where(Document.uploaded_by == current_user.id)
        .group_by(Document.status)
    ).all()

    lifecycle_counts = {
        status: count
        for status, count in lifecycle_rows
    }

    recent_documents = db.scalars(
        select(Document)
        .where(Document.uploaded_by == current_user.id)
        .order_by(Document.created_at.desc())
        .limit(5)
    ).all()

    return DashboardResponse(
        stats=DashboardStats(
            total_documents=total_documents,
            pending_review=pending_review,
            approved=approved,
            rejected=rejected,
        ),
        lifecycle=DashboardLifecycle(
            draft=lifecycle_counts.get(DocumentStatus.DRAFT, 0),
            processing=lifecycle_counts.get(DocumentStatus.PROCESSING, 0),
            pending_review=lifecycle_counts.get(
                DocumentStatus.PENDING_REVIEW,
                0,
            ),
            approved=lifecycle_counts.get(
                DocumentStatus.APPROVED,
                0,
            ),
            rejected=lifecycle_counts.get(
                DocumentStatus.REJECTED,
                0,
            ),
        ),
        recent_documents=[
            RecentDocument(
                id=document.id,
                title=document.title,
                file_name=document.file_name,
                status=document.status,
                created_at=document.created_at.isoformat(),
            )
            for document in recent_documents
        ],
    )