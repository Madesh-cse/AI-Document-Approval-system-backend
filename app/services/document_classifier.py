from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.schemas.classification import DocumentClassification


llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=settings.OPENAI_API_KEY,
    temperature=0,
)


structured_llm = llm.with_structured_output(
    DocumentClassification
)


classification_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a document classification assistant for an
AI-powered Document Intelligence and Approval Platform.

Classify the provided document into exactly one of these categories:

- invoice
- insurance_policy
- purchase_order
- expense_report
- financial_statement
- contract
- unsupported

Supported documents are business, finance, insurance,
and organizational documents relevant to document
processing and approval workflows.

Rules:
- Use only information explicitly present in the document.
- Do not invent information.
- Do not classify a document based on a single isolated word.
- Consider the overall content and purpose of the document.
- If the document does not clearly belong to one of the
  supported categories, classify it as unsupported.
- If the document is a technical, coding, educational,
  personal, entertainment, or unrelated document,
  classify it as unsupported.
- Return the result using the required structured schema.
"""
        ),
        (
            "human",
            """
Classify the following document:

{document_text}
"""
        ),
    ]
)


classification_chain = classification_prompt | structured_llm


def classify_document(
    document_text: str,
) -> DocumentClassification:

    return classification_chain.invoke(
        {
            "document_text": document_text,
        }
    )