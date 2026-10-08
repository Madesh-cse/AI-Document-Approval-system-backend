from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.conversation import (
    Conversation,
    ConversationMessage,
)


def get_conversation(
    db: Session,
    document_id: int,
    user_id: int,
) -> Conversation | None:
    return db.scalar(
        select(Conversation).where(
            Conversation.document_id == document_id,
            Conversation.user_id == user_id,
        )
    )


def get_or_create_conversation(
    db: Session,
    document_id: int,
    user_id: int,
) -> Conversation:
    conversation = get_conversation(
        db=db,
        document_id=document_id,
        user_id=user_id,
    )

    if conversation:
        return conversation

    conversation = Conversation(
        document_id=document_id,
        user_id=user_id,
    )

    db.add(conversation)
    db.flush()

    return conversation


def get_messages(
    db: Session,
    conversation_id: int,
) -> list[ConversationMessage]:
    return list(
        db.scalars(
            select(ConversationMessage)
            .where(
                ConversationMessage.conversation_id
                == conversation_id
            )
            .order_by(
                ConversationMessage.created_at.asc(),
                ConversationMessage.id.asc(),
            )
        ).all()
    )


def add_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str,
) -> ConversationMessage:
    message = ConversationMessage(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.flush()

    return message