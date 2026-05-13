from app.application.ports.extractor import IDocumentExtractor
from app.application.ports.repositories.document import IDocumentRepository
from app.domain.document import DocumentId
from app.domain.events import DocumentProcessed, DocumentProcessingStarted
from app.domain.job import JobId


class ProcessDocument:
    def __init__(
        self,
        documents: IDocumentRepository,
        extractor: IDocumentExtractor,
    ) -> None:
        self._documents = documents
        self._extractor = extractor

    def execute(
        self, document_id: DocumentId, job_id: JobId
    ) -> tuple[DocumentProcessingStarted, DocumentProcessed]:
        document = self._documents.get(document_id)

        started = document.mark_processing(job_id)
        self._documents.save(document)

        try:
            pages = self._extractor.extract(document.id_)
            document.attach_pages(pages)
            processed = document.mark_processed()
            self._documents.save(document)
        except Exception:
            document.mark_failed()
            self._documents.save(document)
            raise

        return started, processed
