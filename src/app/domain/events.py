from datetime import datetime

from app.domain.document import DocumentId
from app.domain.job import JobId


class DocumentProcessingStarted:
    document_id: DocumentId
    job_id: JobId
    occurred_at: datetime


class DocumentProcessed:
    document_id: DocumentId
    occurred_at: datetime
