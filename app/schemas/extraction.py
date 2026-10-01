from pydantic import BaseModel, Field


class DocumentExtraction(BaseModel):
    document_type: str = Field(
        description="The type or category of the document."
    )

    title: str | None = Field(
        default=None,
        description="The title of the document if explicitly available."
    )

    document_number: str | None = Field(
        default=None,
        description="Document identifier or reference number if available."
    )

    document_date: str | None = Field(
        default=None,
        description="Date explicitly mentioned in the document."
    )

    organizations: list[str] = Field(
        default_factory=list,
        description="Organizations, companies, institutions, or departments explicitly mentioned."
    )

    people: list[str] = Field(
        default_factory=list,
        description="People explicitly mentioned in the document."
    )

    key_topics: list[str] = Field(
        default_factory=list,
        description="Important topics or subjects discussed in the document."
    )

    summary: str = Field(
        description="A concise summary of the document."
    )