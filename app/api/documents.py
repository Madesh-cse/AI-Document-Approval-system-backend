from pathlib import Path
from uuid import uuid4

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

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.documents import DocumentStatus
from app.schemas.document import (
    DocumentListResponse,
    DocumentProcessingResponse,
    DocumentResponse,
    DocumentQARequest,
    DocumentQAResponse,
)
from app.services.rag_service import answer_question
from app.services.document_service import (
    create_document,
    get_document_by_id,
    get_user_documents,
)

from app.services.document_processing import (
    process_document,
)


router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)


UPLOAD_DIR = Path("uploads")


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

    user_upload_dir = UPLOAD_DIR / str(current_user.id)
    user_upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_extension = Path(file.filename).suffix.lower()
    stored_file_name = f"{uuid4().hex}{file_extension}"

    file_path = user_upload_dir / stored_file_name

    file_path.write_bytes(file_content)

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
        storage_path=str(file_path),
        uploaded_by=current_user.id,
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
def process_document_endpoint(
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
            status_code=404,
            detail="Document not found",
        )

    document.status = DocumentStatus.PROCESSING
    document.processing_error = None
    db.commit()
    db.refresh(document)

    try:
        result = process_document(
            file_path=document.storage_path,
            document_id=document.id,
        )

        document.document_category = result["category"]
        document.classification_confidence = result["confidence"]
        document.classification_reason = result["reason"]
        document.guardrail_passed = result["guardrail_passed"]
        document.guardrail_errors = result["guardrail_errors"]

        if result["extraction"]:
            document.extracted_data = result["extraction"].model_dump()
        else:
            document.extracted_data = None

        if not result["indexed"]:
            document.status = DocumentStatus.REJECTED
        else:
            document.status = DocumentStatus.PENDING_REVIEW

        db.commit()
        db.refresh(document)

        return DocumentProcessingResponse(
            document_id=document.id,
            status=document.status,
            category=result["category"],
            confidence=result["confidence"],
            reason=result["reason"],
            extraction=(
                result["extraction"].model_dump()
                if result["extraction"]
                else None
            ),
            guardrail_passed=result["guardrail_passed"],
            guardrail_errors=result["guardrail_errors"],
            indexed=result["indexed"],
        )

    except Exception as error:
        document.status = DocumentStatus.REJECTED
        document.processing_error = str(error)

        db.commit()
        db.refresh(document)

        raise HTTPException(
            status_code=500,
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

    result = answer_question(
        question=request.question,
        document_id=document_id,
        conversation=request.conversation,
    )

    return DocumentQAResponse(
        answer=result["answer"],
        sources=result["sources"],
    )


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
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

    return document