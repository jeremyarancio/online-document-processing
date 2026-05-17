import sqlite3
from datetime import datetime
from pathlib import Path
from uuid import UUID

from app.application.ports.repositories.document import IDocumentRepository
from app.domain.document import (
    Document,
    DocumentId,
    DocumentStatus,
    Format,
    Page,
    PageId,
)


_SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    format TEXT NOT NULL,
    status TEXT NOT NULL,
    uploaded_at TEXT,
    started_at TEXT,
    completed_at TEXT
);

CREATE TABLE IF NOT EXISTS pages (
    id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL,
    number INTEGER NOT NULL,
    markdown TEXT,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);
"""


class SqliteDocumentRepository(IDocumentRepository):
    def __init__(self, db_path: Path) -> None:
        self._connection = sqlite3.connect(
            str(db_path),
            check_same_thread=False,
            isolation_level=None,
        )
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._connection.executescript(_SCHEMA)

    def add(self, document: Document) -> None:
        with self._connection:
            self._connection.execute(
                "INSERT INTO documents "
                "(id, filename, format, status, uploaded_at, started_at, completed_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                self._document_row(document),
            )
            self._insert_pages(document)

    def get(self, document_id: DocumentId) -> Document:
        row = self._connection.execute(
            "SELECT id, filename, format, status, uploaded_at, started_at, completed_at "
            "FROM documents WHERE id = ?",
            (str(document_id),),
        ).fetchone()
        if row is None:
            raise LookupError(f"Document {document_id} not found")
        return self._row_to_document(row, self._fetch_pages(document_id))

    def update(self, document: Document) -> None:
        with self._connection:
            self._connection.execute(
                "UPDATE documents SET filename = ?, format = ?, status = ?, "
                "uploaded_at = ?, started_at = ?, completed_at = ? WHERE id = ?",
                (
                    document.filename,
                    document.format.value,
                    document.status.value,
                    _iso(document.uploaded_at),
                    _iso(document.started_at),
                    _iso(document.completed_at),
                    str(document.id_),
                ),
            )
            self._connection.execute(
                "DELETE FROM pages WHERE document_id = ?",
                (str(document.id_),),
            )
            self._insert_pages(document)

    def _insert_pages(self, document: Document) -> None:
        rows = [
            (str(page.id_), str(document.id_), page.number, page.markdown)
            for page in document.pages
        ]
        if rows:
            self._connection.executemany(
                "INSERT INTO pages (id, document_id, number, markdown) "
                "VALUES (?, ?, ?, ?)",
                rows,
            )

    def _fetch_pages(self, document_id: DocumentId) -> list[Page]:
        rows = self._connection.execute(
            "SELECT id, number, markdown FROM pages WHERE document_id = ?",
            (str(document_id),),
        ).fetchall()
        return [
            Page(id_=PageId(UUID(row[0])), number=row[1], markdown=row[2])
            for row in rows
        ]

    def _document_row(self, document: Document) -> tuple:
        return (
            str(document.id_),
            document.filename,
            document.format.value,
            document.status.value,
            _iso(document.uploaded_at),
            _iso(document.started_at),
            _iso(document.completed_at),
        )

    def _row_to_document(self, row: tuple, pages: list[Page]) -> Document:
        document = Document(
            id_=DocumentId(UUID(row[0])),
            filename=row[1],
            format=Format(row[2]),
            status=DocumentStatus(row[3]),
            uploaded_at=_parse(row[4]),
            started_at=_parse(row[5]),
            completed_at=_parse(row[6]),
        )
        document.add_pages(pages)
        return document


def _iso(value: datetime | None) -> str | None:
    return value.isoformat() if value is not None else None


def _parse(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value is not None else None
