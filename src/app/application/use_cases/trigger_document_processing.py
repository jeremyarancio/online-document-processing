from app.application.ports.queue import IProcessingQueue
from app.application.ports.repositories.document import IDocumentRepository
from app.domain.document import Document
from app.domain.events import DocumentUploaded
from app.domain.job import JobId


class TriggerDocumentProcessing:
    def __init__(
        self,
        queue: IProcessingQueue,
        documents: IDocumentRepository,
    ) -> None:
        self._queue = queue
        self._documents = documents

    def execute(self, event: DocumentUploaded) -> JobId:
        document = Document.create(
            id_=event.document_id,
            filename=event.filename,
            format=event.format,
        )
        self._documents.add(document)
        return self._queue.enqueue(document.id_)
