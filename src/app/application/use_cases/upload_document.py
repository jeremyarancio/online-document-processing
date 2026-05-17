from app.application.ports.storage import IStorageService
from app.application.ports.repositories.document import IDocumentRepository
from app.domain.document import Document, DocumentId, Format


class UploadDocument:
    def __init__(
        self, storage: IStorageService, documents: IDocumentRepository
    ) -> None:
        self._storage = storage
        self._documents = documents

    def execute(self, filename: str, format: Format) -> tuple[str, DocumentId]:
        document = Document.create(filename=filename, format=format)
        presigned_url = self._storage.get_presigned_url(document_id=document.id_)
        self._documents.add(document=document)
        return presigned_url, document.id_
