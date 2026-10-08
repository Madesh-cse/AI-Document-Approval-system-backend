from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConversationMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationHistoryResponse(BaseModel):
    conversation_id: int | None
    document_id: int
    messages: list[ConversationMessageResponse]