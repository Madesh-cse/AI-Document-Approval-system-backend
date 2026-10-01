from pydantic import BaseModel

from app.models.documents import DocumentStatus
from datetime import datetime


class DashboardStats(BaseModel):
    total_documents: int
    pending_review: int
    approved: int
    rejected: int


class DashboardLifecycle(BaseModel):
    draft: int
    processing: int
    pending_review: int
    approved: int
    rejected: int


class RecentDocument(BaseModel):
    id: int
    title: str
    file_name: str
    status: DocumentStatus
    created_at: datetime


class DashboardResponse(BaseModel):
    stats: DashboardStats
    lifecycle: DashboardLifecycle
    recent_documents: list[RecentDocument]