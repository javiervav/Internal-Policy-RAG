from abc import ABC, abstractmethod

class DocumentDatasource(ABC):
    @abstractmethod
    def load(self) -> str:
        pass
