from app.services.rag_service import retrieve_document_chunks


question = "What are the main topics covered in this document?"

document_id = 1

results = retrieve_document_chunks(
    question=question,
    document_id=document_id,
)

print("\n==============================")
print("RAG RETRIEVAL")
print("==============================")

print(f"Question: {question}")
print(f"Document ID: {document_id}")
print(f"Retrieved chunks: {len(results)}")

for index, document in enumerate(
    results,
    start=1,
):
    print(f"\n===== RESULT {index} =====")

    print(
        f"Document ID: "
        f"{document.metadata.get('document_id')}"
    )

    print("\nContent:")
    print(document.page_content)

print("\n==============================")
print("RETRIEVAL COMPLETE")
print("==============================")