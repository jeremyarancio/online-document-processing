from datetime import datetime
from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID
from typing import NewType


DocumentId = NewType("DocumentId", UUID)

PageId = NewType("PageId", UUID)

JobId = NewType("JobId", UUID)


class Status(StrEnum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"
    UPLOADING = "UPLOADING"
    UPLOADED = "UPLOADED"


class Format(StrEnum):
    pdf = "pdf"
    png = "png"
    jpg = "jpg"


@dataclass
class BoundingBox:
    x0: int
    x1: int
    y0: int
    y1: int


class FigureKind(StrEnum):
    TABLE = "TABLE"
    CHART = "CHART"
    PICTURE = "PICTURE"


@dataclass
class Figure:
    kind: FigureKind
    bounding_box: BoundingBox
    caption: str | None = None
    order_on_page: int = 0


@dataclass
class Page:
    id_: PageId
    number: int = 0
    markdown: str | None = None
    figures: list[Figure] = field(default_factory=list)


@dataclass
class DocumentUploadRequested:
    document_id: DocumentId
    presigned_url: str
    at: datetime = field(default_factory=datetime.now)


@dataclass
class DocumentUploaded:
    document_id: DocumentId
    filename: str
    format: Format


@dataclass
class DocumentProcessingTriggered:
    document_id: DocumentId
    job_id: JobId
    at: datetime = field(default_factory=datetime.now)


@dataclass
class DocumentProcessed:
    document_id: DocumentId
    at: datetime = field(default_factory=datetime.now)


@dataclass
class Document:
    id_: DocumentId
    filename: str
    status: Status
    format: Format
    uploaded_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    _pages: list[Page] = field(default_factory=list)

    @classmethod
    def create(cls, id_: DocumentId, filename: str, format: Format) -> "Document":
        return cls(
            id_=id_,
            filename=filename,
            format=format,
            status=Status.UPLOADED,
            uploaded_at=datetime.now(),
        )
