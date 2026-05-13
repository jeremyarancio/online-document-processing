from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import NewType
from uuid import UUID, uuid4


from app.domain.events import DocumentProcessingStarted, DocumentProcessed
from app.domain.job import JobId

DocumentId = NewType("DocumentId", UUID)
PageId = NewType("PageId", UUID)


class DocumentStatus(StrEnum):
    UPLOADING = "UPLOADING"
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"


class Format(StrEnum):
    PDF = "pdf"
    PNG = "png"
    JPG = "jpg"


class FigureKind(StrEnum):
    TABLE = "TABLE"
    CHART = "CHART"
    PICTURE = "PICTURE"


@dataclass(frozen=True)
class BoundingBox:
    x0: int
    x1: int
    y0: int
    y1: int


@dataclass(frozen=True)
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
class Document:
    id_: DocumentId
    filename: str
    format: Format
    status: DocumentStatus
    uploaded_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    _pages: list[Page] = field(default_factory=list)

    @property
    def pages(self) -> list[Page]:
        return list(sorted(self._pages, key=lambda page: page.number))

    @classmethod
    def create(cls, filename: str, format: Format) -> "Document":
        return cls(
            id_=DocumentId(uuid4()),
            filename=filename,
            format=format,
            status=DocumentStatus.UPLOADING,
            uploaded_at=datetime.now(),
        )

    def mark_processing(self, job_id: JobId) -> "DocumentProcessingStarted":
        if self.status != DocumentStatus.UPLOADED:
            raise ValueError(f"cannot start processing from status {self.status}")
        self.status = DocumentStatus.PROCESSING
        self.started_at = datetime.now()
        return DocumentProcessingStarted(
            document_id=self.id_, job_id=job_id, occurred_at=self.started_at
        )

    def mark_processed(self) -> "DocumentProcessed":
        if self.status != DocumentStatus.PROCESSING:
            raise ValueError(f"cannot mark processed from status {self.status}")
        self.status = DocumentStatus.PROCESSED
        self.completed_at = datetime.now()
        return DocumentProcessed(document_id=self.id_, occurred_at=self.completed_at)

    def mark_failed(self) -> None:
        self.status = DocumentStatus.FAILED
        self.completed_at = datetime.now()

    def attach_pages(self, pages: list[Page]) -> None:
        self._pages = list(pages)
