from typing import BinaryIO

from app.application.ports.repositories.document import IDocumentRepository
from app.application.ports.storage import IStorageService
from app.domain.document import Page


class Processor:
    def __init__(
        self, documents: IDocumentRepository, storage: IStorageService
    ) -> None:
        self._documents = documents
        self._storage = storage

    def process(self, content: BinaryIO) -> list[Page]:  # noqa: F821
        return [
            Page(
                number=i,
                markdown="md",
            )
            for i in range(3)
        ]
