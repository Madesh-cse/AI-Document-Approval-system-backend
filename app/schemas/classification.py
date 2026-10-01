from enum import Enum

from pydantic import BaseModel, Field


class DocumentCategory(str, Enum):
    INVOICE = "invoice"
    INSURANCE_POLICY = "insurance_policy"
    PURCHASE_ORDER = "purchase_order"
    EXPENSE_REPORT = "expense_report"
    FINANCIAL_STATEMENT = "financial_statement"
    CONTRACT = "contract"
    UNSUPPORTED = "unsupported"


class DocumentClassification(BaseModel):
    category: DocumentCategory = Field(
        description="The category of the uploaded document."
    )

    confidence: str = Field(
        description="Classification confidence: high, medium, or low."
    )

    reason: str = Field(
        description="Brief explanation based only on information present in the document."
    )