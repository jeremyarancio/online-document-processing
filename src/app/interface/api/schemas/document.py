from enum import StrEnum
from uuid import UUID
from typing import Annotated
from pydantic import BaseModel, Field

from app.domain.document import Format


class MimeType(StrEnum):
    PDF = "application/pdf"
    PNG = "image/png"
    JPG = "image/jpeg"

    def to_format(self) -> Format:
        return _MIME_TO_FORMAT[self]


_MIME_TO_FORMAT: dict[MimeType, Format] = {
    MimeType.PDF: Format.PDF,
    MimeType.PNG: Format.PNG,
    MimeType.JPG: Format.JPG,
}


class UploadDocumentPayload(BaseModel):
    filename: Annotated[str, Field(ge=3, le=100)]
    mime_type: MimeType


class UploadDocumentResponse(BaseModel):
    presigned_url: str
    document_id: UUID


class UploadedDocumentResponse(BaseModel):
    message: str
    job_id: str
