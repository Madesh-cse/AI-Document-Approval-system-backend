from app.schemas.classification import DocumentCategory
from app.services.document_classifier import classify_document
from app.services.document_chunker import split_documents
from app.services.document_extraction import extract_document_data
from app.services.document_loader import load_document
from app.services.extraction_guardrails import validate_extraction
from app.services.vector_store import get_vector_store


def process_document(
    file_path: str,
    document_id: int,
):
    documents = load_document(file_path)

    if not documents:
        raise ValueError(
            "The document contains no readable text."
        )

    document_text = "\n\n".join(
        document.page_content
        for document in documents
    )

    classification = classify_document(
        document_text=document_text,
    )

    if classification.category == DocumentCategory.UNSUPPORTED:
        return {
            "category": classification.category.value,
            "confidence": classification.confidence,
            "reason": classification.reason,
            "extraction": None,
            "guardrail_passed": False,
            "guardrail_errors": [
                "Document type is not supported."
            ],
            "indexed": False,
        }

    extraction = extract_document_data(
        document_text=document_text,
        category=classification.category,
    )

    guardrail_passed, guardrail_errors = validate_extraction(
        extraction=extraction,
        document_text=document_text,
    )

    if not guardrail_passed:
        return {
            "category": classification.category.value,
            "confidence": classification.confidence,
            "reason": classification.reason,
            "extraction": extraction,
            "guardrail_passed": False,
            "guardrail_errors": guardrail_errors,
            "indexed": False,
        }

    chunks = split_documents(documents)

    for chunk in chunks:
        chunk.metadata["document_id"] = str(document_id)
        chunk.metadata["document_category"] = (
            classification.category.value
        )

    vector_store = get_vector_store()

    vector_store.add_documents(chunks)

    return {
        "category": classification.category.value,
        "confidence": classification.confidence,
        "reason": classification.reason,
        "extraction": extraction,
        "guardrail_passed": True,
        "guardrail_errors": [],
        "indexed": True,
    }