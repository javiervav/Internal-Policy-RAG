from abc import ABC, abstractmethod

class DocumentRepository(ABC):
    @abstractmethod
    async def load_document(self) -> str:
        pass