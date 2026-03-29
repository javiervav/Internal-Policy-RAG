from abc import ABC, abstractmethod

class DocumentRepository(ABC):
    @abstractmethod
    def load_document(self) -> str:
        pass