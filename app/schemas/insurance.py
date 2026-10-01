from pydantic import BaseModel, Field


class InsurancePolicyExtraction(BaseModel):
    document_type: str = Field(
        description="The type of insurance document."
    )

    policy_number: str | None = Field(
        default=None,
        description="Insurance policy number."
    )

    insurer_name: str | None = Field(
        default=None,
        description="Name of the insurance provider."
    )

    insured_name: str | None = Field(
        default=None,
        description="Name of the insured person or organization."
    )

    policy_start_date: str | None = Field(
        default=None,
        description="Policy start date."
    )

    policy_end_date: str | None = Field(
        default=None,
        description="Policy end date."
    )

    coverage_type: str | None = Field(
        default=None,
        description="Type of insurance coverage."
    )

    premium: float | None = Field(
        default=None,
        description="Insurance premium amount."
    )

    deductible: float | None = Field(
        default=None,
        description="Deductible amount."
    )

    coverage_limit: float | None = Field(
        default=None,
        description="Maximum coverage amount explicitly stated."
    )

    exclusions: list[str] = Field(
        default_factory=list,
        description="Explicit exclusions listed in the policy."
    )

    summary: str = Field(
        description="Concise summary of the insurance policy."
    )