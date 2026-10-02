from datetime import datetime

from pydantic import BaseModel

from app.models.documents import DocumentStatus


class DocumentResponse(BaseModel):
    id: int
    title: str
    file_name: str
    file_type: str
    file_size: int
    storage_path: str
    status: DocumentStatus
    document_category: str | None = None
    classification_confidence: str | None = None
    classification_reason: str | None = None
    extracted_data: dict | None = None
    guardrail_passed: bool | None = None
    guardrail_errors: list[str] | None = None
    processing_error: str | None = None
    uploaded_by: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int


class DocumentProcessingResponse(BaseModel):
    document_id: int
    status: DocumentStatus
    category: str
    confidence: str
    reason: str
    extraction: dict | None = None
    guardrail_passed: bool
    guardrail_errors: list[str] = []
    indexed: bool


class DocumentQARequest(BaseModel):
    question: str
    conversation: list[dict] = []


class DocumentQASource(BaseModel):
    document_id: int
    page: int | None = None


class DocumentQAResponse(BaseModel):
    answer: str
    sources: list[DocumentQASource]