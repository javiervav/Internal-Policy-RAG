from abc import ABC, abstractmethod
from app.domain.models.text_embedding import TextEmbedding


class VectorStoreDatasource(ABC):

    @abstractmethod
    async def add(self, text_embeddings: list[TextEmbedding]) -> None:
        pass

    @abstractmethod
    async def search_similarities(
            self,
            embedded_question: list[float],
            max_results: int,
            threshold: float,
    ) -> list[str]:
        pass
