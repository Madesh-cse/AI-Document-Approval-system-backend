from typing import Any

from pydantic import BaseModel


class DocumentProcessingResult(BaseModel):
    category: str
    confidence: str
    reason: str
    extraction: Any | None = None
    guardrail_passed: bool
    guardrail_errors: list[str] = []
    indexed: bool