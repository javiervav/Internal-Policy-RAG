from abc import ABC, abstractmethod
from app.domain.models.text_embedding import TextEmbedding


class VectorStoreRepository(ABC):

    @abstractmethod
    async def add(self, text_embeddings: list[TextEmbedding]) -> None:
        pass

    @abstractmethod
    async def get_relevant_documents(self, embedded_question: list[float], max_results: int, threshold: float) -> list[str]:
        pass

    @abstractmethod
    async def is_empty(self) -> bool:
        pass
