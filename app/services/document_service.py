from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.documents import Document


def create_document(
    db: Session,
    title: str,
    file_name: str,
    file_type: str,
    file_size: int,
    storage_path: str,
    uploaded_by: int,
) -> Document:
    document = Document(
        title=title,
        file_name=file_name,
        file_type=file_type,
        file_size=file_size,
        storage_path=storage_path,
        uploaded_by=uploaded_by,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_user_documents(
    db: Session,
    user_id: int,
) -> tuple[list[Document], int]:
    documents = db.scalars(
        select(Document)
        .where(Document.uploaded_by == user_id)
        .order_by(Document.created_at.desc())
    ).all()

    total = db.scalar(
        select(func.count(Document.id)).where(
            Document.uploaded_by == user_id
        )
    ) or 0

    return list(documents), total


def get_document_by_id(
    db: Session,
    document_id: int,
    user_id: int,
) -> Document | None:
    return db.scalar(
        select(Document).where(
            Document.id == document_id,
            Document.uploaded_by == user_id,
        )
    )