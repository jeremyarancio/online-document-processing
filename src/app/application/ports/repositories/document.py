from abc import ABC, abstractmethod

from app.domain.document import Document


class IDocumentRepository(ABC):
    @abstractmethod
    def add(self, document: Document) -> None: ...
