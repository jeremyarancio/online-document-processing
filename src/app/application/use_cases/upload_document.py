from app.application.ports.storage import IStorageService
from app.domain.document import DocumentId, DocumentUploadRequested


class UploadDocument:
    @staticmethod
    def execute(
        document_id: DocumentId, storage_service: IStorageService
    ) -> DocumentUploadRequested:
        presigned_url = storage_service.get_presigned_url(id_=document_id)
        return DocumentUploadRequested(presigned_url=presigned_url)
