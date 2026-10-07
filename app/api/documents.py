from pathlib import Path
from urllib import request
from urllib import request
from uuid import uuid4
from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User, UserRole
from app.models.documents import Document, DocumentStatus
from app.models.audit_log import AuditAction, AuditStatus

from app.schemas.document import (
    DocumentListResponse,
    DocumentProcessingResponse,
    DocumentResponse,
    DocumentQARequest,
    DocumentQAResponse,
)
from app.schemas.rejection import DocumentRejectionRequest

from app.services.rag_service import answer_question
from app.services.document_service import ( create_document,get_document_by_id,get_user_documents,)
# from app.services.document_processing import (process_document,)
from app.services.document_graph import document_graph
from app.services.audit_service import create_audit_log
from app.services.s3_service import upload_file_to_s3


router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)



ALLOWED_FILE_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
}


MAX_FILE_SIZE = 20 * 1024 * 1024


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    title: str | None = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, JPG, and PNG files are supported.",
        )

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 20 MB.",
        )

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is required.",
        )
    
    file_extension = Path(file.filename).suffix.lower()
    stored_file_name = f"{uuid4().hex}{file_extension}"

    s3_key = f"documents/{current_user.id}/{stored_file_name}"

    upload_file_to_s3(
      file_content=file_content,
      object_key=s3_key,
      content_type=file.content_type,
    )

    document_title = (
        title.strip()
        if title and title.strip()
        else Path(file.filename).stem
    )

    document = create_document(
        db=db,
        title=document_title,
        file_name=file.filename,
        file_type=file.content_type,
        file_size=len(file_content),
        storage_path=s3_key,
        uploaded_by=current_user.id,
    )
    create_audit_log(
     db=db,
     action=AuditAction.UPLOADED_DOCUMENT,
     status=AuditStatus.SUCCESS,
     user_id=current_user.id,
     document_id=document.id,
   )

    return document


@router.get(
    "",
    response_model=DocumentListResponse,
)
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    documents, total = get_user_documents(
        db=db,
        user_id=current_user.id,
    )

    return DocumentListResponse(
        documents=documents,
        total=total,
    )
    
    
@router.post(
    "/{document_id}/process",
    response_model=DocumentProcessingResponse,
)
async def process_document_endpoint(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = get_document_by_id(
        db=db,
        document_id=document_id,
        user_id=current_user.id,
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    document.status = DocumentStatus.PROCESSING
    document.processing_error = None

    db.commit()
    db.refresh(document)

    create_audit_log(
        db=db,
        action=AuditAction.PROCESSING_STARTED,
        status=AuditStatus.SUCCESS,
        user_id=current_user.id,
        document_id=document.id,
    )

    db.commit()

    initial_state = {
        "document_id": document.id,
        "file_path": document.storage_path,
        "documents": [],
        "document_text": "",
        "category": None,
        "classification_confidence": None,
        "classification_reason": None,
        "extraction": None,
        "guardrail_passed": False,
        "guardrail_errors": [],
        "chunks": [],
        "indexed": False,
        "status": "started",
        "error": None,
        "classification_retries": 0,
        "extraction_retries": 0,
        "max_retries": 2,
        "approval_status": None,
        "approval_reason": None,
        "reviewed_by": None,
        "approval_deadline": None,
        "calendar_event_id": None,
        "calendar_event_created": False,
    }

    try:
        result = await document_graph.ainvoke(
            initial_state,
            config={
                "configurable": {
                    "thread_id": f"document-{document.id}",
                }
            },
        )

        document.document_category = result.get("category")

        document.classification_confidence = result.get(
            "classification_confidence"
        )

        document.classification_reason = result.get(
            "classification_reason"
        )

        document.guardrail_passed = result.get(
            "guardrail_passed"
        )

        document.guardrail_errors = result.get(
            "guardrail_errors",
            [],
        )

        extraction = result.get("extraction")

        if extraction:
            if hasattr(extraction, "model_dump"):
                document.extracted_data = extraction.model_dump()
            else:
                document.extracted_data = extraction

            create_audit_log(
                db=db,
                action=AuditAction.DATA_EXTRACTED,
                status=AuditStatus.SUCCESS,
                user_id=current_user.id,
                document_id=document.id,
            )
        else:
            document.extracted_data = None

        create_audit_log(
            db=db,
            action=AuditAction.DOCUMENT_CLASSIFIED,
            status=AuditStatus.SUCCESS,
            user_id=current_user.id,
            document_id=document.id,
        )

        calendar_event_id = result.get(
            "calendar_event_id"
        )

        calendar_event_created = result.get(
            "calendar_event_created",
            False,
        )

        approval_deadline = result.get(
            "approval_deadline"
        )

        document.calendar_event_id = calendar_event_id

        document.calendar_event_created = (
            calendar_event_created
        )

        if approval_deadline:
            if isinstance(approval_deadline, datetime):
                document.approval_deadline = approval_deadline
            else:
                document.approval_deadline = (
                    datetime.fromisoformat(
                        approval_deadline
                    )
                )
        else:
            document.approval_deadline = None

        guardrail_passed = result.get(
            "guardrail_passed",
            False,
        )

        approval_status = result.get(
            "approval_status"
        )

        if not guardrail_passed:
            document.status = DocumentStatus.REJECTED

            create_audit_log(
                db=db,
                action=AuditAction.VALIDATION_FAILED,
                status=AuditStatus.FAILED,
                user_id=current_user.id,
                document_id=document.id,
                error_message=str(
                    result.get("guardrail_errors", [])
                ),
            )

        elif approval_status == "rejected":
            document.status = DocumentStatus.REJECTED

            create_audit_log(
                db=db,
                action=AuditAction.REJECTED_DOCUMENT,
                status=AuditStatus.SUCCESS,
                user_id=current_user.id,
                document_id=document.id,
            )

        elif approval_status == "approved":
            document.status = DocumentStatus.APPROVED

            create_audit_log(
                db=db,
                action=AuditAction.APPROVED_DOCUMENT,
                status=AuditStatus.SUCCESS,
                user_id=current_user.id,
                document_id=document.id,
            )

        else:
            document.status = DocumentStatus.PENDING_REVIEW

            create_audit_log(
                db=db,
                action=AuditAction.SENT_FOR_REVIEW,
                status=AuditStatus.SUCCESS,
                user_id=current_user.id,
                document_id=document.id,
            )

        db.commit()
        db.refresh(document)

        if hasattr(extraction, "model_dump"):
            extraction_response = extraction.model_dump()
        else:
            extraction_response = extraction

        return DocumentProcessingResponse(
            document_id=document.id,
            status=document.status,
            category=result.get("category"),
            confidence=result.get(
                "classification_confidence"
            ),
            reason=result.get(
                "classification_reason"
            ),
            extraction=extraction_response,
            guardrail_passed=result.get(
                "guardrail_passed"
            ),
            guardrail_errors=result.get(
                "guardrail_errors",
                [],
            ),
            indexed=result.get(
                "indexed",
                False,
            ),
            calendar_event_id=result.get(
                "calendar_event_id"
            ),
            calendar_event_created=result.get(
                "calendar_event_created",
                False,
            ),
            approval_deadline=result.get(
                "approval_deadline"
            ),
        )

    except Exception as error:
        document.status = DocumentStatus.REJECTED
        document.processing_error = str(error)

        db.commit()
        db.refresh(document)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document processing failed: {error}",
        )

@router.post(
    "/{document_id}/qa",
    response_model=DocumentQAResponse,
)
def document_question_answer(
    document_id: int,
    request: DocumentQARequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = get_document_by_id(
        db=db,
        document_id=document_id,
        user_id=current_user.id,
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    if not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty.",
        )

    try:
        result = answer_question(
            question=request.question,
            document_id=document_id,
            conversation=request.conversation,
        )

        create_audit_log(
            db=db,
            action=AuditAction.DOCUMENT_QA,
            status=AuditStatus.SUCCESS,
            user_id=current_user.id,
            document_id=document.id,
        )

        db.commit()

        return DocumentQAResponse(
            answer=result["answer"],
            sources=result["sources"],
        )

    except Exception as exc:
        create_audit_log(
            db=db,
            action=AuditAction.DOCUMENT_QA,
            status=AuditStatus.FAILED,
            user_id=current_user.id,
            document_id=document.id,
            error_message=str(exc),
        )

        db.commit()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to answer the document question.",
        )


@router.get("/review/pending", response_model=DocumentListResponse)
def get_pending_review_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in {
        UserRole.ADMIN,
        UserRole.MANAGER,
    }:
        raise HTTPException(
            status_code=403,
            detail="Only managers and admins can view pending documents.",
        )

    documents = (
        db.query(Document)
        .filter(
            Document.status == DocumentStatus.PENDING_REVIEW
        )
        .order_by(Document.created_at.desc())
        .all()
    )

    return DocumentListResponse(
        documents=documents,
        total=len(documents),
    )


@router.get("/{document_id}/file")
def get_document_file(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Document).filter(
        Document.id == document_id
    )

    if current_user.role not in {
        UserRole.MANAGER,
        UserRole.ADMIN,
    }:
        query = query.filter(
            Document.uploaded_by == current_user.id
        )

    document = query.first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    file_path = Path(document.storage_path)

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document file not found.",
        )

    if document.file_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF documents can be previewed.",
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=document.file_name,
        content_disposition_type="inline",
    )

@router.get(
    "/review/all",
    response_model=DocumentListResponse,
)
def get_all_review_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in {
        UserRole.ADMIN,
        UserRole.MANAGER,
    }:
        raise HTTPException(
            status_code=403,
            detail="Only managers and admins can view all documents.",
        )

    documents = (
        db.query(Document)
        .order_by(Document.created_at.desc())
        .all()
    )

    return DocumentListResponse(
        documents=documents,
        total=len(documents),
    )

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Document).filter(
        Document.id == document_id
    )

    if current_user.role not in {
        UserRole.MANAGER,
        UserRole.ADMIN,
    }:
        query = query.filter(
            Document.uploaded_by == current_user.id
        )

    document = query.first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return document

@router.post("/{document_id}/approve", response_model=DocumentResponse)
def approve_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in {
        UserRole.ADMIN,
        UserRole.MANAGER,
    }:
        raise HTTPException(
            status_code=403,
            detail="Only managers and admins can approve documents.",
        )

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.status == DocumentStatus.PENDING_REVIEW,
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found or is not pending review.",
        )

    document.status = DocumentStatus.APPROVED
    create_audit_log(
       db=db,
       action=AuditAction.APPROVED_DOCUMENT,
       status=AuditStatus.SUCCESS,
       user_id=current_user.id,
       document_id=document.id,
    )


    db.commit()
    db.refresh(document)

    return document

@router.get("/review/approved", response_model=DocumentListResponse)
def get_approved_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(Document)
        .filter(Document.status == DocumentStatus.APPROVED)
    )

    # Employee → only their own approved documents
    if current_user.role == UserRole.EMPLOYEE:
        query = query.filter(
            Document.uploaded_by == current_user.id
        )

    # Manager/Admin → all approved documents
    documents = (
        query
        .order_by(Document.created_at.desc())
        .all()
    )

    return DocumentListResponse(
        documents=documents,
        total=len(documents),
    )

@router.get("/review/rejected", response_model=DocumentListResponse)
def get_rejected_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(Document)
        .filter(Document.status == DocumentStatus.REJECTED)
    )

    if current_user.role == UserRole.EMPLOYEE:
        query = query.filter(
            Document.uploaded_by == current_user.id
        )

    documents = (
        query
        .order_by(Document.created_at.desc())
        .all()
    )

    return DocumentListResponse(
        documents=documents,
        total=len(documents),
    )
    

@router.post("/{document_id}/reject", response_model=DocumentResponse)
def reject_document(
    document_id: int,
    rejection: DocumentRejectionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in {
        UserRole.ADMIN,
        UserRole.MANAGER,
    }:
        raise HTTPException(
            status_code=403,
            detail="Only managers and admins can reject documents.",
        )

    reason = rejection.reason.strip()

    if not reason:
        raise HTTPException(
            status_code=400,
            detail="Rejection reason is required.",
        )

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.status == DocumentStatus.PENDING_REVIEW,
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found or is not pending review.",
        )
    
    document.status = DocumentStatus.REJECTED
    document.rejection_reason = request.reason.strip()
    db.commit()
    db.refresh(document)

    create_audit_log(
       db=db,
       action=AuditAction.REJECTED_DOCUMENT,
       status=AuditStatus.SUCCESS,
       user_id=current_user.id,
       document_id=document.id,
    )
    return document