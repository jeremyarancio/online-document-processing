from typing import BinaryIO
from abc import ABC, abstractmethod

from app.domain.document import DocumentId


class IStorageService(ABC):
    @abstractmethod
    def get_presigned_url(self, document_id: DocumentId) -> str: ...

    @abstractmethod
    def get_document(self, document_id: DocumentId) -> BinaryIO: ...
