from abc import ABC, abstractmethod

from app.domain.document import DocumentId
from app.domain.job import JobId


class IProcessingQueue(ABC):
    @abstractmethod
    def enqueue(self, document_id: DocumentId) -> JobId: ...
