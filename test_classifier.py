from app.services.document_classifier import classify_document
from app.services.document_extraction import extract_document_data


document_text = """
INVOICE

Invoice Number: INV-2026-1001
Invoice Date: 15 September 2026

Vendor:
ABC Technologies Pvt Ltd

Subtotal: $5,000
Tax: $900
Total Amount: $5,900

Payment Terms: Net 30 days.
"""

classification = classify_document(document_text)

print("Classification:")
print(classification)

extraction = extract_document_data(
    document_text,
    classification.category,
)

print("\nExtraction:")
print(extraction)