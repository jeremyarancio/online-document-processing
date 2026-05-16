from app.application.ports.process import IProcessService
from app.application.ports.repositories.document import IDocumentRepository
from app.application.ports.storage import IStorageService
from app.domain.document import DocumentId


class ProcessDocument:
    def __init__(
        self,
        storage: IStorageService,
        documents: IDocumentRepository,
        processor: IProcessService,
    ) -> None:
        self._storage = storage
        self._documents = documents
        self._processor = processor

    def execute(self, document_id: DocumentId):
        document = self._documents.get(document_id=document_id)
        document.mark_started()
        try:
            content = self._storage.get_document(document_id=document_id)
            pages = self._processor.process(content=content)
            document.add_pages(pages=pages)
            document.mark_processed()
            self._documents.update(document=document)
        except Exception:
            document.mark_failed()
            self._documents.update(document=document)
