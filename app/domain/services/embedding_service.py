from abc import ABC, abstractmethod


class EmbeddingService(ABC):
    
    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        pass
