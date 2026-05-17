from app.application.ports.queue import IProcessingQueue
from app.application.ports.repositories.document import IDocumentRepository
from app.domain.document import DocumentId
from app.domain.job import JobId


class TriggerDocumentProcessing:
    def __init__(
        self,
        queue: IProcessingQueue,
        documents: IDocumentRepository,
    ) -> None:
        self._queue = queue
        self._documents = documents

    def execute(self, document_id: DocumentId, job_name: str) -> JobId:
        document = self._documents.get(document_id=document_id)
        document.mark_uploaded()
        self._documents.update(document=document)
        job_id = self._queue.enqueue(document_id=document_id, job_name=job_name)
        return job_id
