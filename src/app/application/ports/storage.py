from abc import ABC, abstractmethod

from app.domain.document import DocumentId


class IStorageService(ABC):
    @abstractmethod
    def get_presigned_url(self, document_id: DocumentId) -> str: ...
