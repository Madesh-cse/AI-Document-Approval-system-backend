from pydantic import BaseModel, Field


class InvoiceExtraction(BaseModel):
    document_type: str = Field(
        description="The type of document."
    )

    invoice_number: str | None = Field(
        default=None,
        description="Invoice number explicitly stated in the document."
    )

    invoice_date: str | None = Field(
        default=None,
        description="Invoice date explicitly stated in the document."
    )

    due_date: str | None = Field(
        default=None,
        description="Payment due date explicitly stated in the document."
    )

    vendor_name: str | None = Field(
        default=None,
        description="Name of the vendor or supplier."
    )

    customer_name: str | None = Field(
        default=None,
        description="Name of the customer or buyer."
    )

    currency: str | None = Field(
        default=None,
        description="Currency used in the invoice."
    )

    subtotal: float | None = Field(
        default=None,
        description="Invoice subtotal before taxes or additional charges."
    )

    tax_amount: float | None = Field(
        default=None,
        description="Total tax amount explicitly stated."
    )

    total_amount: float | None = Field(
        default=None,
        description="Final invoice amount."
    )

    payment_terms: str | None = Field(
        default=None,
        description="Payment terms explicitly stated in the invoice."
    )

    summary: str = Field(
        description="Concise summary of the invoice."
    )