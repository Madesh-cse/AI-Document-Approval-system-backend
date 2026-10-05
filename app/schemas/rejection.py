from pydantic import BaseModel, Field


class DocumentRejectionRequest(BaseModel):
    reason: str = Field(
        min_length=1,
        max_length=2000,
    )