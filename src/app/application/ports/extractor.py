from abc import ABC, abstractmethod

from app.domain.document import DocumentId, Page


class IDocumentExtractor(ABC):
    @abstractmethod
    def extract(self, document_id: DocumentId) -> list[Page]: ...
