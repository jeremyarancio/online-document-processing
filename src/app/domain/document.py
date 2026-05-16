from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import NewType
from uuid import UUID, uuid4


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


class BoundingBox:
    x0: int
    x1: int
    y0: int
    y1: int


class Figure:
    kind: FigureKind
    bounding_box: BoundingBox
    caption: str | None = None
    order_on_page: int = 0


@dataclass
class Page:
    id_: PageId = field(default_factory=lambda: PageId(uuid4()))
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

    def mark_uploaded(self) -> None:
        self.status = DocumentStatus.UPLOADED
        self.uploaded_at = datetime.now()

    def mark_started(self) -> None:
        self.status = DocumentStatus.PROCESSING
        self.started_at = datetime.now()

    def mark_failed(self) -> None:
        self.status = DocumentStatus.FAILED
        self.completed_at = datetime.now()

    def mark_finished(self) -> None:
        self.status = DocumentStatus.PROCESSED
        self.completed_at = datetime.now()

    def add_pages(self, pages: list[Page]) -> None:
        self._pages = pages
