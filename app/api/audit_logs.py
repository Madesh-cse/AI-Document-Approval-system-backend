from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.audit_log import AuditLog
from app.models.documents import Document
from app.models.user import User, UserRole
from app.schemas.audit_log import ( AuditLogListResponse,AuditLogResponse,)


router = APIRouter(
    prefix="/api/v1/audit-logs",
    tags=["Audit Logs"],
)


@router.get(
    "",
    response_model=AuditLogListResponse,
)
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(
            AuditLog,
            User.full_name,
            Document.title,
        )
        .outerjoin(
            User,
            AuditLog.user_id == User.id,
        )
        .outerjoin(
            Document,
            AuditLog.document_id == Document.id,
        )
    )

    if current_user.role == UserRole.EMPLOYEE:
        query = query.filter(
            Document.uploaded_by == current_user.id
        )

    elif current_user.role not in {
        UserRole.ADMIN,
        UserRole.MANAGER,
    }:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view audit logs.",
        )

    results = (
        query
        .order_by(AuditLog.created_at.desc())
        .all()
    )

    logs = [
        AuditLogResponse(
            id=audit_log.id,
            timestamp=audit_log.created_at,
            user=full_name or "AI System",
            action=audit_log.action.value.replace("_", " ").title(),
            document=document_title,
            status=audit_log.status.value,
            error_message=audit_log.error_message,
        )
        for audit_log, full_name, document_title in results
    ]

    return AuditLogListResponse(
        logs=logs,
        total=len(logs),
    )