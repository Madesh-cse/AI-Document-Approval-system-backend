from app.services.document_processing import process_document
from app.services.document_extraction import extract_document_data
from app.services.extraction_guardrails import validate_extraction



file_path = "uploads/1/Infosys_SP_DSE_Final_3_Hour_DSA_Revision.pdf"

result = process_document(file_path)

print("\n==============================")
print("DOCUMENT PROCESSING")
print("==============================")

print(f"Pages: {len(result['documents'])}")
print(f"Chunks: {len(result['chunks'])}")

document_text = "\n\n".join(
    chunk.page_content
    for chunk in result["chunks"]
)

print("\nSending document to LLM...")

extracted_data = extract_document_data(document_text)

print("\n==============================")
print("STRUCTURED EXTRACTION")
print("==============================")

print(
    extracted_data.model_dump_json(indent=2)
)

print("\n==============================")
print("GUARDRAIL VALIDATION")
print("==============================")

is_valid, errors = validate_extraction(
    extracted_data,
    document_text,
)
if is_valid:
    print("STATUS: VALID")
    print("All validation checks passed.")

else:
    print("STATUS: INVALID")

    for error in errors:
        print(f"- {error}")

print("\n==============================")
print("PROCESSING COMPLETE")
print("==============================")