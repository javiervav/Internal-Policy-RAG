from app.data.datasources.vector_store_datasource import VectorStoreDatasource
from app.domain.models.text_embedding import TextEmbedding
from app.domain.repositories.vector_store_repository import VectorStoreRepository


class VectorStoreRepositoryImpl(VectorStoreRepository):

    def __init__(self, vector_store_datasource: VectorStoreDatasource):
        self._vector_store_datasource = vector_store_datasource

    async def add(self, text_embeddings: list[TextEmbedding]) -> None:
        await self._vector_store_datasource.add(text_embeddings)

    async def get_relevant_documents(self, embedded_question: list[float], max_results: int, threshold: float) -> list[str]:
        return await self._vector_store_datasource.search_similarities(embedded_question, max_results, threshold)
