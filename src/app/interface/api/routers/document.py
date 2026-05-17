from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Query

from app.application.ports.queue import IProcessingQueue
from app.application.ports.repositories.document import IDocumentRepository
from app.application.ports.storage import IStorageService
from app.application.use_cases.trigger_document_processing import (
    TriggerDocumentProcessing,
)
from app.application.use_cases.upload_document import UploadDocument
from app.domain.document import DocumentId
from app.interface import dependencies
from app.interface.api.schemas.document import (
    UploadDocumentPayload,
    UploadDocumentResponse,
    UploadedDocumentResponse,
)
from app.interface.worker.tasks import JobName

router = APIRouter(prefix="documents", tags=["Document"])


@router.post("")
def upload_document(
    payload: UploadDocumentPayload,
    storage: Annotated[IStorageService, Depends(dependencies.get_storage_service)],
    documents: Annotated[
        IDocumentRepository, Depends(dependencies.get_document_repository)
    ],
) -> UploadDocumentResponse:
    presigned_url, document_id = UploadDocument(
        storage=storage, documents=documents
    ).execute(
        filename=payload.filename,
        format=payload.mime_type.to_format(),
    )
    return UploadDocumentResponse(presigned_url=presigned_url, document_id=document_id)


@router.post("/{document_id}")
def uploaded(
    document_id: UUID,
    documents: Annotated[
        IDocumentRepository, Depends(dependencies.get_document_repository)
    ],
    queue: Annotated[IProcessingQueue, Depends(dependencies.get_queue)],
) -> UploadedDocumentResponse:
    job_id = TriggerDocumentProcessing(queue=queue, documents=documents).execute(
        document_id=DocumentId(document_id),
        job_name=JobName.PROCESS_DOCUMENT,
    )
    return UploadedDocumentResponse(
        message="Document processing is triggered.",
        job_id=job_id,
    )
