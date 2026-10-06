from typing import Any


def validate_extraction(
    extraction: Any,
    document_text: str,
) -> tuple[bool, list[str]]:

    errors = []

    source_text = document_text.lower()

    if isinstance(extraction, dict):
        document_type = extraction.get("document_type")
        summary = extraction.get("summary")
    else:
        document_type = extraction.document_type
        summary = extraction.summary

    if not isinstance(document_type, str) or not document_type.strip():
        errors.append(
            "document_type cannot be empty."
        )

    if not isinstance(summary, str) or not summary.strip():
        errors.append(
            "summary cannot be empty."
        )

    if isinstance(summary, str) and len(summary) > 1000:
        errors.append(
            "summary cannot exceed 1000 characters."
        )

    if isinstance(summary, str):
        if summary.lower() not in source_text:
            pass

    _validate_common_fields(
        extraction=extraction,
        source_text=source_text,
        errors=errors,
    )

    _validate_invoice(
        extraction=extraction,
        source_text=source_text,
        errors=errors,
    )

    _validate_insurance(
        extraction=extraction,
        source_text=source_text,
        errors=errors,
    )

    _validate_purchase_order(
        extraction=extraction,
        source_text=source_text,
        errors=errors,
    )

    _validate_expense_report(
        extraction=extraction,
        source_text=source_text,
        errors=errors,
    )

    _validate_financial_statement(
        extraction=extraction,
        source_text=source_text,
        errors=errors,
    )

    _validate_contract(
        extraction=extraction,
        source_text=source_text,
        errors=errors,
    )

    return len(errors) == 0, errors


def _validate_common_fields(
    extraction: Any,
    source_text: str,
    errors: list[str],
) -> None:

    fields_to_check = [
        "invoice_number",
        "policy_number",
        "purchase_order_number",
        "report_number",
        "contract_number",
    ]

    for field_name in fields_to_check:
        value = getattr(
            extraction,
            field_name,
            None,
        )

        if value and value.lower() not in source_text:
            errors.append(
                f"{field_name} was not found in the document."
            )


def _validate_invoice(
    extraction: Any,
    source_text: str,
    errors: list[str],
) -> None:

    if not hasattr(extraction, "invoice_number"):
        return

    _check_text_field(
        extraction,
        "vendor_name",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "customer_name",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "invoice_date",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "due_date",
        source_text,
        errors,
    )


def _validate_insurance(
    extraction: Any,
    source_text: str,
    errors: list[str],
) -> None:

    if not hasattr(extraction, "policy_number"):
        return

    _check_text_field(
        extraction,
        "insurer_name",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "insured_name",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "policy_start_date",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "policy_end_date",
        source_text,
        errors,
    )


def _validate_purchase_order(
    extraction: Any,
    source_text: str,
    errors: list[str],
) -> None:

    if not hasattr(extraction, "purchase_order_number"):
        return

    _check_text_field(
        extraction,
        "supplier_name",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "buyer_name",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "order_date",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "delivery_date",
        source_text,
        errors,
    )


def _validate_expense_report(
    extraction: Any,
    source_text: str,
    errors: list[str],
) -> None:

    if not hasattr(extraction, "report_number"):
        return

    _check_text_field(
        extraction,
        "employee_name",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "department",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "report_date",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "expense_period_start",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "expense_period_end",
        source_text,
        errors,
    )


def _validate_financial_statement(
    extraction: Any,
    source_text: str,
    errors: list[str],
) -> None:

    if not hasattr(extraction, "company_name"):
        return

    _check_text_field(
        extraction,
        "company_name",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "statement_period",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "fiscal_year",
        source_text,
        errors,
    )


def _validate_contract(
    extraction: Any,
    source_text: str,
    errors: list[str],
) -> None:

    if not hasattr(extraction, "contract_number"):
        return

    _check_text_field(
        extraction,
        "contract_title",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "effective_date",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "expiration_date",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "party_a",
        source_text,
        errors,
    )

    _check_text_field(
        extraction,
        "party_b",
        source_text,
        errors,
    )

    if len(extraction.obligations) > 50:
        errors.append(
            "obligations cannot contain more than 50 items."
        )


def _check_text_field(
    extraction: Any,
    field_name: str,
    source_text: str,
    errors: list[str],
) -> None:

    value = getattr(
        extraction,
        field_name,
        None,
    )

    if value and isinstance(value, str):
        if value.lower() not in source_text:
            errors.append(
                f"{field_name} was not found in the document."
            )