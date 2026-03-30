from abc import ABC, abstractmethod
from app.domain.models.text_embedding import TextEmbedding


class VectorStoreRepository(ABC):
    
    @abstractmethod
    async def add(self, text_embeddings: list[TextEmbedding]) -> None:
        pass
