from app.application.ports.dispatcher import IProcessingQueue
from app.domain.document import (
    Document,
    DocumentProcessingTriggered,
    DocumentUploaded,
)
from app.application.ports.repositories.document import IDocumentRepository


class TriggerDocumentProcesing:
    @staticmethod
    def execute(
        event: DocumentUploaded,
        dispatcher: IProcessingQueue,
        document_repository: IDocumentRepository,
    ) -> DocumentProcessingTriggered:
        document = Document.create(
            id_=event.document_id,
            filename=event.filename,
            format=event.format,
        )
        document_repository.add(document=document)
        job_id = dispatcher.process_document(document.id_)
        return DocumentProcessingTriggered(document_id=document.id_, job_id=job_id)
