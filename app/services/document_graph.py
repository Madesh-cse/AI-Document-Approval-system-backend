from typing import TypedDict

from langchain_core.documents import Document
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from app.schemas.classification import DocumentCategory
from app.services.document_chunker import split_documents
from app.services.document_classifier import classify_document
from app.services.document_extraction import extract_document_data
from app.services.document_loader import load_document
from app.services.extraction_guardrails import validate_extraction
from app.services.vector_store import get_vector_store


class DocumentProcessingState(TypedDict):
    document_id: int
    file_path: str

    documents: list
    document_text: str

    category: str | None
    classification_confidence: str | None
    classification_reason: str | None

    extraction: dict | None

    guardrail_passed: bool
    guardrail_errors: list[str]

    chunks: list[dict]

    indexed: bool

    status: str
    error: str | None

    classification_retries: int
    extraction_retries: int
    max_retries: int

    approval_status: str | None
    approval_reason: str | None
    reviewed_by: int | None


def load_document_node(
    state: DocumentProcessingState,
):
    try:
        documents = load_document(
            state["file_path"]
        )

        if not documents:
            return {
                "documents": [],
                "document_text": "",
                "status": "failed",
                "error": (
                    "The document contains "
                    "no readable text."
                ),
            }

        document_text = "\n\n".join(
            document.page_content
            for document in documents
        )

        if not document_text.strip():
            return {
                "documents": [],
                "document_text": "",
                "status": "failed",
                "error": (
                    "The document contains "
                    "no readable text."
                ),
            }

        return {
            "documents": documents,
            "document_text": document_text,
            "status": "loaded",
            "error": None,
        }

    except Exception as exc:
        return {
            "documents": [],
            "document_text": "",
            "status": "failed",
            "error": str(exc),
        }


def classify_document_node(
    state: DocumentProcessingState,
):
    try:
        classification = classify_document(
            document_text=state["document_text"],
        )

        return {
            "category": classification.category.value,
            "classification_confidence": (
                classification.confidence
            ),
            "classification_reason": (
                classification.reason
            ),
            "status": "classified",
            "error": None,
        }

    except Exception as exc:
        return {
            "status": "classification_failed",
            "error": str(exc),
        }


def retry_classification_node(
    state: DocumentProcessingState,
):
    return {
        "classification_retries": (
            state["classification_retries"] + 1
        ),
        "status": "retrying_classification",
        "error": None,
    }


def route_after_classification(
    state: DocumentProcessingState,
):
    if state["status"] == "classification_failed":
        if (
            state["classification_retries"]
            < state["max_retries"]
        ):
            return "retry"

        return "failed"

    if (
        state["category"]
        == DocumentCategory.UNSUPPORTED.value
    ):
        return "reject"

    return "extract"


def reject_unsupported_document_node(
    state: DocumentProcessingState,
):
    return {
        "status": "rejected",
        "guardrail_passed": False,
        "guardrail_errors": [
            "Document type is not supported."
        ],
        "indexed": False,
        "error": None,
    }


def extract_document_node(
    state: DocumentProcessingState,
):
    try:
        category = DocumentCategory(
            state["category"]
        )

        extraction = extract_document_data(
            document_text=state["document_text"],
            category=category,
        )

        return {
            "extraction": extraction.model_dump(),
            "status": "extracted",
            "error": None,
        }

    except Exception as exc:
        return {
            "status": "extraction_failed",
            "error": str(exc),
        }


def retry_extraction_node(
    state: DocumentProcessingState,
):
    return {
        "extraction_retries": (
            state["extraction_retries"] + 1
        ),
        "status": "retrying_extraction",
        "error": None,
    }


def route_after_extraction(
    state: DocumentProcessingState,
):
    if state["status"] == "extraction_failed":
        if (
            state["extraction_retries"]
            < state["max_retries"]
        ):
            return "retry"

        return "failed"

    return "validate"


def validate_extraction_node(
    state: DocumentProcessingState,
):
    try:
        extraction = state["extraction"]

        passed, errors = validate_extraction(
            extraction=extraction,
            document_text=state["document_text"],
        )

        if passed:
            return {
                "guardrail_passed": True,
                "guardrail_errors": [],
                "status": "validated",
                "error": None,
            }

        return {
            "guardrail_passed": False,
            "guardrail_errors": errors,
            "status": "validation_failed",
            "error": None,
        }

    except Exception as exc:
        return {
            "guardrail_passed": False,
            "guardrail_errors": [str(exc)],
            "status": "validation_failed",
            "error": str(exc),
        }


def route_after_validation(
    state: DocumentProcessingState,
):
    if state["guardrail_passed"]:
        return "chunk"

    return "failed"


def chunk_document_node(
    state: DocumentProcessingState,
):
    try:
        documents = state["documents"]

        chunks = split_documents(documents)

        if not chunks:
            return {
                "chunks": [],
                "status": "failed",
                "error": (
                    "Document chunking produced "
                    "no chunks."
                ),
            }

        chunk_data = []

        for chunk in chunks:
            chunk_data.append(
                {
                    "page_content": chunk.page_content,
                    "metadata": chunk.metadata,
                }
            )

        return {
            "chunks": chunk_data,
            "status": "chunked",
            "error": None,
        }

    except Exception as exc:
        return {
            "chunks": [],
            "status": "failed",
            "error": str(exc),
        }


def index_document_node(
    state: DocumentProcessingState,
):
    try:
        vector_store = get_vector_store()

        chunks = [
            Document(
                page_content=chunk["page_content"],
                metadata=chunk["metadata"],
            )
            for chunk in state["chunks"]
        ]

        if not chunks:
            return {
                "status": "failed",
                "indexed": False,
                "error": (
                    "No chunks available "
                    "for indexing."
                ),
            }

        for chunk in chunks:
            chunk.metadata["document_id"] = str(
                state["document_id"]
            )

            chunk.metadata[
                "document_category"
            ] = state["category"]

        vector_store.add_documents(chunks)

        return {
            "status": "indexed",
            "indexed": True,
            "error": None,
        }

    except Exception as exc:
        return {
            "status": "failed",
            "indexed": False,
            "error": str(exc),
        }


def human_review_node(
    state: DocumentProcessingState,
):
    decision = interrupt(
        {
            "type": "document_approval",
            "document_id": state["document_id"],
            "category": state["category"],
            "extraction": state["extraction"],
            "message": (
                "Manager approval is required."
            ),
        }
    )

    return {
        "approval_status": decision["decision"],
        "approval_reason": decision.get("reason"),
        "reviewed_by": decision.get("reviewed_by"),
        "status": "reviewed",
        "error": None,
    }


def route_after_human_review(
    state: DocumentProcessingState,
):
    if state["approval_status"] == "approved":
        return "approved"

    if state["approval_status"] == "rejected":
        return "rejected"

    return "failed"


def approve_document_node(
    state: DocumentProcessingState,
):
    return {
        "status": "approved",
        "error": None,
    }


def reject_after_review_node(
    state: DocumentProcessingState,
):
    return {
        "status": "rejected",
        "error": None,
    }


def failed_document_node(
    state: DocumentProcessingState,
):
    return {
        "status": "failed",
        "indexed": False,
    }


graph = StateGraph(
    DocumentProcessingState
)


graph.add_node(
    "load_document",
    load_document_node,
)

graph.add_node(
    "classify_document",
    classify_document_node,
)

graph.add_node(
    "retry_classification",
    retry_classification_node,
)

graph.add_node(
    "reject_unsupported",
    reject_unsupported_document_node,
)

graph.add_node(
    "extract",
    extract_document_node,
)

graph.add_node(
    "retry_extraction",
    retry_extraction_node,
)

graph.add_node(
    "validate_extraction",
    validate_extraction_node,
)

graph.add_node(
    "chunk",
    chunk_document_node,
)

graph.add_node(
    "index",
    index_document_node,
)

graph.add_node(
    "human_review",
    human_review_node,
)

graph.add_node(
    "approved",
    approve_document_node,
)

graph.add_node(
    "rejected",
    reject_after_review_node,
)

graph.add_node(
    "failed",
    failed_document_node,
)


graph.add_edge(
    START,
    "load_document",
)

graph.add_edge(
    "load_document",
    "classify_document",
)


graph.add_conditional_edges(
    "classify_document",
    route_after_classification,
    {
        "retry": "retry_classification",
        "reject": "reject_unsupported",
        "extract": "extract",
        "failed": "failed",
    },
)


graph.add_edge(
    "retry_classification",
    "classify_document",
)


graph.add_conditional_edges(
    "extract",
    route_after_extraction,
    {
        "retry": "retry_extraction",
        "validate": "validate_extraction",
        "failed": "failed",
    },
)


graph.add_edge(
    "retry_extraction",
    "extract",
)


graph.add_conditional_edges(
    "validate_extraction",
    route_after_validation,
    {
        "chunk": "chunk",
        "failed": "failed",
    },
)


graph.add_edge(
    "reject_unsupported",
    END,
)

graph.add_edge(
    "chunk",
    "index",
)

graph.add_edge(
    "index",
    "human_review",
)


graph.add_conditional_edges(
    "human_review",
    route_after_human_review,
    {
        "approved": "approved",
        "rejected": "rejected",
        "failed": "failed",
    },
)


graph.add_edge(
    "approved",
    END,
)

graph.add_edge(
    "rejected",
    END,
)

graph.add_edge(
    "failed",
    END,
)


checkpointer = MemorySaver()

document_graph = graph.compile(
    checkpointer=checkpointer,
)