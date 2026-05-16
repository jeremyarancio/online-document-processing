from uuid import UUID

from celery import Celery

from app.application.ports.queue import IProcessingQueue
from app.domain.document import DocumentId
from app.domain.job import JobId


celery_app = Celery("worker", broker="redis://localhost:6379/0")


class CeleryProcessingQueue(IProcessingQueue):
    def enqueue(self, document_id: DocumentId) -> JobId:
        result = process_document_task.delay(str(document_id))
        return JobId(UUID(result.id))


@celery_app.task(name="process_document")
def process_document_task(document_id: str) -> None:
    from app.infrastructure.queue.worker import run_process_document

    run_process_document(DocumentId(UUID(document_id)))
