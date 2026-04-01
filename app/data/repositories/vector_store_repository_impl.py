from app.data.datasources.vector_store_datasource import VectorStoreDatasource
from app.domain.models.text_embedding import TextEmbedding
from app.domain.repositories.vector_store_repository import VectorStoreRepository


class VectorStoreRepositoryImpl(VectorStoreRepository):

    def __init__(self, vector_store: VectorStoreDatasource):
        self.vector_store = vector_store

    async def add(self, text_embeddings: list[TextEmbedding]) -> None:
        await self.vector_store.add(text_embeddings)
