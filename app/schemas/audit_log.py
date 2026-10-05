from datetime import datetime

from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: int
    timestamp: datetime
    user: str
    action: str
    document: str | None
    status: str
    error_message: str | None = None


class AuditLogListResponse(BaseModel):
    logs: list[AuditLogResponse]
    total: int