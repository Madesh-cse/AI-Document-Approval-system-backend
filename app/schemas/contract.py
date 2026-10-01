from pydantic import BaseModel, Field


class ContractExtraction(BaseModel):
    document_type: str = Field(
        description="The type of contract."
    )
    contract_number: str | None = Field(
        default=None,
        description="Contract number if explicitly stated."
    )
    contract_title: str | None = Field(
        default=None,
        description="Title of the contract."
    )
    effective_date: str | None = Field(
        default=None,
        description="Date on which the contract becomes effective."
    )
    expiration_date: str | None = Field(
        default=None,
        description="Contract expiration date if explicitly stated."
    )
    party_a: str | None = Field(
        default=None,
        description="First contracting party."
    )
    party_b: str | None = Field(
        default=None,
        description="Second contracting party."
    )
    contract_value: float | None = Field(
        default=None,
        description="Contract value if explicitly stated."
    )
    currency: str | None = Field(
        default=None,
        description="Currency used for the contract value."
    )
    payment_terms: str | None = Field(
        default=None,
        description="Payment terms explicitly stated."
    )
    termination_terms: str | None = Field(
        default=None,
        description="Termination conditions explicitly stated."
    )
    obligations: list[str] = Field(
        default_factory=list,
        description="Important obligations explicitly stated in the contract."
    )
    summary: str = Field(
        description="Concise summary of the contract."
    )