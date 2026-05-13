from abc import ABC, abstractmethod

from app.domain.document import DocumentId, JobId


class IProcessingQueue(ABC):
    @abstractmethod
    def process_document(self, document_id: DocumentId) -> JobId: ...
