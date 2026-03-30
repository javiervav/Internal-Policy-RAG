from abc import ABC, abstractmethod

class DocumentDatasource(ABC):
    @abstractmethod
    async def load(self) -> str:
        pass
