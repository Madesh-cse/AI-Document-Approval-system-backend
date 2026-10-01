from pydantic import BaseModel, Field


class ExpenseReportExtraction(BaseModel):
    document_type: str = Field(
        description="The type of document."
    )
    report_number: str | None = Field(
        default=None,
        description="Expense report number if explicitly available."
    )
    employee_name: str | None = Field(
        default=None,
        description="Name of the employee submitting the expense report."
    )
    department: str | None = Field(
        default=None,
        description="Employee department if explicitly stated."
    )
    report_date: str | None = Field(
        default=None,
        description="Date of the expense report."
    )
    expense_period_start: str | None = Field(
        default=None,
        description="Beginning of the expense period."
    )
    expense_period_end: str | None = Field(
        default=None,
        description="End of the expense period."
    )
    currency: str | None = Field(
        default=None,
        description="Currency used in the expense report."
    )
    total_amount: float | None = Field(
        default=None,
        description="Total expense amount."
    )
    reimbursable_amount: float | None = Field(
        default=None,
        description="Total amount eligible for reimbursement."
    )
    purpose: str | None = Field(
        default=None,
        description="Business purpose of the reported expenses."
    )
    summary: str = Field(
        description="Concise summary of the expense report."
    )