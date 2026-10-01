from pydantic import BaseModel, Field


class PurchaseOrderExtraction(BaseModel):
    document_type: str = Field(
        description="The type of document."
    )
    purchase_order_number: str | None = Field(
        default=None,
        description="Purchase order number explicitly stated in the document."
    )
    order_date: str | None = Field(
        default=None,
        description="Purchase order date."
    )
    delivery_date: str | None = Field(
        default=None,
        description="Expected delivery date."
    )
    supplier_name: str | None = Field(
        default=None,
        description="Name of the supplier or vendor."
    )
    buyer_name: str | None = Field(
        default=None,
        description="Name of the buyer or purchasing organization."
    )
    currency: str | None = Field(
        default=None,
        description="Currency used in the purchase order."
    )
    subtotal: float | None = Field(
        default=None,
        description="Subtotal before taxes or additional charges."
    )
    tax_amount: float | None = Field(
        default=None,
        description="Tax amount explicitly stated."
    )
    total_amount: float | None = Field(
        default=None,
        description="Total purchase order amount."
    )
    payment_terms: str | None = Field(
        default=None,
        description="Payment terms explicitly stated."
    )
    delivery_terms: str | None = Field(
        default=None,
        description="Delivery or shipping terms explicitly stated."
    )
    summary: str = Field(
        description="Concise summary of the purchase order."
    )