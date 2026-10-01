from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


CHROMA_DIR = Path("chroma_db")


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def get_vector_store() -> Chroma:
    return Chroma(
        collection_name="document_chunks",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )