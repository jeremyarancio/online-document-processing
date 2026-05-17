import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator
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


class SqliteDocumentRepository(IDocumentRepository):
    def __init__(self, db_path: Path) -> None:
        self._db_path = str(db_path)

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self._db_path)
        try:
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA synchronous = NORMAL")
            yield conn
        finally:
            conn.close()

    def add(self, document: Document) -> None:
        with self._connect() as conn:
            conn.execute(
                """INSERT INTO documents
                    (id, filename, format, status, uploaded_at, started_at, completed_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                self._document_row(document),
            )
            self._insert_pages(conn, document)

    def get(self, document_id: DocumentId) -> Document:
        with self._connect() as conn:
            row = conn.execute(
                """SELECT id, filename, format, status, uploaded_at, started_at, completed_at
                FROM documents
                WHERE id = ?
                """,
                (str(document_id),),
            ).fetchone()
            if row:
                return self._row_to_document(row, self._fetch_pages(conn, document_id))
            raise LookupError(f"Document {document_id} not found")

    def update(self, document: Document) -> None:
        with self._connect() as conn:
            conn.execute(
                """UPDATE documents 
                SET filename = ?, format = ?, status = ?, "uploaded_at = ?, started_at = ?, completed_at = ? 
                WHERE id = ?,
                """,
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
            conn.execute(
                "DELETE FROM pages WHERE document_id = ?",
                (str(document.id_),),
            )
            self._insert_pages(conn, document)

    def _insert_pages(self, conn: sqlite3.Connection, document: Document) -> None:
        rows = [
            (str(page.id_), str(document.id_), page.number, page.markdown)
            for page in document.pages
        ]
        if rows:
            conn.executemany(
                "INSERT INTO pages (id, document_id, number, markdown) "
                "VALUES (?, ?, ?, ?)",
                rows,
            )

    def _fetch_pages(
        self, conn: sqlite3.Connection, document_id: DocumentId
    ) -> list[Page]:
        rows = conn.execute(
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
