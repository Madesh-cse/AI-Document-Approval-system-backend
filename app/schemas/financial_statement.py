from pydantic import BaseModel, Field


class FinancialStatementExtraction(BaseModel):
    document_type: str = Field(
        description="The type of financial statement."
    )
    company_name: str | None = Field(
        default=None,
        description="Company or organization name."
    )
    statement_period: str | None = Field(
        default=None,
        description="Reporting period covered by the statement."
    )
    fiscal_year: str | None = Field(
        default=None,
        description="Fiscal year explicitly stated."
    )
    currency: str | None = Field(
        default=None,
        description="Currency used in the financial statement."
    )
    total_revenue: float | None = Field(
        default=None,
        description="Total revenue explicitly stated."
    )
    total_expenses: float | None = Field(
        default=None,
        description="Total expenses explicitly stated."
    )
    operating_income: float | None = Field(
        default=None,
        description="Operating income explicitly stated."
    )
    net_income: float | None = Field(
        default=None,
        description="Net income explicitly stated."
    )
    total_assets: float | None = Field(
        default=None,
        description="Total assets explicitly stated."
    )
    total_liabilities: float | None = Field(
        default=None,
        description="Total liabilities explicitly stated."
    )
    total_equity: float | None = Field(
        default=None,
        description="Total equity explicitly stated."
    )
    summary: str = Field(
        description="Concise summary of the financial statement."
    )