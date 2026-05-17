from app.application.ports.process import IProcessService
from app.application.ports.queue import IProcessingQueue
from app.application.ports.repositories.document import IDocumentRepository
from app.application.ports.storage import IStorageService
from app.infrastructure.storage import LocalStorageService
from app.infrastructure.queue import CeleryProcessingQueue


def get_storage_service() -> IStorageService:
    return LocalStorageService(base_dir=settings.base_dir, dir=settings.dir)


def get_document_repository() -> IDocumentRepository: ...


def get_processor() -> IProcessService: ...


def get_queue(app) -> IProcessingQueue:
    return CeleryProcessingQueue(celery_app=app)
