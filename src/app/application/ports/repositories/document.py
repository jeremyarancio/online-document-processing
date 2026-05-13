from abc import ABC, abstractmethod

from app.domain.document import Document, DocumentId


class IDocumentRepository(ABC):
    @abstractmethod
    def add(self, document: Document) -> None: ...

    @abstractmethod
    def get(self, document_id: DocumentId) -> Document: ...

    @abstractmethod
    def save(self, document: Document) -> None: ...
