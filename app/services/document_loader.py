import os
import tempfile
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)

from app.services.s3_service import download_file_from_s3


def load_document(file_path: str):
    extension = Path(file_path).suffix.lower()

    if extension not in {".pdf", ".txt"}:
        raise ValueError(
            f"Unsupported document type: {extension}"
        )

    file_content = download_file_from_s3(file_path)

    if not file_content:
        raise ValueError(
            f"Document is empty: {file_path}"
        )

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=extension,
            delete=False,
        ) as temporary_file:
            temporary_file.write(file_content)
            temporary_path = temporary_file.name

        if extension == ".pdf":
            loader = PyPDFLoader(temporary_path)

        elif extension == ".txt":
            loader = TextLoader(
                temporary_path,
                encoding="utf-8",
            )

        documents = loader.load()

        if not documents:
            raise ValueError(
                f"Document contains no readable text: {file_path}"
            )

        return documents

    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)