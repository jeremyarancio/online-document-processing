from abc import ABC, abstractmethod
from typing import BinaryIO

from app.domain.document import Page


class IProcessService(ABC):
    @abstractmethod
    def process(self, content: BinaryIO) -> list[Page]:
        pass
