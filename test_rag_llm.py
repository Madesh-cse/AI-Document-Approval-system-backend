from app.services.rag_service import answer_question


document_id = 1

question = (
    "What are the main topics covered "
    "in this document?"
)


result = answer_question(
    question=question,
    document_id=document_id,
)


print("\n==============================")
print("RAG QUESTION ANSWERING")
print("==============================")

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(result["answer"])

print("\nSources:")

for source in result["sources"]:
    if source["page"] is not None:
        print(
            f"- Document {source['document_id']}, "
            f"Page {source['page']}"
        )
    else:
        print(
            f"- Document {source['document_id']}"
        )

print("\n==============================")
print("RAG COMPLETE")
print("==============================")