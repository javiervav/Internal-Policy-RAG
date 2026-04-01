from abc import ABC, abstractmethod


class EmbeddingService(ABC):

    @abstractmethod
    async def embed_text(self, text: str) -> list[float]:
        pass

    @abstractmethod
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        pass
