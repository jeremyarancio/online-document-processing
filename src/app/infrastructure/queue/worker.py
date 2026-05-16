from app.application.use_cases.process_document import ProcessDocument
from app.domain.document import DocumentId


def run_process_document(document_id: DocumentId) -> None:
    from app.interface.dependencies import get_storage, get_document_repository

    storage = get_storage()
    documents = get_document_repository()

    use_case = ProcessDocument(storage=storage, documents=documents)
    use_case.execute(document_id=document_id)
