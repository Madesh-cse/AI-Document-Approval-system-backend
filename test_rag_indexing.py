from app.services.document_processing import process_document


file_path = "uploads/1/Infosys_SP_DSE_Final_3_Hour_DSA_Revision.pdf"

document_id = 1

result = process_document(
    file_path=file_path,
    document_id=document_id,
)

print("\n==============================")
print("RAG INDEXING")
print("==============================")

print(f"Pages: {len(result['documents'])}")
print(f"Chunks: {len(result['chunks'])}")

print("\nDocument indexed successfully.")

for index, chunk in enumerate(
    result["chunks"],
    start=1,
):
    print(
        f"\nChunk {index}"
        f" | document_id={chunk.metadata['document_id']}"
    )

print("\n==============================")
print("INDEXING COMPLETE")
print("==============================")