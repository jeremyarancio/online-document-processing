from enum import StrEnum
from uuid import UUID

from app.application.use_cases.process_document import ProcessDocument
from app.domain.document import DocumentId
from app.interface import dependencies
from app.interface.worker.main import celery_app


class JobName(StrEnum):
    PROCESS_DOCUMENT = "PROCESS_DOCUMENT"


@celery_app.task(name=JobName.PROCESS_DOCUMENT)
def process_document_task(document_id: UUID) -> None:
    ProcessDocument(
        storage=dependencies.get_storage_service(),
        documents=dependencies.get_document_repository(),
        processor=dependencies.get_processor(),
    ).execute(document_id=DocumentId(document_id))
