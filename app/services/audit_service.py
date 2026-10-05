from sqlalchemy.orm import Session

from app.models.audit_log import AuditAction, AuditLog, AuditStatus


def create_audit_log(
    db: Session,
    action: AuditAction,
    status: AuditStatus = AuditStatus.SUCCESS,
    user_id: int | None = None,
    document_id: int | None = None,
    error_message: str | None = None,
) -> AuditLog:
    audit_log = AuditLog(
        action=action,
        status=status,
        user_id=user_id,
        document_id=document_id,
        error_message=error_message,
    )

    db.add(audit_log)
    db.flush()
    return audit_log