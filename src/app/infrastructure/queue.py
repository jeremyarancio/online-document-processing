from uuid import UUID

from celery import Celery

from app.application.ports.queue import IProcessingQueue
from app.domain.document import DocumentId
from app.domain.job import JobId


class CeleryProcessingQueue(IProcessingQueue):
    def __init__(self, celery_app: Celery) -> None:
        self._celery_app = celery_app

    def enqueue(self, document_id: DocumentId, job_name: str) -> JobId:
        result = self._celery_app.send_task(
            job_name,
            args=[document_id],
        )
        return JobId(UUID(result.id))
