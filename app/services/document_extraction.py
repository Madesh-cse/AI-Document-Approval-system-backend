from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.schemas.classification import DocumentCategory
from app.schemas.contract import ContractExtraction
from app.schemas.expense_report import ExpenseReportExtraction
from app.schemas.financial_statement import FinancialStatementExtraction
from app.schemas.insurance import InsurancePolicyExtraction
from app.schemas.invoice import InvoiceExtraction
from app.schemas.purchase_order import PurchaseOrderExtraction


llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=settings.OPENAI_API_KEY,
    temperature=0,
)


invoice_llm = llm.with_structured_output(
    InvoiceExtraction
)

insurance_llm = llm.with_structured_output(
    InsurancePolicyExtraction
)

purchase_order_llm = llm.with_structured_output(
    PurchaseOrderExtraction
)

expense_report_llm = llm.with_structured_output(
    ExpenseReportExtraction
)

financial_statement_llm = llm.with_structured_output(
    FinancialStatementExtraction
)

contract_llm = llm.with_structured_output(
    ContractExtraction
)


invoice_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an invoice extraction assistant.

Extract information only from the provided invoice.

Rules:
- Only extract information explicitly present.
- Do not invent missing values.
- Use null when a value is unavailable.
- Do not infer amounts or dates.
- Return the required structured schema.
"""
        ),
        (
            "human",
            """
Analyze the following invoice:

{document_text}
"""
        ),
    ]
)


insurance_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an insurance policy extraction assistant.

Extract information only from the provided insurance document.

Rules:
- Only extract information explicitly present.
- Do not invent missing values.
- Use null when a value is unavailable.
- Do not infer coverage, exclusions, limits, or financial values.
- Return the required structured schema.
"""
        ),
        (
            "human",
            """
Analyze the following insurance policy:

{document_text}
"""
        ),
    ]
)


purchase_order_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a purchase order extraction assistant.

Extract information only from the provided purchase order.

Rules:
- Only extract information explicitly present.
- Do not invent missing values.
- Use null when a value is unavailable.
- Do not infer amounts, dates, suppliers, or delivery terms.
- Return the required structured schema.
"""
        ),
        (
            "human",
            """
Analyze the following purchase order:

{document_text}
"""
        ),
    ]
)


expense_report_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expense report extraction assistant.

Extract information only from the provided expense report.

Rules:
- Only extract information explicitly present.
- Do not invent missing values.
- Use null when a value is unavailable.
- Do not infer financial values.
- Return the required structured schema.
"""
        ),
        (
            "human",
            """
Analyze the following expense report:

{document_text}
"""
        ),
    ]
)


financial_statement_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a financial statement extraction assistant.

Extract information only from the provided financial statement.

Rules:
- Only extract information explicitly present.
- Do not invent missing values.
- Use null when a value is unavailable.
- Do not calculate financial metrics that are not explicitly stated.
- Return the required structured schema.
"""
        ),
        (
            "human",
            """
Analyze the following financial statement:

{document_text}
"""
        ),
    ]
)


contract_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a contract extraction assistant.

Extract information only from the provided contract.

Rules:
- Only extract information explicitly present.
- Do not invent missing values.
- Use null when a value is unavailable.
- Do not infer legal obligations or terms.
- Return the required structured schema.
"""
        ),
        (
            "human",
            """
Analyze the following contract:

{document_text}
"""
        ),
    ]
)


invoice_chain = invoice_prompt | invoice_llm
insurance_chain = insurance_prompt | insurance_llm
purchase_order_chain = purchase_order_prompt | purchase_order_llm
expense_report_chain = expense_report_prompt | expense_report_llm
financial_statement_chain = financial_statement_prompt | financial_statement_llm
contract_chain = contract_prompt | contract_llm


def extract_document_data(
    document_text: str,
    category: DocumentCategory,
):

    if category == DocumentCategory.INVOICE:
        return invoice_chain.invoke(
            {
                "document_text": document_text,
            }
        )

    if category == DocumentCategory.INSURANCE_POLICY:
        return insurance_chain.invoke(
            {
                "document_text": document_text,
            }
        )

    if category == DocumentCategory.PURCHASE_ORDER:
        return purchase_order_chain.invoke(
            {
                "document_text": document_text,
            }
        )

    if category == DocumentCategory.EXPENSE_REPORT:
        return expense_report_chain.invoke(
            {
                "document_text": document_text,
            }
        )

    if category == DocumentCategory.FINANCIAL_STATEMENT:
        return financial_statement_chain.invoke(
            {
                "document_text": document_text,
            }
        )

    if category == DocumentCategory.CONTRACT:
        return contract_chain.invoke(
            {
                "document_text": document_text,
            }
        )

    raise ValueError(
        f"Extraction is not supported for category: {category}"
    )