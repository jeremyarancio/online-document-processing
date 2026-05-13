from abc import ABC, abstractmethod
from uuid import UUID


class IStorageService(ABC):
    @abstractmethod
    def get_presigned_url(self, id_: UUID) -> str: ...
